# Generated by Django 3.2.7 on 2021-10-22 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidencias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidencia',
            name='numServizoExterno',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='incidencia',
            name='tipoServizoExterno',
            field=models.CharField(blank=True, choices=[('U', 'Unidade de Atención a Centros'), ('P', 'Servizo Premium EDIXGAL')], max_length=1, null=True),
        ),
    ]