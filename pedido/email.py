from django.core.mail import send_mail


def envia_email(cliente, pedido, pedido_pago, items):
    pagamento = 'Aguardando pagamento'
    if pedido_pago:
        pagamento = 'Pago com sucesso!'

    produtos = ''
    for item in items:
        produtos = produtos + '- {0} {1} {2} {3} x {4} \n'.format(
            item.produto, item.cor.tipo_variacao.descricao, item.tamanho.tipo_variacao.descricao, item.modelo, item.quantidade)

    message = "Ola {0} ! \n \n \
    Seu pedido #{1} foi gerado com sucesso! \n \
    Status pagamento: {2} \n \n \
    Produtos: \n \
    {3} \n Caso tiver alguma duvida pode nos responder esse mail. \n Ou entrar em contato por whatsapp (35) 9999-7619".format(cliente.user.first_name, pedido, pagamento, produtos)

    send_mail("Like Estampa - Pedido: #" + str(pedido), message,
              "Like Estampa <contato@likeestampa.com.br>", [cliente.user.email])
