# Generated by Django 3.2.7 on 2021-10-18 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Incidencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aberta', models.BooleanField(default=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('equipo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.equipo')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='ComentarioIncidencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricion', models.CharField(max_length=400)),
                ('ficheiro', models.FileField(blank=True, null=True, upload_to='comentario/%Y/%m/%d/')),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('incidencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incidencias.incidencia')),
            ],
        ),
    ]
