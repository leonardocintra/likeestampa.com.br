from django.urls import path
from . import views

app_name = 'usuario'

urlpatterns = [
    path('', views.cliente, name='cliente'),
    path('alterar/<int:pk>', views.cliente_update, name='cliente_update'),
]
