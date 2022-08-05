from django.apps import AppConfig
from django.core import management

class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventario'

    def ready(self):
        management.call_command('dbbackup')
        management.call_command('mediabackup')
        return True
