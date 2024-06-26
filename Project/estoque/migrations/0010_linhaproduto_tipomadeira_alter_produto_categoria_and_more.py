# Generated by Django 5.0.4 on 2024-05-05 03:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0009_remove_imagem_materiaprima_alter_imagem_imagem_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinhaProduto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linha', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='TipoMadeira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=40)),
            ],
        ),
        migrations.AlterField(
            model_name='produto',
            name='categoria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='estoque.categoria'),
        ),
        migrations.CreateModel(
            name='Mercadoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_produto', models.CharField(default='', max_length=7)),
                ('nomenclatura', models.CharField(default='', max_length=255)),
                ('quantidade', models.IntegerField()),
                ('comprimento_M', models.DecimalField(decimal_places=2, max_digits=10)),
                ('altura_M', models.DecimalField(decimal_places=2, max_digits=10)),
                ('m2', models.DecimalField(decimal_places=3, max_digits=10)),
                ('valor_m2', models.DecimalField(decimal_places=2, max_digits=10)),
                ('custo_madeira', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('P_V_madeira_4x', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('fundo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fundo_total_x4', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('custo_MDF', models.DecimalField(decimal_places=2, max_digits=10)),
                ('P_V_MDF', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('tercerizacao', models.DecimalField(decimal_places=2, max_digits=10)),
                ('P_V_Terc', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('corte', models.DecimalField(decimal_places=2, max_digits=10)),
                ('montagem', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lixa', models.DecimalField(decimal_places=2, max_digits=10)),
                ('acabamento_pintura', models.DecimalField(decimal_places=2, max_digits=10)),
                ('custo_final', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('valor_sugerido', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('valor_venda', models.DecimalField(decimal_places=2, max_digits=10)),
                ('lucro', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='estoque.categoria')),
                ('linha_produto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='estoque.linhaproduto')),
                ('tipo_madeira', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='estoque.tipomadeira')),
            ],
        ),
    ]
