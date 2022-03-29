#-----------------------
# BIBLIOTECAS
#-----------------------
import telebot
import requests
from login import senhas as dz
#-----------------------
# FUNÇÕES
#-----------------------
bot = telebot.TeleBot(dz.CHAVE_API);


def verificar(mensagem):
    return True;

@bot.message_handler(func=verificar)
def responder(mensagem):
    texto = """
    Escolha uma opção para continuar :
    \tPara rastrear sua encomenda:
    \t\t/rastrear "codido"
    \t\tExemplo /rastrear QK395235673BR
    Responder qualquer outra coisa não vai funcionar, clique em uma das opções"""
    bot.reply_to(mensagem, texto);
bot.polling();
