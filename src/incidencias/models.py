from django.db import models
from inventario.models import Equipo, Usuario, Asignacion

class Incidencia (models.Model):
    equipo = models.ForeignKey(
        Equipo,
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    usuario = models.ForeignKey(
        Usuario,
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    aberta = models.BooleanField(default=True)
    data = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk is None and not self.usuario and self.equipo:
            asignaciones = Asignacion.objects.filter(equipo=self.equipo).exclude(data_fin__isnull=False)
            if asignaciones:
                self.usuario = asignaciones[0].usuario
        super(Incidencia, self).save(*args, **kwargs)

class ComentarioIncidencia (models.Model):
    incidencia = models.ForeignKey(
        Incidencia,
        on_delete=models.CASCADE)
    descricion = models.CharField(max_length=400)
    ficheiro = models.FileField(
        upload_to='comentario/%Y/%m/%d/',
        blank=True,
        null=True,)
    data = models.DateTimeField(auto_now_add=True)
