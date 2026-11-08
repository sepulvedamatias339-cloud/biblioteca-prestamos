"""Casos de uso del servicio de Préstamos y Reservas."""
from datetime import timedelta
from typing import Optional

from app.dominio.errores import (
    LimitePrestamosExcedido,
    PrestamoNoEncontrado,
    PrestamoYaDevuelto,
    ReservaDuplicada,
    SinStockDisponible,
    UsuarioNoHabilitado,
)
from app.dominio.modelos import Prestamo, Reserva
from app.dominio.puertos import (
    CatalogoPuerto,
    PrestamoRepositorio,
    Reloj,
    ReservaRepositorio,
    UsuariosPuerto,
)
from app.servicios.multas import PoliticaMulta

DIAS_PRESTAMO = 14
MAX_PRESTAMOS_ACTIVOS = 3


class PrestamoServicio:
    """Responsabilidad única: orquestar préstamos, devoluciones y reservas."""

    def __init__(
        self,
        prestamos: PrestamoRepositorio,
        reservas: ReservaRepositorio,
        catalogo: CatalogoPuerto,
        usuarios: UsuariosPuerto,
        politica_multa: PoliticaMulta,
        reloj: Reloj,
    ):
        self._prestamos = prestamos
        self._reservas = reservas
        self._catalogo = catalogo
        self._usuarios = usuarios
        self._politica_multa = politica_multa
        self._reloj = reloj

    def prestar(self, usuario_id: int, libro_id: int) -> Prestamo:
        if not self._usuarios.esta_habilitado(usuario_id):
            raise UsuarioNoHabilitado(f"Usuario {usuario_id} no habilitado")
        if len(self._prestamos.activos_de_usuario(usuario_id)) >= MAX_PRESTAMOS_ACTIVOS:
            raise LimitePrestamosExcedido("Máximo de préstamos activos alcanzado")
        if self._catalogo.ejemplares_disponibles(libro_id) <= 0:
            raise SinStockDisponible(f"Libro {libro_id} sin stock; puede reservarlo")

        ahora = self._reloj.ahora()
        self._catalogo.descontar_ejemplar(libro_id)
        return self._prestamos.guardar(
            Prestamo(
                id=0,
                usuario_id=usuario_id,
                libro_id=libro_id,
                fecha_prestamo=ahora,
                fecha_vencimiento=ahora + timedelta(days=DIAS_PRESTAMO),
            )
        )

    def reservar(self, usuario_id: int, libro_id: int) -> Reserva:
        if not self._usuarios.esta_habilitado(usuario_id):
            raise UsuarioNoHabilitado(f"Usuario {usuario_id} no habilitado")
        if self._reservas.existe(usuario_id, libro_id):
            raise ReservaDuplicada("El usuario ya reservó este libro")
        return self._reservas.agregar(usuario_id, libro_id, self._reloj.ahora())

    def devolver(self, prestamo_id: int) -> Prestamo:
        prestamo = self._prestamos.obtener(prestamo_id)
        if prestamo is None:
            raise PrestamoNoEncontrado(f"Préstamo {prestamo_id} no existe")
        if not prestamo.activo:
            raise PrestamoYaDevuelto(f"Préstamo {prestamo_id} ya fue devuelto")

        ahora = self._reloj.ahora()
        prestamo.fecha_devolucion = ahora
        prestamo.multa = self._politica_multa.calcular(prestamo.fecha_vencimiento, ahora)
        self._catalogo.reponer_ejemplar(prestamo.libro_id)
        return self._prestamos.guardar(prestamo)

    def siguiente_reserva(self, libro_id: int) -> Optional[Reserva]:
        """Consulta quién sigue en la cola de reservas de un libro."""
        return self._reservas.siguiente_en_cola(libro_id)
