import "./Configuracion.css";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";

import { ErrorDeApi } from "../api/cliente";
import {
  crearTipoDeCita,
  editarTipoDeCita,
  guardarHorario,
  tiposDeCita,
  verHorario,
  type Cita,
  type Franja,
  type TipoDeCita,
} from "../api/citas";
import { fechaLarga, hora } from "../comunes/fechas";
import { PlusIcon, TrashIcon } from "../comunes/iconos";
import { Boton } from "../comunes/piezas/Boton";
import { Campo, Entrada } from "../comunes/piezas/Campo";
import { Estado } from "../comunes/piezas/Estado";
import { Nota } from "../comunes/piezas/Nota";
import { Tarjeta } from "../comunes/piezas/Tarjeta";

const DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];

/** M-08 y M-10. Horario semanal de atención y tipos de cita (HU-008, HU-010). */
export function Configuracion() {
  return (
    <main className="zona-medico__contenido">
      <h1 className="configuracion__titulo">Configuración</h1>
      <Horario />
      <Tipos />
    </main>
  );
}

type FranjaEditable = Franja & { clave: number };

function Horario() {
  const consultas = useQueryClient();
  const horario = useQuery({ queryKey: ["horario"], queryFn: verHorario });
  const [franjas, setFranjas] = useState<FranjaEditable[]>([]);
  const [errores, setErrores] = useState<Record<number, string>>({});
  const [afectadas, setAfectadas] = useState<Cita[] | null>(null);
  const [fallo, setFallo] = useState<string | null>(null);
  const [siguiente, setSiguiente] = useState(0);

  useEffect(() => {
    if (horario.data) {
      setFranjas(horario.data.franjas.map((f, indice) => ({ ...f, clave: indice })));
      setSiguiente(horario.data.franjas.length);
    }
  }, [horario.data]);

  function cambiar(clave: number, cambio: Partial<Franja>) {
    setFranjas(franjas.map((f) => (f.clave === clave ? { ...f, ...cambio } : f)));
  }

  function agregar(dia: number) {
    setFranjas([...franjas, { clave: siguiente, dia_semana: dia, hora_inicio: "08:00", hora_fin: "12:00" }]);
    setSiguiente(siguiente + 1);
  }

  async function guardar() {
    setErrores({});
    setFallo(null);
    setAfectadas(null);
    const enviadas = franjas.map(({ clave, ...franja }) => ({ ...franja, clave }));
    try {
      const resultado = await guardarHorario(enviadas.map(({ clave: _, ...franja }) => franja));
      setAfectadas(resultado.citas_afectadas);
      await consultas.invalidateQueries({ queryKey: ["horario"] });
      await consultas.invalidateQueries({ queryKey: ["agenda-hoy"] });
    } catch (error) {
      if (error instanceof ErrorDeApi && Object.keys(error.campos).length) {
        // El servidor dice qué franja falla por su posición en la lista enviada.
        const porClave: Record<number, string> = {};
        for (const [campo, mensaje] of Object.entries(error.campos)) {
          const posicion = Number(campo.split(".")[1]);
          if (enviadas[posicion]) porClave[enviadas[posicion].clave] = mensaje;
        }
        setErrores(porClave);
      } else {
        setFallo(error instanceof ErrorDeApi ? error.message : "No se pudo guardar el horario.");
      }
    }
  }

  return (
    <Tarjeta nombre="Horario de atención">
      <div className="configuracion__seccion">
        <div>
          <h2>Horario de atención</h2>
          <p className="texto-suave">
            Los pacientes solo ven espacios dentro de estas franjas. Un día sin franjas no ofrece
            ninguno.
          </p>
        </div>
        {DIAS.map((nombre, indice) => {
          const dia = indice + 1;
          const delDia = franjas.filter((f) => f.dia_semana === dia);
          return (
            <div key={nombre} className="configuracion__dia">
              <span className="configuracion__nombre-dia">{nombre}</span>
              <div className="configuracion__franjas">
                {!delDia.length && <span className="texto-suave">Sin atención</span>}
                {delDia.map((franja) => (
                  <div key={franja.clave} className="configuracion__franja">
                    <div className="configuracion__horas">
                      <Entrada
                        type="time"
                        aria-label={`${nombre}: desde`}
                        value={franja.hora_inicio.slice(0, 5)}
                        invalido={Boolean(errores[franja.clave])}
                        onChange={(e) => cambiar(franja.clave, { hora_inicio: e.target.value })}
                      />
                      <span className="texto-suave">a</span>
                      <Entrada
                        type="time"
                        aria-label={`${nombre}: hasta`}
                        value={franja.hora_fin.slice(0, 5)}
                        invalido={Boolean(errores[franja.clave])}
                        onChange={(e) => cambiar(franja.clave, { hora_fin: e.target.value })}
                      />
                      <button
                        type="button"
                        className="configuracion__quitar"
                        aria-label={`Quitar la franja del ${nombre.toLowerCase()}`}
                        onClick={() => setFranjas(franjas.filter((f) => f.clave !== franja.clave))}
                      >
                        <TrashIcon />
                      </button>
                    </div>
                    {errores[franja.clave] && (
                      <p className="campo__error" role="alert">
                        <span className="campo__punto" aria-hidden="true" />
                        {errores[franja.clave]}
                      </p>
                    )}
                  </div>
                ))}
              </div>
              <button type="button" className="enlace" onClick={() => agregar(dia)}>
                <PlusIcon />
                Agregar franja
              </button>
            </div>
          );
        })}
        {fallo && <Nota tono="rojo">{fallo}</Nota>}
        {afectadas && !afectadas.length && <Estado tono="verde">Guardado</Estado>}
        {afectadas && afectadas.length > 0 && (
          <Nota>
            <span>
              Horario guardado. Estas citas quedaron por fuera y se conservan hasta que usted las
              mueva o las cancele:
            </span>
            <ul className="configuracion__afectadas">
              {afectadas.map((cita) => (
                <li key={cita.id}>
                  {cita.paciente}: {fechaLarga(cita.inicio)} a las {hora(cita.inicio)}
                </li>
              ))}
            </ul>
          </Nota>
        )}
        <div className="configuracion__acciones">
          <Boton onClick={guardar} disabled={horario.isPending}>
            Guardar el horario
          </Boton>
        </div>
      </div>
    </Tarjeta>
  );
}

