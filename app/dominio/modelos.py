"""Entidades del dominio de Préstamos."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Prestamo:
    id: int
    usuario_id: int
    libro_id: int
    fecha_prestamo: datetime
    fecha_vencimiento: datetime
    fecha_devolucion: Optional[datetime] = None
    multa: int = 0  # en pesos chilenos

    @property
    def activo(self) -> bool:
        return self.fecha_devolucion is None


@dataclass
class Reserva:
    id: int
    usuario_id: int
    libro_id: int
    fecha: datetime
