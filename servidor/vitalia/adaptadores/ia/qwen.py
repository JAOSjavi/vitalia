"""Qwen en Alibaba Cloud Model Studio, región Singapur (diseno/04-asistente-ia.md).

El proveedor usa el mismo formato que la API de OpenAI, así que se le habla por HTTP directo,
sin su biblioteca. La clave nunca se escribe en el registro ni en un mensaje de error.
"""

import base64
import json
from collections.abc import AsyncIterator, Sequence

import httpx

from vitalia.casos_de_uso.puertos import ProveedorNoDisponible, Turno

# El proveedor acepta hasta 10 textos por petición de vectores.
_TEXTOS_POR_PETICION = 10
_SEGUNDOS = 60

_LEER = (
    "Transcribe todo el texto de esta imagen tal como aparece, respetando las líneas. "
    "Si una palabra no se lee, escribe [ilegible]. No agregues nada."
)


class ErrorDelProveedor(ProveedorNoDisponible):
    """El proveedor respondió con error. Lleva el estado y el código, nunca la clave."""

    def __init__(self, estado: int, codigo: str) -> None:
        super().__init__(f"El proveedor de IA respondió {estado} {codigo}")
        self.estado = estado
        self.codigo = codigo


class _Conexion:
    def __init__(self, direccion: str, clave: str) -> None:
        self.direccion = direccion.rstrip("/")
        self.encabezados = {"Authorization": f"Bearer {clave}"}

    def cliente(self, transporte: httpx.AsyncBaseTransport | None) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=_SEGUNDOS, transport=transporte)


class VectoresQwen:
    def __init__(
        self,
        direccion: str,
        clave: str,
        modelo: str,
        dimensiones: int,
        transporte: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._conexion = _Conexion(direccion, clave)
        self._modelo = modelo
        self._dimensiones = dimensiones
        self._transporte = transporte

    @property
    def modelo(self) -> str:
        return self._modelo

    async def vectorizar(self, textos: Sequence[str]) -> list[list[float]]:
        vectores: list[list[float]] = []
        try:
            async with self._conexion.cliente(self._transporte) as cliente:
                for inicio in range(0, len(textos), _TEXTOS_POR_PETICION):
                    respuesta = await cliente.post(
                        f"{self._conexion.direccion}/embeddings",
                        headers=self._conexion.encabezados,
                        json={
                            "model": self._modelo,
                            "input": list(textos[inicio : inicio + _TEXTOS_POR_PETICION]),
                            "dimensions": self._dimensiones,
                            "encoding_format": "float",
                        },
                    )
                    _revisar(respuesta)
                    datos = sorted(respuesta.json()["data"], key=lambda d: d["index"])
                    vectores += [d["embedding"] for d in datos]
        except httpx.HTTPError as error:
            raise ProveedorNoDisponible(type(error).__name__) from error
        return vectores


class IAQwen:
    """Leer páginas con el modelo de lectura y responder con el de respuestas."""

    def __init__(
        self,
        direccion: str,
        clave: str,
        modelo_respuestas: str,
        modelo_lectura: str,
        transporte: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._conexion = _Conexion(direccion, clave)
        self._modelo_respuestas = modelo_respuestas
        self._modelo_lectura = modelo_lectura
        self._transporte = transporte

    async def leer_pagina(self, imagen: bytes) -> str:
        tipo = "image/png" if imagen.startswith(b"\x89PNG") else "image/jpeg"
        contenido = base64.b64encode(imagen).decode()
        try:
            async with self._conexion.cliente(self._transporte) as cliente:
                respuesta = await cliente.post(
                    f"{self._conexion.direccion}/chat/completions",
                    headers=self._conexion.encabezados,
                    json={
                        "model": self._modelo_lectura,
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:{tipo};base64,{contenido}"},
                                    },
                                    {"type": "text", "text": _LEER},
                                ],
                            }
                        ],
                    },
                )
        except httpx.HTTPError as error:
            raise ProveedorNoDisponible(type(error).__name__) from error
        _revisar(respuesta)
        texto: str = respuesta.json()["choices"][0]["message"]["content"]
        return texto.strip()

    async def responder(self, instrucciones: str, turnos: Sequence[Turno]) -> AsyncIterator[str]:
        mensajes = [{"role": "system", "content": instrucciones}] + [
            {"role": "user" if t.autor == "medico" else "assistant", "content": t.texto}
            for t in turnos
        ]
        try:
            async with (
                self._conexion.cliente(self._transporte) as cliente,
                cliente.stream(
                    "POST",
                    f"{self._conexion.direccion}/chat/completions",
                    headers=self._conexion.encabezados,
                    json={
                        "model": self._modelo_respuestas,
                        "messages": mensajes,
                        "stream": True,
                        # Lo más repetible posible: resume, no inventa.
                        "temperature": 0,
                    },
                ) as respuesta,
            ):
                if not respuesta.is_success:
                    await respuesta.aread()
                    _revisar(respuesta)
                async for linea in respuesta.aiter_lines():
                    parte = _parte(linea)
                    if parte:
                        yield parte
        except httpx.HTTPError as error:
            raise ProveedorNoDisponible(type(error).__name__) from error


def _parte(linea: str) -> str | None:
    """Una línea de eventos del servidor: "data: {...}" con un pedazo del texto."""
    if not linea.startswith("data:"):
        return None
    datos = linea[len("data:") :].strip()
    if datos == "[DONE]":
        return None
    opciones = json.loads(datos).get("choices") or []
    if not opciones:
        return None
    contenido: str | None = opciones[0].get("delta", {}).get("content")
    return contenido


def _revisar(respuesta: httpx.Response) -> None:
    if respuesta.is_success:
        return
    try:
        codigo = str(respuesta.json().get("error", {}).get("code", "desconocido"))
    except ValueError:
        codigo = "desconocido"
    raise ErrorDelProveedor(respuesta.status_code, codigo)
