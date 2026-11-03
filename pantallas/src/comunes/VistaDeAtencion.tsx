import "./VistaDeAtencion.css";

import { useQuery } from "@tanstack/react-query";
import type { ReactNode } from "react";

import { formulario, type Atencion, type Formulario, type Valor } from "../api/historia";
import { diaCorto, diaIso, hora } from "./fechas";

export function useFormulario() {
  return useQuery({ queryKey: ["formulario-historia"], queryFn: formulario, staleTime: Infinity });
}

/** Un valor como lo lee una persona: la opción con su nombre, el decimal con coma, sí o no. */
export function legible(campo: string, valor: Valor, f: Formulario): string | null {
  if (valor === null || valor === "") return null;
  const descripcion = f.atencion[campo] ?? f.identificacion[campo];
  if (descripcion?.lista) return f.listas[descripcion.lista]?.[String(valor)] ?? String(valor);
  if (typeof valor === "boolean") return valor ? "Sí" : "No";
  if (typeof valor === "number") {
    const numero = String(valor).replace(".", ",");
    return descripcion?.unidad ? `${numero} ${descripcion.unidad}` : numero;
  }
  return valor;
}

function Dato({ etiqueta, children }: { etiqueta: string; children: ReactNode }) {
  if (children === null || children === undefined || children === "") return null;
  return (
    <div className="vista-atencion__dato">
      <dt>{etiqueta}</dt>
      <dd>{children}</dd>
    </div>
  );
}

function Seccion({ titulo, children }: { titulo: string; children: ReactNode }) {
  return (
    <section className="vista-atencion__seccion">
      <h3>{titulo}</h3>
      <dl>{children}</dl>
    </section>
  );
}

/**
 * Una atención cerrada, de solo lectura, en el orden del formulario. La usan el médico en la
 * historia del paciente (HU-045) y el paciente en la suya.
 */
