#../config.py
import json

def load_config(file_path="config.json"):
    with open(file_path, "r") as config_file:
        return json.load(config_file)

config = load_config()  # Carga la configuración por defecto desde config.json

# Ahora puedes acceder a las configuraciones de base de datos y correo
database_config = config["database"]
email_config = config["email"]

# Ejemplo de acceso a la configuración de la base de datos
database_host = database_config["host"]
database_path = database_config["database_path"]
database_user = database_config["user"]
database_password = database_config["password"]
database_role = database_config["role"]
database_port = database_config["port"]

smtp_server = email_config["smtp_server"]
smtp_port = email_config["smtp_port"]
smtp_username = email_config["smtp_username"]
smtp_password = email_config["smtp_password"]



