from django.core.mail import send_mail


def envia_email(cliente, pedido, pedido_pago):
    pagamento = 'Aguardando pagamento'
    if pedido_pago:
        pagamento = 'Pago com sucesso!'

    message = "Ola {0} ! \n \
        Seu pedido #{1} foi gerado com sucesso! \n \
        Status pagamento: {2} \n \n \
        Produtos: \n \
        - Camiseta X - Tamanho G Branca".format(
        cliente.user.first_name, pedido, pagamento)

    send_mail("Like Estampa - Pedido: #" + str(pedido), message,
              "Like Estampa <contato@likeestampa.com.br>", [cliente.user.email])
