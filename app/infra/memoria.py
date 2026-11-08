"""Adaptadores en memoria (para pruebas y desarrollo local)."""
from datetime import datetime
from typing import Dict, List, Optional

from app.dominio.modelos import Prestamo, Reserva


class PrestamoRepoMemoria:
    def __init__(self) -> None:
        self._datos: Dict[int, Prestamo] = {}
        self._seq = 0

    def guardar(self, prestamo: Prestamo) -> Prestamo:
        if prestamo.id == 0:
            self._seq += 1
            prestamo.id = self._seq
        self._datos[prestamo.id] = prestamo
        return prestamo

    def obtener(self, prestamo_id: int) -> Optional[Prestamo]:
        return self._datos.get(prestamo_id)

    def activos_de_usuario(self, usuario_id: int) -> List[Prestamo]:
        return [p for p in self._datos.values() if p.usuario_id == usuario_id and p.activo]


class ReservaRepoMemoria:
    def __init__(self) -> None:
        self._datos: List[Reserva] = []
        self._seq = 0

    def agregar(self, usuario_id: int, libro_id: int, fecha: datetime) -> Reserva:
        self._seq += 1
        reserva = Reserva(self._seq, usuario_id, libro_id, fecha)
        self._datos.append(reserva)
        return reserva

    def existe(self, usuario_id: int, libro_id: int) -> bool:
        return any(r.usuario_id == usuario_id and r.libro_id == libro_id for r in self._datos)

    def siguiente_en_cola(self, libro_id: int) -> Optional[Reserva]:
        cola = [r for r in self._datos if r.libro_id == libro_id]
        return min(cola, key=lambda r: r.fecha) if cola else None

    def eliminar(self, reserva_id: int) -> None:
        self._datos = [r for r in self._datos if r.id != reserva_id]
