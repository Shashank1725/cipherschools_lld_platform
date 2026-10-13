from sqlalchemy.orm import Session
from .models import Problem

PROBLEMS = [
 {"id":"parking-lot","title":"Parking Lot","level":"Beginner","estimated_minutes":35,
  "summary":"Design a parking lot that assigns suitable spots, tracks occupancy, and calculates a parking fee.",
  "requirements":["Support multiple vehicle types and compatible spot types.","Issue a ticket on entry and close it on exit.","Calculate fees from duration and a configurable pricing policy.","Reject entry when no compatible spot is available."],
  "constraints":["Do not implement payment processing.","Explain how concurrent entry requests avoid double-booking."]},
 {"id":"elevator","title":"Elevator Controller","level":"Intermediate","estimated_minutes":45,
  "summary":"Model an elevator system that accepts hall/car requests and decides which request to serve next.",
  "requirements":["Represent elevators, floors, and requests.","Separate request collection from scheduling policy.","Represent idle, moving, and out-of-service states.","Explain how a scheduling policy can be replaced."],
  "constraints":["You do not need to simulate real time.","Describe emergency and out-of-service behaviour."]},
 {"id":"vending-machine","title":"Vending Machine","level":"Beginner","estimated_minutes":30,
  "summary":"Design a vending machine that sells items, accepts payment, dispenses products, and handles refunds.",
  "requirements":["Track inventory and product prices.","Model purchase and payment/dispense outcomes.","Return change or refund when a purchase cannot complete.","Make state transitions explicit."],
  "constraints":["No real payment gateway is needed.","Explain what happens if dispensing fails after payment."]}
]

def seed_problems(db: Session):
    for item in PROBLEMS:
        if db.get(Problem, item["id"]) is None:
            db.add(Problem(**item))
    db.commit()
