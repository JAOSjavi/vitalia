import "./MisDocumentos.css";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useId, useRef, useState } from "react";

import { ErrorDeApi } from "../api/cliente";
import {
  direccionDelArchivo,
  eliminarDocumento,
  misDocumentos,
  subirDocumento,
  TAMANO_MAXIMO,
  type Documento,
  type TipoDeDocumento,
} from "../api/documentos";
import { ESTADOS_DE_LECTURA, TIPOS_DE_DOCUMENTO } from "../comunes/estados";
import { diaCorto, diaIso } from "../comunes/fechas";
import {
  CameraIcon,
  EyeIcon,
  FileTextIcon,
  ImageIcon,
  SparkleIcon,
  TrashIcon,
  UploadSimpleIcon,
  XIcon,
} from "../comunes/iconos";
import { Boton } from "../comunes/piezas/Boton";
import { Campo, Entrada } from "../comunes/piezas/Campo";
import { Estado } from "../comunes/piezas/Estado";
import { Hoja } from "../comunes/piezas/Hoja";
import { Nota } from "../comunes/piezas/Nota";

const EXPLICACION: Partial<Record<Documento["estado_lectura"], string>> = {
  en_proceso: "Estamos leyendo el documento. Tarda unos segundos.",
  sin_leer:
    "Es una foto o un escaneado: se lee cuando autorice el uso de IA. La doctora sí puede verlo.",
  no_legible:
    "No se pudo leer el texto. La doctora puede verlo, pero el asistente no lo usa. Pruebe con una foto más nítida.",
};

function detalle(documento: Documento) {
  const partes = [TIPOS_DE_DOCUMENTO[documento.tipo], diaCorto(documento.fecha_documento)];
  if (documento.formato !== "pdf") partes.push("foto");
  else if (documento.paginas) partes.push(`${documento.paginas} pág.`);
  return partes.join(" · ");
}

/** P-07, como en el lienzo: subir, ver y eliminar mis documentos (HU-028, HU-029, HU-031). */
export function MisDocumentos() {
  const consultas = useQueryClient();
  const lista = useQuery({
    queryKey: ["mis-documentos"],
    queryFn: misDocumentos,
    // Mientras alguno se está leyendo, la lista se vuelve a pedir cada pocos segundos.
    refetchInterval: (consulta) =>
      consulta.state.data?.documentos.some((d) => d.estado_lectura === "en_proceso") ? 3000 : false,
  });
  const [subiendo, setSubiendo] = useState(false);
  const [porEliminar, setPorEliminar] = useState<string | null>(null);
  const [fallo, setFallo] = useState<string | null>(null);
  const documentos = lista.data?.documentos ?? [];

  async function eliminar(documento: Documento) {
    setFallo(null);
    try {
      await eliminarDocumento(documento.id);
      setPorEliminar(null);
      await consultas.invalidateQueries({ queryKey: ["mis-documentos"] });
    } catch (error) {
      setFallo(error instanceof ErrorDeApi ? error.message : "No se pudo eliminar el documento.");
    }
  }

  return (
    <main className="mis-documentos">
      <header className="zona-paciente__encabezado">
        <h1>Mis documentos</h1>
        <button type="button" className="mis-documentos__subir" onClick={() => setSubiendo(true)}>
          <UploadSimpleIcon aria-hidden="true" />
          Subir
        </button>
      </header>

      {lista.data && (
        <div className="mis-documentos__ia">
          <span className="mis-documentos__ia-icono" aria-hidden="true">
            <SparkleIcon />
          </span>
          <span className="mis-documentos__ia-texto">
            <strong>
              {lista.data.ia_autorizada ? "Asistente de IA autorizado" : "Asistente de IA sin autorizar"}
            </strong>
            <span>
              {lista.data.ia_autorizada
                ? "La doctora puede resumir sus documentos."
                : "La doctora ve sus documentos, pero el asistente no los usa."}
            </span>
          </span>
        </div>
      )}

      {fallo && <Nota tono="rojo">{fallo}</Nota>}
      {lista.isError && <Nota tono="rojo">No se pudo cargar la lista. Recargue la página.</Nota>}
      {lista.data && !documentos.length && (
        <Nota>Todavía no ha subido documentos. Suba sus historias clínicas, exámenes o fórmulas.</Nota>
      )}

      {documentos.length > 0 && (
        <>
          <h2 className="mis-documentos__rotulo">
            {documentos.length} {documentos.length === 1 ? "documento subido" : "documentos subidos"}
          </h2>
          <section className="mis-documentos__lista" aria-label="Documentos subidos">
            {documentos.map((documento) => {
              const estado = ESTADOS_DE_LECTURA[documento.estado_lectura];
              return (
                <article key={documento.id} className="mis-documentos__documento">
                  <div className="mis-documentos__cabeza">
                    <span className="mis-documentos__icono" aria-hidden="true">
                      {documento.formato === "pdf" ? <FileTextIcon /> : <ImageIcon />}
                    </span>
                    <div className="mis-documentos__texto">
                      <span className="mis-documentos__nombre">{documento.nombre}</span>
                      <span className="mis-documentos__detalle">{detalle(documento)}</span>
                    </div>
                  </div>
                  {EXPLICACION[documento.estado_lectura] && (
                    <p className="mis-documentos__explicacion">{EXPLICACION[documento.estado_lectura]}</p>
                  )}
                  {porEliminar === documento.id ? (
                    <Nota tono="rojo">
                      <span>
                        ¿Eliminar «{documento.nombre}»? La doctora y el asistente dejarán de verlo.
                      </span>
                      <div className="mis-documentos__confirmar">
                        <Boton clase="neutro" onClick={() => setPorEliminar(null)}>
                          No
                        </Boton>
                        <Boton onClick={() => eliminar(documento)}>Sí, eliminar</Boton>
                      </div>
                    </Nota>
                  ) : (
                    <div className="mis-documentos__pie">
                      <Estado tono={estado.tono}>{estado.nombre}</Estado>
                      <div className="mis-documentos__acciones">
                        <a
                          className="mis-documentos__ver"
                          href={direccionDelArchivo(documento.id)}
                          target="_blank"
                          rel="noopener"
                        >
                          <EyeIcon aria-hidden="true" />
                          Ver
                        </a>
                        <button
                          type="button"
                          className="mis-documentos__eliminar"
                          aria-label={`Eliminar ${documento.nombre}`}
                          onClick={() => setPorEliminar(documento.id)}
                        >
                          <TrashIcon aria-hidden="true" />
                        </button>
                      </div>
                    </div>
                  )}
                </article>
              );
            })}
          </section>
        </>
      )}

      {subiendo && (
        <SubirDocumentos
          alCerrar={() => setSubiendo(false)}
          alSubir={() => consultas.invalidateQueries({ queryKey: ["mis-documentos"] })}
        />
      )}
    </main>
  );
}

