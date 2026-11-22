"""Script de simulación y verificación para el Sistema Integral Software FJ."""

from src.entidades import Cliente
from src.excepciones import ErrorSistemaFJ
from src.gestor import GestorSoftwareFJ
from src.servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def ejecutar_simulacion() -> None:
    print("=== INICIO DE SIMULACIÓN - SISTEMA INTEGRAL SOFTWARE FJ ===\n")
    gestor = GestorSoftwareFJ(log_path="logs/sistema_fj.log")

    # 1. Registro de clientes
    cliente_1 = Cliente("CLI-001", "Laura Sofía Méndez", "laura.mendez@empresa.co", "3105551234", activo=True)
    cliente_2 = Cliente("CLI-002", "Carlos Andrés Rojas", "carlos.rojas@correo.org", "3204449876", activo=True)
    cliente_inactivo = Cliente("CLI-003", "María Fernanda Gómez", "m.gomez@dominio.com", "3157778899", activo=False)

    for cli in (cliente_1, cliente_2, cliente_inactivo):
        gestor.registrar_cliente(cli)
        print("Registrado:", cli.resumir())

    print("\n--- Servicios Especializados (Polimorfismo) ---")
    sala = ReservaSala("SAL-101", "Sala Ejecutiva Norte", tarifa_base=85000.0, capacidad_personas=12, disponible=True)
    equipo = AlquilerEquipo("EQP-204", "Estación Portátil Workstation", tarifa_base=120000.0, especificacion="32GB RAM / 1TB NVMe", disponible=True)
    asesoria = AsesoriaEspecializada("ASE-305", "Arquitectura en la Nube", tarifa_base=180000.0, especialidad="Cloud & Seguridad", disponible=True)
    servicio_no_disp = ReservaSala("SAL-102", "Auditorio Principal", tarifa_base=150000.0, capacidad_personas=60, disponible=False)

    servicios_catalogo = [sala, equipo, asesoria, servicio_no_disp]
    for srv in servicios_catalogo:
        gestor.registrar_servicio(srv)
        costo_estimado = srv.calcular_costo(cantidad=2, descuento=0.10)
        print(f"{srv.describir()} -> Simulación 2 und (10% desc.): ${costo_estimado:,.2f}")

    print("\n--- Gestión de Reservas en Memoria ---")
    r1 = gestor.crear_reserva("RSV-1001", "CLI-001", "SAL-101", cantidad=3, fecha_reserva="2026-12-01")
    r2 = gestor.crear_reserva("RSV-1002", "CLI-002", "EQP-204", cantidad=4, fecha_reserva="2026-12-03", descuento=0.05)
    r3 = gestor.crear_reserva("RSV-1003", "CLI-001", "ASE-305", cantidad=5, fecha_reserva="2026-12-05")

    gestor.completar_reserva("RSV-1001")
    gestor.cancelar_reserva("RSV-1002")

    for rsv in gestor.reservas:
        print(rsv.resumir())

    print(f"\nIngresos activos (CONFIRMADA + COMPLETADA): ${gestor.calcular_ingresos_activos():,.2f}")

    print("\n--- Pruebas de Excepciones y Encadenamiento ---")
    casos_error = [
        ("Cliente inactivo", lambda: gestor.crear_reserva("RSV-9001", "CLI-003", "SAL-101", 2, "2026-12-10")),
        ("Servicio no disponible", lambda: gestor.crear_reserva("RSV-9002", "CLI-001", "SAL-102", 2, "2026-12-10")),
        ("Cantidad fuera de rango (encadenamiento)", lambda: gestor.crear_reserva("RSV-9003", "CLI-001", "SAL-101", 20, "2026-12-10")),
        ("Cancelar reserva ya completada", lambda: gestor.cancelar_reserva("RSV-1001")),
    ]

    for descripcion, accion in casos_error:
        try:
            accion()
        except ErrorSistemaFJ as exc:
            causa = type(exc.__cause__).__name__ if exc.__cause__ else "Ninguna"
            print(f"[OK Capturado] {descripcion} -> {type(exc).__name__}: {exc} (Causa encadenada: {causa})")

    print("\n=== FIN DE SIMULACIÓN ===")


if __name__ == "__main__":
    ejecutar_simulacion()
