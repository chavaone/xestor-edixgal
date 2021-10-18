from django.urls import path
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('cargar/login/', TemplateView.as_view(template_name='login-cargar-datos.html'), name='login-cargar-datos-xestor'),
    path('cargar/', views.cargarDatosXestor, name='cargar-datos-xestor'),
]
