import type { ReactNode } from "react";

// Markdown sencillo para las respuestas del asistente: títulos (#), listas con guion o número,
// **negrita**, *cursiva*, `código` y saltos de línea. Nada de HTML: React escapa todo el texto,
// así lo que escriba el modelo nunca se ejecuta. Las citas las resuelve quien llama, en
// `enLinea`, antes de que se busquen negritas dentro de ellas.

type EnLinea = (texto: string, clave: string) => ReactNode;

const VINETA = /^\s*[-*•]\s+(.*)$/;
const NUMERO = /^\s*\d+[.)]\s+(.*)$/;
const TITULO = /^\s*#{1,6}\s+(.*?)\s*#*\s*$/;

type Bloque =
  | { tipo: "parrafo"; lineas: string[] }
  | { tipo: "titulo"; texto: string }
  | { tipo: "lista"; ordenada: boolean; items: string[] };

function bloques(texto: string): Bloque[] {
  const lista: Bloque[] = [];
  for (const linea of texto.split("\n")) {
    const ultimo = lista[lista.length - 1];
    if (!linea.trim()) {
      lista.push({ tipo: "parrafo", lineas: [] });
      continue;
    }
    const titulo = linea.match(TITULO);
    const vineta = linea.match(VINETA);
    const numero = linea.match(NUMERO);
    if (titulo) lista.push({ tipo: "titulo", texto: titulo[1] });
    else if (vineta || numero) {
      const ordenada = Boolean(numero);
      const item = (vineta ?? numero)![1];
      if (ultimo?.tipo === "lista" && ultimo.ordenada === ordenada) ultimo.items.push(item);
      else lista.push({ tipo: "lista", ordenada, items: [item] });
    } else if (ultimo?.tipo === "lista" && /^\s{2,}/.test(linea)) {
      // Una línea con sangría sigue el punto anterior.
      ultimo.items[ultimo.items.length - 1] += ` ${linea.trim()}`;
    } else if (ultimo?.tipo === "parrafo") ultimo.lineas.push(linea);
    else lista.push({ tipo: "parrafo", lineas: [linea] });
  }
  return lista.filter((b) => b.tipo !== "parrafo" || b.lineas.length > 0);
}

const ENFASIS = /(\*\*|__)(.+?)\1|(\*|_)(?!\s)(.+?)(?<!\s)\3|`([^`]+)`/g;

/** Negrita, cursiva y código dentro de un pedazo de texto que no es una cita. */
export function conEnfasis(texto: string, clave: string): ReactNode[] {
  const partes: ReactNode[] = [];
  let desde = 0;
  for (const marca of texto.matchAll(ENFASIS)) {
    partes.push(texto.slice(desde, marca.index));
    const k = `${clave}-${marca.index}`;
    if (marca[2] !== undefined) partes.push(<strong key={k}>{marca[2]}</strong>);
    else if (marca[4] !== undefined) partes.push(<em key={k}>{marca[4]}</em>);
    else partes.push(<code key={k}>{marca[5]}</code>);
    desde = (marca.index ?? 0) + marca[0].length;
  }
  partes.push(texto.slice(desde));
  return partes;
}

export function Markdown({ texto, enLinea }: { texto: string; enLinea: EnLinea }) {
  return (
    <>
      {bloques(texto).map((bloque, i) => {
        if (bloque.tipo === "titulo") return <h4 key={i}>{enLinea(bloque.texto, `t${i}`)}</h4>;
        if (bloque.tipo === "lista") {
          const Lista = bloque.ordenada ? "ol" : "ul";
          return (
            <Lista key={i}>
              {bloque.items.map((item, j) => (
                <li key={j}>{enLinea(item, `l${i}-${j}`)}</li>
              ))}
            </Lista>
          );
        }
        return (
          <p key={i}>
            {bloque.lineas.map((linea, j) => (
              <span key={j}>
                {j > 0 && <br />}
                {enLinea(linea, `p${i}-${j}`)}
              </span>
            ))}
          </p>
        );
      })}
    </>
  );
}
