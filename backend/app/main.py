from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from .database import Base, engine, get_db
from .models import Problem, Attempt
from .schemas import ProblemOut, AttemptCreate, AttemptOut, ClassInput
from .evaluation import RubricEvaluator
from .seed import seed_problems

app = FastAPI(title="LLD Practice Platform API", version="1.0.0",
              description="Practice LLD, submit a design, and review explainable feedback.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://172.18.113.231:5173", 
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
evaluator = RubricEvaluator()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    with Session(engine) as db:
        seed_problems(db)

@app.get("/api/health")
def health():
    return {"status":"ok"}

@app.get("/api/problems", response_model=list[ProblemOut])
def list_problems(db: Session = Depends(get_db)):
    return list(db.scalars(select(Problem).order_by(Problem.title)).all())

@app.get("/api/problems/{problem_id}", response_model=ProblemOut)
def get_problem(problem_id: str, db: Session = Depends(get_db)):
    problem = db.get(Problem, problem_id)
    if not problem: raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@app.post("/api/attempts", response_model=AttemptOut, status_code=status.HTTP_201_CREATED)
def create_attempt(payload: AttemptCreate, db: Session = Depends(get_db)):
    if not db.get(Problem, payload.problem_id):
        raise HTTPException(status_code=404, detail="Problem not found")
    attempt = Attempt(problem_id=payload.problem_id, learner_id=payload.learner_id.strip(),
      status="evaluating", classes=[item.model_dump() for item in payload.classes],
      relationships_text=payload.relationships_text, patterns=payload.patterns,
      tradeoffs=payload.tradeoffs, edge_cases=payload.edge_cases)
    db.add(attempt); db.commit(); db.refresh(attempt)
    try:
        feedback = evaluator.evaluate(payload)
        attempt.feedback, attempt.score, attempt.status = feedback, feedback["score"], "evaluated"
    except Exception:
        attempt.status = "evaluation_failed"
        attempt.error_message = "Evaluation failed. Your submission was saved; retry evaluation."
    db.commit(); db.refresh(attempt)
    return attempt

@app.get("/api/attempts/{attempt_id}", response_model=AttemptOut)
def get_attempt(attempt_id: int, db: Session = Depends(get_db)):
    attempt = db.get(Attempt, attempt_id)
    if not attempt: raise HTTPException(status_code=404, detail="Attempt not found")
    return attempt

@app.get("/api/problems/{problem_id}/attempts", response_model=list[AttemptOut])
def attempt_history(problem_id: str, learner_id: str = "demo-learner", db: Session = Depends(get_db)):
    if not db.get(Problem, problem_id): raise HTTPException(status_code=404, detail="Problem not found")
    query = select(Attempt).where(Attempt.problem_id == problem_id, Attempt.learner_id == learner_id).order_by(desc(Attempt.submitted_at), desc(Attempt.id))
    return list(db.scalars(query).all())

@app.post("/api/attempts/{attempt_id}/retry-evaluation", response_model=AttemptOut)
def retry_evaluation(attempt_id: int, db: Session = Depends(get_db)):
    attempt = db.get(Attempt, attempt_id)
    if not attempt: raise HTTPException(status_code=404, detail="Attempt not found")
    if attempt.status != "evaluation_failed":
        raise HTTPException(status_code=409, detail="Only failed evaluations can be retried")
    payload = AttemptCreate(problem_id=attempt.problem_id, learner_id=attempt.learner_id,
      classes=[ClassInput(**item) for item in attempt.classes], relationships_text=attempt.relationships_text,
      patterns=attempt.patterns, tradeoffs=attempt.tradeoffs, edge_cases=attempt.edge_cases)
    try:
        feedback = evaluator.evaluate(payload)
        attempt.feedback, attempt.score, attempt.status, attempt.error_message = feedback, feedback["score"], "evaluated", None
    except Exception:
        attempt.error_message = "Evaluation failed again. Your submission is still saved."
    db.commit(); db.refresh(attempt)
    return attempt
