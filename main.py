#-----------------------
# BIBLIOTECAS
#-----------------------
import telebot
import requests
from login import senhas as dz
#-----------------------
# FUNÇÕES
#-----------------------
def rastrearEncomendaBanco(codigo:str = '',idUser:str = '',novo:bool = False)-> bool:
    print('\noi\n');
    return False;

def rastrearEncomendaNova(codigo:str = '',idUser:str = '') -> list:
    if not(rastrearEncomendaBanco(codigo=codigo,idUser=idUser,novo=True)):
        url = f'https://proxyapp.correios.com.br/v1/sro-rastro/{codigo}';
        informacoes = requests.get(url);
        todasInformacoes = informacoes.json();
        # print(todasInformacoes['objetos'][0]);
        nome = {}
        if 'eventos' in todasInformacoes['objetos'][0]:
            eventos = todasInformacoes['objetos'][0]['eventos'];
            print(todasInformacoes);
        else:
            return False;

def limparMensagem(mensagem:dict = {}):
    pass;
#-----------------------
# M A I N ()
#-----------------------
if __name__ == '__main__':
    bot = telebot.TeleBot(dz.CHAVE_API);

    @bot.message_handler(commands=["rastrear"])
    def rastrear(mensagem):
        codigo = mensagem.text.replace('/rastrear ','');
        idUser = mensagem.chat.id;
        resposta = f"Procurando encomenda";
        bot.reply_to(mensagem,resposta);
        resposta = rastrearEncomendaNova(codigo=codigo,idUser=idUser);
        if resposta == False:
            resposta = f"Encomenda não localizada";
            bot.reply_to(mensagem,resposta);
    
    @bot.message_handler(commands=["encomendas"])
    def atualizarEncomendas(mensagem):
        idUser = mensagem.chat.id;
        encomendas = rastrearEncomendaBanco(idUser=idUser);
        if encomendas == False:
            resposta = f"Infelizmente tu não contém nenhuma encomenda guardada";
            bot.send_message(mensagem.chat.id,resposta);

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
#-----------------------