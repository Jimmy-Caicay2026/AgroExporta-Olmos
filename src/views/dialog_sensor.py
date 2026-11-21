import os
from PySide6.QtCore import QFile, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QMessageBox
from src.controller.sensor_controller import SensorController
from src.exceptions.custom_exceptions import ReglaNegocioError


class DialogSensor:

    def __init__(self, parent=None):
        self.controller = SensorController()

        # Cargar el archivo .ui directamente como QDialog
        ruta_ui = os.path.join(
            os.path.dirname(__file__), "ui", "dialog_sensor.ui"
        )
        archivo_ui = QFile(ruta_ui)
        if not archivo_ui.open(QFile.ReadOnly):
            raise FileNotFoundError(
                f"No se pudo abrir el archivo UI en: {ruta_ui}"
            )

        loader = QUiLoader()
        self.dialog = loader.load(archivo_ui, parent)
        archivo_ui.close()

        self.configurar_validadores()

        # Conectar botones
        self.dialog.btnGuardar.clicked.connect(self.guardar)
        self.dialog.btnCancelar.clicked.connect(self.dialog.reject)

    def exec(self):
        return self.dialog.exec()

    def configurar_validadores(self):
        # Validador para código de parcela (letras, números y guiones)
        regex_parcela = QRegularExpression(r"^[A-Za-z0-9\-]{1,20}$")
        self.dialog.txtParcela.setValidator(
            QRegularExpressionValidator(regex_parcela, self.dialog)
        )

        # Validador para decimales positivos (Humedad)
        regex_humedad = QRegularExpression(r"^\d{1,3}(\.\d{1,2})?$")
        self.dialog.txtHumedad.setValidator(
            QRegularExpressionValidator(regex_humedad, self.dialog)
        )

        # Validador para decimales con signo opcional (Temperatura)
        regex_temp = QRegularExpression(r"^-?\d{1,2}(\.\d{1,2})?$")
        self.dialog.txtTemperatura.setValidator(
            QRegularExpressionValidator(regex_temp, self.dialog)
        )

    def guardar(self):
        parcela = self.dialog.txtParcela.text()
        humedad = self.dialog.txtHumedad.text()
        temperatura = self.dialog.txtTemperatura.text()

        try:
            mensaje_alerta = self.controller.guardar_lectura(
                parcela, humedad, temperatura
            )

            if "ALERTA" in mensaje_alerta:
                QMessageBox.warning(
                    self.dialog, "Resultado de Evaluación", mensaje_alerta
                )
            else:
                QMessageBox.information(
                    self.dialog, "Resultado de Evaluación", mensaje_alerta
                )

            self.dialog.accept()
        except ReglaNegocioError as e:
            QMessageBox.warning(self.dialog, "Validación", str(e))
        except Exception as e:
            QMessageBox.critical(self.dialog, "Error del Sistema", str(e))
