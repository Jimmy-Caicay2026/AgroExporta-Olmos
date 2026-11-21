class DatabaseConnectionError(Exception):
    """Excepción para errores de conexión a la base de datos."""

    pass


class ReglaNegocioError(Exception):
    """Excepción para validaciones de datos o duplicados."""

    pass
