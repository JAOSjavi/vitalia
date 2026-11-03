import "./Atencion.css";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useId, useRef, useState, type ReactNode } from "react";
import { Link, useParams } from "react-router";

import { ErrorDeApi } from "../api/cliente";
import { etiquetasDeDocumentos, fichaDelPaciente } from "../api/documentos";
import {
  agregarNota,
  buscarCie10,
  cerrarAtencion,
  guardarBorrador,
  guardarIdentificacion,
  verAtencion,
  type AtencionParaEscribir,
  type CampoDelFormulario,
  type Diagnostico,
  type Faltantes,
  type Formulario,
  type Medicamento,
  type Valor,
} from "../api/historia";
import { hora } from "../comunes/fechas";
import { CaretRightIcon, LockKeyIcon, PlusIcon, TrashIcon } from "../comunes/iconos";
import { Boton } from "../comunes/piezas/Boton";
import { EntradaDeContrasena } from "../comunes/piezas/Campo";
import { Estado } from "../comunes/piezas/Estado";
import { Hoja } from "../comunes/piezas/Hoja";
import { Nota } from "../comunes/piezas/Nota";
import { useFormulario, VistaDeAtencion } from "../comunes/VistaDeAtencion";
import { Asistente } from "./Asistente";
import { edad, enGrupos, iniciales } from "./Ficha";

const SECCIONES = [
  "Consulta",
  "Motivo",
  "Antecedentes",
  "Sistemas",
  "Examen",
  "Diagnóstico",
  "Plan",
  "Cierre",
] as const;

/** M-15, como en el lienzo: el formulario en el centro y el asistente al lado (HU-042 a HU-044). */
export function Atencion() {
  const { atencion: id = "" } = useParams();
  const consulta = useQuery({ queryKey: ["atencion", id], queryFn: () => verAtencion(id) });
  const formulario = useFormulario();
  const paciente = consulta.data?.atencion.paciente_id;
  const ficha = useQuery({
    queryKey: ["ficha", paciente],
    queryFn: () => fichaDelPaciente(paciente!),
    enabled: Boolean(paciente),
  });
  const [lado, setLado] = useState<"formulario" | "asistente">("formulario");

  if (consulta.isError || ficha.isError) {
    return (
      <main className="atencion">
        <Nota tono="rojo">No se pudo cargar la atención. Recargue la página.</Nota>
      </main>
    );
  }
  if (!consulta.data || !ficha.data || !formulario.data) {
    return <main className="atencion" aria-busy="true" />;
  }

  const { atencion } = consulta.data;
  const datos = ficha.data.paciente;
  const nombre = `${datos.nombres} ${datos.apellidos}`;
  const abierta = atencion.estado === "abierta";

  return (
    <main className="atencion">
      <nav aria-label="Ruta" className="atencion__ruta">
        <Link to="/medico/pacientes">Pacientes</Link>
        <CaretRightIcon aria-hidden="true" />
        <Link to={`/medico/pacientes/${datos.id}`}>{nombre}</Link>
        <CaretRightIcon aria-hidden="true" />
        <span>Atención</span>
      </nav>

      <Encabezado
        nombre={nombre}
        iniciales={iniciales(datos.nombres, datos.apellidos)}
        detalle={
          <>
            <span>{edad(datos.fecha_nacimiento)} años</span>
            <span className="atencion__dato">
              {datos.tipo_documento} {enGrupos(datos.numero_documento)}
            </span>
            <span>Atención iniciada a las {hora(atencion.inicio)}</span>
          </>
        }
        consulta={consulta.data}
      />

      <div className="atencion__pestanas" role="tablist" aria-label="Vista">
        {(["formulario", "asistente"] as const).map((vista) => (
          <button
            key={vista}
            type="button"
            role="tab"
            aria-selected={lado === vista}
            className="atencion__pestana"
            onClick={() => setLado(vista)}
          >
            {vista === "formulario" ? (abierta ? "Historia clínica" : "Atención") : "Asistente"}
          </button>
        ))}
      </div>

      <div className={`atencion__columnas atencion__columnas--${lado}`}>
        <div className="atencion__centro">
          {abierta ? (
            <Editor key={atencion.id} consulta={consulta.data} f={formulario.data} />
          ) : (
            <Cerrada consulta={consulta.data} />
          )}
        </div>
        <div className="atencion__lado">
          <Asistente
            paciente={datos.id}
            iaAutorizada={ficha.data.ia_autorizada}
            etiquetas={etiquetasDeDocumentos(ficha.data.documentos)}
          />
        </div>
      </div>
    </main>
  );
}

