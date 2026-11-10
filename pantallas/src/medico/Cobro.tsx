import "./Cobro.css";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { Link } from "react-router";

import { ErrorDeApi } from "../api/cliente";
import {
  direccionDelPdf,
  facturar,
  MEDIOS_DE_PAGO,
  verCobros,
  type Ambiente,
  type Cobro as CobroDeCita,
  type Factura,
  type MedioDePago,
} from "../api/facturas";
import { conMayuscula, fechaCorta, hora } from "../comunes/fechas";
import { CreditCardIcon, FileTextIcon } from "../comunes/iconos";
import { Boton } from "../comunes/piezas/Boton";
import { Campo, Entrada } from "../comunes/piezas/Campo";
import { Estado } from "../comunes/piezas/Estado";
import { Hoja } from "../comunes/piezas/Hoja";
import { Nota } from "../comunes/piezas/Nota";
import { Tarjeta } from "../comunes/piezas/Tarjeta";

const pesos = new Intl.NumberFormat("es-CO", {
  style: "currency",
  currency: "COP",
  maximumFractionDigits: 0,
});

export function enPesos(valor: number) {
  return pesos.format(valor);
}

const AMBIENTES: Record<
  Ambiente,
  { texto: string; tono: "ambar" | "gris" | "verde" }
> = {
  pruebas: { texto: "Factus · ambiente de pruebas de la DIAN", tono: "ambar" },
  produccion: { texto: "Factus · producción", tono: "verde" },
  de_mentira: {
    texto: "Sin Factus conectado: facturas de mentira, sin validez",
    tono: "gris",
  },
};

/** M-08. Cobrar una cita atendida con factura electrónica (D-35, reemplaza HU-026). */
export function Cobro() {
  const lista = useQuery({ queryKey: ["cobros"], queryFn: verCobros });
  const [cobrando, setCobrando] = useState<CobroDeCita | null>(null);
  const datos = lista.data;
  const sinFacturar = datos?.cobros.filter((c) => !c.factura).length ?? 0;

  return (
    <main className="zona-medico__contenido zona-medico__contenido--angosto">
      <div className="cobro__encabezado">
        <h1 className="cobro__titulo">Cobro</h1>
        {datos && (
          <Estado tono={AMBIENTES[datos.ambiente].tono}>
            {AMBIENTES[datos.ambiente].texto}
          </Estado>
        )}
      </div>
      <p className="texto-suave cobro__ayuda">
        Las citas atendidas de los últimos 30 días. Al cobrar, Vitalia emite la
        factura electrónica con Factus y la DIAN la valida en unos segundos.
      </p>

      {lista.isError && (
        <Nota tono="rojo">
          No se pudieron cargar los cobros. Intente de nuevo.
        </Nota>
      )}

      {datos && !datos.cobros.length && (
        <Nota>
          Todavía no hay citas atendidas. Marque una cita como atendida en{" "}
          <Link to="/medico/hoy">Hoy</Link> para poder cobrarla.
        </Nota>
      )}

      {datos && datos.cobros.length > 0 && (
        <Tarjeta nombre="Citas atendidas">
          <div className="cobro__cabecera texto-suave">
            {sinFacturar === 0
              ? "Todas las citas atendidas están facturadas"
              : `${sinFacturar} ${sinFacturar === 1 ? "cita por cobrar" : "citas por cobrar"}`}
          </div>
          {datos.cobros.map((cobro) => (
            <Fila
              key={cobro.cita.id}
              cobro={cobro}
              alCobrar={() => setCobrando(cobro)}
            />
          ))}
        </Tarjeta>
      )}

      {cobrando && (
        <HojaDeCobro cobro={cobrando} alCerrar={() => setCobrando(null)} />
      )}
    </main>
  );
}

function Fila({
  cobro,
  alCobrar,
}: {
  cobro: CobroDeCita;
  alCobrar: () => void;
}) {
  const { cita, factura } = cobro;
  return (
    <div className="cobro__fila">
      <div className="cobro__datos">
        <Link
          to={`/medico/pacientes/${cita.paciente_id}`}
          className="cobro__paciente"
        >
          {cita.paciente}
        </Link>
        <span className="texto-suave">
          {cita.tipo} · {conMayuscula(fechaCorta(cita.inicio))},{" "}
          {hora(cita.inicio)}
        </span>
      </div>
      {factura ? (
        <Facturada citaId={cita.id} factura={factura} />
      ) : (
        <Boton onClick={alCobrar} className="cobro__boton">
          <CreditCardIcon aria-hidden="true" />
          Cobrar
        </Boton>
      )}
    </div>
  );
}

