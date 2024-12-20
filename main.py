import sys
from PyQt5.QtCore import QUrl, pyqtSlot, pyqtProperty, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QInputDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWebChannel import QWebChannel
from database_connection import DatabaseConnection  # Asegúrate de tener esta clase implementada correctamente
from datetime import datetime  # Importar para la fecha actual

class DentalView(QWebEngineView):
    # Definir una señal para cuando el valor de id_persona cambie
    idPersonaChanged = pyqtSignal()

    def __init__(self, id_persona):
        super().__init__()
        self._id_persona = id_persona  # Usamos una propiedad privada para id_persona

        # Configuración del canal web
        self.channel = QWebChannel()
        self.channel.registerObject("backend", self)
        self.page().setWebChannel(self.channel)

        # Carga la interfaz HTML
        file_path = "D:/CRISTIAN/PRUEBA/dental_view.html"
        self.load(QUrl(f"file:///{file_path}"))

    @pyqtProperty(int, notify=idPersonaChanged)
    def id_persona(self):
        """Propiedad del ID de la persona."""
        return self._id_persona

    @id_persona.setter
    def id_persona(self, value):
        if self._id_persona != value:
            self._id_persona = value
            self.idPersonaChanged.emit()  

    @pyqtSlot(result=list)
    def cargar_datos_dentales(self):
        """Carga datos desde la base de datos para inicializar los dientes."""
        cursor = None
        connection = None
        try:
            db_conn = DatabaseConnection()  # Instancia manual de DatabaseConnection
            connection = db_conn.get_connection()
            cursor = connection.cursor()

            # Verificar si la ficha existe, si no, crearla
            cursor.execute("SELECT id FROM ficha_catastral WHERE id_persona = ?", (self._id_persona,))
            ficha = cursor.fetchone()

            if not ficha:  # Si no existe, crear la ficha
                print(f"Ficha no encontrada para la persona {self._id_persona}. Creando ficha...")
                fecha_realizacion = datetime.now().strftime('%Y-%m-%d')  # Fecha actual
                cursor.execute(
                    """INSERT INTO ficha_catastral (id_persona, fecha_realizacion)
                        VALUES (?, ?)""", (self._id_persona, fecha_realizacion)
                )
                connection.commit()

                # Obtener el ID de la nueva ficha
                cursor.execute("SELECT id FROM ficha_catastral WHERE id_persona = ?", (self._id_persona,))
                ficha = cursor.fetchone()  # Ahora tenemos el ID de la ficha recién creada

            # Cargar los datos dentales
            cursor.execute(
            """SELECT id_diente, 
                    estado_oclusal, 
                    estado_vestibular, 
                    estado_distal, 
                    estado_palatino, 
                    estado_mesial, 
                    estado_general
            FROM ficha_catastral_items 
            WHERE FICHA_CAT_ID = ?""",
            (ficha[0],)
        )
            datos = cursor.fetchall()
            
            # Imprimir los datos para verificar
            print(f"Datos recuperados: {datos}")
            print(f"ID de ficha: {ficha}")  # Verifica el ID de la ficha

            
            return [list(row) for row in datos]  # Convertir a lista compatible con JSON
        except Exception as e:
            print(f"Error al cargar datos dentales: {e}")
            return []
        finally:
            # Asegurarse de que cursor y connection sean cerrados si fueron creados
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @pyqtSlot(list)
    def guardar_datos_dentales(self, datos):
        """Guarda los datos enviados desde JavaScript en la base de datos sin eliminar los existentes."""
        print(f"Datos recibidos para guardar: {datos}")
        cursor = None
        connection = None
        try:
            db_conn = DatabaseConnection()  # Instancia manual de DatabaseConnection
            connection = db_conn.get_connection()
            cursor = connection.cursor()
            print("Conexión a la base de datos establecida.")

            # Verificar si la ficha existe, si no, crearla
            cursor.execute("SELECT id FROM ficha_catastral WHERE id_persona = ?", (self._id_persona,))
            ficha = cursor.fetchone()

            if not ficha:  # Si no existe, crear la ficha
                print(f"Ficha no encontrada para la persona {self._id_persona}. Creando ficha...")
                fecha_realizacion = datetime.now().strftime('%Y-%m-%d')  # Fecha actual
                cursor.execute(
                    """INSERT INTO ficha_catastral (id_persona, fecha_realizacion)
                    VALUES (?, ?)""", (self._id_persona, fecha_realizacion)
                )
                connection.commit()
                ficha = (cursor.lastrowid,)  # Obtener el ID de la nueva ficha recién creada

            # Lista de dientes válidos según los números proporcionados
            dientes_validos = [
                                "18", "17", "16", "15", "14", "13", "12", "11",
                                "21", "22", "23", "24", "25", "26", "27", "28",
                                "48", "47", "46", "45", "44", "43", "42", "41",
                                "31", "32", "33", "34", "35", "36", "37", "38"
                            ]

            # Insertar o actualizar los datos de los dientes y sus estados
            for diente in datos:
                print(f"Diente recibido: {diente}")
                if len(diente) == 3:  # Completar con valores por defecto si faltan
                    diente.extend([None, None, None, None])  # Agregar los valores faltantes

                if len(diente) == 7:  # Asegúrate de que haya 7 elementos por cada diente
                    nombre_diente, estado_oclusal, estado_vestibular, estado_distal, estado_palatino, estado_mesial, estado_general = diente

                    # Convertir el nombre del diente a su número correspondiente
                    if nombre_diente.startswith("Inferior") or nombre_diente.startswith("Superior"):
                        # Extraer el número del diente (por ejemplo: "Inferior 18" -> 18)
                        try:
                            numero_diente = int(nombre_diente.split()[-1])  # Extrae el número del nombre
                        except ValueError:
                            print(f"Advertencia: El nombre del diente no tiene un número válido: {nombre_diente}")
                            continue  # Ignorar esta fila si el nombre del diente no tiene un número válido

                        # Verificar si el diente es válido
                        if str(numero_diente) in dientes_validos:
                            # Si el diente es válido, proceder con la actualización o inserción
                            cursor.execute(
                                """SELECT id FROM ficha_catastral_items 
                                WHERE FICHA_CAT_ID = ? AND ID_DIENTE = ?""",
                                (ficha[0], numero_diente)
                            )
                            existing_item = cursor.fetchone()

                            if existing_item:
                                # Si el diente ya existe, actualizar su estado
                                cursor.execute(
                                    """UPDATE ficha_catastral_items
                                    SET ESTADO_OCLUSAL = ?, ESTADO_VESTIBULAR = ?, 
                                        ESTADO_DISTAL = ?, ESTADO_PALATINO = ?, 
                                        ESTADO_MESIAL = ?, ESTADO_GENERAL = ?
                                    WHERE FICHA_CAT_ID = ? AND ID_DIENTE = ?""",
                                    (estado_oclusal, estado_vestibular, estado_distal,
                                    estado_palatino, estado_mesial, estado_general, ficha[0], numero_diente)
                                )
                            else:
                                # Si el diente no existe, insertar un nuevo registro
                                cursor.execute(
                                    """INSERT INTO ficha_catastral_items (
                                        FICHA_CAT_ID, ID_DIENTE, ESTADO_OCLUSAL, ESTADO_VESTIBULAR, 
                                        ESTADO_DISTAL, ESTADO_PALATINO, ESTADO_MESIAL, ESTADO_GENERAL)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                    (ficha[0], numero_diente, estado_oclusal, estado_vestibular, estado_distal, estado_palatino, estado_mesial, estado_general)
                                )
                                print(f"Datos insertados: {ficha[0]}, {numero_diente}, {estado_oclusal}, {estado_vestibular}, {estado_distal}, {estado_palatino}, {estado_mesial}, {estado_general}")
                        else:
                            print(f"Advertencia: Diente no válido: {nombre_diente}")
                            continue  # Si el diente no está en los válidos, ignorarlo
                    else:
                        print(f"Advertencia: Diente no reconocido: {nombre_diente}")
                        continue  # Si el nombre del diente no es reconocido, ignorarlo
                else:
                    print(f"Advertencia: La fila no tiene 7 valores: {diente}")

            connection.commit()
            print("Datos guardados en la base de datos.")
        except Exception as e:
            print(f"Error al guardar datos dentales: {e}")
        finally:
            # Asegurarse de que cursor y connection sean cerrados si fueron creados
            if cursor:
                cursor.close()
            if connection:
                connection.close()








class VentanaPrincipal(QMainWindow):
    def __init__(self, id_persona):
        super().__init__()
        self.setWindowTitle(f"Ficha Dental - Persona {id_persona}")
        self.setGeometry(100, 100, 1300, 600)

        # Configuración del diseño principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Vista dental interactiva
        self.dental_view = DentalView(id_persona)
        layout.addWidget(self.dental_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Solicitar ID de la persona
    id_persona, ok_persona = QInputDialog.getInt(None, "ID Persona", "Introduce el ID de la persona:")

    if not ok_persona:
        sys.exit(0)

    ventana = VentanaPrincipal(id_persona)
    ventana.show()
    sys.exit(app.exec_())
