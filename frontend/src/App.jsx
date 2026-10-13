import React, { useEffect, useState } from 'react';
import { Layers3, Code2, History, Clock3, BookOpen, Target, ArrowUpRight, CircleHelp, X, Plus, Trash2, Send, Sparkles, CheckCircle2, AlertCircle, ChevronRight, RotateCcw } from 'lucide-react';

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';
const blankClass = () => ({name:'', responsibility:''});
const blankDraft = () => ({classes:[blankClass(),blankClass()], relationships_text:'', patterns:'', tradeoffs:'', edge_cases:''});
async function api(path, options={}) {
  const res = await fetch(`${API}${path}`, {headers:{'Content-Type':'application/json', ...(options.headers||{})}, ...options});
  const body = await res.json().catch(()=>({}));
  if (!res.ok) throw new Error(Array.isArray(body.detail) ? body.detail.map(x=>x.msg).join(', ') : (body.detail || `Request failed (${res.status})`));
  return body;
}
export default function App() {
  const [problems,setProblems] = useState([]), [problem,setProblem] = useState(null), [selected,setSelected] = useState('parking-lot');
  const [draft,setDraft] = useState(blankDraft()), [history,setHistory] = useState([]), [result,setResult] = useState(null);
  const [tab,setTab] = useState('practice'), [busy,setBusy] = useState(false), [error,setError] = useState(''), [loading,setLoading] = useState(true);
  const learner = 'demo-learner';

  useEffect(()=>{api('/api/problems').then(setProblems).catch(e=>setError(`API connection failed: ${e.message}. Start FastAPI, then refresh.`)).finally(()=>setLoading(false));},[]);
  useEffect(()=>{if(!selected)return; let live=true; setProblem(null); setResult(null); setDraft(blankDraft()); setError('');
    Promise.all([api(`/api/problems/${selected}`),api(`/api/problems/${selected}/attempts?learner_id=${learner}`)])
      .then(([p,h])=>{if(live){setProblem(p);setHistory(h);}}).catch(e=>{if(live)setError(e.message);});
    return ()=>{live=false;};
  },[selected]);
  const field=(name,value)=>setDraft(d=>({...d,[name]:value}));
  const classField=(i,key,value)=>setDraft(d=>({...d,classes:d.classes.map((c,j)=>i===j?{...c,[key]:value}:c)}));
  async function submit(e){e.preventDefault();setBusy(true);setError('');setResult(null);
    try {const r=await api('/api/attempts',{method:'POST',body:JSON.stringify({...draft,problem_id:selected,learner_id:learner})});setResult(r);setTab('feedback');setHistory(await api(`/api/problems/${selected}/attempts?learner_id=${learner}`));}
    catch(err){setError(err.message);}finally{setBusy(false);}
  }
  function review(a){setResult(a);setDraft({classes:a.classes,relationships_text:a.relationships_text,patterns:a.patterns||'',tradeoffs:a.tradeoffs,edge_cases:a.edge_cases});setTab('feedback');}
  if(loading)return <div className="loading"><div className="loader"/>Setting up your practice space…</div>;
  return <div className="app">
    <aside className="sidebar">
      <div className="brand"><div className="brand-icon"><Layers3 size={19}/></div><div><b>craft<span>.</span></b><small>LLD PRACTICE STUDIO</small></div></div>
      <div className="nav-caption">YOUR WORKSPACE</div>
      <button className={`nav-item ${tab==='practice'?'active':''}`} onClick={()=>setTab('practice')}><Code2 size={17}/> Practice room</button>
      <button className={`nav-item ${tab==='history'?'active':''}`} onClick={()=>setTab('history')}><History size={17}/> Attempt history <span className="nav-count">{history.length||''}</span></button>
      <div className="side-rule"/>
      <div className="nav-caption">PROBLEM SET <span>{String(problems.length).padStart(2,'0')}</span></div>
      <div className="problem-list">{problems.map((p,i)=><button key={p.id} className={`problem-link ${selected===p.id?'selected':''}`} onClick={()=>setSelected(p.id)}><span className="problem-index">{String(i+1).padStart(2,'0')}</span><span className="problem-label"><b>{p.title}</b><small>{p.level} · {p.estimated_minutes} min</small></span>{selected===p.id&&<ArrowUpRight size={15}/>}</button>)}</div>
      <div className="sidebar-footer"><div className="avatar">DL</div><div><b>Demo learner</b><small>Personal practice space</small></div><span className="online"/></div>
    </aside>
    <main className="main">
      <header className="topbar"><div className="crumb">Workspace <span>/</span> <b>{tab==='history'?'Attempt history':tab==='feedback'?'Review feedback':'Practice room'}</b></div><div className="api-status"><i/> API connected <span className="top-avatar">DL</span></div></header>
      <div className="content">
        {error&&<div className="error-banner"><AlertCircle size={17}/><span>{error}</span><button onClick={()=>setError('')}><X size={15}/></button></div>}
        {problem&&<section className="hero"><div className="hero-main"><div className="eyebrow"><span/> DESIGN CHALLENGE <em>{problem.level}</em></div><h1>{problem.title}<span>.</span></h1><p>{problem.summary}</p><div className="hero-stats"><span><Clock3 size={15}/>{problem.estimated_minutes} min estimate</span><span><BookOpen size={15}/>{problem.requirements.length} requirements</span><span><Target size={15}/>{history.length?`${history.length} attempt${history.length>1?'s':''}`:'Not started'}</span></div></div><div className="hero-score"><div className="score-orbit"><strong>{history[0]?.score??'—'}{history.length?<small>/100</small>:null}</strong></div><span>{history.length?'LATEST SCORE':'YOUR BEST START'}</span><small>{history.length?'Keep iterating':'One design at a time'}</small></div></section>}
        {problem&&<div className="tabs"><button className={tab==='practice'?'tab active-tab':''} onClick={()=>setTab('practice')}>01 <span>Practice</span></button><button className={tab==='feedback'?'tab active-tab':''} onClick={()=>setTab('feedback')} disabled={!result}>02 <span>Feedback</span></button><button className={tab==='history'?'tab active-tab':''} onClick={()=>setTab('history')}>03 <span>History</span></button></div>}
        {problem&&tab==='practice'&&<div className="workspace">
          <section className="panel requirements"><div className="panel-head"><div><span className="step-label">START HERE</span><h2>Problem brief</h2></div><BookOpen size={19}/></div><p className="brief-intro">Read the requirements, then describe the design you would build. There can be more than one good answer.</p>
            <h3>Functional requirements</h3><ul className="requirement-list">{problem.requirements.map((r,i)=><li key={r}><span>{String(i+1).padStart(2,'0')}</span>{r}</li>)}</ul>
            <div className="constraints"><div><Target size={16}/><b>Constraints to consider</b></div>{problem.constraints.map(c=><p key={c}>• {c}</p>)}</div>
            <div className="tip-card"><Sparkles size={17}/><div><b>Think in responsibilities</b><p>Prefer cohesive classes and explicit contracts. Explain why you chose a design rather than just naming a pattern.</p></div></div>
          </section>
          <form className="panel editor" onSubmit={submit}><div className="panel-head"><div><span className="step-label">YOUR SOLUTION</span><h2>Design canvas</h2></div><span className="draft-tag">TEXT DESIGN</span></div><p className="brief-intro">Start with the core domain objects. You can submit again after reviewing feedback.</p>
            <div className="field-heading"><label>Classes & responsibilities</label><span>{draft.classes.length} classes</span></div>
            <div className="class-stack">{draft.classes.map((c,i)=><div className="class-card" key={i}><div className="class-top"><span className="class-chip">CLASS {String(i+1).padStart(2,'0')}</span>{draft.classes.length>2&&<button type="button" className="icon-button" onClick={()=>field('classes',draft.classes.filter((_,j)=>i!==j))} aria-label="Remove class"><Trash2 size={14}/></button>}</div><input required minLength="2" maxLength="80" value={c.name} onChange={e=>classField(i,'name',e.target.value)} placeholder="e.g. ParkingSpot"/><textarea required minLength="8" maxLength="500" value={c.responsibility} onChange={e=>classField(i,'responsibility',e.target.value)} placeholder="What does this class own or do?" rows="2"/></div>)}</div>
            <button type="button" className="add-class" disabled={draft.classes.length>=20} onClick={()=>field('classes',[...draft.classes,{name:'',responsibility:''}])}><Plus size={15}/> Add another class</button>
            <div className="form-field"><label>Relationships & collaboration <span>REQUIRED</span></label><textarea required minLength="12" value={draft.relationships_text} onChange={e=>field('relationships_text',e.target.value)} rows="3" placeholder="How do objects know about or create each other? Mention ownership, cardinality, and interactions."/></div>
            <div className="form-field"><label>Patterns or interfaces <span>OPTIONAL</span></label><textarea value={draft.patterns} onChange={e=>field('patterns',e.target.value)} rows="2" placeholder="Which abstraction or pattern helps? Why? It is okay to use none."/></div>
            <div className="form-field"><label>Trade-offs <span>REQUIRED</span></label><textarea required minLength="12" value={draft.tradeoffs} onChange={e=>field('tradeoffs',e.target.value)} rows="3" placeholder="What alternative did you consider? What does your choice make easier or harder?"/></div>
            <div className="form-field"><label>Edge cases & failures <span>REQUIRED</span></label><textarea required minLength="12" value={draft.edge_cases} onChange={e=>field('edge_cases',e.target.value)} rows="3" placeholder="What if the lot is full, a payment fails, or an elevator is out of service?"/></div>
            <div className="submit-row"><div><span className="save-dot"/> Your draft is in this form</div><button type="submit" disabled={busy}>{busy?'Evaluating…':<>Submit design <Send size={15}/></>}</button></div>
          </form>
        </div>}
        {problem&&tab==='feedback'&&<section className="panel feedback-panel">{result?<><div className="panel-head"><div><span className="step-label">ATTEMPT #{result.id}</span><h2>Design review</h2></div><span className={`status ${result.status}`}>{result.status.replace('_',' ')}</span></div>{result.status==='evaluation_failed'?<div className="error-banner">Your design is saved, but evaluation failed. You can retry from the API.</div>:<><div className="feedback-summary"><div className="big-score">{result.score}<small>/100</small></div><div><h3>{result.feedback?.summary||'Review your submission'}</h3><p>This score reflects a small heuristic checklist, not whether your design is the only correct solution.</p></div></div><div className="dimension-list">{(result.feedback?.dimensions||[]).map(d=><div className="dimension" key={d.dimension}><span className={d.passed?'pass-icon':'miss-icon'}>{d.passed?<CheckCircle2 size={17}/>:<AlertCircle size={17}/>}</span><div><b>{d.dimension}</b><p>{d.feedback}</p><small>{d.principle}</small></div><span className={`dimension-state ${d.passed?'good':'improve'}`}>{d.passed?'Signal found':'To review'}</span></div>)}</div><div className="feedback-columns"><div><h3>What is working</h3>{(result.feedback?.strengths||[]).map((x,i)=><p key={i}><CheckCircle2 size={15}/>{x}</p>)}</div><div><h3>Next improvements</h3>{(result.feedback?.improvements||[]).map((x,i)=><p key={i}><ArrowUpRight size={15}/>{x}</p>)}</div></div><div className="next-step"><Sparkles size={17}/><div><b>Your next step</b><p>{result.feedback?.next_step}</p></div></div></>}<div className="feedback-actions"><button className="secondary-button" onClick={()=>setTab('history')}><History size={15}/> View history</button><button onClick={()=>{setDraft(blankDraft());setResult(null);setTab('practice');}}><RotateCcw size={15}/> Try again</button></div></>:<div className="empty-state"><Sparkles size={24}/><h2>Your feedback will appear here</h2><p>Submit a design to get a dimension-by-dimension review.</p><button onClick={()=>setTab('practice')}>Go to design canvas <ChevronRight size={15}/></button></div>}</section>}
        {problem&&tab==='history'&&<section className="panel history-panel"><div className="panel-head"><div><span className="step-label">YOUR PROGRESS</span><h2>Attempt history</h2></div><History size={20}/></div><p className="brief-intro">Every submission is kept so you can revisit feedback and see how your thinking evolves.</p>{history.length?<div className="history-list">{history.map((a,i)=><article className="history-item" key={a.id}><div className="history-num">{String(history.length-i).padStart(2,'0')}</div><div className="history-copy"><b>Attempt #{a.id}</b><p>{new Date(a.submitted_at).toLocaleString()} · {a.classes.length} classes</p><span className={`status ${a.status}`}>{a.status.replace('_',' ')}</span></div><div className="history-score">{a.score??'—'}<small>/100</small></div><button className="review-button" onClick={()=>review(a)}>Review <ArrowUpRight size={14}/></button></article>)}</div>:<div className="empty-state"><History size={25}/><h2>No attempts yet</h2><p>Your first design will appear here after submission.</p><button onClick={()=>setTab('practice')}>Start your first attempt <ChevronRight size={15}/></button></div>}</section>}
        <footer className="footer"><span>CRAFT / LLD PRACTICE STUDIO</span><span>Built for deliberate practice <span className="footer-dot">●</span></span></footer>
      </div>
    </main>
  </div>;
}
