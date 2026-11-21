import mysql.connector
from mysql.connector import Error
from src.exceptions.custom_exceptions import DatabaseConnectionError


class ConexionDB:

    @staticmethod
    def obtener_conexion():
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",  # Cambia por tu usuario de MySQL
                password="Ati2026$",  # Cambia por tu contraseña de MySQL
                database="bd_agroexporta_olmos",
            )
            return conexion
        except Error as e:
            raise DatabaseConnectionError(
                f"Error al conectar con MySQL: {str(e)}"
            )
