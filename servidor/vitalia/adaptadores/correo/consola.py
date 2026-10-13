"""Correo en la consola: muestra el mensaje en vez de enviarlo. Solo para desarrollo."""


class CorreoEnConsola:
    async def enviar(self, destinatario: str, asunto: str, cuerpo: str) -> None:
        print(
            f"--- Correo para {destinatario} ---\nAsunto: {asunto}\n\n{cuerpo}\n---",
            flush=True,
        )
