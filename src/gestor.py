"""Gestor central en memoria para el Sistema Integral Software FJ."""

from typing import List, Optional
from src.entidades import Cliente
from src.excepciones import (
    DatoInvalidoError,
    ErrorSistemaFJ,
    OperacionNoPermitidaError,
)
from src.logger_config import configurar_logger
from src.reservas import Reserva
from src.servicios import Servicio


class GestorSoftwareFJ:
    """Coordina clientes, servicios y reservas en memoria con registro de auditoría."""

    def __init__(self, log_path: str = "logs/sistema_fj.log") -> None:
        self._clientes: List[Cliente] = []
        self._servicios: List[Servicio] = []
        self._reservas: List[Reserva] = []
        self._logger = configurar_logger(nombre_logger="SoftwareFJ.Gestor", archivo_log=log_path)
        self._logger.info("GestorSoftwareFJ inicializado en memoria.")

    @property
    def clientes(self) -> List[Cliente]:
        return list(self._clientes)

    @property
    def servicios(self) -> List[Servicio]:
        return list(self._servicios)

    @property
    def reservas(self) -> List[Reserva]:
        return list(self._reservas)

    def registrar_cliente(self, cliente: Cliente) -> Cliente:
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Solo se pueden registrar objetos de tipo Cliente.")
        if self.buscar_cliente(cliente.id_entidad) is not None:
            raise OperacionNoPermitidaError(f"Ya existe un cliente registrado con ID '{cliente.id_entidad}'.")
        self._clientes.append(cliente)
        self._logger.info("Cliente registrado: %s (%s)", cliente.nombre_completo, cliente.id_entidad)
        return cliente

    def buscar_cliente(self, id_cliente: str) -> Optional[Cliente]:
        for cli in self._clientes:
            if cli.id_entidad == id_cliente:
                return cli
        return None

    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Solo se pueden registrar objetos derivados de Servicio.")
        if self.buscar_servicio(servicio.codigo) is not None:
            raise OperacionNoPermitidaError(f"Ya existe un servicio con código '{servicio.codigo}'.")
        self._servicios.append(servicio)
        self._logger.info("Servicio registrado: %s - %s", servicio.codigo, servicio.nombre)
        return servicio

    def buscar_servicio(self, codigo_servicio: str) -> Optional[Servicio]:
        for srv in self._servicios:
            if srv.codigo == codigo_servicio:
                return srv
        return None

    def buscar_reserva(self, id_reserva: str) -> Optional[Reserva]:
        for rsv in self._reservas:
            if rsv.id_reserva == id_reserva:
                return rsv
        return None

    def crear_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        codigo_servicio: str,
        cantidad: int,
        fecha_reserva: str,
        descuento: float = 0.0,
        impuesto: float = 0.19,
    ) -> Reserva:
        try:
            cliente = self.buscar_cliente(id_cliente)
            if cliente is None:
                raise DatoInvalidoError(f"No se encontró el cliente con ID '{id_cliente}'.")

            servicio = self.buscar_servicio(codigo_servicio)
            if servicio is None:
                raise DatoInvalidoError(f"No se encontró el servicio con código '{codigo_servicio}'.")

            if self.buscar_reserva(id_reserva) is not None:
                raise OperacionNoPermitidaError(f"Ya existe una reserva con ID '{id_reserva}'.")

            reserva = Reserva(
                id_reserva=id_reserva,
                cliente=cliente,
                servicio=servicio,
                cantidad=cantidad,
                fecha_reserva=fecha_reserva,
                descuento=descuento,
                impuesto=impuesto,
            )
            self._reservas.append(reserva)
            self._logger.info(
                "Reserva creada: %s | Cliente: %s | Servicio: %s | Total: $%.2f",
                reserva.id_reserva,
                cliente.id_entidad,
                servicio.codigo,
                reserva.costo_total,
            )
            return reserva
        except ErrorSistemaFJ as exc:
            self._logger.error("Error de dominio al crear reserva '%s': %s", id_reserva, exc)
            raise

    def cancelar_reserva(self, id_reserva: str) -> Reserva:
        reserva = self.buscar_reserva(id_reserva)
        if reserva is None:
            raise DatoInvalidoError(f"No existe la reserva con ID '{id_reserva}'.")
        reserva.cancelar()
        self._logger.warning("Reserva cancelada: %s", id_reserva)
        return reserva

    def completar_reserva(self, id_reserva: str) -> Reserva:
        reserva = self.buscar_reserva(id_reserva)
        if reserva is None:
            raise DatoInvalidoError(f"No existe la reserva con ID '{id_reserva}'.")
        reserva.completar()
        self._logger.info("Reserva completada: %s", id_reserva)
        return reserva

    def calcular_ingresos_activos(self) -> float:
        total = sum(r.costo_total for r in self._reservas if r.estado in ("CONFIRMADA", "COMPLETADA"))
        return round(total, 2)
