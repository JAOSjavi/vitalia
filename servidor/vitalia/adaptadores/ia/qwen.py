"""Qwen en Alibaba Cloud Model Studio, región Singapur (diseno/04-asistente-ia.md).

El proveedor usa el mismo formato que la API de OpenAI, así que se le habla por HTTP directo,
sin su biblioteca. La clave nunca se escribe en el registro ni en un mensaje de error.
"""

from collections.abc import Sequence

import httpx

# El proveedor acepta hasta 10 textos por petición de vectores.
_TEXTOS_POR_PETICION = 10
_SEGUNDOS = 60


class ErrorDelProveedor(Exception):
    """El proveedor respondió con error. Lleva el estado y el código, nunca la clave."""

    def __init__(self, estado: int, codigo: str) -> None:
        super().__init__(f"El proveedor de IA respondió {estado} {codigo}")
        self.estado = estado
        self.codigo = codigo


class VectoresQwen:
    def __init__(self, direccion: str, clave: str, modelo: str, dimensiones: int) -> None:
        self._direccion = direccion.rstrip("/")
        self._clave = clave
        self._modelo = modelo
        self._dimensiones = dimensiones

    @property
    def modelo(self) -> str:
        return self._modelo

    async def vectorizar(self, textos: Sequence[str]) -> list[list[float]]:
        vectores: list[list[float]] = []
        async with httpx.AsyncClient(timeout=_SEGUNDOS) as cliente:
            for inicio in range(0, len(textos), _TEXTOS_POR_PETICION):
                grupo = list(textos[inicio : inicio + _TEXTOS_POR_PETICION])
                respuesta = await cliente.post(
                    f"{self._direccion}/embeddings",
                    headers={"Authorization": f"Bearer {self._clave}"},
                    json={
                        "model": self._modelo,
                        "input": grupo,
                        "dimensions": self._dimensiones,
                        "encoding_format": "float",
                    },
                )
                _revisar(respuesta)
                datos = sorted(respuesta.json()["data"], key=lambda d: d["index"])
                vectores += [d["embedding"] for d in datos]
        return vectores


def _revisar(respuesta: httpx.Response) -> None:
    if respuesta.is_success:
        return
    try:
        codigo = str(respuesta.json().get("error", {}).get("code", "desconocido"))
    except ValueError:
        codigo = "desconocido"
    raise ErrorDelProveedor(respuesta.status_code, codigo)