type Resultado = "esperando" | "subiendo" | "subido" | string;

type PorSubir = { clave: string; archivo: File; nombre: string; resultado: Resultado };

const FORMATOS = ".pdf,.jpg,.jpeg,.png,application/pdf,image/jpeg,image/png";

/** El nombre del archivo sin la extensión, como punto de partida para el nombre del documento. */
function nombreInicial(archivo: File) {
  return archivo.name.replace(/\.[^.]+$/, "").replace(/[_-]+/g, " ").trim().slice(0, 120);
}

/** Lo que se puede saber antes de enviarlo. El servidor lo vuelve a revisar todo. */
function problemaDelArchivo(archivo: File): string | null {
  if (archivo.size > TAMANO_MAXIMO) return "Pesa más de 20 MB.";
  const aceptado =
    /\.(pdf|jpe?g|png)$/i.test(archivo.name) ||
    /^(application\/pdf|image\/(jpeg|png))$/.test(archivo.type);
  return aceptado ? null : "Solo se aceptan archivos PDF, JPG o PNG.";
}

/** La hoja para subir: varios archivos o una foto, cada uno con su nombre (HU-028). */
function SubirDocumentos({ alCerrar, alSubir }: { alCerrar: () => void; alSubir: () => void }) {
  const [porSubir, setPorSubir] = useState<PorSubir[]>([]);
  const [fecha, setFecha] = useState(diaIso(new Date()));
  const [tipo, setTipo] = useState<TipoDeDocumento>("historia_clinica");
  const [enviando, setEnviando] = useState(false);
  const elegir = useRef<HTMLInputElement>(null);
  const foto = useRef<HTMLInputElement>(null);
  const id = useId();

  function agregar(archivos: FileList | null) {
    if (!archivos?.length) return;
    const nuevos = Array.from(archivos).map((archivo) => ({
      clave: `${archivo.name}-${archivo.size}-${archivo.lastModified}`,
      archivo,
      nombre: nombreInicial(archivo) || "Documento",
      resultado: problemaDelArchivo(archivo) ?? "esperando",
    }));
    setPorSubir((antes) => [
      ...antes.filter((a) => a.resultado !== "subido"),
      ...nuevos.filter((n) => !antes.some((a) => a.clave === n.clave)),
    ]);
  }

  function cambiar(clave: string, cambio: Partial<PorSubir>) {
    setPorSubir((antes) => antes.map((a) => (a.clave === clave ? { ...a, ...cambio } : a)));
  }

  const listos = porSubir.filter((a) => a.resultado !== "subido" && !problemaDelArchivo(a.archivo));

  async function subir() {
    setEnviando(true);
    // Cada archivo va por su lado: si uno falla, los demás se guardan igual (CA-3).
    const resultados = await Promise.all(
      listos.map(async (a) => {
        cambiar(a.clave, { resultado: "subiendo" });
        try {
          await subirDocumento({ archivo: a.archivo, nombre: a.nombre, fecha_documento: fecha, tipo });
        } catch (error) {
          // El mismo archivo otra vez: ya está guardado, no es un fallo (CA-5).
          if (!(error instanceof ErrorDeApi && error.codigo === "documento_repetido")) {
            const motivo =
              error instanceof ErrorDeApi
                ? (Object.values(error.campos)[0] ?? error.message)
                : "Se perdió la conexión. Puede reintentar.";
            cambiar(a.clave, { resultado: motivo });
            return false;
          }
        }
        cambiar(a.clave, { resultado: "subido" });
        return true;
      }),
    );
    setEnviando(false);
    alSubir();
    if (resultados.every(Boolean) && porSubir.every((a) => !problemaDelArchivo(a.archivo))) {
      alCerrar();
    }
  }

  const reintentar = listos.some((a) => a.resultado !== "esperando");

  return (
    <Hoja titulo="Subir documentos" icono={<UploadSimpleIcon />} alCerrar={alCerrar}>
      <p className="texto-suave mis-documentos__ayuda">
        PDF, JPG o PNG de hasta 20 MB. Puede elegir varios a la vez.
      </p>
      <div className="mis-documentos__elegir">
        <Boton clase="borde" onClick={() => elegir.current?.click()}>
          <UploadSimpleIcon />
          Elegir archivos
        </Boton>
        <Boton clase="borde" onClick={() => foto.current?.click()}>
          <CameraIcon />
          Tomar foto
        </Boton>
        <input
          ref={elegir}
          type="file"
          multiple
          accept={FORMATOS}
          hidden
          data-testid="elegir-archivos"
          onChange={(evento) => {
            agregar(evento.target.files);
            evento.target.value = "";
          }}
        />
        <input
          ref={foto}
          type="file"
          accept="image/jpeg,image/png"
          capture="environment"
          hidden
          onChange={(evento) => {
            agregar(evento.target.files);
            evento.target.value = "";
          }}
        />
      </div>

      {porSubir.length > 0 && (
        <ul className="mis-documentos__por-subir">
          {porSubir.map((a) => (
            <li key={a.clave} className="mis-documentos__archivo">
              <div className="mis-documentos__fila">
                <Entrada
                  aria-label={`Nombre del documento ${a.archivo.name}`}
                  value={a.nombre}
                  maxLength={120}
                  disabled={a.resultado === "subido" || enviando}
                  onChange={(evento) => cambiar(a.clave, { nombre: evento.target.value })}
                />
                {a.resultado !== "subido" && !enviando && (
                  <button
                    type="button"
                    className="mis-documentos__quitar"
                    aria-label={`Quitar ${a.archivo.name}`}
                    onClick={() => setPorSubir((antes) => antes.filter((x) => x.clave !== a.clave))}
                  >
                    <XIcon />
                  </button>
                )}
              </div>
              <ResultadoDeSubida resultado={a.resultado} />
            </li>
          ))}
        </ul>
      )}

      {listos.length > 0 && (
        <div className="mis-documentos__datos">
          <Campo id={`${id}-fecha`} etiqueta="Fecha del documento">
            <Entrada
              id={`${id}-fecha`}
              type="date"
              value={fecha}
              max={diaIso(new Date())}
              onChange={(evento) => setFecha(evento.target.value)}
            />
          </Campo>
          <Campo id={`${id}-tipo`} etiqueta="Tipo">
            <select
              id={`${id}-tipo`}
              className="selector"
              value={tipo}
              onChange={(evento) => setTipo(evento.target.value as TipoDeDocumento)}
            >
              {Object.entries(TIPOS_DE_DOCUMENTO).map(([valor, nombre]) => (
                <option key={valor} value={valor}>
                  {nombre}
                </option>
              ))}
            </select>
          </Campo>
          <Boton onClick={subir} disabled={enviando || listos.some((a) => !a.nombre.trim())}>
            {enviando
              ? "Subiendo…"
              : reintentar
                ? "Reintentar"
                : listos.length === 1
                  ? "Subir documento"
                  : `Subir ${listos.length} documentos`}
          </Boton>
        </div>
      )}
    </Hoja>
  );
}

function ResultadoDeSubida({ resultado }: { resultado: Resultado }) {
  if (resultado === "esperando") return null;
  if (resultado === "subiendo") return <span className="texto-suave">Subiendo…</span>;
  if (resultado === "subido") return <Estado tono="verde">Subido</Estado>;
  return (
    <p className="mis-documentos__fallo" role="alert">
      <span className="mis-documentos__punto" aria-hidden="true" />
      {resultado}
    </p>
  );
}
