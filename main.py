import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from src.views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
        ventana = MainWindow()
        ventana.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(
            None,
            "Error Crítico - AgroExporta Olmos",
            f"No se pudo iniciar la aplicación:\n{str(e)}",
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
