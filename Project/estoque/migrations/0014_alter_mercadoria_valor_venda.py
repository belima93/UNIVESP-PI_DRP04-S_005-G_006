# Generated by Django 5.0.4 on 2024-05-05 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0013_alter_mercadoria_valor_venda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mercadoria',
            name='valor_venda',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
