# Generated by Django 4.0.4 on 2022-04-28 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0064_cormodelo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categoria',
            new_name='TipoProduto',
        ),
        migrations.AlterModelOptions(
            name='tipoproduto',
            options={'ordering': ('-created_at',), 'verbose_name': 'Tipo produto'},
        ),
        migrations.AlterModelTable(
            name='tipoproduto',
            table='tipo_produto',
        ),
    ]