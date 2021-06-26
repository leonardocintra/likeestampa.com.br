# Generated by Django 3.2.4 on 2021-06-24 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0025_modeloproduto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produtovariacao',
            name='produto',
        ),
        migrations.AddField(
            model_name='produtovariacao',
            name='modelo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variacao_modelo_produto', to='catalogo.modeloproduto'),
        ),
    ]
