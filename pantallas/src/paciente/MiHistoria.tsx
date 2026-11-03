import "./MiHistoria.css";

import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router";

import { miHistoria } from "../api/historia";
import { diaCorto, diaIso, hora } from "../comunes/fechas";
import { CaretLeftIcon, CaretRightIcon } from "../comunes/iconos";
import { Nota } from "../comunes/piezas/Nota";
import { resumenDeAtencion, useFormulario, VistaDeAtencion } from "../comunes/VistaDeAtencion";

/**
 * Las atenciones cerradas del consultorio, con su diagnóstico, su fórmula y las notas del médico
 * (HU-045). En computador la lista y la atención elegida van lado a lado; en celular, una a la vez.
 */
export function MiHistoria() {
  const { atencion: elegida } = useParams();
  const historia = useQuery({ queryKey: ["mi-historia"], queryFn: miHistoria });
  const f = useFormulario().data;
  const atenciones = historia.data ?? [];
  const actual = atenciones.find((a) => a.id === elegida) ?? (elegida ? undefined : atenciones[0]);

  return (
    <main className={`mi-historia ${elegida ? "mi-historia--con-detalle" : ""}`}>
      <header className="zona-paciente__encabezado">
        <h1>Mi historia clínica</h1>
      </header>
      <p className="mi-historia__ayuda">
        Lo que su médico registró en cada atención del consultorio. Los documentos que usted sube
        están en Documentos.
      </p>

      {historia.isError && <Nota tono="rojo">No se pudo cargar su historia clínica.</Nota>}
      {historia.isSuccess && !atenciones.length && (
        <Nota>Todavía no tiene atenciones cerradas en el consultorio.</Nota>
      )}

      {atenciones.length > 0 && (
        <div className="mi-historia__columnas">
          <nav className="mi-historia__lista" aria-label="Atenciones">
            {atenciones.map((atencion) => {
              const principal = atencion.diagnosticos.find((dx) => dx.principal);
              return (
                <Link
                  key={atencion.id}
                  to={`/paciente/historia/${atencion.id}`}
                  className="mi-historia__atencion"
                  aria-current={actual?.id === atencion.id ? "page" : undefined}
                >
                  <span className="mi-historia__fecha">
                    {diaCorto(diaIso(atencion.inicio))} · {hora(atencion.inicio)}
                  </span>
                  <span className="mi-historia__titulo">
                    {principal?.nombre ?? resumenDeAtencion(atencion, f)}
                  </span>
                  <span className="mi-historia__medico">{atencion.firma?.nombre}</span>
                  <CaretRightIcon aria-hidden="true" className="mi-historia__flecha" />
                </Link>
              );
            })}
          </nav>

          {actual && (
            <article className="mi-historia__detalle" aria-label="Atención elegida">
              <Link to="/paciente/historia" className="mi-historia__volver">
                <CaretLeftIcon aria-hidden="true" />
                Todas las atenciones
              </Link>
              <h2>
                {diaCorto(diaIso(actual.inicio))}
                <span className="mi-historia__suave"> · {resumenDeAtencion(actual, f)}</span>
              </h2>
              <VistaDeAtencion atencion={actual} />
            </article>
          )}
        </div>
      )}
    </main>
  );
}
