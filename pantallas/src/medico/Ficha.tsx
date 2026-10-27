import "./Ficha.css";

import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router";

import { ErrorDeApi } from "../api/cliente";
import {
  direccionDelArchivo,
  etiquetasDeDocumentos,
  fichaDelPaciente,
  type Documento,
} from "../api/documentos";
import { ESTADOS_DE_CITA, ESTADOS_DE_LECTURA } from "../comunes/estados";
import { cuandoCorto, diaCorto, diaIso, hora } from "../comunes/fechas";
import {
  CalendarBlankIcon,
  CalendarPlusIcon,
  CaretRightIcon,
  EyeIcon,
  FileTextIcon,
  PhoneIcon,
} from "../comunes/iconos";
import { Estado } from "../comunes/piezas/Estado";
import { Nota } from "../comunes/piezas/Nota";
import { Asistente } from "./Asistente";

function edad(nacimiento: string, hoy = new Date()) {
  const [anio, mes, dia] = nacimiento.split("-").map(Number);
  let anios = hoy.getFullYear() - anio;
  if (hoy.getMonth() + 1 < mes || (hoy.getMonth() + 1 === mes && hoy.getDate() < dia)) anios -= 1;
  return anios;
}

/** "41652318" como "41 652 318": en grupos de tres desde la derecha, más fácil de leer. */
function enGrupos(numero: string) {
  return /^\d+$/.test(numero) ? numero.replace(/\B(?=(\d{3})+(?!\d))/g, " ") : numero;
}

function iniciales(nombres: string, apellidos: string) {
  return `${nombres.trim().charAt(0)}${apellidos.trim().charAt(0)}`.toUpperCase();
}

function detalle(documento: Documento) {
  const partes = [diaCorto(documento.fecha_documento)];
  if (documento.formato !== "pdf") partes.push("foto");
  else if (documento.paginas) partes.push(`${documento.paginas} pág.`);
  return partes.join(" · ");
}

/** M-06, como en el lienzo: datos, citas, documentos y el asistente al lado (HU-025, HU-034). */
export function Ficha() {
  const { paciente = "" } = useParams();
  const ficha = useQuery({
    queryKey: ["ficha", paciente],
    queryFn: () => fichaDelPaciente(paciente),
  });

  if (ficha.isError) {
    const noExiste = ficha.error instanceof ErrorDeApi && ficha.error.estado === 404;
    return (
      <main className="ficha">
        <Nota tono="rojo">
          {noExiste ? "Ese paciente no existe." : "No se pudo cargar la ficha. Recargue la página."}
        </Nota>
      </main>
    );
  }
  if (!ficha.data) return <main className="ficha" aria-busy="true" />;

  const { paciente: datos, citas, documentos, ia_autorizada } = ficha.data;
  const nombre = `${datos.nombres} ${datos.apellidos}`;
  const etiquetas = etiquetasDeDocumentos(documentos);
  const porEtiqueta = [...documentos].sort((a, b) => (a.id < b.id ? -1 : 1));
  const ahora = Date.now();
  const proximas = citas.filter((c) => c.estado === "confirmada" && Date.parse(c.fin) > ahora);
  const anteriores = citas.filter((c) => !proximas.includes(c)).reverse().slice(0, 5);

  return (
    <main className="ficha">
      <nav aria-label="Ruta" className="ficha__ruta">
        <Link to="/medico/pacientes">Pacientes</Link>
        <CaretRightIcon aria-hidden="true" />
        <span>{nombre}</span>
      </nav>

      <header className="ficha__encabezado">
        <span className="ficha__avatar" aria-hidden="true">
          {iniciales(datos.nombres, datos.apellidos)}
        </span>
        <div className="ficha__identidad">
          <h1>{nombre}</h1>
          <div className="ficha__datos">
            <span>{edad(datos.fecha_nacimiento)} años</span>
            <span className="ficha__dato">
              {datos.tipo_documento} {enGrupos(datos.numero_documento)}
            </span>
            <span className="ficha__telefono">
              <PhoneIcon aria-hidden="true" />
              <span className="ficha__dato">{datos.telefono}</span>
            </span>
            {datos.activo ? (
              <Estado tono="verde">Cuenta activa</Estado>
            ) : (
              <Estado tono="gris">Cuenta sin activar</Estado>
            )}
          </div>
        </div>
        <div className="ficha__acciones">
          <Link
            to={`/medico/citas/nueva?paciente=${datos.id}&nombre=${encodeURIComponent(nombre)}`}
            className="ficha__agendar"
          >
            <CalendarPlusIcon aria-hidden="true" />
            Agendar cita
          </Link>
        </div>
      </header>

      <div className="ficha__columnas">
        <div className="ficha__izquierda">
          <section className="ficha__tarjeta" aria-labelledby="ficha-citas">
            <h2 id="ficha-citas">
              <CalendarBlankIcon aria-hidden="true" />
              Citas
            </h2>
            {!citas.length && <p className="ficha__vacio">Sin citas registradas.</p>}
            {[...proximas, ...anteriores].map((cita) => {
              const esFutura = proximas.includes(cita);
              const dia =
                esFutura || diaIso(cita.inicio) === diaIso(new Date())
                  ? cuandoCorto(cita.inicio)
                  : diaCorto(diaIso(cita.inicio));
              return (
                <div key={cita.id} className="ficha__fila">
                  <div className="ficha__texto">
                    <span className="ficha__titulo">
                      {dia} · <span className="ficha__dato">{hora(cita.inicio)}</span>
                    </span>
                    <span className="ficha__detalle">
                      {cita.tipo} · {cita.duracion_minutos} min
                    </span>
                  </div>
                  <Estado tono={ESTADOS_DE_CITA[cita.estado].tono}>
                    {ESTADOS_DE_CITA[cita.estado].nombre}
                  </Estado>
                </div>
              );
            })}
          </section>

          <section className="ficha__tarjeta" aria-labelledby="ficha-documentos">
            <h2 id="ficha-documentos">
              <FileTextIcon aria-hidden="true" />
              Documentos que subió
            </h2>
            {!documentos.length && (
              <p className="ficha__vacio">El paciente todavía no ha subido documentos.</p>
            )}
            {porEtiqueta.map((documento) => {
              const estado = ESTADOS_DE_LECTURA[documento.estado_lectura];
              return (
                <div key={documento.id} className="ficha__fila ficha__fila--documento">
                  <span className="ficha__etiqueta">{etiquetas.get(documento.id)}</span>
                  <div className="ficha__texto">
                    <span className="ficha__titulo">{documento.nombre}</span>
                    <span className="ficha__detalle">{detalle(documento)}</span>
                  </div>
                  <Estado tono={estado.tono}>{estado.nombre}</Estado>
                  <a
                    className="ficha__ver"
                    href={direccionDelArchivo(documento.id)}
                    target="_blank"
                    rel="noopener"
                    aria-label={`Ver ${documento.nombre}`}
                  >
                    <EyeIcon aria-hidden="true" />
                  </a>
                </div>
              );
            })}
          </section>
        </div>

        <Asistente paciente={datos.id} iaAutorizada={ia_autorizada} etiquetas={etiquetas} />
      </div>
    </main>
  );
}
