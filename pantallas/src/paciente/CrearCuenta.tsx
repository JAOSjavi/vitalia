import "./CrearCuenta.css";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, type ReactNode } from "react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router";

import {
  ArrowLeftIcon,
  EnvelopeSimpleIcon,
  LockKeyIcon,
  PhoneIcon,
  ShieldCheckIcon,
  UserIcon,
} from "../comunes/iconos";
import { ErrorDeApi } from "../api/cliente";
import { registrarse, textoDeAutorizacion, type TipoDocumento } from "../api/cuentas";
import { CampoDeDocumento } from "../comunes/CampoDeDocumento";
import { Boton } from "../comunes/piezas/Boton";
import { Campo, Entrada, EntradaDeContrasena } from "../comunes/piezas/Campo";
import { Hoja } from "../comunes/piezas/Hoja";
import { Nota } from "../comunes/piezas/Nota";
import { Pasos } from "../comunes/piezas/Pasos";
import {
  CORREO,
  TELEFONO,
  esMayorDeEdad,
  faltasDeLaContrasena,
  sinSeparadores,
} from "../comunes/reglas";
import { CLAVE_DE_LA_CUENTA } from "../comunes/sesion";

type Formulario = {
  nombres: string;
  apellidos: string;
  tipo_documento: TipoDocumento;
  numero_documento: string;
  fecha_nacimiento: string;
  telefono: string;
  correo: string;
  contrasena: string;
  acepta_datos: boolean;
  acepta_ia: boolean;
};

const CAMPOS_DEL_PASO: Record<1 | 2, (keyof Formulario)[]> = {
  1: ["nombres", "apellidos", "numero_documento", "fecha_nacimiento", "telefono", "correo"],
  2: ["contrasena"],
};

const MENOR_DE_EDAD = "Las cuentas son para mayores de edad. Comuníquese con el consultorio.";

