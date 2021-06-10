
from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('carrinho/', views.carrinho, name='carrinho'),
]
