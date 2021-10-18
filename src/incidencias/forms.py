from django.forms import ModelForm, HiddenInput, Textarea
from .models import ComentarioIncidencia

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
