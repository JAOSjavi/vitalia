import "./Pacientes.css";

import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { Link } from "react-router";

import { buscarPacientes } from "../api/citas";
import { CalendarPlusIcon, MagnifyingGlassIcon } from "../comunes/iconos";
import { Boton } from "../comunes/piezas/Boton";
import { Entrada } from "../comunes/piezas/Campo";
import { Nota } from "../comunes/piezas/Nota";
import { Tarjeta } from "../comunes/piezas/Tarjeta";

/** Lo que se escribe se busca un momento después de dejar de escribir. */
function useDemorado(valor: string, milisegundos = 300) {
  const [demorado, setDemorado] = useState(valor);
  useEffect(() => {
    const espera = setTimeout(() => setDemorado(valor), milisegundos);
    return () => clearTimeout(espera);
  }, [valor, milisegundos]);
  return demorado;
}

/** M-04. Lista alfabética por páginas y búsqueda por nombre o documento (HU-023). */
export function Pacientes() {
  const [texto, setTexto] = useState("");
  const [pagina, setPagina] = useState(1);
  const buscado = useDemorado(texto);
  const resultado = useQuery({
    queryKey: ["pacientes", buscado, pagina],
    queryFn: () => buscarPacientes(buscado, pagina),
    placeholderData: keepPreviousData,
  });
  const datos = resultado.data;
  const paginas = datos ? Math.max(1, Math.ceil(datos.total / datos.tamano)) : 1;

  return (
    <main className="zona-medico__contenido">
      <h1 className="pacientes__titulo">Pacientes</h1>
      <Entrada
        type="search"
        aria-label="Buscar paciente por nombre o documento"
        placeholder="Buscar por nombre o documento"
        icono={<MagnifyingGlassIcon />}
        value={texto}
        onChange={(evento) => {
          setTexto(evento.target.value);
          setPagina(1);
        }}
      />

      {datos && !datos.pacientes.length && (
        <Nota>{buscado ? "Ningún paciente coincide con la búsqueda." : "Todavía no hay pacientes."}</Nota>
      )}

      {datos && datos.pacientes.length > 0 && (
        <Tarjeta nombre="Lista de pacientes">
          <div className="pacientes__cabecera texto-suave">
            {datos.total} {datos.total === 1 ? "paciente" : "pacientes"}
          </div>
          {datos.pacientes.map((paciente) => {
            const nombre = `${paciente.nombres} ${paciente.apellidos}`;
            return (
              <div key={paciente.id} className="pacientes__fila">
                <div className="pacientes__datos">
                  <Link to={`/medico/pacientes/${paciente.id}`} className="pacientes__nombre">
                    {nombre}
                  </Link>
                  <span className="texto-suave">
                    <span className="pacientes__dato">
                      {paciente.tipo_documento} {paciente.numero_documento}
                    </span>{" "}
                    · <span className="pacientes__dato">{paciente.telefono}</span>
                  </span>
                </div>
                <Link
                  to={`/medico/citas/nueva?paciente=${paciente.id}&nombre=${encodeURIComponent(nombre)}`}
                  className="boton boton--neutro pacientes__agendar"
                >
                  <CalendarPlusIcon />
                  Agendar cita
                </Link>
              </div>
            );
          })}
        </Tarjeta>
      )}

      {paginas > 1 && (
        <div className="pacientes__paginas">
          <Boton clase="neutro" disabled={pagina === 1} onClick={() => setPagina(pagina - 1)}>
            Anteriores
          </Boton>
          <span className="texto-suave">
            Página {pagina} de {paginas}
          </span>
          <Boton
            clase="neutro"
            disabled={pagina === paginas}
            onClick={() => setPagina(pagina + 1)}
          >
            Siguientes
          </Boton>
        </div>
      )}
    </main>
  );
}