function Encabezado({
  nombre,
  iniciales,
  detalle,
  consulta,
}: {
  nombre: string;
  iniciales: string;
  detalle: ReactNode;
  consulta: AtencionParaEscribir;
}) {
  const { atencion } = consulta;
  const [cerrando, setCerrando] = useState(false);
  return (
    <header className="atencion__encabezado">
      <span className="atencion__avatar" aria-hidden="true">
        {iniciales}
      </span>
      <div className="atencion__identidad">
        <h1>{nombre}</h1>
        <div className="atencion__datos">
          {detalle}
          {atencion.estado === "abierta" ? (
            <Estado tono="verde">Borrador guardado {hora(atencion.guardada_en)}</Estado>
          ) : (
            <Estado tono="gris">Cerrada {atencion.fin ? hora(atencion.fin) : ""}</Estado>
          )}
        </div>
      </div>
      {atencion.estado === "abierta" && (
        <>
          <Boton className="atencion__cerrar" onClick={() => setCerrando(true)}>
            <LockKeyIcon aria-hidden="true" />
            Cerrar y firmar
          </Boton>
          {cerrando && <CerrarYFirmar consulta={consulta} alCerrar={() => setCerrando(false)} />}
        </>
      )}
    </header>
  );
}

// --- Editor del borrador -------------------------------------------------------------------

type EstadoDelEditor = {
  datos: Record<string, Valor>;
  errores: Record<string, string>;
};

function comoTexto(valor: Valor) {
  if (valor === null || valor === undefined) return "";
  return typeof valor === "number" ? String(valor).replace(".", ",") : String(valor);
}

