# Generated by Django 3.2.5 on 2021-07-13 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0032_produto_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipovariacao',
            name='preco_variacao',
            field=models.DecimalField(decimal_places=2, default=51.9, max_digits=10, verbose_name='Preço'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='preco_base',
            field=models.DecimalField(decimal_places=2, default=51.9, max_digits=10, verbose_name='Preço base'),
        ),
    ]
