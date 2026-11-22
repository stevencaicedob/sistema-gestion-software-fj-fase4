"""Configuración del registro de eventos y errores en archivo de texto."""

import logging
from pathlib import Path


def configurar_logger(
    nombre_logger: str = "SoftwareFJ",
    archivo_log: str = "logs/sistema_fj.log",
) -> logging.Logger:
    """Configura y devuelve un logger que escribe eventos y errores en archivo."""
    ruta_log = Path(archivo_log)
    ruta_log.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(nombre_logger)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Evita duplicar manejadores si se llama la función más de una vez
    if not logger.handlers:
        formato = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        manejador_archivo = logging.FileHandler(ruta_log, mode="a", encoding="utf-8")
        manejador_archivo.setFormatter(formato)
        logger.addHandler(manejador_archivo)

    return logger