function Facturada({ citaId, factura }: { citaId: string; factura: Factura }) {
  return (
    <div className="cobro__factura">
      <div className="cobro__resumen">
        <Estado tono="verde">Facturada</Estado>
        <span className="cobro__numero">{factura.numero}</span>
        <span className="cobro__valor">{enPesos(factura.valor)}</span>
      </div>
      <div className="cobro__enlaces">
        <a href={direccionDelPdf(citaId)} target="_blank" rel="noreferrer">
          <FileTextIcon aria-hidden="true" />
          Ver PDF
        </a>
        {factura.enlace_qr && (
          <a href={factura.enlace_qr} target="_blank" rel="noreferrer">
            Consultar en la DIAN
          </a>
        )}
      </div>
    </div>
  );
}

function HojaDeCobro({
  cobro,
  alCerrar,
}: {
  cobro: CobroDeCita;
  alCerrar: () => void;
}) {
  const cliente = useQueryClient();
  const [valor, setValor] = useState("");
  const [medio, setMedio] = useState<MedioDePago | "">("");
  const emitir = useMutation({
    mutationFn: () =>
      facturar(cobro.cita.id, Number(valor), medio as MedioDePago),
    onSuccess: async () => {
      await cliente.invalidateQueries({ queryKey: ["cobros"] });
      alCerrar();
    },
  });
  const error = emitir.error instanceof ErrorDeApi ? emitir.error : null;
  const campos = error?.campos ?? {};
  const motivos =
    error?.codigo === "factura_rechazada"
      ? ((error.detalle as { motivos?: string[] } | undefined)?.motivos ?? [])
      : [];

  function enviarCobro(evento: FormEvent) {
    evento.preventDefault();
    emitir.mutate();
  }

  return (
    <Hoja
      titulo="Cobrar la consulta"
      icono={<CreditCardIcon />}
      alCerrar={alCerrar}
    >
      <form className="cobro__formulario" onSubmit={enviarCobro} noValidate>
        <div className="cobro__quien">
          <span className="cobro__paciente">{cobro.cita.paciente}</span>
          <span className="texto-suave">
            Consulta médica: {cobro.cita.tipo} ·{" "}
            {conMayuscula(fechaCorta(cobro.cita.inicio))}
          </span>
        </div>
        <Campo
          id="cobro-valor"
          etiqueta="Valor de la consulta"
          ayuda="En pesos. La consulta médica no lleva IVA."
          error={campos.valor}
        >
          <Entrada
            id="cobro-valor"
            inputMode="numeric"
            autoComplete="off"
            placeholder="80000"
            value={valor}
            invalido={Boolean(campos.valor)}
            onChange={(e) => setValor(e.target.value.replace(/\D/g, ""))}
          />
        </Campo>
        {valor && (
          <p className="cobro__total">Total: {enPesos(Number(valor))}</p>
        )}
        <Campo id="cobro-medio" etiqueta="Cómo pagó" error={campos.medio_pago}>
          <select
            id="cobro-medio"
            className="selector"
            value={medio}
            onChange={(e) => setMedio(e.target.value as MedioDePago)}
          >
            <option value="">Elija una opción</option>
            {Object.entries(MEDIOS_DE_PAGO).map(([codigo, nombre]) => (
              <option key={codigo} value={codigo}>
                {nombre}
              </option>
            ))}
          </select>
        </Campo>

        {error && !Object.keys(campos).length && (
          <Nota tono="rojo">
            {error.message}
            {motivos.length > 0 && (
              <ul className="cobro__motivos">
                {motivos.map((m) => (
                  <li key={m}>{m}</li>
                ))}
              </ul>
            )}
          </Nota>
        )}

        <div className="cobro__acciones">
          <Boton clase="neutro" onClick={alCerrar} disabled={emitir.isPending}>
            Cancelar
          </Boton>
          <Boton type="submit" disabled={emitir.isPending}>
            {emitir.isPending ? "Emitiendo con Factus…" : "Emitir factura"}
          </Boton>
        </div>
      </form>
    </Hoja>
  );
}
