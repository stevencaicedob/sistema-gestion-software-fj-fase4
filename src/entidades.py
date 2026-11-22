"""Entidades base y clase Cliente con encapsulación y validaciones estrictas."""

from abc import ABC, abstractmethod
import re
from src.excepciones import DatoInvalidoError, ParametroFaltanteError


class EntidadBase(ABC):
    """Clase abstracta que representa una entidad general del sistema Software FJ."""

    def __init__(self, id_entidad: str) -> None:
        self._id_entidad = self._validar_id(id_entidad)

    @staticmethod
    def _validar_id(valor: str) -> str:
        if valor is None or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio.")
        limpio = valor.strip()
        if len(limpio) < 3:
            raise DatoInvalidoError(f"El identificador '{limpio}' debe tener al menos 3 caracteres.")
        return limpio

    @property
    def id_entidad(self) -> str:
        """Retorna el identificador único de la entidad."""
        return self._id_entidad

    @abstractmethod
    def resumir(self) -> str:
        """Retorna un resumen legible de la entidad."""


class Cliente(EntidadBase):
    """Representa un cliente de Software FJ con datos personales encapsulados."""

    _REGEX_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(
        self,
        id_cliente: str,
        nombre_completo: str,
        correo: str,
        telefono: str,
        activo: bool = True,
    ) -> None:
        super().__init__(id_cliente)
        self.nombre_completo = nombre_completo
        self.correo = correo
        self.telefono = telefono
        self.activo = activo

    @property
    def nombre_completo(self) -> str:
        return self._nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, valor: str) -> None:
        if valor is None or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError("El nombre completo del cliente es obligatorio.")
        limpio = " ".join(valor.strip().split())
        if len(limpio) < 3:
            raise DatoInvalidoError("El nombre completo debe tener al menos 3 caracteres.")
        self._nombre_completo = limpio

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if valor is None or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError("El correo electrónico del cliente es obligatorio.")
        limpio = valor.strip().lower()
        if not self._REGEX_CORREO.match(limpio):
            raise DatoInvalidoError(f"El correo electrónico '{valor}' no tiene un formato válido.")
        self._correo = limpio

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        if valor is None or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError("El teléfono del cliente es obligatorio.")
        digitos = "".join(ch for ch in valor if ch.isdigit())
        if len(digitos) < 7 or len(digitos) > 15:
            raise DatoInvalidoError(f"El teléfono '{valor}' debe contener entre 7 y 15 dígitos.")
        self._telefono = digitos

    @property
    def activo(self) -> bool:
        return self._activo

    @activo.setter
    def activo(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise DatoInvalidoError("El estado 'activo' del cliente debe ser booleano (True/False).")
        self._activo = valor

    def resumir(self) -> str:
        estado = "Activo" if self._activo else "Inactivo"
        return (
            f"Cliente [{self._id_entidad}] | {self._nombre_completo} | "
            f"Correo: {self._correo} | Tel: {self._telefono} | Estado: {estado}"
        )
