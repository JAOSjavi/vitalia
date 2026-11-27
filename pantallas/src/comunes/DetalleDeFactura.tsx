import "./DetalleDeFactura.css";

import { direccionDelPdf, MEDIOS_DE_PAGO, type Factura } from "../api/facturas";
import { conMayuscula, fechaConAnio, hora } from "./fechas";
import { FileTextIcon } from "./iconos";
import { Estado } from "./piezas/Estado";

const pesos = new Intl.NumberFormat("es-CO", {
  style: "currency",
  currency: "COP",
  maximumFractionDigits: 0,
});

export function enPesos(valor: number) {
  return pesos.format(valor);
}

const AMBIENTE: Record<Factura["ambiente"], { texto: string; tono: "ambar" | "gris" | "verde" }> = {
  pruebas: { texto: "Validada · ambiente de pruebas de la DIAN", tono: "ambar" },
  produccion: { texto: "Validada por la DIAN", tono: "verde" },
  de_mentira: { texto: "Factura de mentira, sin validez", tono: "gris" },
};

type Propiedades = {
  factura: Factura;
  /** El médico ve a quién se le facturó; el paciente no lo necesita. */
  paciente?: string;
  /** Cuándo fue la atención que se cobró. */
  atencion?: string;
};

/** La factura electrónica como la ve quien la consulta: lo que dice el papel y sus enlaces. */
export function DetalleDeFactura({ factura, paciente, atencion }: Propiedades) {
  const ambiente = AMBIENTE[factura.ambiente];
  return (
    <div className="detalle-factura">
      <div className="detalle-factura__cabeza">
        <span className="detalle-factura__etiqueta">Factura electrónica de venta</span>
        <span className="detalle-factura__numero">{factura.numero}</span>
        <Estado tono={ambiente.tono}>{ambiente.texto}</Estado>
      </div>

      <dl className="detalle-factura__datos">
        {paciente && (
          <div>
            <dt>Paciente</dt>
            <dd>{paciente}</dd>
          </div>
        )}
        <div>
          <dt>Concepto</dt>
          <dd>{factura.concepto}</dd>
        </div>
        {atencion && (
          <div>
            <dt>Atención</dt>
            <dd>
              {conMayuscula(fechaConAnio(atencion))}, {hora(atencion)}
            </dd>
          </div>
        )}
        <div>
          <dt>Emitida</dt>
          <dd>
            {conMayuscula(fechaConAnio(factura.emitida_en))}, {hora(factura.emitida_en)}
          </dd>
        </div>
        <div>
          <dt>Medio de pago</dt>
          <dd>{MEDIOS_DE_PAGO[factura.medio_pago]} · de contado</dd>
        </div>
        <div>
          <dt>IVA</dt>
          <dd>Excluido (consulta médica)</dd>
        </div>
      </dl>

      <div className="detalle-factura__total">
        <span>Total pagado</span>
        <strong>{enPesos(factura.valor)}</strong>
      </div>

      <div className="detalle-factura__cufe">
        <span className="detalle-factura__etiqueta">CUFE · código único ante la DIAN</span>
        <code>{factura.cufe}</code>
      </div>

      <div className="detalle-factura__acciones">
        <a
          className="boton boton--principal"
          href={direccionDelPdf(factura.cita_id)}
          target="_blank"
          rel="noreferrer"
        >
          <FileTextIcon aria-hidden="true" />
          Ver PDF
        </a>
        {factura.enlace_qr && (
          <a className="boton boton--borde" href={factura.enlace_qr} target="_blank" rel="noreferrer">
            Consultar en la DIAN
          </a>
        )}
        {factura.enlace_publico && (
          <a
            className="boton boton--neutro"
            href={factura.enlace_publico}
            target="_blank"
            rel="noreferrer"
          >
            Ver en Factus
          </a>
        )}
      </div>
    </div>
  );
}
