# Generated by Django 4.1 on 2022-08-30 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidencias', '0005_alter_incidencia_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidencia',
            name='aberta',
        ),
    ]
