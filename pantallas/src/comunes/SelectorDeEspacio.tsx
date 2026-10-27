import "./SelectorDeEspacio.css";

import { useQuery } from "@tanstack/react-query";
import { useState } from "react";

import { ErrorDeApi } from "../api/cliente";
import { disponibilidad } from "../api/citas";
import { deDia, diaDeLaSemana, diaDelMes, esManana, fechaLarga, hora } from "./fechas";
import { InfoIcon } from "./iconos";
import { Nota } from "./piezas/Nota";

type Propiedades = {
  tipo: string;
  elegido: string | null;
  alElegir: (inicio: string) => void;
  /** Al mover una cita, su propio espacio cuenta como libre. */
  cita?: string;
  /** El día con que abre, "2026-10-14"; por ejemplo, el que se eligió en el calendario. */
  diaInicial?: string | null;
};

/** Elegir día y hora: solo aparecen los días y las horas disponibles (HU-012, CA-5). */
export function SelectorDeEspacio({ tipo, elegido, alElegir, cita, diaInicial }: Propiedades) {
  const [dia, setDia] = useState<string | null>(diaInicial ?? null);
  const consulta = useQuery({
    queryKey: ["disponibilidad", tipo, dia, cita],
    queryFn: () => disponibilidad(tipo, dia, cita),
  });

  if (consulta.isError) {
    const error = consulta.error;
    return (
      <Nota tono="rojo">
        {error instanceof ErrorDeApi ? error.message : "No se pudo consultar la agenda."}
      </Nota>
    );
  }
  if (!consulta.data) return <p className="texto-suave">Buscando espacios…</p>;

  const { dias, dia: diaMostrado, horas } = consulta.data;
  if (!dias.length) {
    return (
      <Nota>No hay espacios libres en las próximas semanas. Comuníquese con el consultorio.</Nota>
    );
  }
  const porFranja: [string, string[]][] = [
    ["Mañana", horas.filter(esManana)],
    ["Tarde", horas.filter((h) => !esManana(h))],
  ];

  return (
    <div className="selector-de-espacio">
      <section className="selector-de-espacio__grupo">
        <h2>Elija el día</h2>
        <div className="selector-de-espacio__dias" role="group" aria-label="Días disponibles">
          {dias.map((d) => (
            <button
              key={d}
              type="button"
              aria-pressed={d === diaMostrado}
              aria-label={fechaLarga(deDia(d))}
              className="selector-de-espacio__dia"
              onClick={() => setDia(d)}
            >
              <span>{diaDeLaSemana(deDia(d))}</span>
              <span className="selector-de-espacio__numero">{diaDelMes(deDia(d))}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="selector-de-espacio__grupo">
        <div className="selector-de-espacio__titulo">
          <h2>Horas disponibles</h2>
          {diaMostrado && <span className="texto-suave">{fechaLarga(deDia(diaMostrado))}</span>}
        </div>
        {porFranja.map(([nombre, lista]) =>
          lista.length ? (
            <div key={nombre} className="selector-de-espacio__franja">
              <span className="selector-de-espacio__rotulo">{nombre}</span>
              <div
                className="selector-de-espacio__horas"
                role="group"
                aria-label={`Horas de la ${nombre.toLowerCase()}`}
              >
                {lista.map((h) => (
                  <button
                    key={h}
                    type="button"
                    aria-pressed={h === elegido}
                    className="selector-de-espacio__hora"
                    onClick={() => alElegir(h)}
                  >
                    {hora(h)}
                  </button>
                ))}
              </div>
            </div>
          ) : null,
        )}
        <p className="selector-de-espacio__aviso texto-suave">
          <InfoIcon aria-hidden="true" />
          Solo aparecen los días y las horas disponibles.
        </p>
      </section>
    </div>
  );
}