function Editor({ consulta, f }: { consulta: AtencionParaEscribir; f: Formulario }) {
  const { atencion } = consulta;
  const cliente = useQueryClient();
  const [estado, setEstado] = useState<EstadoDelEditor>({ datos: { ...atencion.datos }, errores: {} });
  const guardados = useRef<Record<string, Valor>>({ ...atencion.datos });
  const [diagnosticos, setDiagnosticos] = useState<Diagnostico[]>(atencion.diagnosticos);
  const [medicamentos, setMedicamentos] = useState<Medicamento[]>(atencion.medicamentos);
  const [identificando, setIdentificando] = useState(false);

  const guardar = useMutation({
    mutationFn: (cambios: Parameters<typeof guardarBorrador>[1]) =>
      guardarBorrador(atencion.id, cambios),
    onSuccess: (respuesta, cambios) => {
      Object.assign(guardados.current, cambios.datos ?? {});
      cliente.setQueryData<AtencionParaEscribir>(["atencion", atencion.id], (anterior) =>
        anterior
          ? {
              ...anterior,
              atencion: {
                ...anterior.atencion,
                guardada_en: respuesta.guardada_en,
                datos: { ...anterior.atencion.datos, ...(cambios.datos ?? {}) },
              },
            }
          : anterior,
      );
      setEstado((e) => {
        const errores = { ...e.errores };
        for (const campo of Object.keys(cambios.datos ?? {})) delete errores[campo];
        if (cambios.diagnosticos) delete errores.diagnosticos;
        if (cambios.medicamentos) delete errores.medicamentos;
        return { ...e, errores };
      });
    },
    onError: (error) => {
      const campos = error instanceof ErrorDeApi ? error.campos : {};
      setEstado((e) => ({
        ...e,
        errores: {
          ...e.errores,
          ...(Object.keys(campos).length
            ? Object.fromEntries(
                Object.entries(campos).map(([k, v]) => [k.split(".")[0], v]),
              )
            : { general: "No se pudo guardar. Revise la conexión e intente de nuevo." }),
        },
      }));
    },
  });

  function cambiar(campo: string, valor: Valor) {
    setEstado((e) => ({ ...e, datos: { ...e.datos, [campo]: valor } }));
  }

  /** Al salir de un campo se guarda, si cambió (HU-042, CA-5). */
  function soltar(campo: string, valor: Valor = estado.datos[campo] ?? null) {
    const normal = valor === "" ? null : valor;
    if (comoTexto(normal) === comoTexto(guardados.current[campo] ?? null)) return;
    guardar.mutate({ datos: { [campo]: normal } });
  }

  function elegir(campo: string, valor: Valor) {
    cambiar(campo, valor);
    soltar(campo, valor);
  }

  function guardarDiagnosticos(lista: Diagnostico[]) {
    setDiagnosticos(lista);
    guardar.mutate({
      diagnosticos: lista.map(({ codigo, tipo, principal }) => ({ codigo, tipo, principal })),
    });
  }

  function guardarMedicamentos(lista: Medicamento[]) {
    setMedicamentos(lista);
    guardar.mutate({ medicamentos: lista });
  }

  // Al cerrar la pestaña se guarda lo que estuviera escribiendo.
  useEffect(() => {
    const antesDeSalir = () => {
      const activo = document.activeElement as HTMLElement | null;
      activo?.blur();
    };
    window.addEventListener("beforeunload", antesDeSalir);
    return () => window.removeEventListener("beforeunload", antesDeSalir);
  }, []);

  const p = {
    f,
    datos: estado.datos,
    errores: estado.errores,
    cambiar,
    soltar,
    elegir,
  };
  const pendientes = consulta.faltantes.identificacion;

  return (
    <>
      {pendientes.length > 0 && (
        <div className="atencion__pendientes">
          <Nota>
            <span>
              A la historia clínica le faltan datos de identificación:{" "}
              <strong>{pendientes.join(", ").toLowerCase()}</strong>. Sin ellos no se puede cerrar la
              atención.
            </span>
          </Nota>
          <Boton clase="borde" onClick={() => setIdentificando(true)}>
            Completar ahora
          </Boton>
        </div>
      )}
      {pendientes.length === 0 && (
        <button
          type="button"
          className="atencion__enlace-identificacion"
          onClick={() => setIdentificando(true)}
        >
          Ver o corregir los datos de identificación
        </button>
      )}
      {identificando && (
        <Identificacion consulta={consulta} f={f} alCerrar={() => setIdentificando(false)} />
      )}
      {estado.errores.general && <Nota tono="rojo">{estado.errores.general}</Nota>}

      <form className="atencion__formulario" onSubmit={(e) => e.preventDefault()} noValidate>
        <nav className="atencion__indice" aria-label="Secciones de la historia clínica">
          {SECCIONES.map((nombre, i) => (
            <a key={nombre} href={`#seccion-${i + 1}`} className="atencion__salto">
              {i + 1} · {nombre}
            </a>
          ))}
        </nav>

        <Tarjeta numero={1} titulo="Datos de la consulta">
          <div className="atencion__rejilla">
            <Opcion {...p} campo="tipo_consulta" />
            <Opcion {...p} campo="finalidad" />
            <Opcion {...p} campo="causa" />
          </div>
          <div className="atencion__rejilla">
            <Texto {...p} campo="acompanante_nombre" ayuda="si vino con alguien" />
            <Texto {...p} campo="acompanante_parentesco" />
            <Texto {...p} campo="acompanante_telefono" modo="tel" />
          </div>
        </Tarjeta>

        <Tarjeta numero={2} titulo="Motivo de consulta y enfermedad actual">
          <Area {...p} campo="motivo" filas={2} />
          <Area {...p} campo="enfermedad_actual" filas={4} />
        </Tarjeta>

        <Tarjeta numero={3} titulo="Antecedentes">
          {atencion.datos.antecedentes_personales && (
            <p className="atencion__ayuda">
              Traídos de la atención anterior. Confírmelos o cámbielos.
            </p>
          )}
          {(["antecedentes_personales", "antecedentes_familiares", "alergias", "factores_riesgo"] as const).map(
            (campo) => (
              <Area key={campo} {...p} campo={campo} filas={2} atajo="No refiere" />
            ),
          )}
        </Tarjeta>

        <Tarjeta numero={4} titulo="Revisión por sistemas">
          <Area {...p} campo="revision_sistemas" filas={3} atajo="Sin hallazgos" />
          <div className="atencion__rejilla">
            <SiNo {...p} campo="sintomatico_respiratorio" ayuda="tos de más de 15 días" />
            <SiNo {...p} campo="sintomatico_piel" ayuda="manchas con pérdida de sensibilidad" />
          </div>
        </Tarjeta>

        <Tarjeta numero={5} titulo="Signos vitales y examen físico">
          <div className="atencion__signos">
            <Numero {...p} campo="tension_sistolica" etiqueta="Tensión sistólica" />
            <Numero {...p} campo="tension_diastolica" etiqueta="Tensión diastólica" />
            <Numero {...p} campo="frecuencia_cardiaca" etiqueta="Frec. cardiaca" />
            <Numero {...p} campo="frecuencia_respiratoria" etiqueta="Frec. respiratoria" />
            <Numero {...p} campo="temperatura" />
            <Numero {...p} campo="saturacion" etiqueta="Saturación" />
            <Numero {...p} campo="peso" />
            <Numero {...p} campo="talla" />
            <Imc peso={estado.datos.peso} talla={estado.datos.talla} />
          </div>
          <Area {...p} campo="examen_fisico" filas={4} />
        </Tarjeta>

        <Tarjeta numero={6} titulo="Diagnóstico">
          <Diagnosticos
            lista={diagnosticos}
            f={f}
            error={estado.errores.diagnosticos}
            alCambiar={guardarDiagnosticos}
          />
          <Area {...p} campo="analisis" filas={3} ayuda="concepto o impresión del médico" />
        </Tarjeta>

        <Tarjeta numero={7} titulo="Plan, fórmula, órdenes e incapacidad">
          <Area {...p} campo="plan" filas={3} />
          <Area {...p} campo="recomendaciones" filas={2} />
          <Formula
            lista={medicamentos}
            f={f}
            error={estado.errores.medicamentos}
            alCambiar={guardarMedicamentos}
          />
          <Area {...p} campo="ordenes" filas={2} />
          <div className="atencion__rejilla">
            <Numero {...p} campo="incapacidad_dias" etiqueta="Incapacidad" ayuda="en días; 0 si no se da" />
          </div>
        </Tarjeta>

        <Tarjeta numero={8} titulo="Cómo termina la atención">
          <Radios {...p} campo="destino" />
          {estado.datos.destino === "remitido" && (
            <Texto {...p} campo="remitido_a" ayuda="prestador o servicio" />
          )}
          <p className="atencion__ayuda">
            Al cerrar, la atención queda con su nombre, su registro, la fecha y la hora, y ya no se
            puede cambiar. Si después hay que corregir algo, se agrega una nota aclaratoria.
          </p>
        </Tarjeta>
      </form>
    </>
  );
}

