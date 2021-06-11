import mercadopago

sdk = mercadopago.SDK("TEST-10952-060717-f0939c9fbd2497ef5aefd253b66bf2df-4990865")


def mercado_pago(request):
    print('Entrei aqui caralio')
    payment_data = {
        "transaction_amount": float(request.POST.get("transaction_amount")),
        "token": request.POST.get("token"),
        "description": request.POST.get("description"),
        "installments": int(request.POST.get("installments")),
        "payment_method_id": request.POST.get("payment_method_id"),
        "payer": {
            "email": request.POST.get("email"),
            "identification": {
                "type": request.POST.get("type"), 
                "number": request.POST.get("number")
            }
        }
    }

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]

    print(payment)