export function VistaDeAtencion({ atencion }: { atencion: Atencion }) {
  const f = useFormulario().data;
  if (!f) return null;
  const d = atencion.datos;
  const v = (campo: string) => legible(campo, d[campo] ?? null, f);
  const texto = (campo: string) => (
    <Dato etiqueta={f.atencion[campo].nombre}>{v(campo)}</Dato>
  );
  const tension =
    d.tension_sistolica && d.tension_diastolica
      ? `${d.tension_sistolica}/${d.tension_diastolica} mmHg`
      : null;
  const tipos = f.listas.tipo_diagnostico;
  const vias = f.listas.via;
  const acompanante = [d.acompanante_nombre, d.acompanante_parentesco, d.acompanante_telefono]
    .filter(Boolean)
    .join(" · ");

  return (
    <div className="vista-atencion">
      <Seccion titulo="Datos de la consulta">
        {texto("tipo_consulta")}
        {texto("finalidad")}
        {texto("causa")}
        <Dato etiqueta="Acompañante">{acompanante}</Dato>
      </Seccion>

      <Seccion titulo="Motivo de consulta y enfermedad actual">
        {texto("motivo")}
        {texto("enfermedad_actual")}
      </Seccion>

      <Seccion titulo="Antecedentes">
        {texto("antecedentes_personales")}
        {texto("antecedentes_familiares")}
        {texto("alergias")}
        {texto("factores_riesgo")}
      </Seccion>

      <Seccion titulo="Revisión por sistemas">
        {texto("revision_sistemas")}
        {texto("sintomatico_respiratorio")}
        {texto("sintomatico_piel")}
      </Seccion>

      <Seccion titulo="Signos vitales y examen físico">
        <div className="vista-atencion__signos">
          <Dato etiqueta="Tensión arterial">{tension}</Dato>
          <Dato etiqueta="Frec. cardiaca">{v("frecuencia_cardiaca")}</Dato>
          <Dato etiqueta="Frec. respiratoria">{v("frecuencia_respiratoria")}</Dato>
          <Dato etiqueta="Temperatura">{v("temperatura")}</Dato>
          <Dato etiqueta="Saturación">{v("saturacion")}</Dato>
          <Dato etiqueta="Peso">{v("peso")}</Dato>
          <Dato etiqueta="Talla">{v("talla")}</Dato>
          <Dato etiqueta="Índice de masa corporal">
            {atencion.imc === null ? null : String(atencion.imc).replace(".", ",")}
          </Dato>
        </div>
        {texto("examen_fisico")}
      </Seccion>

      <Seccion titulo="Diagnóstico">
        {atencion.diagnosticos.length > 0 && (
          <div className="vista-atencion__dato">
            <dt>Diagnósticos</dt>
            <dd>
              <ul className="vista-atencion__lista">
                {atencion.diagnosticos.map((dx) => (
                  <li key={dx.codigo}>
                    <span className="vista-atencion__codigo">{dx.codigo}</span> {dx.nombre}
                    <span className="vista-atencion__detalle">
                      {dx.principal ? "Principal" : "Relacionado"} · {tipos[dx.tipo] ?? dx.tipo}
                    </span>
                  </li>
                ))}
              </ul>
            </dd>
          </div>
        )}
        {texto("analisis")}
      </Seccion>

      <Seccion titulo="Plan, fórmula, órdenes e incapacidad">
        {texto("plan")}
        {texto("recomendaciones")}
        {atencion.medicamentos.length > 0 && (
          <div className="vista-atencion__dato">
            <dt>Fórmula</dt>
            <dd>
              <ul className="vista-atencion__lista">
                {atencion.medicamentos.map((m, i) => (
                  <li key={i}>
                    <strong>{m.nombre}</strong>
                    <span className="vista-atencion__detalle">
                      {[m.dosis, `vía ${(vias[m.via] ?? m.via).toLowerCase()}`, m.frecuencia, `${m.dias} días`, m.indicaciones]
                        .filter(Boolean)
                        .join(" · ")}
                    </span>
                  </li>
                ))}
              </ul>
            </dd>
          </div>
        )}
        {texto("ordenes")}
        <Dato etiqueta="Incapacidad">
          {d.incapacidad_dias ? `${d.incapacidad_dias} días` : d.incapacidad_dias === 0 ? "No se da" : null}
        </Dato>
      </Seccion>

      <Seccion titulo="Cómo termina la atención">
        {texto("destino")}
        {texto("remitido_a")}
      </Seccion>

      {atencion.firma && (
        <p className="vista-atencion__firma">
          Firmada por <strong>{atencion.firma.nombre}</strong>
          {atencion.firma.registro && <> · Registro {atencion.firma.registro}</>}
          {atencion.fin && (
            <>
              {" "}
              · {diaCorto(diaIso(atencion.fin))}, {hora(atencion.fin)}
            </>
          )}
        </p>
      )}

      {atencion.notas.length > 0 && (
        <section className="vista-atencion__notas" aria-label="Notas aclaratorias">
          <h3>Notas aclaratorias</h3>
          {atencion.notas.map((nota, i) => (
            <div key={i} className="vista-atencion__nota">
              <p>{nota.texto}</p>
              <span className="vista-atencion__detalle">
                {nota.firma_nombre} · {diaCorto(diaIso(nota.fecha))}, {hora(nota.fecha)}
              </span>
            </div>
          ))}
        </section>
      )}
    </div>
  );
}

/** "Control · Hipertensión esencial (primaria)": la línea que resume una atención en una lista. */
export function resumenDeAtencion(atencion: Atencion, f: Formulario | undefined) {
  const principal = atencion.diagnosticos.find((dx) => dx.principal);
  const tipo = f ? legible("tipo_consulta", atencion.datos.tipo_consulta ?? null, f) : null;
  return [tipo, principal?.nombre].filter(Boolean).join(" · ") || "Consulta de medicina general";
}
