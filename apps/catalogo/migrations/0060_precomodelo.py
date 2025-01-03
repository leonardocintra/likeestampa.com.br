# Generated by Django 3.2.9 on 2021-11-27 15:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0059_auto_20211012_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrecoModelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, default=51.9, max_digits=10, verbose_name='Valor')),
                ('ativo', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('modelo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogo.modelo')),
            ],
            options={
                'verbose_name': 'Preço por demolo',
                'verbose_name_plural': 'Preços por modelo',
                'db_table': 'preco_modelo',
                'ordering': ('created_at',),
            },
        ),
    ]
