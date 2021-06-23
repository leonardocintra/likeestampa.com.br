from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from localflavor.br.models import BRCPFField


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = BRCPFField("CPF")
    peoplesoft_id = models.PositiveIntegerField(null=True)
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'cliente'

    def __str__(self):
        return self.user.first_name


@receiver(post_save, sender=User)
def create_user_cliente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_cliente(sender, instance, **kwargs):
#     instance.cliente.save()

# https://stackoverflow.com/questions/12303478/how-to-customize-user-profile-when-using-django-allauth
