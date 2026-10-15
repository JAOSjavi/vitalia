import "./Marca.css";

type Propiedades = { tamano?: "grande" | "pequena"; conNombre?: boolean };

/** El sello de Vitalia. Grande en el ingreso, pequeño en los menús. */
export function Marca({ tamano = "pequena", conNombre = false }: Propiedades) {
  return (
    <span className={`marca marca--${tamano}`}>
      <span className="marca__sello" aria-hidden="true">
        V
      </span>
      {conNombre && <span className="marca__nombre">Vitalia</span>}
    </span>
  );
}
