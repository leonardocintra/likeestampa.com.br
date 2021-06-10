import mercadopago

sdk = mercadopago.SDK("TEST-10952-060717-f0939c9fbd2497ef5aefd253b66bf2df-4990865")

preference_data = {
    "items": [
        {
            "title": "My Item",
            "quantity": 1,
            "unit_price": 75.76
        }
    ]
}

preference_response = sdk.preference().create(preference_data)
preference = preference_response["response"]