function Tarjeta({ numero, titulo, children }: { numero: number; titulo: string; children: ReactNode }) {
  return (
    <section id={`seccion-${numero}`} className="atencion__tarjeta" aria-labelledby={`titulo-${numero}`}>
      <h2 id={`titulo-${numero}`}>
        {numero} · {titulo}
      </h2>
      {children}
    </section>
  );
}

type PropiedadesDeCampo = {
  f: Formulario;
  datos: Record<string, Valor>;
  errores: Record<string, string>;
  campo: string;
  etiqueta?: string;
  ayuda?: string;
  cambiar: (campo: string, valor: Valor) => void;
  soltar: (campo: string, valor?: Valor) => void;
  elegir: (campo: string, valor: Valor) => void;
};

function Envoltura({
  id,
  descripcion,
  etiqueta,
  ayuda,
  error,
  children,
}: {
  id: string;
  descripcion: CampoDelFormulario;
  etiqueta?: string;
  ayuda?: string;
  error?: string;
  children: ReactNode;
}) {
  return (
    <div className="atencion__campo">
      <label htmlFor={id} className="atencion__etiqueta">
        {etiqueta ?? descripcion.nombre}
        {ayuda && <span className="atencion__suave"> ({ayuda})</span>}
        {descripcion.obligatorio && <span className="atencion__suave visually-hidden"> obligatorio</span>}
      </label>
      {children}
      {error && (
        <p className="atencion__error" role="alert">
          <span className="atencion__punto" aria-hidden="true" />
          {error}
        </p>
      )}
    </div>
  );
}

function Texto({ f, datos, errores, campo, etiqueta, ayuda, cambiar, soltar, modo }: PropiedadesDeCampo & { modo?: "tel" }) {
  const id = useId();
  const descripcion = f.atencion[campo];
  return (
    <Envoltura id={id} descripcion={descripcion} etiqueta={etiqueta} ayuda={ayuda} error={errores[campo]}>
      <input
        id={id}
        className="atencion__control"
        type={modo ?? "text"}
        maxLength={descripcion.largo}
        value={comoTexto(datos[campo] ?? null)}
        aria-invalid={Boolean(errores[campo]) || undefined}
        onChange={(e) => cambiar(campo, e.target.value)}
        onBlur={() => soltar(campo)}
      />
    </Envoltura>
  );
}

function Area({
  f,
  datos,
  errores,
  campo,
  etiqueta,
  ayuda,
  cambiar,
  soltar,
  elegir,
  filas,
  atajo,
}: PropiedadesDeCampo & { filas: number; atajo?: string }) {
  const id = useId();
  const descripcion = f.atencion[campo];
  return (
    <Envoltura id={id} descripcion={descripcion} etiqueta={etiqueta} ayuda={ayuda} error={errores[campo]}>
      <textarea
        id={id}
        className="atencion__control atencion__control--area"
        rows={filas}
        maxLength={descripcion.largo}
        value={comoTexto(datos[campo] ?? null)}
        aria-invalid={Boolean(errores[campo]) || undefined}
        onChange={(e) => cambiar(campo, e.target.value)}
        onBlur={() => soltar(campo)}
      />
      {atajo && datos[campo] !== atajo && (
        <button type="button" className="atencion__atajo" onClick={() => elegir(campo, atajo)}>
          Marcar "{atajo}"
        </button>
      )}
    </Envoltura>
  );
}

