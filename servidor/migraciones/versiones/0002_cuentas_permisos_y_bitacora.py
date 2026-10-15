"""Cuentas, roles, matriz de permisos y bitácora, con permisos por fila (HU-006, HU-036, HU-037).

Cómo sabe la base quién pregunta (diseno/02-modelo-de-datos.md, sección 3):

- La API declara al abrir cada transacción el usuario y la identidad; las políticas los leen con
  usuario_actual() e identidad(). Sin identidad ninguna política deja pasar filas.
- Lo que ocurre sin sesión pasa por funciones con permiso propio. Dentro de ellas el usuario de
  la base es el dueño de las tablas y no quien se conectó: eso es lo que revisa la política
  "interna". La API no puede fingirlo.
- Los permisos por fila van forzados: ni el dueño lee las tablas si se conecta directamente.
"""

from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"

# Solo las funciones con permiso propio ven la tabla completa.
_INTERNA = "session_user <> current_user"

_CATALOGOS = ("roles", "permisos", "rol_permiso")
_TABLAS = (*_CATALOGOS, "usuarios", "medicos", "pacientes", "consultorio", "bitacora")


def _forzar_permisos_por_fila(tabla: str) -> None:
    op.execute(f"ALTER TABLE {tabla} ENABLE ROW LEVEL SECURITY")
    op.execute(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY")


def _politica_interna(tabla: str) -> None:
    op.execute(
        f"CREATE POLICY interna ON {tabla} TO CURRENT_USER "
        f"USING ({_INTERNA}) WITH CHECK ({_INTERNA})"
    )


def upgrade() -> None:
    op.execute(
        """
        CREATE FUNCTION identidad() RETURNS text LANGUAGE sql STABLE
        AS $$ SELECT nullif(current_setting('vitalia.identidad', true), '') $$
        """
    )
    op.execute(
        """
        CREATE FUNCTION usuario_actual() RETURNS uuid LANGUAGE sql STABLE
        AS $$ SELECT nullif(current_setting('vitalia.usuario', true), '')::uuid $$
        """
    )

    # --- Roles y matriz de permisos (HU-006). Lo que no está en rol_permiso queda denegado.
    op.execute("CREATE TABLE roles (codigo text PRIMARY KEY, nombre text NOT NULL)")
    op.execute("CREATE TABLE permisos (codigo text PRIMARY KEY, descripcion text NOT NULL)")
    op.execute(
        """
        CREATE TABLE rol_permiso (
            rol text NOT NULL REFERENCES roles,
            permiso text NOT NULL REFERENCES permisos,
            PRIMARY KEY (rol, permiso)
        )
        """
    )
    op.execute("INSERT INTO roles VALUES ('medico', 'Médico'), ('paciente', 'Paciente')")
    op.execute(
        """
        INSERT INTO permisos VALUES
            ('cuenta.ver', 'Ver mi usuario y mi rol'),
            ('sesion.cerrar', 'Cerrar mi sesión'),
            ('consultorio.ver', 'Ver los datos del consultorio'),
            ('consultorio.editar', 'Editar los datos del consultorio y del médico')
        """
    )
    op.execute(
        """
        INSERT INTO rol_permiso VALUES
            ('medico', 'cuenta.ver'), ('paciente', 'cuenta.ver'),
            ('medico', 'sesion.cerrar'), ('paciente', 'sesion.cerrar'),
            ('medico', 'consultorio.ver'), ('paciente', 'consultorio.ver'),
            ('medico', 'consultorio.editar')
        """
    )

    # --- Cuentas
    op.execute(
        """
        CREATE TABLE usuarios (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            tipo_documento text NOT NULL CHECK (tipo_documento IN ('CC', 'CE', 'PA', 'PT')),
            numero_documento text NOT NULL,
            correo text,
            hash_contrasena text,
            rol text NOT NULL REFERENCES roles,
            activo boolean NOT NULL DEFAULT true,
            creado_en timestamptz NOT NULL DEFAULT now(),
            UNIQUE (tipo_documento, numero_documento)
        )
        """
    )
    op.execute(
        """
        CREATE TABLE medicos (
            usuario_id uuid PRIMARY KEY REFERENCES usuarios,
            nombres text NOT NULL,
            apellidos text NOT NULL,
            registro_profesional text
        )
        """
    )
    op.execute(
        """
        CREATE TABLE pacientes (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            usuario_id uuid NOT NULL UNIQUE REFERENCES usuarios,
            nombres text NOT NULL,
            apellidos text NOT NULL,
            fecha_nacimiento date NOT NULL,
            telefono text NOT NULL,
            registrado_por uuid REFERENCES usuarios
        )
        """
    )
    op.execute(
        """
        CREATE TABLE consultorio (
            unico boolean PRIMARY KEY DEFAULT true CHECK (unico),
            nombre text,
            direccion text,
            telefono text,
            correo text,
            anticipacion_horas integer NOT NULL DEFAULT 24 CHECK (anticipacion_horas >= 0),
            margen_agenda_minutos integer NOT NULL DEFAULT 60 CHECK (margen_agenda_minutos >= 0)
        )
        """
    )
    op.execute("INSERT INTO consultorio DEFAULT VALUES")

    # --- Bitácora (HU-037): solo inserción
    op.execute(
        """
        CREATE TABLE bitacora (
            id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            fecha timestamptz NOT NULL DEFAULT now(),
            usuario_id uuid REFERENCES usuarios,
            rol text,
            paciente_id uuid REFERENCES pacientes,
            accion text NOT NULL,
            objeto text,
            detalle jsonb
        )
        """
    )
    op.execute("CREATE INDEX bitacora_por_paciente ON bitacora (paciente_id, fecha)")
    op.execute(
        """
        CREATE FUNCTION bitacora_no_cambia() RETURNS trigger LANGUAGE plpgsql
        AS $$
        BEGIN
            RAISE EXCEPTION 'La bitácora solo admite inserciones'
                USING ERRCODE = 'restrict_violation';
        END
        $$
        """
    )
    op.execute(
        """
        CREATE TRIGGER solo_insercion BEFORE UPDATE OR DELETE ON bitacora
        FOR EACH ROW EXECUTE FUNCTION bitacora_no_cambia()
        """
    )
    op.execute(
        """
        CREATE TRIGGER sin_vaciar BEFORE TRUNCATE ON bitacora
        FOR EACH STATEMENT EXECUTE FUNCTION bitacora_no_cambia()
        """
    )

    # --- Permisos por fila (HU-036): matriz de la sección 3.3 del modelo de datos
    for tabla in _TABLAS:
        _forzar_permisos_por_fila(tabla)
        _politica_interna(tabla)

    for tabla in _CATALOGOS:
        op.execute(f"GRANT SELECT ON {tabla} TO vitalia_api")
        op.execute(
            f"CREATE POLICY lectura ON {tabla} FOR SELECT TO vitalia_api "
            "USING (identidad() IS NOT NULL)"
        )

    # La contraseña nunca se lee desde la aplicación: solo dentro de buscar_credencial.
    op.execute(
        """
        GRANT SELECT (id, tipo_documento, numero_documento, correo, rol, activo, creado_en)
        ON usuarios TO vitalia_api
        """
    )
    op.execute(
        "CREATE POLICY propia ON usuarios FOR SELECT TO vitalia_api "
        "USING (identidad() IN ('paciente', 'medico') AND id = usuario_actual())"
    )
    op.execute(
        "CREATE POLICY medico_lee ON usuarios FOR SELECT TO vitalia_api "
        "USING (identidad() = 'medico')"
    )

    op.execute("GRANT SELECT ON pacientes TO vitalia_api")
    op.execute(
        "CREATE POLICY propia ON pacientes FOR SELECT TO vitalia_api "
        "USING (identidad() = 'paciente' AND usuario_id = usuario_actual())"
    )
    op.execute(
        "CREATE POLICY medico_lee ON pacientes FOR SELECT TO vitalia_api "
        "USING (identidad() = 'medico')"
    )

    op.execute("GRANT SELECT ON medicos TO vitalia_api")
    op.execute("GRANT UPDATE (nombres, apellidos, registro_profesional) ON medicos TO vitalia_api")
    op.execute(
        "CREATE POLICY lectura ON medicos FOR SELECT TO vitalia_api "
        "USING (identidad() IN ('paciente', 'medico'))"
    )
    op.execute(
        "CREATE POLICY medico_edita ON medicos FOR UPDATE TO vitalia_api "
        "USING (identidad() = 'medico' AND usuario_id = usuario_actual()) "
        "WITH CHECK (identidad() = 'medico' AND usuario_id = usuario_actual())"
    )

    op.execute("GRANT SELECT ON consultorio TO vitalia_api")
    op.execute(
        """
        GRANT UPDATE (
            nombre, direccion, telefono, correo, anticipacion_horas, margen_agenda_minutos
        ) ON consultorio TO vitalia_api
        """
    )
    op.execute(
        "CREATE POLICY lectura ON consultorio FOR SELECT TO vitalia_api "
        "USING (identidad() IN ('paciente', 'medico'))"
    )
    op.execute(
        "CREATE POLICY medico_edita ON consultorio FOR UPDATE TO vitalia_api "
        "USING (identidad() = 'medico') WITH CHECK (identidad() = 'medico')"
    )

    # Cada quien inserta a su propio nombre; solo el médico lee. Nadie modifica ni borra.
    op.execute("GRANT SELECT, INSERT ON bitacora TO vitalia_api")
    op.execute(
        """
        CREATE POLICY inserta ON bitacora FOR INSERT TO vitalia_api
        WITH CHECK (
            identidad() IS NOT NULL
            AND rol IS NOT DISTINCT FROM identidad()
            AND usuario_id IS NOT DISTINCT FROM usuario_actual()
        )
        """
    )
    op.execute(
        "CREATE POLICY medico_lee ON bitacora FOR SELECT TO vitalia_api "
        "USING (identidad() = 'medico')"
    )


def downgrade() -> None:
    for tabla in reversed(_TABLAS):
        op.execute(f"DROP TABLE {tabla}")
    op.execute("DROP FUNCTION bitacora_no_cambia()")
    op.execute("DROP FUNCTION usuario_actual()")
    op.execute("DROP FUNCTION identidad()")
