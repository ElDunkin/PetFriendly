import os
from datetime import datetime
try:
    import pytz
    USE_PYTZ = True
except ImportError:
    USE_PYTZ = False

class LogSystem:
    def __init__(self, log_file='log.txt'):
        self.log_file = log_file
        if USE_PYTZ:
            self.timezone = pytz.timezone('America/Bogota')
        else:
            # Fallback sin pytz
            self.timezone = None

    def log_action(self, usuario, accion, tabla_afectada, detalles=None, id_registro=None):
        """
        Registra una acción en el archivo de log

        Args:
            usuario (str): Nombre del usuario que realizó la acción
            accion (str): Tipo de acción (INSERT, UPDATE, DELETE, etc.)
            tabla_afectada (str): Nombre de la tabla/modulo afectado
            detalles (str, optional): Detalles adicionales de la acción
            id_registro (str, optional): ID del registro afectado
        """
        try:
            # Obtener fecha y hora actual en zona horaria de Colombia
            if USE_PYTZ and self.timezone:
                now = datetime.now(self.timezone)
            else:
                # Fallback usando UTC sin conversión de zona horaria
                now = datetime.utcnow()
            fecha = now.strftime('%Y-%m-%d')
            hora = now.strftime('%H:%M:%S')

            # Crear entrada de log
            log_entry = f"[{fecha} {hora}] USUARIO: {usuario} | ACCION: {accion} | TABLA: {tabla_afectada}"

            if id_registro:
                log_entry += f" | ID_REGISTRO: {id_registro}"

            if detalles:
                log_entry += f" | DETALLES: {detalles}"

            log_entry += "\n"

            # Escribir en el archivo de log
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

        except Exception as e:
            print(f"Error al escribir en el log: {e}")

    def log_insert(self, usuario, tabla, id_registro=None, detalles=None):
        """Registra una inserción"""
        self.log_action(usuario, "INSERT", tabla, detalles, id_registro)

    def log_update(self, usuario, tabla, id_registro=None, detalles=None):
        """Registra una actualización"""
        self.log_action(usuario, "UPDATE", tabla, detalles, id_registro)

    def log_delete(self, usuario, tabla, id_registro=None, detalles=None):
        """Registra una eliminación"""
        self.log_action(usuario, "DELETE", tabla, detalles, id_registro)

    def log_login(self, usuario, detalles=None):
        """Registra un inicio de sesión"""
        self.log_action(usuario, "LOGIN", "sistema", detalles)

    def log_logout(self, usuario, detalles=None):
        """Registra un cierre de sesión"""
        self.log_action(usuario, "LOGOUT", "sistema", detalles)

    def get_logs(self, limit=100):
        """Obtiene las últimas entradas del log"""
        try:
            if not os.path.exists(self.log_file):
                return []

            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Retornar las últimas 'limit' líneas
            return lines[-limit:] if len(lines) > limit else lines

        except Exception as e:
            print(f"Error al leer el log: {e}")
            return []

# Instancia global del sistema de logging
log_system = LogSystem()