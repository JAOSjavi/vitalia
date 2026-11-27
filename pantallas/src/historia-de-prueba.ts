// Datos inventados de la historia clínica para las pruebas de pantallas.

export const FORMULARIO = {
  atencion: {
    tipo_consulta: campo("Tipo de consulta", "opcion", true, "tipo_consulta"),
    finalidad: campo("Finalidad", "opcion", true, "finalidad"),
    causa: campo("Causa que motiva la atención", "opcion", true, "causa"),
    acompanante_nombre: campo("Acompañante"),
    acompanante_telefono: campo("Teléfono del acompañante"),
    acompanante_parentesco: campo("Parentesco del acompañante"),
    motivo: campo("Motivo de consulta", "texto", true),
    enfermedad_actual: campo("Enfermedad actual", "texto", true),
    antecedentes_personales: campo("Antecedentes personales", "texto", true),
    antecedentes_familiares: campo("Antecedentes familiares", "texto", true),
    alergias: campo("Alergias", "texto", true),
    factores_riesgo: campo("Factores de riesgo", "texto", true),
    revision_sistemas: campo("Revisión por sistemas", "texto", true),
    sintomatico_respiratorio: campo("Sintomático respiratorio", "si_no"),
    sintomatico_piel: campo("Sintomático de piel", "si_no"),
    tension_sistolica: campo("Tensión arterial sistólica", "entero", true, null, "mmHg"),
    tension_diastolica: campo("Tensión arterial diastólica", "entero", true, null, "mmHg"),
    frecuencia_cardiaca: campo("Frecuencia cardiaca", "entero", true, null, "lat/min"),
    frecuencia_respiratoria: campo("Frecuencia respiratoria", "entero", true, null, "resp/min"),
    temperatura: campo("Temperatura", "decimal", true, null, "°C"),
    saturacion: campo("Saturación de oxígeno", "entero", false, null, "%"),
    peso: campo("Peso", "decimal", true, null, "kg"),
    talla: campo("Talla", "entero", true, null, "cm"),
    examen_fisico: campo("Examen físico", "texto", true),
    analisis: campo("Análisis"),
    plan: campo("Plan de manejo", "texto", true),
    recomendaciones: campo("Recomendaciones y signos de alarma"),
    ordenes: campo("Órdenes de exámenes o procedimientos"),
    incapacidad_dias: campo("Incapacidad", "entero", false, null, "días"),
    destino: campo("Cómo termina la atención", "opcion", true, "destino"),
    remitido_a: campo("Remitido a"),
  },
  identificacion: {
    sexo: campo("Sexo", "opcion", true, "sexo"),
    ocupacion: campo("Ocupación", "texto", true),
  },
  listas: {
    sexo: { H: "Hombre", M: "Mujer" },
    tipo_consulta: { primera_vez: "Primera vez", control: "Control" },
    finalidad: { tratamiento: "Tratamiento" },
    causa: { enfermedad_general: "Enfermedad general" },
    tipo_diagnostico: {
      impresion_diagnostica: "Impresión diagnóstica",
      confirmado_repetido: "Confirmado repetido",
    },
    destino: { casa: "A casa", remitido: "Remitido a otro prestador" },
    via: { oral: "Oral" },
  },
};

function campo(
  nombre: string,
  clase = "texto",
  obligatorio = false,
  lista: string | null = null,
  unidad: string | null = null,
) {
  return { nombre, clase, obligatorio, lista, minimo: null, maximo: null, unidad, largo: 4000 };
}

export function atencion(cambios: object = {}) {
  return {
    id: "a1",
    paciente_id: "p1",
    cita_id: null,
    estado: "cerrada",
    inicio: "2026-08-20T14:00:00Z",
    fin: "2026-08-20T14:25:00Z",
    guardada_en: "2026-08-20T14:25:00Z",
    datos: {
      tipo_consulta: "control",
      motivo: "Control de hipertensión arterial.",
      temperatura: 36.5,
      tension_sistolica: 128,
      tension_diastolica: 82,
      destino: "casa",
    },
    diagnosticos: [
      {
        codigo: "I10X",
        nombre: "Hipertensión esencial (primaria)",
        tipo: "confirmado_repetido",
        principal: true,
      },
    ],
    medicamentos: [
      {
        nombre: "Losartán 50 mg",
        dosis: "1 tableta",
        via: "oral",
        frecuencia: "cada 12 horas",
        dias: 90,
        indicaciones: null,
      },
    ],
    imc: 25.5,
    firma: { nombre: "Camila Ríos", registro: "RM 79-4521", documento: "CC 52345678" },
    notas: [],
    ...cambios,
  };
}
