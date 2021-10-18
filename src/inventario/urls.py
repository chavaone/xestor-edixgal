from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('equipo/lista', login_required(views.listaEquipos), name='lista-equipos'),
    path('equipo/crear', login_required(views.VistaCreacionEquipo.as_view()), name='crear-equipo' ),
    path('equipo/ver/<int:pk>', login_required(views.vistaEquipo), name='vista-equipo'),
    path('equipo/eliminar/<int:pk>', login_required(views.VistaBorradoEquipo.as_view()), name='eliminar-equipo'),
    path('equipo/editar/<int:pk>', login_required(views.VistaEdicionEquipo.as_view()), name='editar-equipo'),
    path('equipo/cambiar-estado/<int:pk>', login_required(views.cambiarEstadoEquipo), name='cambiar-estado-equipo'),
    path('asignar/', login_required(views.VistaCreacionAsignacion.as_view()), name='asignar-equipo'),
    path('asignar/terminar/<int:pk>', login_required(views.terminarAsignacion), name='terminar-asignacion'),
    path('usuario/lista', login_required(views.listaUsuarios), name='lista-usuarios'),
    path('usuario/crear', login_required(views.VistaCreacionUsuario.as_view()), name='crear-usuario'),
    path('usuario/ver/<int:pk>', login_required(views.vistaUsuario), name='vista-usuario'),
    path('usuario/eliminar/<int:pk>', login_required(views.VistaBorradoUsuario.as_view()), name='eliminar-usuario'),
    path('usuario/editar/<int:pk>', login_required(views.VistaEdicionUsuario.as_view()), name='editar-usuario'),
    path('usuario/baixa/<int:pk>', login_required(views.darDeBaixaUsuario), name='baixa-usuario')
]
