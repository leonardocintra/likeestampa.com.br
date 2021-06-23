from django.urls import path
from . import views

app_name = 'pagamento'

urlpatterns = [
    path('', views.pagamento, name='pagamento'),
    # path('webhook/', None, name='webhook'),
]
