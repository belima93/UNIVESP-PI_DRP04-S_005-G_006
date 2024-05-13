# Generated by Django 5.0.4 on 2024-05-06 00:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0015_alter_imagem_produto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagem',
            name='produto',
        ),
        migrations.AddField(
            model_name='imagem',
            name='materia_prima',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='estoque.materiaprima'),
        ),
    ]