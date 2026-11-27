import "./DatosDelConsultorio.css";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { ErrorDeApi } from "../api/cliente";
import { guardarConsultorio, verConsultorio, type Consultorio } from "../api/consultorio";
import { Boton } from "../comunes/piezas/Boton";
import { Campo, Entrada } from "../comunes/piezas/Campo";
import { Estado } from "../comunes/piezas/Estado";
import { Nota } from "../comunes/piezas/Nota";
import { Tarjeta } from "../comunes/piezas/Tarjeta";

type Formulario = { [K in keyof Consultorio]: string };

const VACIO: Formulario = {
  nombre: "",
  direccion: "",
  telefono: "",
  correo: "",
  medico_nombres: "",
  medico_apellidos: "",
  registro_profesional: "",
};

/** M-11. El médico registra su consultorio, su nombre y su registro profesional (HU-001, CA-2). */
export function DatosDelConsultorio() {
  const consultas = useQueryClient();
  const consultorio = useQuery({ queryKey: ["consultorio"], queryFn: verConsultorio });
  const [guardado, setGuardado] = useState(false);
  const [fallo, setFallo] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    reset,
    setError,
    formState: { errors, isSubmitting, isDirty },
  } = useForm<Formulario>({ defaultValues: VACIO });

  useEffect(() => {
    if (consultorio.data) {
      const datos = consultorio.data;
      reset(
        Object.fromEntries(
          Object.keys(VACIO).map((campo) => [campo, datos[campo as keyof Consultorio] ?? ""]),
        ) as Formulario,
      );
    }
  }, [consultorio.data, reset]);

  const guardar = handleSubmit(async (datos) => {
    setGuardado(false);
    setFallo(null);
    try {
      await guardarConsultorio({
        ...datos,
        direccion: datos.direccion || null,
        telefono: datos.telefono || null,
        correo: datos.correo || null,
        registro_profesional: datos.registro_profesional || null,
      });
      await consultas.invalidateQueries({ queryKey: ["consultorio"] });
      await consultas.invalidateQueries({ queryKey: ["consultorio-publico"] });
      setGuardado(true);
    } catch (error) {
      if (error instanceof ErrorDeApi && Object.keys(error.campos).length) {
        for (const [campo, mensaje] of Object.entries(error.campos)) {
          setError(campo as keyof Formulario, { message: mensaje });
        }
        return;
      }
      setFallo(error instanceof ErrorDeApi ? error.message : "No se pudo guardar. Intente de nuevo.");
    }
  });

  function campo(nombre: keyof Formulario, etiqueta: string, opciones: { requerido?: string; tipo?: string } = {}) {
    const id = `consultorio-${nombre}`;
    return (
      <Campo id={id} etiqueta={etiqueta} error={errors[nombre]?.message}>
        <Entrada
          id={id}
          type={opciones.tipo ?? "text"}
          invalido={Boolean(errors[nombre])}
          {...register(nombre, opciones.requerido ? { required: opciones.requerido } : {})}
        />
      </Campo>
    );
  }

  return (
    <main className="zona-medico__contenido zona-medico__contenido--angosto">
      <div className="consultorio__titulo">
        <h1>Consultorio</h1>
        <p className="texto-suave">Estos datos los ven sus pacientes al ingresar y en su inicio.</p>
      </div>
      <form className="consultorio__formulario" onSubmit={guardar} noValidate>
        <Tarjeta nombre="Datos del consultorio">
          <div className="consultorio__seccion">
            <h2>Datos del consultorio</h2>
            {campo("nombre", "Nombre del consultorio", { requerido: "Escriba el nombre del consultorio" })}
            {campo("direccion", "Dirección")}
            <div className="rejilla">
              {campo("telefono", "Teléfono", { tipo: "tel" })}
              {campo("correo", "Correo", { tipo: "email" })}
            </div>
          </div>
        </Tarjeta>
        <Tarjeta nombre="Sus datos">
          <div className="consultorio__seccion">
            <h2>Sus datos</h2>
            <div className="rejilla">
              {campo("medico_nombres", "Nombres", { requerido: "Escriba sus nombres" })}
              {campo("medico_apellidos", "Apellidos", { requerido: "Escriba sus apellidos" })}
            </div>
            {campo("registro_profesional", "Registro profesional")}
          </div>
        </Tarjeta>
        {fallo && <Nota tono="rojo">{fallo}</Nota>}
        <div className="consultorio__acciones">
          {guardado && !isDirty && <Estado tono="verde">Guardado</Estado>}
          <Boton type="submit" disabled={isSubmitting || consultorio.isPending}>
            Guardar
          </Boton>
        </div>
      </form>
    </main>
  );
}
