"""Contraseñas con argon2id y sal única (RNF-04)."""

import asyncio
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError


class ContrasenasArgon2:
    def __init__(self) -> None:
        self._cifrador = PasswordHasher()
        # Se compara contra este hash cuando la cuenta no existe, para tardar lo mismo.
        self._de_relleno = self._cifrador.hash(secrets.token_urlsafe(16))

    async def cifrar(self, contrasena: str) -> str:
        # Cifrar toma su tiempo a propósito: fuera del hilo que atiende las peticiones.
        return await asyncio.to_thread(self._cifrador.hash, contrasena)

    async def verificar(self, contrasena: str, hash_contrasena: str | None) -> bool:
        objetivo = hash_contrasena or self._de_relleno
        try:
            await asyncio.to_thread(self._cifrador.verify, objetivo, contrasena)
        except (VerificationError, InvalidHashError):
            return False
        return hash_contrasena is not None
