import "../comunes/Ingresar.css";

import { useQueryClient } from "@tanstack/react-query";
import { useState, type ReactNode } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate, useSearchParams } from "react-router";

import { EnvelopeSimpleIcon, LockKeyIcon, StethoscopeIcon, UserIcon } from "../comunes/iconos";
import { ErrorDeApi } from "../api/cliente";
import { ponerEnMarcha, type TipoDocumento } from "../api/cuentas";
import { CampoDeDocumento } from "../comunes/CampoDeDocumento";
import { Boton } from "../comunes/piezas/Boton";
import { Campo, Entrada, EntradaDeContrasena } from "../comunes/piezas/Campo";
import { Marca } from "../comunes/piezas/Marca";
import { Nota } from "../comunes/piezas/Nota";
import { CORREO, faltasDeLaContrasena } from "../comunes/reglas";
import { CLAVE_DE_LA_CUENTA } from "../comunes/sesion";

type Formulario = {
  tipo_documento: TipoDocumento;
  numero_documento: string;
  nombres: string;
  apellidos: string;
  correo: string;
  contrasena: string;
};

/** P-13 en su entrada de puesta en marcha: el médico crea su cuenta (HU-001, CA-1 y CA-3). */
export default function PuestaEnMarcha() {
  const [parametros] = useSearchParams();
  const enlace = parametros.get("enlace") ?? "";
  const navegar = useNavigate();
  const consultas = useQueryClient();
  const [fallo, setFallo] = useState<ReactNode>(null);
  const {
    register,
    handleSubmit,
    getValues,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<Formulario>({ defaultValues: { tipo_documento: "CC" } });

  const crear = handleSubmit(async (datos) => {
    setFallo(null);
    try {
      await ponerEnMarcha({ ...datos, enlace });
      consultas.removeQueries({ queryKey: CLAVE_DE_LA_CUENTA });
      navegar("/medico/consultorio", { replace: true });
    } catch (error) {
      if (!(error instanceof ErrorDeApi)) {
        setFallo("No se pudo conectar con Vitalia. Revise su conexión e intente de nuevo.");
        return;
      }
      for (const [campo, mensaje] of Object.entries(error.campos)) {
        setError(campo as keyof Formulario, { message: mensaje });
      }
      if (error.codigo === "ya_hay_medico") {
        setFallo(
          <>
            {error.message} <Link to="/ingresar">Ingresar</Link>
          </>,
        );
      } else if (!Object.keys(error.campos).length) {
        setFallo(error.message);
      }
    }
  });

  return (
    <main className="pantalla-movil">
      <header className="ingresar__encabezado">
        <Marca tamano="grande" />
        <div className="ingresar__titulo">
          <h1>Cree su cuenta de médico</h1>
          <span className="texto-suave">
            Es la cuenta con la que manejará el consultorio. Este enlace sirve una sola vez.
          </span>
        </div>
      </header>

      {!enlace ? (
        <Nota tono="rojo">Este enlace no está completo. Pida uno nuevo a quien instaló Vitalia.</Nota>
      ) : (
        <form className="tarjeta-formulario" onSubmit={crear} noValidate>
          <div className="rejilla">
            <Campo id="medico-nombres" etiqueta="Nombres" error={errors.nombres?.message}>
              <Entrada
                id="medico-nombres"
                icono={<UserIcon />}
                autoComplete="given-name"
                invalido={Boolean(errors.nombres)}
                {...register("nombres", { required: "Escriba sus nombres" })}
              />
            </Campo>
            <Campo id="medico-apellidos" etiqueta="Apellidos" error={errors.apellidos?.message}>
              <Entrada
                id="medico-apellidos"
                autoComplete="family-name"
                invalido={Boolean(errors.apellidos)}
                {...register("apellidos", { required: "Escriba sus apellidos" })}
              />
            </Campo>
          </div>
          <CampoDeDocumento
            id="medico-documento"
            nombresLargos
            tipo={register("tipo_documento")}
            numero={register("numero_documento", { required: "Escriba su número de documento" })}
            error={errors.numero_documento}
          />
          <Campo id="medico-correo" etiqueta="Correo" error={errors.correo?.message}>
            <Entrada
              id="medico-correo"
              type="email"
              icono={<EnvelopeSimpleIcon />}
              autoComplete="email"
              invalido={Boolean(errors.correo)}
              {...register("correo", {
                required: "Escriba su correo",
                pattern: { value: CORREO, message: "Escriba un correo válido" },
              })}
            />
          </Campo>
          <Campo
            id="medico-clave"
            etiqueta="Cree su contraseña"
            error={errors.contrasena?.message}
            ayuda="Mínimo 8 caracteres y al menos un número. No use su número de documento."
          >
            <EntradaDeContrasena
              id="medico-clave"
              icono={<LockKeyIcon />}
              autoComplete="new-password"
              invalido={Boolean(errors.contrasena)}
              {...register("contrasena", {
                validate: (valor) => faltasDeLaContrasena(valor, getValues("numero_documento")),
              })}
            />
          </Campo>
          {fallo && <Nota tono="rojo">{fallo}</Nota>}
          <Boton type="submit" disabled={isSubmitting}>
            <StethoscopeIcon />
            Crear mi cuenta
          </Boton>
        </form>
      )}
    </main>
  );
}
