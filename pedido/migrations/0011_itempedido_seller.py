# Generated by Django 3.2.5 on 2021-07-13 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0007_seller_ativo'),
        ('pedido', '0010_remove_pedido_frete_dimona_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='itempedido',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='seller.seller'),
        ),
    ]
