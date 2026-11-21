class SensorSuelo:

    def __init__(
        self, parcela: str, humedad_porcentaje: float, temperatura_suelo: float
    ):
        self.parcela = parcela
        self.humedad_porcentaje = float(humedad_porcentaje)
        self.temperatura_suelo = float(temperatura_suelo)
        self.mensaje_alerta = self.evaluar_alerta()

    def evaluar_alerta(self) -> str:
        if self.humedad_porcentaje < 25.0:
            return "ALERTA: RIEGO URGENTE"
        elif 25.0 <= self.humedad_porcentaje <= 45.0:
            return "HUMEDAD OPTIMA"
        else:
            return "ALERTA: EXCESO DE AGUA"
