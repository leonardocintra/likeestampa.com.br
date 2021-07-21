from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from localflavor.br.models import BRCPFField, BRStateField, BRPostalCodeField


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = BRCPFField("CPF")
    telefone = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return self.user.first_name


class EnderecoCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cep = BRPostalCodeField()
    endereco = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    cidade = models.CharField(max_length=100)
    uf = BRStateField()
    bairro = models.CharField(max_length=100)
    complemento = models.CharField(max_length=50)
    referencia = models.CharField(max_length=100)
    pais = models.CharField(max_length=60, default='Brasil')
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'endereco_cliente'

    def __str__(self):
        return self.endereco


@receiver(post_save, sender=User)
def create_user_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_cliente(sender, instance, **kwargs):
#     instance.cliente.save()

# https://stackoverflow.com/questions/12303478/how-to-customize-user-profile-when-using-django-allauth
