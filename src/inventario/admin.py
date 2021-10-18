from django.contrib import admin

from .models import Usuario, Equipo, Asignacion

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    pass

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    pass

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    pass
