from datetime import timedelta

import pytest

from app.dominio.errores import (
    LimitePrestamosExcedido,
    PrestamoNoEncontrado,
    PrestamoYaDevuelto,
    ReservaDuplicada,
    SinStockDisponible,
    UsuarioNoHabilitado,
)


def test_prestar_libro_descuenta_stock_y_fija_vencimiento(servicio, catalogo, reloj):
    prestamo = servicio.prestar(10, 1)
    assert prestamo.id == 1
    assert catalogo.stock[1] == 1
    assert prestamo.fecha_vencimiento == reloj.ahora() + timedelta(days=14)
    assert prestamo.activo


def test_usuario_no_habilitado_no_puede_prestar(servicio):
    with pytest.raises(UsuarioNoHabilitado):
        servicio.prestar(99, 1)


def test_libro_sin_stock_lanza_error(servicio):
    with pytest.raises(SinStockDisponible):
        servicio.prestar(10, 2)


def test_limite_de_tres_prestamos_activos(servicio):
    servicio.prestar(10, 1)
    servicio.prestar(10, 3)
    servicio.prestar(10, 4)
    with pytest.raises(LimitePrestamosExcedido):
        servicio.prestar(10, 1)


def test_devolver_a_tiempo_no_genera_multa(servicio, catalogo, reloj):
    prestamo = servicio.prestar(10, 1)
    reloj.actual += timedelta(days=14)
    devuelto = servicio.devolver(prestamo.id)
    assert devuelto.multa == 0
    assert not devuelto.activo
    assert catalogo.stock[1] == 2


def test_devolver_con_atraso_genera_multa(servicio, reloj):
    prestamo = servicio.prestar(10, 1)
    reloj.actual += timedelta(days=17)  # 3 días de atraso
    assert servicio.devolver(prestamo.id).multa == 600


def test_devolver_prestamo_inexistente(servicio):
    with pytest.raises(PrestamoNoEncontrado):
        servicio.devolver(123)


def test_no_se_puede_devolver_dos_veces(servicio):
    prestamo = servicio.prestar(10, 1)
    servicio.devolver(prestamo.id)
    with pytest.raises(PrestamoYaDevuelto):
        servicio.devolver(prestamo.id)


def test_reservar_y_consultar_cola_respeta_orden(servicio, reloj):
    servicio.reservar(10, 2)
    reloj.actual += timedelta(hours=1)
    servicio.reservar(11, 2)
    assert servicio.siguiente_reserva(2).usuario_id == 10


def test_reserva_duplicada_lanza_error(servicio):
    servicio.reservar(10, 2)
    with pytest.raises(ReservaDuplicada):
        servicio.reservar(10, 2)


def test_usuario_no_habilitado_no_puede_reservar(servicio):
    with pytest.raises(UsuarioNoHabilitado):
        servicio.reservar(99, 2)


def test_siguiente_reserva_sin_cola_retorna_none(servicio):
    assert servicio.siguiente_reserva(3) is None
