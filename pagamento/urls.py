from django.urls import path
from . import views

app_name = 'pagamento'

urlpatterns = [
    path('', views.pagamento, name='pagamento'),
    path('webhook/', views.webhook , name='webhook'),
    path('mp_notifications', views.mp_notifications, name='mp_notifications'),
]
