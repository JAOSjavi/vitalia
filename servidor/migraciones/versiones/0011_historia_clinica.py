"""Historia clínica del consultorio (E9: HU-041 a HU-045).

Medicina general, con el contenido mínimo de la Resolución 1995 de 1999 y los datos de la 866 de
2021 (planificacion/03-marco-normativo.md, sección 4). Lo que pide la norma y de dónde sale cada
campo está en diseno/10-historia-clinica.md.

- Los datos de identificación que el registro no pide se agregan a pacientes y los llena el médico.
- Una atención abierta es el borrador. Al cerrarla queda firmada y ya no cambia: lo impide un
  disparador, y el usuario de la API no tiene permiso de borrar. Se corrige con notas aclaratorias.
- Los diagnósticos y la fórmula van dentro de la atención como listas (jsonb): se guardan y se
  congelan con ella.
- El paciente solo lee sus atenciones cerradas y sus notas.
"""

import csv
from pathlib import Path

from alembic import op

revision: str = "0011"
down_revision: str | None = "0010"

_INTERNA = "session_user <> current_user"
_TABLAS = ("atenciones", "notas_aclaratorias", "cie10")

_PERMISOS = {
    "atenciones.ver": ("Ver la historia clínica de un paciente", ("medico",)),
    "atenciones.registrar": ("Abrir, escribir y cerrar una atención", ("medico",)),
    "pacientes.identificacion": ("Completar los datos de identificación", ("medico",)),
    "historia.propia": ("Ver su propia historia clínica", ("paciente",)),
}

# Datos de identificación que pide el artículo 9 de la Resolución 1995 y la 866 (HU-041).
_IDENTIFICACION = (
    "sexo text CHECK (sexo IN ('H', 'M', 'I'))",
    "estado_civil text CHECK (estado_civil IN "
    "('soltero', 'casado', 'union_libre', 'separado', 'divorciado', 'viudo'))",
    "ocupacion text CHECK (length(ocupacion) <= 120)",
    "nivel_escolar text CHECK (nivel_escolar IN ('ninguno', 'primaria', 'secundaria', "
    "'tecnica', 'tecnologica', 'universitaria', 'posgrado'))",
    "pertenencia_etnica text CHECK (pertenencia_etnica IN "
    "('indigena', 'rom', 'raizal', 'palenquero', 'afrocolombiano', 'ninguna'))",
    "direccion text CHECK (length(direccion) <= 200)",
    "municipio text CHECK (length(municipio) <= 120)",
    "zona text CHECK (zona IN ('urbana', 'rural'))",
    "aseguradora text CHECK (length(aseguradora) <= 120)",
    "tipo_vinculacion text CHECK (tipo_vinculacion IN "
    "('contributivo', 'subsidiado', 'especial', 'particular'))",
    "responsable_nombre text CHECK (length(responsable_nombre) <= 120)",
    "responsable_telefono text CHECK (length(responsable_telefono) <= 30)",
    "responsable_parentesco text CHECK (length(responsable_parentesco) <= 60)",
)


