# Generated by Django 3.2.7 on 2021-10-18 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroDeSerie', models.CharField(max_length=30)),
                ('info', models.CharField(blank=True, max_length=300, null=True)),
                ('enActivo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apelidos', models.CharField(max_length=200)),
                ('nome', models.CharField(max_length=200)),
                ('nivel', models.CharField(choices=[('S1', '1º ESO'), ('S2', '2º ESO'), ('S3', '3º ESO'), ('S4', '4º ESO'), ('PR', 'Profesor'), ('eA', 'Exalumno'), ('eP', 'Exprofesor')], max_length=2)),
                ('curso', models.CharField(blank=True, max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Asignacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_ini', models.DateTimeField(auto_now_add=True)),
                ('data_fin', models.DateTimeField(blank=True, null=True)),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lista_usuarios', to='inventario.equipo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lista_equipos', to='inventario.usuario')),
            ],
        ),
    ]
