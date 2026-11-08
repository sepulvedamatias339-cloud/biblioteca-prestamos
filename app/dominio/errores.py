"""Excepciones de dominio del servicio de Préstamos."""


class ErrorDominio(Exception):
    """Clase base para errores de reglas de negocio."""


class UsuarioNoHabilitado(ErrorDominio):
    pass


class LimitePrestamosExcedido(ErrorDominio):
    pass


class SinStockDisponible(ErrorDominio):
    pass


class PrestamoNoEncontrado(ErrorDominio):
    pass


class PrestamoYaDevuelto(ErrorDominio):
    pass


class ReservaDuplicada(ErrorDominio):
    pass