def _forzar(tabla: str) -> None:
    op.execute(f"ALTER TABLE {tabla} ENABLE ROW LEVEL SECURITY")
    op.execute(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY")
    op.execute(
        f"CREATE POLICY interna ON {tabla} TO CURRENT_USER "
        f"USING ({_INTERNA}) WITH CHECK ({_INTERNA})"
    )


def _sin_forzar(tablas: tuple[str, ...], ordenes: list[str]) -> None:
    """Los catálogos tienen permisos forzados: el dueño los quita un momento para escribir."""
    for tabla in tablas:
        op.execute(f"ALTER TABLE {tabla} NO FORCE ROW LEVEL SECURITY")
    for orden in ordenes:
        op.execute(orden)
    for tabla in tablas:
        op.execute(f"ALTER TABLE {tabla} FORCE ROW LEVEL SECURITY")


def _texto(valor: str) -> str:
    return "'" + valor.replace("'", "''") + "'"


def upgrade() -> None:
    # --- Identificación (HU-041). Se llena una vez y la puede corregir el médico.
    for columna in _IDENTIFICACION:
        op.execute(f"ALTER TABLE pacientes ADD COLUMN {columna}")
    nombres = ", ".join(c.split(" ")[0] for c in _IDENTIFICACION)
    op.execute(f"GRANT UPDATE ({nombres}) ON pacientes TO vitalia_api")
    op.execute(
        "CREATE POLICY medico_identifica ON pacientes FOR UPDATE TO vitalia_api "
        "USING (identidad() = 'medico') WITH CHECK (identidad() = 'medico')"
    )

    # --- Catálogo CIE-10 (HU-043, CA-2).
    op.execute("CREATE TABLE cie10 (codigo text PRIMARY KEY, nombre text NOT NULL)")

    # --- Atenciones (HU-042 a HU-044).
    op.execute(
        """
        CREATE TABLE atenciones (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            paciente_id uuid NOT NULL REFERENCES pacientes,
            medico_id uuid NOT NULL REFERENCES usuarios,
            cita_id uuid REFERENCES citas,
            estado text NOT NULL DEFAULT 'abierta' CHECK (estado IN ('abierta', 'cerrada')),
            inicio timestamptz NOT NULL DEFAULT now(),
            fin timestamptz,
            guardada_en timestamptz NOT NULL DEFAULT now(),

            tipo_consulta text CHECK (tipo_consulta IN ('primera_vez', 'control')),
            finalidad text CHECK (finalidad IN
                ('diagnostico', 'tratamiento', 'promocion_prevencion', 'rehabilitacion')),
            causa text CHECK (causa IN ('enfermedad_general', 'enfermedad_laboral',
                'accidente_trabajo', 'accidente_transito', 'otro_accidente',
                'lesion_por_agresion', 'otra')),
            acompanante_nombre text,
            acompanante_telefono text,
            acompanante_parentesco text,

            motivo text,
            enfermedad_actual text,
            antecedentes_personales text,
            antecedentes_familiares text,
            alergias text,
            factores_riesgo text,
            revision_sistemas text,
            sintomatico_respiratorio boolean,
            sintomatico_piel boolean,

            tension_sistolica integer CHECK (tension_sistolica BETWEEN 50 AND 260),
            tension_diastolica integer CHECK (tension_diastolica BETWEEN 30 AND 160),
            frecuencia_cardiaca integer CHECK (frecuencia_cardiaca BETWEEN 20 AND 250),
            frecuencia_respiratoria integer CHECK (frecuencia_respiratoria BETWEEN 5 AND 60),
            temperatura numeric(3, 1) CHECK (temperatura BETWEEN 30 AND 45),
            saturacion integer CHECK (saturacion BETWEEN 50 AND 100),
            peso numeric(4, 1) CHECK (peso BETWEEN 1 AND 350),
            talla integer CHECK (talla BETWEEN 30 AND 250),
            examen_fisico text,

            diagnosticos jsonb NOT NULL DEFAULT '[]' CHECK (jsonb_typeof(diagnosticos) = 'array'),
            analisis text,
            plan text,
            recomendaciones text,
            medicamentos jsonb NOT NULL DEFAULT '[]' CHECK (jsonb_typeof(medicamentos) = 'array'),
            ordenes text,
            incapacidad_dias integer CHECK (incapacidad_dias BETWEEN 0 AND 180),
            destino text CHECK (destino IN ('casa', 'remitido')),
            remitido_a text,

            firma_nombre text,
            firma_registro text,
            firma_documento text,
            CHECK (estado = 'abierta' OR (fin IS NOT NULL AND firma_nombre IS NOT NULL))
        )
        """
    )
    # Una sola atención abierta por paciente (HU-042, CA-6).
    op.execute(
        "CREATE UNIQUE INDEX una_abierta_por_paciente ON atenciones (paciente_id) "
        "WHERE estado = 'abierta'"
    )
    op.execute("CREATE INDEX atenciones_por_paciente ON atenciones (paciente_id, inicio)")

    op.execute(
        """
        CREATE TABLE notas_aclaratorias (
            id uuid PRIMARY KEY DEFAULT uuidv7(),
            atencion_id uuid NOT NULL REFERENCES atenciones,
            medico_id uuid NOT NULL REFERENCES usuarios,
            texto text NOT NULL CHECK (length(texto) BETWEEN 1 AND 4000),
            fecha timestamptz NOT NULL DEFAULT now(),
            firma_nombre text NOT NULL,
            firma_registro text
        )
        """
    )
    op.execute("CREATE INDEX notas_por_atencion ON notas_aclaratorias (atencion_id, fecha)")

    # Lo cerrado no cambia (Resolución 1995, art. 18; HU-044, CA-3). Ni siquiera el dueño.
    op.execute(
        """
        CREATE FUNCTION atencion_cerrada_no_cambia() RETURNS trigger LANGUAGE plpgsql
        AS $$
        BEGIN
            IF OLD.estado = 'cerrada' THEN
                RAISE EXCEPTION 'Una atención cerrada no se modifica ni se borra'
                    USING ERRCODE = 'integrity_constraint_violation';
            END IF;
            RETURN CASE WHEN TG_OP = 'DELETE' THEN OLD ELSE NEW END;
        END
        $$
        """
    )
    op.execute(
        "CREATE TRIGGER atencion_cerrada_no_cambia BEFORE UPDATE OR DELETE ON atenciones "
        "FOR EACH ROW EXECUTE FUNCTION atencion_cerrada_no_cambia()"
    )
    op.execute(
        """
        CREATE FUNCTION nota_no_cambia() RETURNS trigger LANGUAGE plpgsql
        AS $$
        BEGIN
            RAISE EXCEPTION 'Una nota aclaratoria no se modifica ni se borra'
                USING ERRCODE = 'integrity_constraint_violation';
        END
        $$
        """
    )
    op.execute(
        "CREATE TRIGGER nota_no_cambia BEFORE UPDATE OR DELETE ON notas_aclaratorias "
        "FOR EACH ROW EXECUTE FUNCTION nota_no_cambia()"
    )

    # Para firmar, el médico confirma su contraseña. La API no puede leer la columna del hash:
    # esta función le entrega solo la del médico que tiene la sesión.
    op.execute(
        """
        CREATE FUNCTION hash_del_medico_actual() RETURNS text
        LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public, pg_temp
        AS $$
            SELECT hash_contrasena FROM usuarios
            WHERE id = usuario_actual() AND identidad() = 'medico' AND rol = 'medico' AND activo
        $$
        """
    )
    op.execute("REVOKE ALL ON FUNCTION hash_del_medico_actual() FROM PUBLIC")
    op.execute("GRANT EXECUTE ON FUNCTION hash_del_medico_actual() TO vitalia_api")

    for tabla in _TABLAS:
        _forzar(tabla)

    # --- Atenciones: el médico las abre, las escribe mientras están abiertas y las cierra.
    # El paciente lee solo las suyas cerradas.
    op.execute("GRANT SELECT, INSERT, UPDATE ON atenciones TO vitalia_api")
    op.execute(
        "CREATE POLICY medico_lee ON atenciones FOR SELECT TO vitalia_api "
        "USING (identidad() = 'medico')"
    )
    op.execute(
        "CREATE POLICY medico_abre ON atenciones FOR INSERT TO vitalia_api "
        "WITH CHECK (identidad() = 'medico' AND medico_id = usuario_actual() "
        "AND estado = 'abierta')"
    )
    op.execute(
        "CREATE POLICY medico_escribe ON atenciones FOR UPDATE TO vitalia_api "
        "USING (identidad() = 'medico' AND estado = 'abierta') "
        "WITH CHECK (identidad() = 'medico')"
    )
    op.execute(
        "CREATE POLICY propias_cerradas ON atenciones FOR SELECT TO vitalia_api "
        "USING (identidad() = 'paciente' AND paciente_id = paciente_actual() "
        "AND estado = 'cerrada')"
    )

    # --- Notas aclaratorias: solo se agregan, a una atención cerrada.
    op.execute("GRANT SELECT, INSERT ON notas_aclaratorias TO vitalia_api")
    op.execute(
        "CREATE POLICY medico_lee ON notas_aclaratorias FOR SELECT TO vitalia_api "
        "USING (identidad() = 'medico')"
    )
    op.execute(
        "CREATE POLICY medico_agrega ON notas_aclaratorias FOR INSERT TO vitalia_api "
        "WITH CHECK (identidad() = 'medico' AND medico_id = usuario_actual() "
        "AND atencion_id IN (SELECT id FROM atenciones WHERE estado = 'cerrada'))"
    )
    op.execute(
        "CREATE POLICY propias ON notas_aclaratorias FOR SELECT TO vitalia_api "
        "USING (identidad() = 'paciente' AND atencion_id IN "
        "(SELECT id FROM atenciones WHERE paciente_id = paciente_actual()))"
    )

    # --- CIE-10: lo leen los dos; lo carga el dueño de las tablas.
    op.execute("GRANT SELECT ON cie10 TO vitalia_api")
    op.execute(
        "CREATE POLICY lectura ON cie10 FOR SELECT TO vitalia_api "
        "USING (identidad() IN ('medico', 'paciente'))"
    )
    # Diagnósticos frecuentes en medicina general. La tabla oficial completa se carga con
    # guiones/cargar_cie10.py cuando se descargue de SISPRO.
    with (Path(__file__).parent.parent / "textos" / "cie10-frecuentes.csv").open(
        encoding="utf-8"
    ) as archivo:
        cie10 = [(f["codigo"], f["nombre"]) for f in csv.DictReader(archivo)]
    filas = ", ".join(f"({_texto(codigo)}, {_texto(nombre)})" for codigo, nombre in cie10)
    _sin_forzar(("cie10",), [f"INSERT INTO cie10 (codigo, nombre) VALUES {filas}"])

    ordenes = []
    for codigo, (descripcion, roles) in _PERMISOS.items():
        ordenes.append(f"INSERT INTO permisos VALUES ('{codigo}', '{descripcion}')")
        ordenes += [f"INSERT INTO rol_permiso VALUES ('{rol}', '{codigo}')" for rol in roles]
    _sin_forzar(("permisos", "rol_permiso"), ordenes)


def downgrade() -> None:
    codigos = ", ".join(f"'{codigo}'" for codigo in _PERMISOS)
    _sin_forzar(
        ("permisos", "rol_permiso"),
        [
            f"DELETE FROM rol_permiso WHERE permiso IN ({codigos})",
            f"DELETE FROM permisos WHERE codigo IN ({codigos})",
        ],
    )
    op.execute("DROP TABLE notas_aclaratorias")
    op.execute("DROP TABLE atenciones")
    op.execute("DROP FUNCTION nota_no_cambia()")
    op.execute("DROP FUNCTION atencion_cerrada_no_cambia()")
    op.execute("DROP FUNCTION hash_del_medico_actual()")
    op.execute("DROP TABLE cie10")
    op.execute("DROP POLICY medico_identifica ON pacientes")
    nombres = ", ".join(c.split(" ")[0] for c in _IDENTIFICACION)
    op.execute(f"REVOKE UPDATE ({nombres}) ON pacientes FROM vitalia_api")
    for columna in _IDENTIFICACION:
        op.execute(f"ALTER TABLE pacientes DROP COLUMN {columna.split(' ')[0]}")
