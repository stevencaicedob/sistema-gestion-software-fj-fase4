# Sistema Integral de Gestión de Clientes, Servicios y Reservas (Software FJ)

Aplicación desarrollada en **Python** aplicando Programación Orientada a Objetos (POO), gestión de datos en memoria (sin base de datos), registro de auditoría en archivo de *log* y manejo estructurado de excepciones personalizadas con encadenamiento.

## Características principales

* **Gestión en memoria:** administración de clientes, servicios y reservas mediante listas en memoria desde `GestorSoftwareFJ`.
* **Abstracción y encapsulación:** clase abstracta `EntidadBase` y entidad `Cliente` con propiedades (`@property` y *setters*) y validaciones de formato y obligatoriedad.
* **Polimorfismo y cálculo flexible de costos:** jerarquía encabezada por la clase abstracta `Servicio` y subclases especializadas (`ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`), con sobrescritura de métodos y parámetros opcionales para descuentos, impuestos y recargos.
* **Excepciones personalizadas y encadenamiento:** jerarquía de excepciones del dominio (`ErrorSistemaFJ`, `DatoInvalidoError`, `ParametroFaltanteError`, `OperacionNoPermitidaError`, `ServicioNoDisponibleError`, `ReservaInvalidaError` y `CalculoCostoError`) utilizando `raise ... from exc`.
* **Registro de eventos (Logging):** configuración centralizada en `src/logger_config.py` escribiendo en `logs/sistema_fj.log`.

## Estructura del proyecto

```text
sistema-gestion-software-fj-fase4/
├── logs/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── excepciones.py
│   ├── logger_config.py
│   ├── entidades.py
│   ├── servicios.py
│   ├── reservas.py
│   └── gestor.py
├── main.py
└── README.md

## Ejecución

Desde la raíz del repositorio, ejecuta el script de simulación:

```bash
python3 main.py
```

Para consultar los eventos registrados durante la ejecución:

```bash
cat logs/sistema_fj.log
```
