from django.db import models
from inventario.models import Equipo, Usuario, Asignacion
import re

class Incidencia (models.Model):
    SERVIZOS = [
        ('U', 'Unidade de Atención a Centros'),
        ('P', 'Servizo Premium EDIXGAL')
    ]
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
    tipoServizoExterno = models.CharField(
        max_length=1,
        choices=SERVIZOS,
        blank=True,
        null=True
    )
    numServizoExterno = models.IntegerField(
        blank=True,
        null=True
    )
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

    def save(self, *args, **kwargs):

        if self.pk is None: #Se pk é None, entón é un obxecto novo
            regex = re.compile("([PD])([0-9]+)")
            match = regex.search(self.descricion)

            if match:
                self.incidencia.tipoServizoExterno = match.group(1)
                self.incidencia.numServizoExterno = match.group(2)
                self.incidencia.save()

        super(ComentarioIncidencia, self).save(*args, **kwargs)
