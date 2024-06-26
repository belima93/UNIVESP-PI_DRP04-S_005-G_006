# Generated by Django 5.0.4 on 2024-05-04 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0006_alter_produto_id_material'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Produto',
            new_name='MateriaPrima',
        ),
        migrations.RenameField(
            model_name='imagem',
            old_name='produto',
            new_name='materiaprima',
        ),
        migrations.AlterField(
            model_name='imagem',
            name='imagem',
            field=models.ImageField(upload_to='imagem_materiaprima'),
        ),
    ]
