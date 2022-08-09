from apps.pagamento.models import PagamentoMercadoPago


def atualizar_pagamento_mp(payment):
    # Atualiza os dados do mercado pago na tabela de pagamento
    payment_id = payment['id']
    PagamentoMercadoPago.objects.filter(
        payment_id=payment_id).update(
            transaction_amount=payment['transaction_amount'],
            installments=payment['installments'],
            payment_method_id=payment['payment_method_id'],
            mercado_pago_status=payment['status'],
            mercado_pago_status_detail=payment['status_detail']
    )
