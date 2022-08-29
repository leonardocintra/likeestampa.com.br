from django.db import models
from apps.core.constants import TXT_CRIADO_EM
from apps.pedido.models import Pedido


class PagamentoMercadoPago(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE,
                               related_name='pagamento_mercado_pago_pedido', null=True)
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
    payment_id = models.PositiveBigIntegerField(null=True)
    created_at = models.DateTimeField(TXT_CRIADO_EM, auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'pagamento_mercado_pago'
        verbose_name_plural = 'Pagamentos do MP'
        verbose_name = 'Pagamento do MP'

    def __str__(self):
        return self.mercado_pago_id


class PagamentoMercadoPagoWebhook(models.Model):
    # DEPRECATED: Tabela nao utilizada e sera removida no futuro
    mercado_pago = models.ForeignKey(
        PagamentoMercadoPago, on_delete=models.CASCADE)
    webhook_request = models.JSONField()
    webhook_data_recebimento = models.DateTimeField(auto_now=True)
    webhook_executado = models.BooleanField(default=False)
    created_at = models.DateTimeField(TXT_CRIADO_EM, auto_now_add=True)
    updated_at = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:
        db_table = 'mercado_pago_webhook'