function Numero({ f, datos, errores, campo, etiqueta, ayuda, cambiar, soltar }: PropiedadesDeCampo) {
  const id = useId();
  const descripcion = f.atencion[campo];
  return (
    <Envoltura id={id} descripcion={descripcion} etiqueta={etiqueta} ayuda={ayuda} error={errores[campo]}>
      <div className="atencion__numero">
        <input
          id={id}
          className="atencion__control atencion__control--dato"
          inputMode="decimal"
          value={comoTexto(datos[campo] ?? null)}
          aria-invalid={Boolean(errores[campo]) || undefined}
          onChange={(e) => cambiar(campo, e.target.value)}
          onBlur={() => soltar(campo)}
        />
        {descripcion.unidad && descripcion.unidad !== "días" && (
          <span className="atencion__unidad">{descripcion.unidad}</span>
        )}
      </div>
    </Envoltura>
  );
}

function Opcion({ f, datos, errores, campo, etiqueta, elegir }: PropiedadesDeCampo) {
  const id = useId();
  const descripcion = f.atencion[campo];
  const opciones = f.listas[descripcion.lista ?? ""] ?? {};
  return (
    <Envoltura id={id} descripcion={descripcion} etiqueta={etiqueta} error={errores[campo]}>
      <select
        id={id}
        className="atencion__control"
        value={comoTexto(datos[campo] ?? null)}
        onChange={(e) => elegir(campo, e.target.value || null)}
      >
        <option value="">Elija una opción</option>
        {Object.entries(opciones).map(([codigo, nombre]) => (
          <option key={codigo} value={codigo}>
            {nombre}
          </option>
        ))}
      </select>
    </Envoltura>
  );
}

function Radios({ f, datos, errores, campo, elegir }: PropiedadesDeCampo) {
  const descripcion = f.atencion[campo];
  const opciones = f.listas[descripcion.lista ?? ""] ?? {};
  const nombre = useId();
  return (
    <fieldset className="atencion__radios">
      <legend className="atencion__etiqueta">{descripcion.nombre}</legend>
      {Object.entries(opciones).map(([codigo, texto]) => (
        <label key={codigo} className="atencion__radio">
          <input
            type="radio"
            name={nombre}
            checked={datos[campo] === codigo}
            onChange={() => elegir(campo, codigo)}
          />
          {texto}
        </label>
      ))}
      {errores[campo] && <p className="atencion__error">{errores[campo]}</p>}
    </fieldset>
  );
}

function SiNo({ f, datos, campo, ayuda, elegir }: PropiedadesDeCampo) {
  const descripcion = f.atencion[campo];
  const nombre = useId();
  return (
    <fieldset className="atencion__radios">
      <legend className="atencion__etiqueta">
        {descripcion.nombre}
        {ayuda && <span className="atencion__suave"> ({ayuda})</span>}
      </legend>
      {([true, false] as const).map((valor) => (
        <label key={String(valor)} className="atencion__radio">
          <input
            type="radio"
            name={nombre}
            checked={datos[campo] === valor}
            onChange={() => elegir(campo, valor)}
          />
          {valor ? "Sí" : "No"}
        </label>
      ))}
    </fieldset>
  );
}

function Imc({ peso, talla }: { peso: Valor; talla: Valor }) {
  const kilos = Number(String(peso ?? "").replace(",", "."));
  const metros = Number(String(talla ?? "").replace(",", ".")) / 100;
  const imc = kilos > 0 && metros > 0 ? (kilos / (metros * metros)).toFixed(1).replace(".", ",") : "—";
  return (
    <div className="atencion__campo">
      <span className="atencion__etiqueta">Índice de masa corporal</span>
      <div className="atencion__imc">
        <span className="atencion__dato">{imc}</span>
        <span className="atencion__suave">calculado</span>
      </div>
    </div>
  );
}

// --- Diagnósticos ----------------------------------------------------------------------------