function Tipos() {
  const consultas = useQueryClient();
  const tipos = useQuery({ queryKey: ["tipos-cita"], queryFn: tiposDeCita });
  const [nombre, setNombre] = useState("");
  const [duracion, setDuracion] = useState("30");
  const [errores, setErrores] = useState<Record<string, string>>({});

  async function refrescar() {
    await consultas.invalidateQueries({ queryKey: ["tipos-cita"] });
    await consultas.invalidateQueries({ queryKey: ["agenda-hoy"] });
  }

  async function crear() {
    setErrores({});
    try {
      await crearTipoDeCita({ nombre, duracion_minutos: Number(duracion) });
      setNombre("");
      await refrescar();
    } catch (error) {
      setErrores(error instanceof ErrorDeApi ? error.campos : { nombre: "No se pudo crear." });
    }
  }

  async function cambiarEstado(tipo: TipoDeCita) {
    await editarTipoDeCita(tipo.id, { activo: !tipo.activo });
    await refrescar();
  }

  return (
    <Tarjeta nombre="Tipos de cita">
      <div className="configuracion__seccion">
        <div>
          <h2>Tipos de cita</h2>
          <p className="texto-suave">
            Si cambia la duración, aplica solo a las citas nuevas. Un tipo desactivado deja de
            ofrecerse y sus citas se conservan.
          </p>
        </div>
        {tipos.data?.map((tipo) => (
          <div key={tipo.id} className="configuracion__tipo">
            <div className="configuracion__tipo-datos">
              <span className="configuracion__tipo-nombre">{tipo.nombre}</span>
              <span className="texto-suave">{tipo.duracion_minutos} minutos</span>
            </div>
            <Estado tono={tipo.activo ? "verde" : "gris"}>
              {tipo.activo ? "Se ofrece" : "No se ofrece"}
            </Estado>
            <Boton clase="neutro" onClick={() => cambiarEstado(tipo)}>
              {tipo.activo ? "Dejar de ofrecer" : "Volver a ofrecer"}
            </Boton>
          </div>
        ))}
        <div className="configuracion__nuevo">
          <Campo id="tipo-nombre" etiqueta="Nuevo tipo de cita" error={errores.nombre}>
            <Entrada
              id="tipo-nombre"
              value={nombre}
              placeholder="Por ejemplo, Control"
              invalido={Boolean(errores.nombre)}
              onChange={(e) => setNombre(e.target.value)}
            />
          </Campo>
          <Campo id="tipo-duracion" etiqueta="Minutos" error={errores.duracion_minutos}>
            <Entrada
              id="tipo-duracion"
              type="number"
              min={5}
              max={240}
              step={5}
              value={duracion}
              invalido={Boolean(errores.duracion_minutos)}
              onChange={(e) => setDuracion(e.target.value)}
            />
          </Campo>
          <Boton clase="borde" onClick={crear}>
            <PlusIcon />
            Agregar
          </Boton>
        </div>
      </div>
    </Tarjeta>
  );
}
