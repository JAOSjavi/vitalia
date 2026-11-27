import { useState } from "react";

// Tema claro u oscuro (D-34). "sistema" sigue al dispositivo. Se guarda en este navegador: es
// una preferencia de pantalla, no un dato de la cuenta. index.html lo aplica antes de pintar.
export type Tema = "sistema" | "claro" | "oscuro";

const CLAVE = "vitalia.tema";

export function temaGuardado(): Tema {
  try {
    const guardado = localStorage.getItem(CLAVE);
    return guardado === "claro" || guardado === "oscuro" ? guardado : "sistema";
  } catch {
    return "sistema";
  }
}

function aplicar(tema: Tema) {
  const raiz = document.documentElement;
  const cambiar = () => {
    if (tema === "sistema") delete raiz.dataset.tema;
    else raiz.dataset.tema = tema;
  };
  // El cambio de claro a oscuro se funde en lugar de saltar, salvo con movimiento reducido.
  const sinMovimiento = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (document.startViewTransition && !sinMovimiento) document.startViewTransition(cambiar);
  else cambiar();
}

export function useTema(): [Tema, (tema: Tema) => void] {
  const [tema, setTema] = useState<Tema>(temaGuardado);
  function cambiar(nuevo: Tema) {
    setTema(nuevo);
    aplicar(nuevo);
    try {
      if (nuevo === "sistema") localStorage.removeItem(CLAVE);
      else localStorage.setItem(CLAVE, nuevo);
    } catch {
      // Sin almacenamiento (ventana privada): el tema vale hasta cerrar la pestaña.
    }
  }
  return [tema, cambiar];
}
