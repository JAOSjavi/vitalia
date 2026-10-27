import "./Asistente.css";

import { useId, useState, type FormEvent, type ReactNode } from "react";

import { ErrorDeApi } from "../api/cliente";
import {
  direccionDelArchivo,
  preguntarAlAsistente,
  RespuestaInterrumpida,
  type FinDeRespuesta,
  type Origen,
  type Turno,
} from "../api/documentos";
import { InfoIcon, PaperPlaneRightIcon, SparkleIcon } from "../comunes/iconos";
import { Estado } from "../comunes/piezas/Estado";
import { Nota } from "../comunes/piezas/Nota";

type Mensaje = Turno & { fin?: FinDeRespuesta; error?: string };

const SUGERENCIAS = ["¿Qué medicamentos toma?", "¿Tiene alergias?", "¿Cómo salieron los laboratorios?"];

// Igual que en el servidor: [D2, pág. 1: "frase"], con o sin la frase.
const CITA = /\[\s*(D\d+)\s*,\s*p[áa]g(?:ina)?\.?\s*(\d+)\s*(?::\s*["“«](.*?)["”»]\s*)?\]/gi;

type Propiedades = {
  paciente: string;
  iaAutorizada: boolean;
  /** Documento → etiqueta (D1, D2...), las mismas de la ficha y de las respuestas. */
  etiquetas: Map<string, string>;
};

/** El panel del asistente en la ficha, como en el lienzo (HU-034; HU-025, CA-3). */
export function Asistente({ paciente, iaAutorizada, etiquetas }: Propiedades) {
  const [mensajes, setMensajes] = useState<Mensaje[]>([]);
  const [pregunta, setPregunta] = useState("");
  const [ocupado, setOcupado] = useState(false);
  const id = useId();
  const documentoDe = new Map([...etiquetas].map(([documento, etiqueta]) => [etiqueta, documento]));

  function actualizarUltimo(cambio: (ultimo: Mensaje) => Mensaje) {
    setMensajes((antes) => [...antes.slice(0, -1), cambio(antes[antes.length - 1])]);
  }

  async function preguntar(texto: string) {
    const limpia = texto.trim();
    if (!limpia || ocupado) return;
    // La conversación no se guarda en el servidor: viaja con cada pregunta.
    const conversacion: Turno[] = mensajes
      .filter((m) => !m.error)
      .map(({ autor, texto: t }) => ({ autor, texto: t }));
    setMensajes((antes) => [
      ...antes,
      { autor: "medico", texto: limpia },
      { autor: "asistente", texto: "" },
    ]);
    setPregunta("");
    setOcupado(true);
    try {
      const fin = await preguntarAlAsistente(paciente, limpia, conversacion, (parte) =>
        actualizarUltimo((ultimo) => ({ ...ultimo, texto: ultimo.texto + parte })),
      );
      actualizarUltimo((ultimo) => ({ ...ultimo, fin }));
    } catch (error) {
      const mensaje =
        error instanceof ErrorDeApi || error instanceof RespuestaInterrumpida
          ? error.message
          : "No se pudo hablar con el asistente. Revise la conexión e intente de nuevo.";
      actualizarUltimo((ultimo) => ({ ...ultimo, error: mensaje }));
    } finally {
      setOcupado(false);
    }
  }

  function enviar(evento: FormEvent) {
    evento.preventDefault();
    void preguntar(pregunta);
  }

  return (
    <section className="asistente" aria-labelledby={`${id}-titulo`}>
      <div className="asistente__encabezado">
        <h2 id={`${id}-titulo`}>
          <span className="asistente__icono" aria-hidden="true">
            <SparkleIcon />
          </span>
          Asistente
        </h2>
        {iaAutorizada ? (
          <Estado tono="verde">Autorizado por el paciente</Estado>
        ) : (
          <Estado tono="gris">Sin autorización</Estado>
        )}
      </div>

      {!iaAutorizada ? (
        <p className="asistente__nota">
          El paciente no ha autorizado el uso de inteligencia artificial con sus datos. Sus
          documentos se pueden leer, pero el asistente no está disponible.
        </p>
      ) : (
        <div className="asistente__preguntas">
          <h3>Preguntar sobre los documentos</h3>

          {mensajes.map((m, i) =>
            m.autor === "medico" ? (
              <p key={i} className="asistente__pregunta">
                {m.texto}
              </p>
            ) : (
              <Respuesta key={i} mensaje={m} documentoDe={documentoDe} />
            ),
          )}

          <div className="asistente__sugerencias">
            {SUGERENCIAS.map((s) => (
              <button
                key={s}
                type="button"
                className="asistente__sugerencia"
                disabled={ocupado}
                onClick={() => preguntar(s)}
              >
                {s}
              </button>
            ))}
          </div>

          <form className="asistente__caja" onSubmit={enviar}>
            <label htmlFor={`${id}-pregunta`} className="visualmente-oculto">
              Su pregunta
            </label>
            <input
              id={`${id}-pregunta`}
              type="text"
              className="asistente__entrada"
              placeholder="Escriba su pregunta sobre los documentos"
              maxLength={1000}
              autoComplete="off"
              value={pregunta}
              onChange={(evento) => setPregunta(evento.target.value)}
            />
            <button
              type="submit"
              className="asistente__enviar"
              aria-label="Enviar la pregunta"
              disabled={ocupado || !pregunta.trim()}
            >
              <PaperPlaneRightIcon aria-hidden="true" />
            </button>
          </form>

          <p className="asistente__nota asistente__nota--con-icono">
            <InfoIcon aria-hidden="true" />
            <span>
              El asistente resume lo que está escrito. No diagnostica ni reemplaza la lectura del
              documento. Cada consulta queda en la bitácora.
            </span>
          </p>
        </div>
      )}
    </section>
  );
}

