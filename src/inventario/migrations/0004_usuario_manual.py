# Generated by Django 4.1 on 2022-09-19 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_alter_usuario_nivel'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='manual',
            field=models.BooleanField(default=False),
        ),
    ]