/** P-02. El paciente crea su cuenta y acepta el tratamiento de sus datos (HU-002, HU-003, HU-032). */
export default function CrearCuenta() {
  const navegar = useNavigate();
  const consultas = useQueryClient();
  const [paso, setPaso] = useState<1 | 2 | 3>(1);
  const [aviso, setAviso] = useState<ReactNode>(null);
  const [completa, setCompleta] = useState(false);
  const textoDatos = useQuery({ queryKey: ["texto", "datos"], queryFn: () => textoDeAutorizacion("datos") });
  const textoIa = useQuery({ queryKey: ["texto", "ia"], queryFn: () => textoDeAutorizacion("ia") });
  const {
    register,
    handleSubmit,
    trigger,
    getValues,
    setError,
    formState: { errors, isSubmitting },
  } = useForm<Formulario>({
    defaultValues: { tipo_documento: "CC", acepta_datos: false, acepta_ia: false },
  });

  async function continuar(siguiente: 2 | 3) {
    if (await trigger(CAMPOS_DEL_PASO[(siguiente - 1) as 1 | 2])) {
      setAviso(null);
      setPaso(siguiente);
    }
  }

  const crear = handleSubmit(async (datos) => {
    if (!datos.acepta_datos) {
      setError("acepta_datos", {
        message: "Para crear la cuenta debe autorizar el tratamiento de sus datos.",
      });
      return;
    }
    if (!textoDatos.data || !textoIa.data) return;
    try {
      await registrarse({
        tipo_documento: datos.tipo_documento,
        numero_documento: datos.numero_documento,
        nombres: datos.nombres,
        apellidos: datos.apellidos,
        fecha_nacimiento: datos.fecha_nacimiento,
        telefono: datos.telefono,
        correo: datos.correo,
        contrasena: datos.contrasena,
        texto_datos: textoDatos.data.id,
        texto_ia: datos.acepta_ia ? textoIa.data.id : null,
      });
      consultas.removeQueries({ queryKey: CLAVE_DE_LA_CUENTA });
      navegar("/paciente", { replace: true });
    } catch (error) {
      mostrarFallo(error);
    }
  });

  function mostrarFallo(error: unknown) {
    if (!(error instanceof ErrorDeApi)) {
      setAviso("No se pudo conectar con Vitalia. Revise su conexión e intente de nuevo.");
      return;
    }
    const campos = Object.entries(error.campos) as [keyof Formulario, string][];
    if (campos.length) {
      for (const [campo, mensaje] of campos) setError(campo, { message: mensaje });
      setPaso(CAMPOS_DEL_PASO[1].includes(campos[0][0]) ? 1 : 2);
      return;
    }
    if (error.codigo === "documento_registrado") {
      setPaso(1);
      setAviso(
        <>
          {error.message} <Link to="/ingresar">Ingresar</Link>
        </>,
      );
      return;
    }
    if (error.codigo === "menor_de_edad") setPaso(1);
    if (error.codigo === "autorizacion_desactualizada") {
      void textoDatos.refetch();
      void textoIa.refetch();
    }
    setAviso(error.message);
  }

  return (
    <main className="pantalla-movil crear-cuenta">
      <div className="crear-cuenta__encabezado">
        <div className="crear-cuenta__titulo">
          {paso === 1 ? (
            <Link to="/ingresar" className="crear-cuenta__atras" aria-label="Volver a ingresar">
              <ArrowLeftIcon />
            </Link>
          ) : (
            <button
              type="button"
              className="crear-cuenta__atras"
              aria-label="Paso anterior"
              onClick={() => setPaso(paso === 3 ? 2 : 1)}
            >
              <ArrowLeftIcon />
            </button>
          )}
          <h1>Crear mi cuenta</h1>
        </div>
        <Pasos total={3} actual={paso} />
      </div>

      <form
        className="tarjeta-formulario"
        noValidate
        onSubmit={(evento) => {
          // Enter avanza al paso siguiente; solo el último crea la cuenta.
          evento.preventDefault();
          if (paso === 3) void crear();
          else void continuar(paso === 1 ? 2 : 3);
        }}
      >
        {aviso && paso !== 3 && <Nota tono="rojo">{aviso}</Nota>}

        {paso === 1 && (
          <>
            <div className="rejilla">
              <Campo id="registro-nombres" etiqueta="Nombres" error={errors.nombres?.message}>
                <Entrada
                  id="registro-nombres"
                  icono={<UserIcon />}
                  autoComplete="given-name"
                  invalido={Boolean(errors.nombres)}
                  {...register("nombres", { required: "Escriba sus nombres" })}
                />
              </Campo>
              <Campo id="registro-apellidos" etiqueta="Apellidos" error={errors.apellidos?.message}>
                <Entrada
                  id="registro-apellidos"
                  autoComplete="family-name"
                  invalido={Boolean(errors.apellidos)}
                  {...register("apellidos", { required: "Escriba sus apellidos" })}
                />
              </Campo>
            </div>
            <CampoDeDocumento
              id="registro-documento"
              nombresLargos
              tipo={register("tipo_documento")}
              numero={register("numero_documento", {
                required: "Escriba su número de documento",
              })}
              error={errors.numero_documento}
            />
            <div className="rejilla">
              <Campo
                id="registro-nacimiento"
                etiqueta="Fecha de nacimiento"
                error={errors.fecha_nacimiento?.message}
              >
                <Entrada
                  id="registro-nacimiento"
                  type="date"
                  autoComplete="bday"
                  invalido={Boolean(errors.fecha_nacimiento)}
                  {...register("fecha_nacimiento", {
                    required: "Escriba su fecha de nacimiento",
                    validate: (valor) => esMayorDeEdad(valor) || MENOR_DE_EDAD,
                  })}
                />
              </Campo>
              <Campo id="registro-celular" etiqueta="Celular" error={errors.telefono?.message}>
                <Entrada
                  id="registro-celular"
                  icono={<PhoneIcon />}
                  inputMode="tel"
                  autoComplete="tel"
                  invalido={Boolean(errors.telefono)}
                  {...register("telefono", {
                    required: "Escriba su celular",
                    validate: (valor) =>
                      TELEFONO.test(sinSeparadores(valor)) || "Escriba un teléfono de 7 a 15 números",
                  })}
                />
              </Campo>
            </div>
            <Campo id="registro-correo" etiqueta="Correo" error={errors.correo?.message}>
              <Entrada
                id="registro-correo"
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
            <div className="botones">
              <Boton clase="neutro" onClick={() => navegar("/ingresar")}>
                Ya tengo cuenta
              </Boton>
              <Boton type="submit">Continuar</Boton>
            </div>
          </>
        )}

        {paso >= 2 && (
          <>
            <Campo
              id="registro-clave"
              etiqueta="Cree su contraseña"
              error={errors.contrasena?.message}
              ayuda="Mínimo 8 caracteres y al menos un número. No use su número de documento."
            >
              <EntradaDeContrasena
                id="registro-clave"
                icono={<LockKeyIcon />}
                autoComplete="new-password"
                invalido={Boolean(errors.contrasena)}
                {...register("contrasena", {
                  validate: (valor) => faltasDeLaContrasena(valor, getValues("numero_documento")),
                })}
              />
            </Campo>
            <div className="botones">
              <Boton clase="neutro" onClick={() => setPaso(1)}>
                Atrás
              </Boton>
              <Boton type="submit">Continuar</Boton>
            </div>
          </>
        )}

        {paso === 3 && (
          <Hoja titulo="Tratamiento de sus datos" icono={<ShieldCheckIcon />} alCerrar={() => setPaso(2)}>
            <p className="crear-cuenta__ley texto-suave">
              Lo más importante de nuestra política, según la Ley 1581 de 2012 (Habeas Data).
            </p>
            {textoDatos.data ? (
              <ul className="crear-cuenta__puntos">
                {textoDatos.data.puntos.map((punto) => (
                  <li
                    key={punto.titulo}
                    className={punto.resaltado ? "crear-cuenta__punto--resaltado" : undefined}
                  >
                    <span className="crear-cuenta__vineta" aria-hidden="true" />
                    <span>
                      <strong>{punto.titulo}:</strong> {punto.texto}
                    </span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="texto-suave">Cargando el texto…</p>
            )}
            {completa && textoDatos.data && (
              <div className="crear-cuenta__completa">
                {textoDatos.data.contenido.split("\n\n").map((parrafo) => (
                  <p key={parrafo}>{parrafo}</p>
                ))}
              </div>
            )}
            <button type="button" className="enlace" onClick={() => setCompleta(!completa)}>
              {completa ? "Ocultar la política completa" : "Leer la política completa"}
            </button>

            <label className="casilla" htmlFor="acepto-datos">
              <input id="acepto-datos" type="checkbox" {...register("acepta_datos")} />
              <span>Autorizo el tratamiento de mis datos personales y de salud.</span>
            </label>
            {errors.acepta_datos && <Nota tono="rojo">{errors.acepta_datos.message}</Nota>}
            <label className="casilla" htmlFor="acepto-ia">
              <input id="acepto-ia" type="checkbox" {...register("acepta_ia")} />
              <span>
                Autorizo que mis documentos se analicen con inteligencia artificial.{" "}
                <span className="texto-suave">Es opcional y puede cambiarlo después.</span>
              </span>
            </label>
            {aviso && <Nota tono="rojo">{aviso}</Nota>}

            <div className="botones">
              <Boton clase="neutro" onClick={() => setPaso(2)}>
                Volver
              </Boton>
              <Boton type="submit" disabled={isSubmitting || !textoDatos.data}>
                Aceptar y crear cuenta
              </Boton>
            </div>
          </Hoja>
        )}
      </form>
    </main>
  );
}