type PropiedadesDeRespuesta = { mensaje: Mensaje; documentoDe: Map<string, string> };

function Respuesta({ mensaje, documentoDe }: PropiedadesDeRespuesta) {
  if (mensaje.error) return <Nota tono="rojo">{mensaje.error}</Nota>;
  if (!mensaje.texto) {
    return <p className="asistente__respuesta asistente__buscando">Buscando en los documentos…</p>;
  }
  const consultado = mensaje.fin?.consultado ?? [];
  return (
    <div className="asistente__respuesta">
      {mensaje.texto.split(/\n{2,}/).map((parrafo, i) => (
        <p key={i}>{conCitas(parrafo, documentoDe, mensaje.fin)}</p>
      ))}
      {consultado.length > 0 && (
        <p className="asistente__consultado">
          Consultó:{" "}
          {consultado
            .map(
              (c) =>
                `${[...documentoDe].find(([, d]) => d === c.documento_id)?.[0] ?? c.documento} (${
                  c.paginas.length === 1 ? "pág." : "págs."
                } ${c.paginas.join(", ")})`,
            )
            .join(" · ")}
        </p>
      )}
    </div>
  );
}

/** El texto con cada cita convertida en un botón "D2 · pág. 1" que abre el documento ahí. */
function conCitas(texto: string, documentoDe: Map<string, string>, fin?: FinDeRespuesta) {
  const partes: ReactNode[] = [];
  let desde = 0;
  for (const cita of texto.matchAll(CITA)) {
    const etiqueta = cita[1].toUpperCase();
    const pagina = Number(cita[2]);
    const frase = (cita[3] ?? "").trim();
    partes.push(texto.slice(desde, cita.index));
    partes.push(
      <Cita
        key={cita.index}
        etiqueta={etiqueta}
        pagina={pagina}
        documento={documentoDe.get(etiqueta)}
        origen={fin?.origenes.find(
          (o) => o.etiqueta === etiqueta && o.pagina === pagina && o.frase === frase,
        )}
        terminada={Boolean(fin)}
      />,
    );
    desde = (cita.index ?? 0) + cita[0].length;
  }
  partes.push(texto.slice(desde));
  return partes;
}

type PropiedadesDeCita = {
  etiqueta: string;
  pagina: number;
  documento?: string;
  origen?: Origen;
  terminada: boolean;
};

function Cita({ etiqueta, pagina, documento, origen, terminada }: PropiedadesDeCita) {
  const texto = `${etiqueta} · pág. ${pagina}`;
  // Al terminar, el servidor ya comprobó: sin origen, la cita no corresponde a lo enviado.
  if (terminada && !origen) {
    return (
      <span className="asistente__cita asistente__cita--descartada" title="Origen no comprobado">
        {texto}
      </span>
    );
  }
  const sinVerificar = origen && !origen.verificado;
  const titulo = sinVerificar
    ? "La frase no aparece tal cual en esa página: revise el documento"
    : `Abrir ${origen?.documento ?? etiqueta} en la página ${pagina}`;
  if (!documento) return <span className="asistente__cita">{texto}</span>;
  return (
    <a
      className={`asistente__cita ${sinVerificar ? "asistente__cita--sin-verificar" : ""}`}
      href={direccionDelArchivo(documento, pagina)}
      target="_blank"
      rel="noopener"
      title={titulo}
      aria-label={sinVerificar ? `${texto}, frase sin verificar` : texto}
    >
      {sinVerificar && <span className="asistente__punto" aria-hidden="true" />}
      {texto}
    </a>
  );
}
