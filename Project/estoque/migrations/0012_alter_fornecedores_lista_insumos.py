# Generated by Django 5.0.4 on 2024-05-05 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0011_fornecedores_mercadoria_slug_materiaprima_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fornecedores',
            name='lista_insumos',
            field=models.ManyToManyField(blank=True, related_name='fornecedores_rel', to='estoque.materiaprima'),
        ),
    ]
