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
        ('CE', 'Centro'),
    ]
    apelidos = models.CharField(max_length=200)
    nome = models.CharField(max_length=200)
    nivel = models.CharField(max_length=2,choices=CURSOS)
    curso = models.CharField(max_length=1, blank=True)
    manual = models.BooleanField(default=False)

    def __str__(self):
        return '%s, %s (%s%s)' %(self.apelidos, self.nome, self.nivel, self.curso)

class Equipo (models.Model):
    TIPOS_EQUIPO = [
        ('EA', 'Equipo Alumnado'),
        ('EP', 'Equipo Profesorado'),
        ('EC', 'Equipo Clase'),
        ('PR', 'Proxector'),
        ('CA', 'Carro de carga'),
        ('PD', 'PDI'),
        ('PT', 'Pantalla táctil')
    ]

    numeroDeSerie = models.CharField(max_length=30, unique=True)
    tipo_equipo = models.CharField(max_length=2, choices=TIPOS_EQUIPO, default='EA')
    modelo = models.CharField(
        max_length=100,
        blank=True,
        null=True)
    info = models.CharField(
        max_length=300,
        blank=True,
        null=True)
    enActivo = models.BooleanField(default=True)
    manual = models.BooleanField(default=False)

    def __str__(self):
        return '#%s (%i)' %(self.numeroDeSerie.upper(), self.pk)

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
