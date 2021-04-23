
from django.urls import path
from catalogo import views

app_name = 'core'

urlpatterns = [
    path('', views.product_list.as_view(), name='index'),
]