# Servicio de Préstamos y Reservas – Biblioteca Universidad X

Microservicio en Python (arquitectura hexagonal simple, principios SOLID).

## Ejecutar pruebas
    pip install -r requirements.txt
    python -m pytest --cov=app --cov-report=term-missing

## Estructura
- app/dominio: entidades, errores y puertos (interfaces)
- app/servicios: casos de uso y política de multas (Strategy)
- app/infra: adaptadores (en memoria)
- tests: pruebas unitarias con pytest
