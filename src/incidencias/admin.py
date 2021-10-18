from django.contrib import admin
from .models import Incidencia, ComentarioIncidencia

@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    pass

@admin.register(ComentarioIncidencia)
class ComentarioIncidenciaAdmin(admin.ModelAdmin):
    pass
