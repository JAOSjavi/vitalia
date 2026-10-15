import "./Pasos.css";

/** Barra que muestra en qué paso va un formulario largo. */
export function Pasos({ total, actual }: { total: number; actual: number }) {
  return (
    <div className="pasos" role="img" aria-label={`Paso ${actual} de ${total}`}>
      {Array.from({ length: total }, (_, indice) => (
        <span key={indice} className={indice < actual ? "pasos__hecho" : ""} />
      ))}
    </div>
  );
}
