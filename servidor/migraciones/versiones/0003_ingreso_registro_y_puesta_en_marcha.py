"""Sesiones, intentos, enlaces y autorizaciones (HU-001, HU-002, HU-003, HU-004, HU-007, HU-032).

Lo que ocurre sin sesión pasa por funciones de la base que hacen una sola cosa cada una
(diseno/02-modelo-de-datos.md, sección 3.2). Corren con permiso propio, así que la política
"interna" de cada tabla las deja pasar; la aplicación solo puede ejecutarlas.

Las reglas (cuántos fallos bloquean, cuánto dura una sesión, la mayoría de edad) viven en el
dominio. Las funciones reciben lo ya decidido y solo guardan, salvo dos comprobaciones que se
repiten aquí a propósito: mayoría de edad y un solo médico.
"""

import json
from pathlib import Path

from alembic import op
from sqlalchemy import text

revision: str = "0003"
down_revision: str | None = "0002"

_INTERNA = "session_user <> current_user"
_TABLAS = (
    "sesiones",
    "intentos_ingreso",
    "enlaces_un_uso",
    "textos_autorizacion",
    "autorizaciones",
)
_FUNCIONES = (
    "consultorio_publico()",
    "texto_vigente(text)",
    "buscar_credencial(text, text, text, text)",
    "guardar_intentos(text, text, integer, timestamptz, timestamptz)",
    "anotar_sin_sesion(uuid, text)",
    "abrir_sesion(uuid, text, timestamptz, timestamptz)",
    "sesion_vigente(text, timestamptz, interval, interval)",
    "registrar_paciente(text, text, text, text, date, text, text, text, uuid, uuid, date)",
    "crear_enlace_puesta_en_marcha(text, timestamptz)",
    "usar_enlace_puesta_en_marcha(text, timestamptz, text, text, text, text, text, text)",
)


def _forzar(tabla: str) -> None:
    op.execute(f"ALTER TABLE {tabla} ENABLE ROW LEVEL SECURITY")
    op.execute(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY interna ON {tabla} TO CURRENT_USER "
        f"USING ({_INTERNA}) WITH CHECK ({_INTERNA})"
    )


