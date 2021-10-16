import requests
import telegram
from django.conf import settings

bot = telegram.Bot(token='1903499437:AAEmERka8PLttOZCzs9XqmUNVBVw2U4-z2c')


def enviar_mensagem(mensagem, titulo='*Like Estampa*', subtitulo='_mensagem importante_'):
    if settings.DEBUG:
        return

    CHAT_ID = -481527516
    text = '*{0}* \n _{1}_ \n `{2}`'.format(titulo, subtitulo, mensagem)
    bot.send_message(chat_id=CHAT_ID, text=text,
                     parse_mode=telegram.ParseMode.MARKDOWN_V2)
