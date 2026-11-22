"""Excepciones personalizadas para el sistema integral de Software FJ."""


class ErrorSistemaFJ(Exception):
    """Excepción base de todos los errores del sistema Software FJ."""


class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un dato no cumple las reglas de validación."""


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando falta un argumento o parámetro obligatorio."""


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza ante operaciones o cambios de estado no permitidos."""


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando un servicio no está disponible para reservar."""


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando una reserva es inválida o no puede procesarse."""


class CalculoCostoError(ErrorSistemaFJ):
    """Se lanza cuando ocurre un error al calcular tarifas, descuentos o impuestos."""
