import sys
from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QInputDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from database_connection import DatabaseConnection  # Asegúrate de tener esta clase de conexión a la base de datos


class DentalView(QWebEngineView):
    def __init__(self, paciente_id):
        super().__init__()
        self.paciente_id = paciente_id

        
        self.channel = QWebChannel()
        self.channel.registerObject("backend", self)  
        self.page().setWebChannel(self.channel)

        # Carga la interfaz HTML
        file_path = "D:/CRISTIAN/PRUEBA/dental_view.html"  
        self.load(QUrl(f"file:///{file_path}"))

    @pyqtSlot()  
    def cargar_datos_dentales(self):
        """Carga datos desde la base de datos para inicializar los dientes."""
        try:
            with DatabaseConnection() as db_conn:
                connection = db_conn.get_connection()
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT diente, cara, estado FROM caries_arreglos WHERE paciente_id = %s",
                    (self.paciente_id,)
                )
                datos = cursor.fetchall()
                cursor.close()
                return datos
        except Exception as e:
            print(f"Error al cargar datos dentales: {e}")
            return []

    @pyqtSlot()  
    def guardar_datos_dentales(self, datos):
        """Guarda los datos enviados desde JavaScript en la base de datos."""
        try:
            with DatabaseConnection() as db_conn:
                connection = db_conn.get_connection()
                cursor = connection.cursor()
                cursor.execute("DELETE FROM caries_arreglos WHERE paciente_id = %s", (self.paciente_id,))
                for diente, estado in datos:
                    cursor.execute(""" 
                        INSERT INTO caries_arreglos (paciente_id, diente, estado)
                        VALUES (%s, %s, %s)
                    """, (self.paciente_id, diente, estado))
                connection.commit()
                cursor.close()
        except Exception as e:
            print(f"Error al guardar datos dentales: {e}")


class VentanaPrincipal(QMainWindow):
    def __init__(self, paciente_id):
        super().__init__()
        self.paciente_id = paciente_id
        self.setWindowTitle(f"Ficha Dental - Paciente {paciente_id}")
        self.setGeometry(100, 100, 1300, 600)

        # Configuración del diseño principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Vista dental interactiva
        self.dental_view = DentalView(paciente_id)
        layout.addWidget(self.dental_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Solicitar ID del paciente
    paciente_id, ok = QInputDialog.getInt(None, "ID Paciente", "Introduce el ID del paciente:")
    if not ok:
        sys.exit(0)

    ventana = VentanaPrincipal(paciente_id)
    ventana.show()
    sys.exit(app.exec_())
