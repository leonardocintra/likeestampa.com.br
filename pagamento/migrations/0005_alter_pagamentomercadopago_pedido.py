# Generated by Django 3.2.4 on 2021-06-23 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0003_auto_20210622_2244'),
        ('pagamento', '0004_auto_20210620_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagamentomercadopago',
            name='pedido',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pagamento_mercado_pago_pedido', to='pedido.pedido'),
        ),
    ]