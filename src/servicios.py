"""Servicios especializados de Software FJ con polimorfismo y cálculo flexible de costos."""

from abc import ABC, abstractmethod
from src.excepciones import (
    CalculoCostoError,
    DatoInvalidoError,
    ParametroFaltanteError,
)


class Servicio(ABC):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_base: float,
        disponible: bool = True,
    ) -> None:
        self._codigo = self._validar_texto(codigo, "código del servicio", min_len=2)
        self._nombre = self._validar_texto(nombre, "nombre del servicio", min_len=3)
        self._tarifa_base = self._validar_tarifa(tarifa_base)
        self._disponible = self._validar_booleano(disponible, "disponible")

    @staticmethod
    def _validar_texto(valor: str, campo: str, min_len: int = 1) -> str:
        if valor is None or not isinstance(valor, str) or not valor.strip():
            raise ParametroFaltanteError(f"El {campo} es obligatorio.")
        limpio = " ".join(valor.strip().split())
        if len(limpio) < min_len:
            raise DatoInvalidoError(f"El {campo} '{limpio}' debe tener al menos {min_len} caracteres.")
        return limpio

    @staticmethod
    def _validar_tarifa(valor: float) -> float:
        if valor is None or isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise DatoInvalidoError("La tarifa base debe ser un valor numérico.")
        tarifa = float(valor)
        if tarifa <= 0:
            raise DatoInvalidoError("La tarifa base debe ser mayor que cero.")
        return tarifa

    @staticmethod
    def _validar_booleano(valor: bool, campo: str) -> bool:
        if not isinstance(valor, bool):
            raise DatoInvalidoError(f"El campo '{campo}' debe ser booleano (True/False).")
        return valor

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self._disponible = self._validar_booleano(valor, "disponible")

    @abstractmethod
    def describir(self) -> str:
        """Retorna la descripción detallada del servicio."""

    @abstractmethod
    def validar_parametros(self, cantidad: int) -> None:
        """Valida que la duración o cantidad solicitada sea coherente con el servicio."""

    def calcular_costo(
        self,
        cantidad: int,
        descuento: float = 0.0,
        impuesto: float = 0.19,
        recargo_adicional: float = 0.0,
    ) -> float:
        """Calcula el costo total soportando parámetros opcionales (simula sobrecarga).

        Aplica validación de parámetros, recargos/descuentos e impuestos,
        encadenando cualquier error técnico o de validación en CalculoCostoError.
        """
        try:
            self.validar_parametros(cantidad)

            if isinstance(descuento, bool) or not isinstance(descuento, (int, float)):
                raise DatoInvalidoError("El descuento debe ser numérico.")
            if not (0.0 <= float(descuento) < 1.0):
                raise DatoInvalidoError("El descuento debe estar entre 0.0 y menor que 1.0.")

            if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)):
                raise DatoInvalidoError("El impuesto debe ser numérico.")
            if float(impuesto) < 0.0 or float(impuesto) > 1.0:
                raise DatoInvalidoError("El impuesto debe estar entre 0.0 y 1.0.")

            if isinstance(recargo_adicional, bool) or not isinstance(recargo_adicional, (int, float)):
                raise DatoInvalidoError("El recargo adicional debe ser numérico.")
            if float(recargo_adicional) < 0.0:
                raise DatoInvalidoError("El recargo adicional no puede ser negativo.")

            subtotal = (self._tarifa_base * cantidad) + float(recargo_adicional)
            con_descuento = subtotal * (1.0 - float(descuento))
            total = con_descuento * (1.0 + float(impuesto))
            return round(total, 2)
        except Exception as exc:
            raise CalculoCostoError(
                f"No fue posible calcular el costo para el servicio '{self._codigo}' ({self._nombre})."
            ) from exc


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas de reuniones o capacitación."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_base: float,
        capacidad_personas: int,
        disponible: bool = True,
    ) -> None:
        super().__init__(codigo, nombre, tarifa_base, disponible)
        if isinstance(capacidad_personas, bool) or not isinstance(capacidad_personas, int) or capacidad_personas <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad_personas = capacidad_personas

    @property
    def capacidad_personas(self) -> int:
        return self._capacidad_personas

    def describir(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Sala] {self._codigo} - {self._nombre} | Capacidad: {self._capacidad_personas} pax | "
            f"Tarifa/h: ${self._tarifa_base:,.2f} | {estado}"
        )

    def validar_parametros(self, cantidad: int) -> None:
        if cantidad is None or isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise DatoInvalidoError("La duración en horas para reservar una sala debe ser un número entero.")
        if cantidad < 1 or cantidad > 12:
            raise DatoInvalidoError("Una reserva de sala debe ser de entre 1 y 12 horas.")


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos o audiovisuales."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_base: float,
        especificacion: str,
        disponible: bool = True,
    ) -> None:
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self._especificacion = self._validar_texto(especificacion, "especificación del equipo", min_len=3)

    @property
    def especificacion(self) -> str:
        return self._especificacion

    def describir(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Equipo] {self._codigo} - {self._nombre} ({self._especificacion}) | "
            f"Tarifa/día: ${self._tarifa_base:,.2f} | {estado}"
        )

    def validar_parametros(self, cantidad: int) -> None:
        if cantidad is None or isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise DatoInvalidoError("La cantidad de días para alquiler de equipo debe ser un número entero.")
        if cantidad < 1 or cantidad > 30:
            raise DatoInvalidoError("El alquiler de equipo debe ser de entre 1 y 30 días.")

    def calcular_costo(
        self,
        cantidad: int,
        descuento: float = 0.0,
        impuesto: float = 0.19,
        recargo_adicional: float = 15000.0,
    ) -> float:
        """Sobrescribe el cálculo incluyendo por defecto un cargo fijo de revisión/logística."""
        return super().calcular_costo(
            cantidad=cantidad,
            descuento=descuento,
            impuesto=impuesto,
            recargo_adicional=recargo_adicional,
        )


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para asesorías técnicas o de arquitectura de software."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        tarifa_base: float,
        especialidad: str,
        disponible: bool = True,
    ) -> None:
        super().__init__(codigo, nombre, tarifa_base, disponible)
        self._especialidad = self._validar_texto(especialidad, "especialidad de asesoría", min_len=3)

    @property
    def especialidad(self) -> str:
        return self._especialidad

    def describir(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return (
            f"[Asesoría] {self._codigo} - {self._nombre} [{self._especialidad}] | "
            f"Tarifa/h: ${self._tarifa_base:,.2f} | {estado}"
        )

    def validar_parametros(self, cantidad: int) -> None:
        if cantidad is None or isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise DatoInvalidoError("La duración en horas de la asesoría debe ser un número entero.")
        if cantidad < 1 or cantidad > 40:
            raise DatoInvalidoError("Una asesoría especializada debe ser de entre 1 y 40 horas.")
