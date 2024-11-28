import firebirdsql
import config

class DatabaseConnection:
    def __init__(self):
        self.connection = None

    def get_connection(self, user=None, password=None):
        if self.connection is None:
            self._connect(user, password)
        return self.connection

    def _connect(self, user=None, password=None):
        try:
            host = config.database_host
            database_path = config.database_path
            port = config.database_port
            role = config.database_role

            user = user or config.database_user
            password = password or config.database_password

            self.connection = firebirdsql.connect(
                host=host,
                database=database_path,
                user=user,
                password=password,
                port=port,
                role=role,
                isolation_level=firebirdsql.ISOLATION_LEVEL_READ_COMMITED
            )
            print("Conexión a la base de datos establecida.")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
                print("Conexión cerrada correctamente.")
            except Exception as e:
                print(f"Error al cerrar la conexión: {e}")
            finally:
                self.connection = None

    def __del__(self):
        self.close_connection()
