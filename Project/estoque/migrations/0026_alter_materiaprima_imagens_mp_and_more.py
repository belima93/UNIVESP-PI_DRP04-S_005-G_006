# Generated by Django 5.0.4 on 2024-05-11 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0025_rename_fornecedor_materiaprima_fornecedores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materiaprima',
            name='imagens_MP',
            field=models.ImageField(blank=True, upload_to='imagem_materiaprima/'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='imagens_produto',
            field=models.ImageField(blank=True, upload_to='imagem_produto/'),
        ),
    ]
