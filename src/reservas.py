"""Entidad Reserva para vincular clientes y servicios en Software FJ."""

from datetime import datetime
from src.entidades import Cliente
from src.excepciones import (
    DatoInvalidoError,
    OperacionNoPermitidaError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from src.servicios import Servicio


class Reserva:
    """Representa una reserva de servicio realizada por un cliente."""

    ESTADOS_VALIDOS = ("CONFIRMADA", "CANCELADA", "COMPLETADA")

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        cantidad: int,
        fecha_reserva: str,
        descuento: float = 0.0,
        impuesto: float = 0.19,
    ) -> None:
        self._id_reserva = self._validar_id(id_reserva)

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere una instancia válida de Cliente.")
        if not cliente.activo:
            raise OperacionNoPermitidaError(
                f"El cliente '{cliente.id_entidad}' está inactivo y no puede realizar reservas."
            )

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere una instancia válida de Servicio.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.codigo}' ({servicio.nombre}) no está disponible actualmente."
            )

        self._fecha_reserva = self._validar_fecha(fecha_reserva)
        self._cliente = cliente
        self._servicio = servicio
        self._estado = "CONFIRMADA"
        self._descuento = descuento
        self._impuesto = impuesto
        self._cantidad = self._validar_y_calcular_cantidad(cantidad)

    @staticmethod
    def _validar_id(id_reserva: str) -> str:
        if id_reserva is None or not isinstance(id_reserva, str) or not id_reserva.strip():
            raise ParametroFaltanteError("El identificador de la reserva es obligatorio.")
        limpio = id_reserva.strip()
        if len(limpio) < 3:
            raise DatoInvalidoError(f"El identificador de reserva '{limpio}' debe tener al menos 3 caracteres.")
        return limpio

    @staticmethod
    def _validar_fecha(fecha_str: str) -> str:
        if fecha_str is None or not isinstance(fecha_str, str) or not fecha_str.strip():
            raise ParametroFaltanteError("La fecha de la reserva es obligatoria.")
        limpio = fecha_str.strip()
        try:
            datetime.strptime(limpio, "%Y-%m-%d")
        except ValueError as exc:
            raise DatoInvalidoError(
                f"La fecha '{limpio}' no cumple con el formato esperado YYYY-MM-DD."
            ) from exc
        return limpio

    def _validar_y_calcular_cantidad(self, cantidad: int) -> int:
        try:
            self._costo_total = self._servicio.calcular_costo(
                cantidad=cantidad,
                descuento=self._descuento,
                impuesto=self._impuesto,
            )
            return cantidad
        except Exception as exc:
            raise ReservaInvalidaError(
                f"No fue posible validar o cotizar la reserva '{self._id_reserva}'."
            ) from exc

    @property
    def id_reserva(self) -> str:
        return self._id_reserva

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @property
    def fecha_reserva(self) -> str:
        return self._fecha_reserva

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def cancelar(self) -> None:
        """Cancela la reserva si está confirmada."""
        if self._estado == "COMPLETADA":
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva '{self._id_reserva}' porque ya fue completada."
            )
        if self._estado == "CANCELADA":
            raise OperacionNoPermitidaError(
                f"La reserva '{self._id_reserva}' ya se encuentra cancelada."
            )
        self._estado = "CANCELADA"

    def completar(self) -> None:
        """Marca la reserva como completada si estaba confirmada."""
        if self._estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Solo se pueden completar reservas en estado CONFIRMADA (actual: {self._estado})."
            )
        self._estado = "COMPLETADA"

    def resumir(self) -> str:
        return (
            f"Reserva [{self._id_reserva}] | Fecha: {self._fecha_reserva} | "
            f"Cliente: {self._cliente.nombre_completo} ({self._cliente.id_entidad}) | "
            f"Servicio: {self._servicio.codigo} x{self._cantidad} | "
            f"Total: ${self._costo_total:,.2f} | Estado: {self._estado}"
        )
