
from django.urls import path
from . import views

app_name = 'pagamento'

urlpatterns = [
    path('', views.pagamento, name='pagamento'),
    path('process_payment/', views.process_payment, name='process_payment')
    # path('webhook/', None, name='webhook'),
]
