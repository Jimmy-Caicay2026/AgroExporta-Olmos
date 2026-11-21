import os
from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QColor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDialog, QHeaderView, QMainWindow, QMessageBox, QTableWidgetItem
from src.controller.sensor_controller import SensorController
from src.views.dialog_sensor import DialogSensor


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.controller = SensorController()
        self.cargar_ui()

        # Ajustar columnas de la tabla
        self.ui.tblSensores.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.ui.tblSensores.setColumnHidden(0, True)  # Oculta columna ID

        # Eventos
        self.ui.btnNuevo.clicked.connect(self.abrir_nuevo)
        self.ui.txtBuscar.textChanged.connect(
            self.cargar_datos
        )  # Búsqueda en tiempo real

        self.cargar_datos()

    def cargar_ui(self):
        ruta_ui = os.path.join(
            os.path.dirname(__file__), "ui", "main_window.ui"
        )
        archivo_ui = QFile(ruta_ui)
        archivo_ui.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.ui = loader.load(archivo_ui, self)
        archivo_ui.close()

        self.setWindowTitle(self.ui.windowTitle())
        self.resize(self.ui.size())
        self.setCentralWidget(self.ui.centralwidget)

    def cargar_datos(self):
        filtro = self.ui.txtBuscar.text()
        try:
            registros = self.controller.obtener_lecturas(filtro)
            self.ui.tblSensores.setRowCount(0)

            for fila_idx, datos in enumerate(registros):
                self.ui.tblSensores.insertRow(fila_idx)
                for col_idx, valor in enumerate(datos):
                    item = QTableWidgetItem(str(valor))
                    item.setTextAlignment(Qt.AlignCenter)

                    # Guardar ID oculto en data(99) según objetivo de la guía
                    if col_idx == 1:
                        item.setData(99, datos[0])

                    # Resaltar visualmente la columna de alerta
                    if col_idx == 4:
                        if "URGENTE" in str(valor):
                            item.setBackground(QColor("#ffcdd2"))  # Rojo suave
                        elif "EXCESO" in str(valor):
                            item.setBackground(
                                QColor("#fff9c4")
                            )  # Amarillo suave
                        else:
                            item.setBackground(
                                QColor("#c8e6c9")
                            )  # Verde suave

                    self.ui.tblSensores.setItem(fila_idx, col_idx, item)
        except Exception as e:
            QMessageBox.critical(self, "Error de Conexión", str(e))

    def abrir_nuevo(self):
        dialogo = DialogSensor(self)
        if dialogo.exec() == QDialog.Accepted:
            self.cargar_datos()
