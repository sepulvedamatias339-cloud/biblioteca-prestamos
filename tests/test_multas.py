from datetime import datetime, timedelta

import pytest

from app.servicios.multas import MultaPorDia

VENC = datetime(2026, 3, 16, 10, 0)


@pytest.mark.parametrize(
    "dias_extra, esperado",
    [(-2, 0), (0, 0), (1, 200), (5, 1000)],
)
def test_multa_segun_dias_de_atraso(dias_extra, esperado):
    assert MultaPorDia(200).calcular(VENC, VENC + timedelta(days=dias_extra)) == esperado


def test_valor_dia_negativo_es_invalido():
    with pytest.raises(ValueError):
        MultaPorDia(-1)
