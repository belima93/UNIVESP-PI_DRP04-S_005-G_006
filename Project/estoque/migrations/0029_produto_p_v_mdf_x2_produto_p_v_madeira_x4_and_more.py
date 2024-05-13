# Generated by Django 5.0.4 on 2024-05-13 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0028_produto_custo_final_produto_lucro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='P_V_MDF_x2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='P_V_Madeira_x4',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='P_V_Terc',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='custo_da_madeira',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='fundo_total_x4',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
