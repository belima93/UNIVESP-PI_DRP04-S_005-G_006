# Generated by Django 5.0.4 on 2024-05-01 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0003_remove_produto_nome_remove_produto_preco_compra_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='comprimento',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='produto',
            name='descricao',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='produto',
            name='id',
            field=models.CharField(max_length=7, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='produto',
            name='id_material',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='produto',
            name='largura',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='produto',
            name='valor_m2',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='produto',
            name='valor_peca',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
