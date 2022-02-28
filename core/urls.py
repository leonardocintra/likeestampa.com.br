
from django.urls import path
from .views import index, AboutView, TermosDeUsoView, TrocaCancelamentoView
from catalogo import views

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('quem-somos', AboutView.as_view(), name='about'),
    path('troca-e-cancelamento', TrocaCancelamentoView.as_view(), name='trocacancelamento'),
    path('termos-de-uso', TermosDeUsoView.as_view(), name='termos'),
]