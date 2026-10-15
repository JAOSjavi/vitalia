import "./Ingresar.css";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router";

import { ArrowRightIcon, InfoIcon, LockKeyIcon, UserPlusIcon } from "./iconos";
import { ErrorDeApi } from "../api/cliente";
import { consultorioPublico } from "../api/consultorio";
import { ingresar, type TipoDocumento } from "../api/cuentas";
import { CampoDeDocumento } from "./CampoDeDocumento";
import { Boton, BotonEnlace } from "./piezas/Boton";
import { Campo, EntradaDeContrasena } from "./piezas/Campo";
import { Marca } from "./piezas/Marca";
import { Nota } from "./piezas/Nota";
import { CLAVE_DE_LA_CUENTA, inicioDe } from "./sesion";

type Formulario = {
  tipo_documento: TipoDocumento;
  numero_documento: string;
  contrasena: string;
};

/** P-01. Pacientes y médico ingresan aquí con su documento y su contraseña (HU-004). */
export function Ingresar() {
  const navegar = useNavigate();
  const consultas = useQueryClient();
  const consultorio = useQuery({ queryKey: ["consultorio-publico"], queryFn: consultorioPublico });
  const [fallo, setFallo] = useState<string | null>(null);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<Formulario>({
    defaultValues: { tipo_documento: "CC", numero_documento: "", contrasena: "" },
  });

  const alIngresar = handleSubmit(async (datos) => {
    setFallo(null);
    try {
      const sesion = await ingresar(datos);
      consultas.removeQueries({ queryKey: CLAVE_DE_LA_CUENTA });
      navegar(inicioDe(sesion.rol), { replace: true });
    } catch (error) {
      setFallo(
        error instanceof ErrorDeApi
          ? error.message
          : "No se pudo conectar con Vitalia. Revise su conexión e intente de nuevo.",
      );
    }
  });

  const nombre = consultorio.data?.nombre;
  return (
    <main className="pantalla-movil">
      <header className="ingresar__encabezado">
        <Marca tamano="grande" />
        <div className="ingresar__titulo">
          <h1>Bienvenido a Vitalia</h1>
          <span className="texto-suave">
            {nombre ? `${nombre} · Medicina general` : "Medicina general"}
          </span>
        </div>
      </header>

      <form className="tarjeta-formulario" onSubmit={alIngresar} noValidate>
        <CampoDeDocumento
          id="ingreso-documento"
          tipo={register("tipo_documento")}
          numero={register("numero_documento", { required: "Escriba su número de documento" })}
          error={errors.numero_documento}
        />
        <Campo id="ingreso-clave" etiqueta="Contraseña" error={errors.contrasena?.message}>
          <EntradaDeContrasena
            id="ingreso-clave"
            icono={<LockKeyIcon />}
            autoComplete="current-password"
            invalido={Boolean(errors.contrasena)}
            {...register("contrasena", { required: "Escriba su contraseña" })}
          />
        </Campo>
        {fallo && <Nota tono="rojo">{fallo}</Nota>}
        <Boton type="submit" disabled={isSubmitting}>
          Ingresar
          <ArrowRightIcon />
        </Boton>
      </form>

      <div className="ingresar__nuevo">
        <span className="texto-suave">¿Es su primera vez aquí?</span>
        <BotonEnlace a="/crear-cuenta" clase="borde">
          <UserPlusIcon />
          Crear mi cuenta
        </BotonEnlace>
      </div>

      <p className="ingresar__pie texto-suave">
        <InfoIcon aria-hidden="true" />
        <span>
          Su documento solo dice quién es usted; la contraseña es suya y nadie se la va a pedir.
          Después de cinco intentos fallidos, el ingreso se bloquea 15 minutos.
        </span>
      </p>
    </main>
  );
}
