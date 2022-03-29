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

@bot.message_handler(commands=["rastrear"])
def rastrear(mensagem):
    codigo = mensagem.text.replace('/rastrear ','');
    print(codigo);
    # asldka
    # print(mensagem);
    print(mensagem.text);
    url = f'https://proxyapp.correios.com.br/v1/sro-rastro/{codigo}';
    informacoes = requests.get(url);
    print(informacoes.json());
    todasInformacoes = informacoes.json();
    objetos = todasInformacoes['objetos'];
    objetos = objetos[0];
    dataPrevista = objetos['dtPrevista'];
    print('\n\n\n\n\n');
    print(objetos);
    # resultado = informacoes.json.text;
    # for enventos in resultado.objetos[0].eventos:
    #     print(enventos);

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