def upgrade() -> None:
    op.execute("CREATE UNIQUE INDEX un_solo_medico ON usuarios (rol) WHERE rol = 'medico'")

    op.execute(
        """
        CREATE TABLE sesiones (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            usuario_id uuid NOT NULL REFERENCES usuarios,
            hash_identificador text NOT NULL UNIQUE,
            creada_en timestamptz NOT NULL DEFAULT now(),
            ultima_actividad timestamptz NOT NULL,
            vence_en timestamptz NOT NULL,
            anulada_en timestamptz
        )
        """
    )
    # La cuenta es un resumen del documento, no el usuario: así una cuenta que no existe
    # acumula fallos igual que una que sí, y el ingreso no revela cuál existe.
    # Sin cuenta, la fila es el tope del equipo, sea cual sea la cuenta.
    op.execute(
        """
        CREATE TABLE intentos_ingreso (
            cuenta text,
            origen text NOT NULL,
            fallos integer NOT NULL CHECK (fallos > 0),
            ultimo_fallo timestamptz NOT NULL,
            bloqueado_hasta timestamptz,
            UNIQUE NULLS NOT DISTINCT (cuenta, origen)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE enlaces_un_uso (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            usuario_id uuid REFERENCES usuarios,
            tipo text NOT NULL CHECK (tipo IN ('recuperacion', 'activacion', 'puesta_en_marcha')),
            hash_enlace text NOT NULL UNIQUE,
            creado_en timestamptz NOT NULL DEFAULT now(),
            vence_en timestamptz NOT NULL,
            usado_en timestamptz
        )
        """
    )
    op.execute(
        """
        CREATE TABLE textos_autorizacion (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            tipo text NOT NULL CHECK (tipo IN ('datos', 'ia')),
            version integer NOT NULL,
            puntos jsonb NOT NULL,
            contenido text NOT NULL,
            vigente_desde timestamptz NOT NULL DEFAULT now(),
            UNIQUE (tipo, version)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE autorizaciones (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            paciente_id uuid NOT NULL REFERENCES pacientes,
            texto_id uuid NOT NULL REFERENCES textos_autorizacion,
            decision text NOT NULL CHECK (decision IN ('aceptada', 'rechazada', 'retirada')),
            fecha timestamptz NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX autorizaciones_por_paciente ON autorizaciones (paciente_id, fecha)")

    # Borradores de la versión 1, en su propio archivo para que el abogado los revise.
    for tipo in ("datos", "ia"):
        texto = json.loads(
            (Path(__file__).parent.parent / "textos" / f"{tipo}-v1.json").read_text("utf-8")
        )
        op.execute(
            text(
                "INSERT INTO textos_autorizacion (tipo, version, puntos, contenido) "
                "VALUES (:tipo, 1, CAST(:puntos AS jsonb), :contenido)"
            ).bindparams(
                tipo=tipo,
                puntos=json.dumps(texto["puntos"], ensure_ascii=False),
                contenido=texto["contenido"],
            )
        )

    for tabla in _TABLAS:
        _forzar(tabla)

    # --- Lo que la aplicación hace con sesión
    op.execute("GRANT SELECT, UPDATE (anulada_en) ON sesiones TO vitalia_api")
    op.execute(
        "CREATE POLICY propias ON sesiones FOR ALL TO vitalia_api "
        "USING (identidad() IN ('paciente', 'medico') AND usuario_id = usuario_actual()) "
        "WITH CHECK (identidad() IN ('paciente', 'medico') AND usuario_id = usuario_actual())"
    )
    op.execute("GRANT SELECT ON textos_autorizacion TO vitalia_api")
    op.execute(
        "CREATE POLICY lectura ON textos_autorizacion FOR SELECT TO vitalia_api "
        "USING (identidad() IN ('paciente', 'medico'))"
    )
    op.execute("GRANT SELECT, INSERT ON autorizaciones TO vitalia_api")
    propias = (
        "identidad() = 'paciente' AND paciente_id IN "
        "(SELECT id FROM pacientes WHERE usuario_id = usuario_actual())"
    )
    op.execute(
        f"CREATE POLICY propias ON autorizaciones FOR ALL TO vitalia_api "
        f"USING ({propias}) WITH CHECK ({propias})"
    )
    op.execute(
        "CREATE POLICY medico_y_sistema_leen ON autorizaciones FOR SELECT TO vitalia_api "
        "USING (identidad() IN ('medico', 'sistema'))"
    )
    # intentos_ingreso y enlaces_un_uso: la aplicación no tiene acceso; solo las funciones.

    # --- Funciones para lo que ocurre sin sesión
    op.execute(
        """
        CREATE FUNCTION consultorio_publico()
        RETURNS TABLE (nombre text, telefono text, medico text)
        LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
            SELECT c.nombre, c.telefono, nullif(trim(concat_ws(' ', m.nombres, m.apellidos)), '')
            FROM consultorio c LEFT JOIN medicos m ON true
        $$
        """
    )
    op.execute(
        """
        CREATE FUNCTION texto_vigente(p_tipo text)
        RETURNS TABLE (id uuid, version integer, puntos jsonb, contenido text,
                       vigente_desde timestamptz)
        LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
            SELECT id, version, puntos, contenido, vigente_desde FROM textos_autorizacion
            WHERE tipo = p_tipo AND vigente_desde <= now()
            ORDER BY version DESC LIMIT 1
        $$
        """
    )
    op.execute(
        """
        CREATE FUNCTION buscar_credencial(p_tipo text, p_numero text, p_cuenta text, p_origen text)
        RETURNS TABLE (usuario_id uuid, hash_contrasena text, rol text, activo boolean,
                       fallos integer, ultimo_fallo timestamptz, bloqueado_hasta timestamptz,
                       fallos_equipo integer, ultimo_fallo_equipo timestamptz,
                       equipo_bloqueado_hasta timestamptz)
        LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
            SELECT u.id, u.hash_contrasena, u.rol, coalesce(u.activo, false),
                   c.fallos, c.ultimo_fallo, c.bloqueado_hasta,
                   e.fallos, e.ultimo_fallo, e.bloqueado_hasta
            FROM (SELECT 1) AS una
            LEFT JOIN usuarios u
                ON u.tipo_documento = p_tipo AND u.numero_documento = p_numero
            LEFT JOIN intentos_ingreso c ON c.cuenta = p_cuenta AND c.origen = p_origen
            LEFT JOIN intentos_ingreso e ON e.cuenta IS NULL AND e.origen = p_origen
        $$
        """
    )
    op.execute(
        """
        CREATE FUNCTION guardar_intentos(p_cuenta text, p_origen text, p_fallos integer,
                                         p_ultimo_fallo timestamptz, p_bloqueado_hasta timestamptz)
        RETURNS void
        LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
        BEGIN
            IF p_fallos = 0 THEN
                DELETE FROM intentos_ingreso
                WHERE cuenta IS NOT DISTINCT FROM p_cuenta AND origen = p_origen;
            ELSE
                INSERT INTO intentos_ingreso (cuenta, origen, fallos, ultimo_fallo, bloqueado_hasta)
                VALUES (p_cuenta, p_origen, p_fallos, p_ultimo_fallo, p_bloqueado_hasta)
                ON CONFLICT (cuenta, origen) DO UPDATE
                SET fallos = excluded.fallos, ultimo_fallo = excluded.ultimo_fallo,
                    bloqueado_hasta = excluded.bloqueado_hasta;
            END IF;
        END
        $$
        """
    )
    op.execute(
        """
        CREATE FUNCTION anotar_sin_sesion(p_usuario uuid, p_accion text)
        RETURNS void
        LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
        BEGIN
            IF p_accion NOT IN ('ingreso_fallido', 'ingreso_bloqueado') THEN
                RAISE EXCEPTION 'Acción no admitida sin sesión: %', p_accion;
            END IF;
            INSERT INTO bitacora (usuario_id, rol, accion)
            SELECT p_usuario, (SELECT rol FROM usuarios WHERE id = p_usuario), p_accion;
        END
        $$
        """
    )
    op.execute(
        """
        CREATE FUNCTION abrir_sesion(p_usuario uuid, p_hash text, p_ahora timestamptz,
                                     p_vence timestamptz)
        RETURNS void
        LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
        DECLARE
            v_rol text;
        BEGIN
            SELECT rol INTO v_rol FROM usuarios
            WHERE id = p_usuario AND activo AND hash_contrasena IS NOT NULL;
            IF v_rol IS NULL THEN
                RAISE EXCEPTION 'La cuenta no puede abrir sesión';
            END IF;
            INSERT INTO sesiones (usuario_id, hash_identificador, ultima_actividad, vence_en)
            VALUES (p_usuario, p_hash, p_ahora, p_vence);
            INSERT INTO bitacora (usuario_id, rol, accion) VALUES (p_usuario, v_rol, 'ingreso');
        END
        $$
        """
    )
    # La última actividad se renueva como mucho una vez por minuto (arquitectura, sección 8.1).
    op.execute(
        """
        CREATE FUNCTION sesion_vigente(p_hash text, p_ahora timestamptz,
                                       p_inactividad interval, p_renovar_cada interval)
        RETURNS TABLE (usuario_id uuid, rol text)
        LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
        BEGIN
            UPDATE sesiones s
            SET ultima_actividad = p_ahora, vence_en = p_ahora + p_inactividad
            WHERE s.hash_identificador = p_hash AND s.anulada_en IS NULL
              AND s.vence_en > p_ahora AND s.ultima_actividad <= p_ahora - p_renovar_cada;
            RETURN QUERY
                SELECT s.usuario_id, u.rol FROM sesiones s JOIN usuarios u ON u.id = s.usuario_id
                WHERE s.hash_identificador = p_hash AND s.anulada_en IS NULL
                  AND s.vence_en > p_ahora AND u.activo;
        END
        $$
        """
    )
    op.execute(
        """
        CREATE FUNCTION registrar_paciente(
            p_tipo text, p_numero text, p_nombres text, p_apellidos text,
            p_fecha_nacimiento date, p_telefono text, p_correo text, p_hash_contrasena text,
            p_texto_datos uuid, p_texto_ia uuid, p_hoy date)
        RETURNS uuid
        LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
        DECLARE
            v_usuario uuid;
            v_paciente uuid;
        BEGIN
            IF p_fecha_nacimiento > p_hoy - interval '18 years' THEN
                RAISE EXCEPTION 'menor_de_edad' USING ERRCODE = 'check_violation';
            END IF;
            IF p_texto_datos IS DISTINCT FROM (SELECT id FROM texto_vigente('datos'))
               OR (p_texto_ia IS NOT NULL
                   AND p_texto_ia IS DISTINCT FROM (SELECT id FROM texto_vigente('ia'))) THEN
                RAISE EXCEPTION 'texto_desactualizado' USING ERRCODE = 'check_violation';
            END IF;

            INSERT INTO usuarios (tipo_documento, numero_documento, correo, hash_contrasena, rol)
            VALUES (p_tipo, p_numero, p_correo, p_hash_contrasena, 'paciente')
            RETURNING id INTO v_usuario;
            INSERT INTO pacientes (usuario_id, nombres, apellidos, fecha_nacimiento, telefono)
            VALUES (v_usuario, p_nombres, p_apellidos, p_fecha_nacimiento, p_telefono)
            RETURNING id INTO v_paciente;

            INSERT INTO autorizaciones (paciente_id, texto_id, decision)
            VALUES (v_paciente, p_texto_datos, 'aceptada');
            IF p_texto_ia IS NOT NULL THEN
                INSERT INTO autorizaciones (paciente_id, texto_id, decision)
                VALUES (v_paciente, p_texto_ia, 'aceptada');
            END IF;

            INSERT INTO bitacora (usuario_id, rol, paciente_id, accion)
            VALUES (v_usuario, 'paciente', v_paciente, 'registro');
            RETURN v_usuario;
        END
        $$
        """
    )
    op.execute(
        """
        CREATE FUNCTION crear_enlace_puesta_en_marcha(p_hash text, p_vence timestamptz)
        RETURNS void
        LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
        BEGIN
            IF EXISTS (SELECT 1 FROM usuarios WHERE rol = 'medico') THEN
                RAISE EXCEPTION 'ya_hay_medico' USING ERRCODE = 'unique_violation';
            END IF;
            INSERT INTO enlaces_un_uso (tipo, hash_enlace, vence_en)
            VALUES ('puesta_en_marcha', p_hash, p_vence);
        END
        $$
        """
    )
    op.execute(
        """
        CREATE FUNCTION usar_enlace_puesta_en_marcha(
            p_hash text, p_ahora timestamptz, p_tipo text, p_numero text, p_correo text,
            p_hash_contrasena text, p_nombres text, p_apellidos text)
        RETURNS uuid
        LANGUAGE plpgsql SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
        DECLARE
            v_enlace uuid;
            v_usuario uuid;
        BEGIN
            SELECT id INTO v_enlace FROM enlaces_un_uso
            WHERE hash_enlace = p_hash AND tipo = 'puesta_en_marcha'
              AND usado_en IS NULL AND vence_en > p_ahora
            FOR UPDATE;
            IF v_enlace IS NULL THEN
                RAISE EXCEPTION 'enlace_invalido' USING ERRCODE = 'no_data_found';
            END IF;
            IF EXISTS (SELECT 1 FROM usuarios WHERE rol = 'medico') THEN
                RAISE EXCEPTION 'ya_hay_medico' USING ERRCODE = 'unique_violation';
            END IF;

            INSERT INTO usuarios (tipo_documento, numero_documento, correo, hash_contrasena, rol)
            VALUES (p_tipo, p_numero, p_correo, p_hash_contrasena, 'medico')
            RETURNING id INTO v_usuario;
            INSERT INTO medicos (usuario_id, nombres, apellidos)
            VALUES (v_usuario, p_nombres, p_apellidos);
            UPDATE enlaces_un_uso SET usado_en = p_ahora, usuario_id = v_usuario
            WHERE id = v_enlace;

            INSERT INTO bitacora (usuario_id, rol, accion)
            VALUES (v_usuario, 'medico', 'puesta_en_marcha');
            RETURN v_usuario;
        END
        $$
        """
    )
    for firma in _FUNCIONES:
        op.execute(f"REVOKE EXECUTE ON FUNCTION {firma} FROM PUBLIC")
        op.execute(f"GRANT EXECUTE ON FUNCTION {firma} TO vitalia_api")


def downgrade() -> None:
    for firma in reversed(_FUNCIONES):
        op.execute(f"DROP FUNCTION {firma}")
    for tabla in reversed(_TABLAS):
        op.execute(f"DROP TABLE {tabla}")
    op.execute("DROP INDEX un_solo_medico")
