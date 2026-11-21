from src.exceptions.custom_exceptions import ReglaNegocioError
from src.models.entities.sensor_suelo import SensorSuelo
from src.models.sensor_model import SensorModel


class SensorController:

    def __init__(self):
        self.modelo = SensorModel()

    def guardar_lectura(
        self, parcela: str, humedad_str: str, temperatura_str: str
    ) -> str:
        parcela = parcela.strip().upper()
        if not parcela or not humedad_str.strip() or not temperatura_str.strip():
            raise ReglaNegocioError("Todos los campos son obligatorios.")

        try:
            humedad = float(humedad_str)
            temperatura = float(temperatura_str)
        except ValueError:
            raise ReglaNegocioError(
                "Humedad y Temperatura deben ser valores numéricos válidos."
            )

        if humedad < 0 or humedad > 100:
            raise ReglaNegocioError("La humedad debe estar entre 0% y 100%.")

        sensor = SensorSuelo(parcela, humedad, temperatura)
        self.modelo.registrar(sensor)
        return sensor.mensaje_alerta

    def obtener_lecturas(self, filtro: str = "") -> list:
        return self.modelo.listar_buscar(filtro.strip())
