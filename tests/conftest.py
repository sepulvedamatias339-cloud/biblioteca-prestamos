from datetime import datetime

import pytest

from app.infra.memoria import PrestamoRepoMemoria, ReservaRepoMemoria
from app.servicios.multas import MultaPorDia
from app.servicios.prestamos import PrestamoServicio


class CatalogoFalso:
    def __init__(self, stock):
        self.stock = dict(stock)

    def ejemplares_disponibles(self, libro_id):
        return self.stock.get(libro_id, 0)

    def descontar_ejemplar(self, libro_id):
        self.stock[libro_id] -= 1

    def reponer_ejemplar(self, libro_id):
        self.stock[libro_id] += 1


class UsuariosFalso:
    def __init__(self, habilitados):
        self.habilitados = set(habilitados)

    def esta_habilitado(self, usuario_id):
        return usuario_id in self.habilitados


class RelojFalso:
    def __init__(self, inicio):
        self.actual = inicio

    def ahora(self):
        return self.actual


@pytest.fixture
def reloj():
    return RelojFalso(datetime(2026, 3, 2, 10, 0))


@pytest.fixture
def catalogo():
    return CatalogoFalso({1: 2, 2: 0, 3: 5, 4: 5})


@pytest.fixture
def servicio(reloj, catalogo):
    return PrestamoServicio(
        prestamos=PrestamoRepoMemoria(),
        reservas=ReservaRepoMemoria(),
        catalogo=catalogo,
        usuarios=UsuariosFalso({10, 11}),
        politica_multa=MultaPorDia(200),
        reloj=reloj,
    )
