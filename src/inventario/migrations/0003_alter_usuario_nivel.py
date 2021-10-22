# Generated by Django 3.2.7 on 2021-10-22 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_asignacion_manual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='nivel',
            field=models.CharField(choices=[('S1', '1º ESO'), ('S2', '2º ESO'), ('S3', '3º ESO'), ('S4', '4º ESO'), ('PR', 'Profesor'), ('eA', 'Exalumno'), ('eP', 'Exprofesor'), ('CE', 'Centro')], max_length=2),
        ),
    ]
