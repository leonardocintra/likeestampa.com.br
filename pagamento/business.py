from pagamento.models import PagamentoMercadoPago


def atualizar_pagamento_mp(payment, mercado_pago_id, payment_id):
    # Atualiza os dados do mercado pago na tabela de pagamento
    PagamentoMercadoPago.objects.filter(
        mercado_pago_id=mercado_pago_id).update(
            transaction_amount=payment['transaction_amount'],
            installments=payment['installments'],
            payment_method_id=payment['payment_method_id'],
            mercado_pago_status=payment['status'],
            mercado_pago_status_detail=payment['status_detail'],
            payment_id=payment_id
    )
