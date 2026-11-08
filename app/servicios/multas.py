"""Cálculo de multas. Patrón Strategy: se puede cambiar la política (OCP)."""
from abc import ABC, abstractmethod
from datetime import datetime


class PoliticaMulta(ABC):
    @abstractmethod
    def calcular(self, vencimiento: datetime, devolucion: datetime) -> int:
        """Retorna el monto de la multa en pesos chilenos."""


class MultaPorDia(PoliticaMulta):
    def __init__(self, valor_dia: int = 200):
        if valor_dia < 0:
            raise ValueError("El valor por día no puede ser negativo")
        self.valor_dia = valor_dia

    def calcular(self, vencimiento: datetime, devolucion: datetime) -> int:
        dias_atraso = (devolucion.date() - vencimiento.date()).days
        return max(dias_atraso, 0) * self.valor_dia
