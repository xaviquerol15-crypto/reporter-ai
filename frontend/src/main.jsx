import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";
const labels = { verdadero:"VERDADERO", falso:"FALSO", enganoso:"ENGAÑOSO", no_verificable:"NO VERIFICABLE" };

function App() {
  const [text,setText]=useState(""); const [loading,setLoading]=useState(false);
  const [report,setReport]=useState(null); const [error,setError]=useState("");

  async function analyze() {
    if (text.trim().length<10) return;
    setLoading(true); setError(""); setReport(null);
    try {
      const res=await fetch(`${API}/api/analyze`, {
        method:"POST", headers:{"Content-Type":"application/json"},
        body:JSON.stringify({text})
      });
      const data=await res.json();
      if(!res.ok) throw new Error(data.detail||"No se pudo analizar.");
      setReport(data);
    } catch(e) { setError(e.message); } finally { setLoading(false); }
  }

  return <div className="page">
    <header><div className="brand">REPORTER <span>AI</span></div><p>Verificación de noticias basada en evidencias.</p></header>
    <main>
      <section className="hero">
        <h1>¿Es cierto lo que estás leyendo?</h1>
        <p>Pega una noticia o afirmación. Reporter AI separará las afirmaciones y comprobará cada una.</p>
        <textarea value={text} onChange={e=>setText(e.target.value)} placeholder="Pega aquí una noticia, titular o afirmación..." />
        <button disabled={loading||text.trim().length<10} onClick={analyze}>{loading?"Verificando...":"Analizar noticia"}</button>
        {error&&<div className="error">{error}</div>}
      </section>

      {report&&<section className="report">
        <div className={`global verdict-${report.verdict}`}>
          <div><small>RESULTADO GLOBAL</small><h2>{labels[report.verdict]}</h2></div>
          <strong>{report.confidence}%</strong>
        </div>
        <p className="summary">{report.summary}</p>
        <h2>Afirmaciones verificadas</h2>
        {report.claims.map(item=><article className="claim" key={item.claim.id}>
          <div className="claim-head"><span>Afirmación {item.claim.id}</span><b className={`tag tag-${item.verdict}`}>{labels[item.verdict]}</b></div>
          <h3>{item.claim.text}</h3><div className="confidence">Confianza: {item.confidence}%</div>
          <p>{item.explanation}</p>
          {item.evidence.length>0&&<><h4>Evidencias</h4><ul>{item.evidence.map((ev,i)=><li key={i}>
            <a href={ev.url} target="_blank" rel="noreferrer">{ev.url}</a>
            <span>{ev.supports?"Apoya":"Contradice"} · fuerza {ev.strength}%</span>
            <p>{ev.explanation}</p>
          </li>)}</ul></>}
          <details><summary>Fuentes recuperadas</summary><ul>{item.sources.map(s=><li key={s.url}>
            <a href={s.url} target="_blank" rel="noreferrer">{s.title||s.domain}</a>
            <span>Puntuación heurística: {s.source_score}/100</span>
          </li>)}</ul></details>
        </article>)}
      </section>}
    </main>
    <footer>Reporter AI no sustituye la comprobación humana. “No verificable” significa que la evidencia recuperada no permite una conclusión fiable.</footer>
  </div>;
}
createRoot(document.getElementById("root")).render(<App />);
