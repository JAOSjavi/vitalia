import "./Agendar.css";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, type ReactNode } from "react";
import { Link, useNavigate, useParams } from "react-router";

import { ErrorDeApi } from "../api/cliente";
import { crearCita, misCitas, moverCita, tiposDeCita, type TipoDeCita } from "../api/citas";
import { consultorioPublico } from "../api/consultorio";
import { conMayuscula, fechaCorta, fechaLarga, hora } from "../comunes/fechas";
import { ArrowLeftIcon, ArrowRightIcon, StethoscopeIcon } from "../comunes/iconos";
import { Boton } from "../comunes/piezas/Boton";
import { Nota } from "../comunes/piezas/Nota";
import { Pasos } from "../comunes/piezas/Pasos";
import { SelectorDeEspacio } from "../comunes/SelectorDeEspacio";

/** P-05. Agendar en tres pasos: tipo, día y hora, confirmación (HU-012). También mueve (HU-014). */
export function Agendar() {
  const { cita: citaId } = useParams();
  const moviendo = Boolean(citaId);
  const navegar = useNavigate();
  const consultas = useQueryClient();
  const tipos = useQuery({ queryKey: ["tipos-cita"], queryFn: tiposDeCita, enabled: !moviendo });
  const citas = useQuery({ queryKey: ["mis-citas"], queryFn: misCitas, enabled: moviendo });
  const consultorio = useQuery({ queryKey: ["consultorio-publico"], queryFn: consultorioPublico });
  const cita = citas.data?.find((c) => c.id === citaId);

  const [elegido, setElegido] = useState<TipoDeCita | null>(null);
  const [paso, setPaso] = useState<1 | 2 | 3>(moviendo ? 2 : 1);
  const [inicio, setInicio] = useState<string | null>(null);
  const [fallo, setFallo] = useState<ReactNode>(null);
  const [alternativas, setAlternativas] = useState<string[]>([]);
  const [enviando, setEnviando] = useState(false);

  const tipo = moviendo ? cita?.tipo_id : elegido?.id;
  const nombreDelTipo = moviendo ? cita?.tipo : elegido?.nombre;
  const duracion = moviendo ? cita?.duracion_minutos : elegido?.duracion_minutos;
  const titulo = moviendo ? "Mover mi cita" : "Agendar una cita";

  async function confirmar(repetida = false) {
    if (!tipo || !inicio) return;
    setFallo(null);
    setAlternativas([]);
    setEnviando(true);
    try {
      if (moviendo && citaId) await moverCita(citaId, { inicio });
      else await crearCita({ tipo_cita: tipo, inicio, confirmar_repetida: repetida });
      await consultas.invalidateQueries({ queryKey: ["mis-citas"] });
      await consultas.invalidateQueries({ queryKey: ["inicio"] });
      navegar("/paciente/citas", {
        state: {
          aviso: `Su cita quedó ${moviendo ? "movida" : "confirmada"} para el ${fechaLarga(inicio)} a las ${hora(inicio)}.`,
        },
      });
    } catch (error) {
      if (!(error instanceof ErrorDeApi)) {
        setFallo("No se pudo conectar con Vitalia. Intente de nuevo.");
      } else if (error.codigo === "espacio_ocupado") {
        setAlternativas((error.detalle as { alternativas: string[] }).alternativas);
        setFallo(error.message);
        void consultas.invalidateQueries({ queryKey: ["disponibilidad"] });
      } else if (error.codigo === "cita_repetida") {
        setFallo(
          <>
            {error.message}
            <Boton clase="neutro" onClick={() => confirmar(true)}>
              Agendar de todas formas
            </Boton>
          </>,
        );
      } else {
        setFallo(error.message);
      }
    } finally {
      setEnviando(false);
    }
  }

  function atras() {
    if (paso === 1 || (moviendo && paso === 2)) navegar(-1);
    else setPaso(paso === 3 ? 2 : 1);
  }

  return (
    <main className="agendar">
      <header className="agendar__encabezado">
        <div className="agendar__titulo">
          <button type="button" className="agendar__atras" aria-label="Volver" onClick={atras}>
            <ArrowLeftIcon />
          </button>
          <h1>{titulo}</h1>
          <span className="texto-suave">
            Paso {paso} de 3
          </span>
        </div>
        <Pasos total={3} actual={paso} />
      </header>

      {paso === 1 && (
        <section className="agendar__tipos" aria-label="Tipo de cita">
          <h2>¿Qué tipo de cita necesita?</h2>
          {tipos.data && !tipos.data.length && (
            <Nota>La agenda todavía no está disponible. Comuníquese con el consultorio.</Nota>
          )}
          {tipos.data?.map((t) => (
            <button
              key={t.id}
              type="button"
              className="agendar__tipo"
              onClick={() => {
                setElegido(t);
                setInicio(null);
                setPaso(2);
              }}
            >
              <span className="agendar__icono" aria-hidden="true">
                <StethoscopeIcon />
              </span>
              <span className="agendar__tipo-datos">
                <span className="agendar__tipo-nombre">{t.nombre}</span>
                <span className="texto-suave">{t.duracion_minutos} minutos</span>
              </span>
              <ArrowRightIcon aria-hidden="true" />
            </button>
          ))}
        </section>
      )}

      {paso >= 2 && tipo && (
        <>
          <section className="agendar__resumen" aria-label="Tipo de cita elegido">
            <span className="agendar__icono" aria-hidden="true">
              <StethoscopeIcon />
            </span>
            <span className="agendar__tipo-datos">
              <span className="agendar__tipo-nombre">{nombreDelTipo}</span>
              <span className="texto-suave">
                {duracion} minutos
                {consultorio.data?.medico ? ` · ${consultorio.data.medico}` : ""}
              </span>
            </span>
            {!moviendo && (
              <button type="button" className="enlace" onClick={() => setPaso(1)}>
                Cambiar
              </button>
            )}
          </section>

          {paso === 2 && (
            <SelectorDeEspacio tipo={tipo} cita={citaId} elegido={inicio} alElegir={setInicio} />
          )}

          {paso === 3 && inicio && (
            <section className="agendar__confirmacion tarjeta-formulario">
              <h2>{moviendo ? "Revise el cambio" : "Revise su cita"}</h2>
              {moviendo && cita && (
                <p className="texto-suave">
                  Antes: {conMayuscula(fechaLarga(cita.inicio))} a las {hora(cita.inicio)}
                </p>
              )}
              <p className="agendar__cuando">
                {conMayuscula(fechaLarga(inicio))}
                <span>{hora(inicio)}</span>
              </p>
              {fallo && <Nota tono="rojo">{fallo}</Nota>}
              {alternativas.length > 0 && (
                <div className="agendar__alternativas" role="group" aria-label="Horas cercanas">
                  {alternativas.map((a) => (
                    <button key={a} type="button" onClick={() => setInicio(a)}>
                      {fechaCorta(a)} · {hora(a)}
                    </button>
                  ))}
                </div>
              )}
              <Boton onClick={() => confirmar()} disabled={enviando}>
                {moviendo ? "Mover la cita" : "Confirmar la cita"}
              </Boton>
              <Link to="/paciente/citas" className="enlace">
                Volver a mis citas
              </Link>
            </section>
          )}
        </>
      )}

      {paso === 2 && (
        <footer className="agendar__eleccion">
          <div>
            <span className="texto-suave">Su elección</span>
            <span className="agendar__elegido">
              {inicio ? `${fechaCorta(inicio)} · ${hora(inicio)}` : "Elija día y hora"}
            </span>
          </div>
          <Boton disabled={!inicio} onClick={() => setPaso(3)}>
            Continuar
            <ArrowRightIcon />
          </Boton>
        </footer>
      )}
    </main>
  );
}
