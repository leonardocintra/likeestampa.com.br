
from django.urls import path
from .views import AboutView, TermosDeUsoView, TrocaCancelamentoView
from catalogo import views

app_name = 'core'

urlpatterns = [
    path('', views.product_list.as_view(), name='index'),
    path('quem-somos', AboutView.as_view(), name='about'),
    path('troca-e-cancelamento', TrocaCancelamentoView.as_view(), name='trocacancelamento'),
    path('termos-de-uso', TermosDeUsoView.as_view(), name='termos'),
]