from django.db import models
from pedido.models import Pedido


class PagamentoMercadoPago(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE,
                               related_name='pagamento_mercado_pago_pedido', default=1)
    transaction_amount = models.DecimalField(
        "Valor da Transação", max_digits=10, decimal_places=2, default=9.99
    )
    installments = models.PositiveSmallIntegerField("Parcelas", default=1)
    payment_method_id = models.CharField(
        "Método de Pagamento", max_length=250, default='master')
    mercado_pago_id = models.CharField(
        default=1, max_length=250, blank=True, db_index=True)
    mercado_pago_status = models.CharField(
        max_length=250, blank=True, default='approved')
    mercado_pago_status_detail = models.CharField(
        max_length=250, blank=True, default='accredited')
    created_at = models.DateField('Criado em', auto_now_add=True)
    updated_at = models.DateField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'pagamento_mercado_pago'
        verbose_name_plural = 'Pagamentos do MP'
        verbose_name = 'Pagamento do MP'

    def __str__(self):
        return self.pedido
