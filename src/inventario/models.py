from django.db import models

class Usuario (models.Model):
    CURSOS = [
        ('S1', '1º ESO'),
        ('S2', '2º ESO'),
        ('S3', '3º ESO'),
        ('S4', '4º ESO'),
        ('PR', 'Profesor'),
        ('eA', 'Exalumno'),
        ('eP', 'Exprofesor'),
    ]
    apelidos = models.CharField(max_length=200)
    nome = models.CharField(max_length=200)
    nivel = models.CharField(max_length=2,choices=CURSOS)
    curso = models.CharField(max_length=1, blank=True)

    def __str__(self):
        return '%s, %s (%s%s)' %(self.apelidos, self.nome, self.nivel, self.curso)

class Equipo (models.Model):
    numeroDeSerie = models.CharField(max_length=30)
    info = models.CharField(
        max_length=300,
        blank=True,
        null=True)
    enActivo = models.BooleanField(default=True)

    def __str__(self):
        return '#%s' %(self.numeroDeSerie).upper()

class Asignacion (models.Model):
    usuario =  models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='lista_equipos'
        )
    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='lista_usuarios'
        )
    manual = models.BooleanField(default=False)
    data_ini = models.DateTimeField(auto_now_add=True)
    data_fin = models.DateTimeField(
            blank=True,
            null=True
    )
