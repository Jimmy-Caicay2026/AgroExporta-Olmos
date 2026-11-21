from mysql.connector import Error
from src.database.conexion import ConexionDB
from src.exceptions.custom_exceptions import ReglaNegocioError
from src.models.entities.sensor_suelo import SensorSuelo


class SensorModel:

    def registrar(self, sensor: SensorSuelo):
        conexion = ConexionDB.obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.callproc(
                "sp_registrar_sensor",
                [
                    sensor.parcela,
                    sensor.humedad_porcentaje,
                    sensor.temperatura_suelo,
                ],
            )
            conexion.commit()
        except Error as e:
            conexion.rollback()
            if e.sqlstate == "45000":
                raise ReglaNegocioError(e.msg)
            raise Exception(f"Error en base de datos: {str(e)}")
        finally:
            cursor.close()
            conexion.close()

    def listar_buscar(self, filtro: str = "") -> list:
        conexion = ConexionDB.obtener_conexion()
        cursor = conexion.cursor()
        resultados = []
        try:
            cursor.callproc("sp_listar_buscar_sensores", [filtro])
            for result in cursor.stored_results():
                filas = result.fetchall()
                for fila in filas:
                    # fila = (id, parcela, humedad_porcentaje, temperatura_suelo)
                    sensor = SensorSuelo(fila[1], fila[2], fila[3])
                    resultados.append((
                        fila[0],
                        sensor.parcela,
                        f"{sensor.humedad_porcentaje:.2f}%",
                        f"{sensor.temperatura_suelo:.2f} °C",
                        sensor.mensaje_alerta,
                    ))
            return resultados
        finally:
            cursor.close()
            conexion.close()
