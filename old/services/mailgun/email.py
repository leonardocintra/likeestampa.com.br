from django.core.mail import send_mail


def envia_email_compra():
    pass  # https://docs.djangoproject.com/en/3.2/topics/email/#sending-alternative-content-types


def envia_email_de_teste():
    message = "Ola Leonardo ! \n \n \
    Seu pedido #9039020 foi gerado com sucesso! \n \
    Status pagamento: Aprovado \n \n \
    Produtos: \n \
    - Camiseta de TESTE \n Caso tiver alguma duvida pode nos responder esse mail. \n Ou entrar em contato por whatsapp (35) 9999-7619"

    send_mail("Like Estampa - Pedido: 3892999", message,
              "Like Estampa <likeestampa@gmail.com>", ['leonardo.ncintra@outlook.com', ])
