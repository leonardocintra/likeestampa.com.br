
from django.urls import path
from .views import AboutView
from catalogo import views

app_name = 'core'

urlpatterns = [
    path('', views.product_list.as_view(), name='index'),
    path('quem-somos', AboutView.as_view(), name='about'),
]