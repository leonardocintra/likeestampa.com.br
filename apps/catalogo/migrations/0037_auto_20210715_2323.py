# Generated by Django 3.2.5 on 2021-07-16 02:23

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0036_remove_tipovariacao_sku_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='imagem_design',
            field=cloudinary.models.CloudinaryField(default='NAO_INFORMADO', max_length=255, verbose_name='Imagem design'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='imagem_principal',
            field=cloudinary.models.CloudinaryField(default='NAO_INFORMADO', max_length=255, verbose_name='Imagem principal'),
        ),
    ]