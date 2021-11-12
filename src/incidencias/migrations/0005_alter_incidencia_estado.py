# Generated by Django 3.2.7 on 2021-11-08 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidencias', '0004_alter_incidencia_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidencia',
            name='estado',
            field=models.CharField(choices=[('AC', 'Require Acción'), ('EF', 'Espera Familias'), ('ET', 'Espera Servicio Técnico'), ('PE', 'Pechada')], default='AC', max_length=2),
        ),
    ]
