from django.forms import ModelForm, HiddenInput, Textarea, RadioSelect
from .models import ComentarioIncidencia, Incidencia

class ComentarioIncidenciaForm(ModelForm):
     class Meta:
         model = ComentarioIncidencia
         fields = [
            'incidencia',
            'descricion',
            'ficheiro'
         ]

         widgets = {
            'incidencia': HiddenInput(),
            'descricion': Textarea(attrs={"rows":5}),
        }


class EstadoIncidenciaForm(ModelForm):
     class Meta:
         model = Incidencia
         fields = [
            'estado',
         ]

         widgets = {
            'estado': RadioSelect(),
        }
