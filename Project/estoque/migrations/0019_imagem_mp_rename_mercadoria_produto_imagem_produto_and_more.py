# Generated by Django 5.0.4 on 2024-05-06 18:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0018_materiaprima_imagens'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imagem_MP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='imagem_materiaprima')),
                ('materia_prima', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='estoque.materiaprima')),
            ],
        ),
        migrations.RenameModel(
            old_name='Mercadoria',
            new_name='Produto',
        ),
        migrations.CreateModel(
            name='Imagem_Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='imagem_produto')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='estoque.produto')),
            ],
        ),
        migrations.DeleteModel(
            name='Imagem',
        ),
    ]
