import "./MisFacturas.css";

import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router";

import { misFacturas } from "../api/facturas";
import { DetalleDeFactura, enPesos } from "../comunes/DetalleDeFactura";
import { diaCorto, diaIso } from "../comunes/fechas";
import { CaretLeftIcon, CaretRightIcon } from "../comunes/iconos";
import { Nota } from "../comunes/piezas/Nota";

/**
 * Las facturas electrónicas de las consultas que pagó (D-35). En computador la lista y la factura
 * elegida van lado a lado; en celular, una a la vez, como en Historia.
 */
export function MisFacturas() {
  const { cita: elegida } = useParams();
  const facturas = useQuery({ queryKey: ["mis-facturas"], queryFn: misFacturas });
  const lista = facturas.data ?? [];
  const actual = lista.find((f) => f.cita_id === elegida) ?? (elegida ? undefined : lista[0]);

  return (
    <main className={`mis-facturas ${elegida ? "mis-facturas--con-detalle" : ""}`}>
      <header className="zona-paciente__encabezado">
        <h1>Mis facturas</h1>
      </header>
      <p className="mis-facturas__ayuda">
        La factura electrónica de cada consulta que pagó en el consultorio, validada por la DIAN.
        Puede abrir el PDF o consultarla en la página de la DIAN.
      </p>

      {facturas.isError && <Nota tono="rojo">No se pudieron cargar sus facturas.</Nota>}
      {facturas.isSuccess && !lista.length && (
        <Nota>Todavía no tiene facturas. Aparecen aquí cuando el consultorio cobra una consulta.</Nota>
      )}

      {lista.length > 0 && (
        <div className="mis-facturas__columnas">
          <nav className="mis-facturas__lista" aria-label="Facturas">
            {lista.map((factura) => (
              <Link
                key={factura.cita_id}
                to={`/paciente/facturas/${factura.cita_id}`}
                className="mis-facturas__factura"
                aria-current={actual?.cita_id === factura.cita_id ? "page" : undefined}
              >
                <span className="mis-facturas__fecha">
                  {diaCorto(diaIso(factura.emitida_en))} · {factura.numero}
                </span>
                <span className="mis-facturas__concepto">{factura.concepto}</span>
                <span className="mis-facturas__valor">{enPesos(factura.valor)}</span>
                <CaretRightIcon aria-hidden="true" className="mis-facturas__flecha" />
              </Link>
            ))}
          </nav>

          {actual && (
            <article className="mis-facturas__detalle" aria-label="Factura elegida">
              <Link to="/paciente/facturas" className="mis-facturas__volver">
                <CaretLeftIcon aria-hidden="true" />
                Todas las facturas
              </Link>
              <DetalleDeFactura factura={actual} />
            </article>
          )}
        </div>
      )}
    </main>
  );
}
