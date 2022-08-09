from django.test import TestCase
from django.contrib.auth.models import User
from apps.usuario.models import Cliente
from apps.usuario.admin import ClienteAdmin, admin


class ClienteAdminModelTest(TestCase):

    def setUp(self):
        User.objects.create_user(
            username='leonardo',
            first_name='Leonardo',
            email='leonardo@leonardo.com',
            password='123kkkuuu#')

        self.model_admin = ClienteAdmin(Cliente, admin.site)