function Diagnosticos({
  lista,
  f,
  error,
  alCambiar,
}: {
  lista: Diagnostico[];
  f: Formulario;
  error?: string;
  alCambiar: (lista: Diagnostico[]) => void;
}) {
  const id = useId();
  const [texto, setTexto] = useState("");
  const [buscado, setBuscado] = useState("");
  useEffect(() => {
    const espera = setTimeout(() => setBuscado(texto.trim()), 250);
    return () => clearTimeout(espera);
  }, [texto]);
  const resultados = useQuery({
    queryKey: ["cie10", buscado],
    queryFn: () => buscarCie10(buscado),
    enabled: buscado.length >= 2,
  });
  const tipos = f.listas.tipo_diagnostico;

  function agregar(codigo: string, nombre: string) {
    if (lista.some((d) => d.codigo === codigo)) return;
    alCambiar([
      ...lista,
      { codigo, nombre, tipo: "impresion_diagnostica", principal: !lista.some((d) => d.principal) },
    ]);
    setTexto("");
  }

  function cambiar(codigo: string, cambio: Partial<Diagnostico>) {
    alCambiar(
      lista.map((d) => {
        if (cambio.principal) return { ...d, principal: d.codigo === codigo };
        return d.codigo === codigo ? { ...d, ...cambio } : d;
      }),
    );
  }

  return (
    <div className="atencion__diagnosticos">
      <div className="atencion__campo">
        <label htmlFor={id} className="atencion__etiqueta">
          Buscar un diagnóstico <span className="atencion__suave">(por nombre o código CIE-10)</span>
        </label>
        <input
          id={id}
          className="atencion__control"
          value={texto}
          autoComplete="off"
          placeholder="Ej.: hipertensión o I10"
          onChange={(e) => setTexto(e.target.value)}
        />
        {buscado.length >= 2 && texto && resultados.data && (
          <ul className="atencion__resultados" aria-label="Diagnósticos encontrados">
            {resultados.data.length === 0 && <li className="atencion__suave">Sin resultados.</li>}
            {resultados.data.map((d) => (
              <li key={d.codigo}>
                <button type="button" onClick={() => agregar(d.codigo, d.nombre)}>
                  <span className="atencion__codigo">{d.codigo}</span>
                  {d.nombre}
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
      {error && <p className="atencion__error">{error}</p>}
      {lista.map((d) => (
        <div key={d.codigo} className="atencion__diagnostico">
          <div className="atencion__diagnostico-nombre">
            <span className="atencion__codigo">{d.codigo}</span>
            <span>{d.nombre}</span>
            <Estado tono={d.principal ? "azul" : "gris"}>{d.principal ? "Principal" : "Relacionado"}</Estado>
          </div>
          <div className="atencion__diagnostico-opciones">
            <select
              aria-label={`Tipo de diagnóstico de ${d.codigo}`}
              className="atencion__control"
              value={d.tipo}
              onChange={(e) => cambiar(d.codigo, { tipo: e.target.value })}
            >
              {Object.entries(tipos).map(([codigo, nombre]) => (
                <option key={codigo} value={codigo}>
                  {nombre}
                </option>
              ))}
            </select>
            {!d.principal && (
              <Boton clase="neutro" onClick={() => cambiar(d.codigo, { principal: true })}>
                Hacer principal
              </Boton>
            )}
            <button
              type="button"
              className="atencion__quitar"
              aria-label={`Quitar ${d.codigo}`}
              onClick={() => alCambiar(lista.filter((x) => x.codigo !== d.codigo))}
            >
              <TrashIcon aria-hidden="true" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

// --- Fórmula ---------------------------------------------------------------------------------

const MEDICAMENTO_VACIO = { nombre: "", dosis: "", via: "oral", frecuencia: "", dias: "", indicaciones: "" };

function Formula({
  lista,
  f,
  error,
  alCambiar,
}: {
  lista: Medicamento[];
  f: Formulario;
  error?: string;
  alCambiar: (lista: Medicamento[]) => void;
}) {
  const [nuevo, setNuevo] = useState(MEDICAMENTO_VACIO);
  const [falta, setFalta] = useState("");
  const vias = f.listas.via;
  const id = useId();

  function agregar() {
    const dias = Number(nuevo.dias);
    if (!nuevo.nombre.trim() || !nuevo.dosis.trim() || !nuevo.frecuencia.trim() || !(dias >= 1)) {
      setFalta("Escriba el medicamento, la dosis, la frecuencia y los días.");
      return;
    }
    setFalta("");
    alCambiar([...lista, { ...nuevo, dias, indicaciones: nuevo.indicaciones.trim() || null }]);
    setNuevo(MEDICAMENTO_VACIO);
  }

  const campo = (clave: keyof typeof MEDICAMENTO_VACIO, etiqueta: string, extra?: object) => (
    <div className="atencion__campo">
      <label htmlFor={`${id}-${clave}`} className="atencion__etiqueta">
        {etiqueta}
      </label>
      <input
        id={`${id}-${clave}`}
        className="atencion__control"
        value={nuevo[clave]}
        onChange={(e) => setNuevo({ ...nuevo, [clave]: e.target.value })}
        {...extra}
      />
    </div>
  );

  return (
    <fieldset className="atencion__formula">
      <legend className="atencion__etiqueta">Fórmula</legend>
      {lista.map((m, i) => (
        <div key={i} className="atencion__medicamento">
          <div>
            <strong>{m.nombre}</strong>
            <span className="atencion__suave">
              {[m.dosis, `vía ${(vias[m.via] ?? m.via).toLowerCase()}`, m.frecuencia, `${m.dias} días`, m.indicaciones]
                .filter(Boolean)
                .join(" · ")}
            </span>
          </div>
          <button
            type="button"
            className="atencion__quitar"
            aria-label={`Quitar ${m.nombre}`}
            onClick={() => alCambiar(lista.filter((_, j) => j !== i))}
          >
            <TrashIcon aria-hidden="true" />
          </button>
        </div>
      ))}
      <div className="atencion__nuevo-medicamento">
        {campo("nombre", "Medicamento y concentración", { placeholder: "Ej.: Losartán 50 mg" })}
        {campo("dosis", "Dosis", { placeholder: "1 tableta" })}
        <div className="atencion__campo">
          <label htmlFor={`${id}-via`} className="atencion__etiqueta">
            Vía
          </label>
          <select
            id={`${id}-via`}
            className="atencion__control"
            value={nuevo.via}
            onChange={(e) => setNuevo({ ...nuevo, via: e.target.value })}
          >
            {Object.entries(vias).map(([codigo, nombre]) => (
              <option key={codigo} value={codigo}>
                {nombre}
              </option>
            ))}
          </select>
        </div>
        {campo("frecuencia", "Frecuencia", { placeholder: "cada 12 horas" })}
        {campo("dias", "Días", { inputMode: "numeric" })}
        {campo("indicaciones", "Indicaciones", { placeholder: "después del desayuno" })}
      </div>
      {(falta || error) && <p className="atencion__error">{falta || error}</p>}
      <Boton clase="borde" onClick={agregar}>
        <PlusIcon aria-hidden="true" />
        Agregar medicamento
      </Boton>
    </fieldset>
  );
}

// --- Identificación del paciente (HU-041) ----------------------------------------------------

function Identificacion({
  consulta,
  f,
  alCerrar,
}: {
  consulta: AtencionParaEscribir;
  f: Formulario;
  alCerrar: () => void;
}) {
  const cliente = useQueryClient();
  const [datos, setDatos] = useState<Record<string, Valor>>({ ...consulta.identificacion });
  const [errores, setErrores] = useState<Record<string, string>>({});
  const id = useId();
  const guardar = useMutation({
    mutationFn: () => guardarIdentificacion(consulta.atencion.paciente_id, datos),
    onSuccess: async () => {
      await cliente.invalidateQueries({ queryKey: ["atencion", consulta.atencion.id] });
      alCerrar();
    },
    onError: (error) => setErrores(error instanceof ErrorDeApi ? error.campos : {}),
  });

  return (
    <Hoja titulo="Datos de identificación" alCerrar={alCerrar} ancha>
      <p className="atencion__ayuda">
        Los pide la Resolución 1995 de 1999. Se llenan una vez y quedan en la historia clínica.
      </p>
      <form
        className="atencion__rejilla"
        onSubmit={(e) => {
          e.preventDefault();
          guardar.mutate();
        }}
      >
        {Object.entries(f.identificacion).map(([campo, descripcion]) => {
          const control = `${id}-${campo}`;
          const valor = comoTexto(datos[campo] ?? null);
          return (
            <div key={campo} className="atencion__campo">
              <label htmlFor={control} className="atencion__etiqueta">
                {descripcion.nombre}
                {campo === "aseguradora" ? (
                  <span className="atencion__suave"> (si no es particular)</span>
                ) : (
                  !descripcion.obligatorio && <span className="atencion__suave"> (opcional)</span>
                )}
              </label>
              {descripcion.lista ? (
                <select
                  id={control}
                  className="atencion__control"
                  value={valor}
                  onChange={(e) => setDatos({ ...datos, [campo]: e.target.value || null })}
                >
                  <option value="">Elija una opción</option>
                  {Object.entries(f.listas[descripcion.lista]).map(([codigo, nombre]) => (
                    <option key={codigo} value={codigo}>
                      {nombre}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  id={control}
                  className="atencion__control"
                  maxLength={descripcion.largo}
                  value={valor}
                  onChange={(e) => setDatos({ ...datos, [campo]: e.target.value })}
                />
              )}
              {errores[campo] && <p className="atencion__error">{errores[campo]}</p>}
            </div>
          );
        })}
        <div className="atencion__acciones-hoja">
          <Boton clase="neutro" onClick={alCerrar}>
            Cancelar
          </Boton>
          <Boton type="submit" disabled={guardar.isPending}>
            Guardar datos
          </Boton>
        </div>
      </form>
    </Hoja>
  );
}

// --- Cerrar y firmar (HU-044) ----------------------------------------------------------------

function CerrarYFirmar({ consulta, alCerrar }: { consulta: AtencionParaEscribir; alCerrar: () => void }) {
  const cliente = useQueryClient();
  const [contrasena, setContrasena] = useState("");
  const [faltan, setFaltan] = useState<Faltantes | null>(null);
  const [error, setError] = useState("");
  const id = useId();
  const cerrar = useMutation({
    mutationFn: async () => {
      // Lo que estaba escribiendo se guarda antes de firmar.
      (document.activeElement as HTMLElement | null)?.blur();
      return cerrarAtencion(consulta.atencion.id, contrasena);
    },
    onSuccess: async () => {
      await cliente.invalidateQueries({ queryKey: ["atencion", consulta.atencion.id] });
      await cliente.invalidateQueries({ queryKey: ["historia", consulta.atencion.paciente_id] });
      await cliente.invalidateQueries({ queryKey: ["agenda-hoy"] });
      alCerrar();
    },
    onError: (e) => {
      if (e instanceof ErrorDeApi && e.codigo === "faltan_datos") {
        setFaltan(e.detalle as Faltantes);
        setError("");
      } else {
        setFaltan(null);
        setError(e instanceof Error ? e.message : "No se pudo cerrar la atención.");
      }
    },
  });

  return (
    <Hoja titulo="Cerrar y firmar la atención" icono={<LockKeyIcon />} alCerrar={alCerrar}>
      <p className="atencion__ayuda">
        Al cerrar, la atención queda firmada con su nombre, su registro, la fecha y la hora, y ya no
        se puede cambiar. Confirme con su contraseña.
      </p>
      {faltan && (
        <Nota tono="rojo">
          <span>Faltan datos para cerrar:</span>
          {faltan.identificacion.length > 0 && (
            <span>
              <strong>Identificación:</strong> {faltan.identificacion.join(", ")}.
            </span>
          )}
          {faltan.atencion.length > 0 && (
            <span>
              <strong>Consulta:</strong> {faltan.atencion.join(", ")}.
            </span>
          )}
        </Nota>
      )}
      {error && <Nota tono="rojo">{error}</Nota>}
      <form
        className="atencion__firma"
        onSubmit={(e) => {
          e.preventDefault();
          cerrar.mutate();
        }}
      >
        <label htmlFor={id} className="atencion__etiqueta">
          Su contraseña
        </label>
        <EntradaDeContrasena
          id={id}
          autoComplete="current-password"
          value={contrasena}
          onChange={(e) => setContrasena(e.target.value)}
          icono={<LockKeyIcon />}
        />
        <div className="atencion__acciones-hoja">
          <Boton clase="neutro" onClick={alCerrar}>
            Seguir escribiendo
          </Boton>
          <Boton type="submit" disabled={!contrasena || cerrar.isPending}>
            Cerrar y firmar
          </Boton>
        </div>
      </form>
    </Hoja>
  );
}

// --- Atención cerrada ------------------------------------------------------------------------

function Cerrada({ consulta }: { consulta: AtencionParaEscribir }) {
  const cliente = useQueryClient();
  const [texto, setTexto] = useState("");
  const id = useId();
  const nota = useMutation({
    mutationFn: () => agregarNota(consulta.atencion.id, texto),
    onSuccess: async () => {
      setTexto("");
      await cliente.invalidateQueries({ queryKey: ["atencion", consulta.atencion.id] });
    },
  });
  return (
    <div className="atencion__cerrada">
      <section className="atencion__tarjeta">
        <VistaDeAtencion atencion={consulta.atencion} />
      </section>
      <form
        className="atencion__tarjeta"
        onSubmit={(e) => {
          e.preventDefault();
          if (texto.trim()) nota.mutate();
        }}
      >
        <h2>Agregar una nota aclaratoria</h2>
        <p className="atencion__ayuda">
          La atención cerrada no se cambia. La nota queda debajo, con su nombre, la fecha y la hora.
        </p>
        <label htmlFor={id} className="visually-hidden">
          Nota aclaratoria
        </label>
        <textarea
          id={id}
          className="atencion__control atencion__control--area"
          rows={3}
          maxLength={4000}
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
        />
        {nota.isError && <Nota tono="rojo">No se pudo guardar la nota. Intente de nuevo.</Nota>}
        <Boton type="submit" clase="borde" disabled={!texto.trim() || nota.isPending}>
          Agregar nota
        </Boton>
      </form>
    </div>
  );
}
