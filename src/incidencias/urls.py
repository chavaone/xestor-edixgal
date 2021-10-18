from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('incidencia/lista', login_required(views.listaIncidencias), name='lista-incidencias'),
    path('incidencia/crear', login_required(views.VistaCreacionIncidencia.as_view()), name='crear-incidencia' ),
    path('incidencia/eliminar/<int:pk>', login_required(views.VistaBorradoIncidencia.as_view()), name='eliminar-incidencia'),
    path('incidencia/ver/<int:pk>', login_required(views.vistaIncidencia), name='vista-incidencia'),
    path('incidencia/abrircerrar/<int:pk>', login_required(views.cambiarEstadoIncidencia), name='cambiar-estado-incidencia'),
    path('incidencia/comentario/crear', login_required(views.engadirComentario), name='crear-comentario'),
    path('incidencia/comentario/eliminar/<int:pk>', login_required(views.VistaBorradoComentario.as_view()), name='eliminar-comentario'),
]
