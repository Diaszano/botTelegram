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
        if 'eventos' in todasInformacoes['objetos'][0]:
            eventos = todasInformacoes['objetos'][0]['eventos'];
            print(eventos);
            for evento in eventos:
                print(evento['descricao'],evento['dtHrCriado'],evento['unidade'],evento['unidadeDestino']);
        else:
            return False;

def limparMensagem(mensagem:dict = {}):
    pass;

def verificacaoDeCpf(numerosDoCpf:str = '000.000.000-00')->bool:
    cpf = [int(char) for char in numerosDoCpf if char.isdigit()];
    if len(cpf) != 11 or cpf == cpf[::-1]:
        return False;
    for i in range(9, 11):
        valor = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)));
        digito = ((valor * 10) % 11) % 10;
        if digito != cpf[i]:
            return False;
    return True;

def verificacaoDeCnpj(cnpj:str = '00.000.000/0000-00')->bool:
    cnpjo = [int(char) for char in cnpj if char.isdigit()];
    cnpj = cnpjo[:12];
    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    
    while len(cnpj) < 14:
        valor = sum([x*y for (x, y) in zip(cnpj, prod)])%11;
        if valor > 1:
            resto = 11 - valor;
        else:
            resto = 0;
        cnpj.append(resto);
        prod.insert(0, 6);
    if cnpj == cnpjo:
        return True;
    return False;
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

    @bot.message_handler(commands=["cpf","CPF"])
    def cpf(mensagem):
        cpf = mensagem.text;
        cpf = cpf.lower();
        cpf = cpf.replace('/cpf ','');
        valido = verificacaoDeCpf(numerosDoCpf=cpf);
        if valido:
            resposta = f"O cpf é válido";
        else:
            resposta = f"O cpf é inválido";
        bot.reply_to(mensagem,resposta);
    
    @bot.message_handler(commands=["cnpj"])
    def cnpj(mensagem):
        cnpj = mensagem.text
        cnpj = cnpj.lower();
        cnpj = cnpj.replace('/cnpj ','');
        valido = verificacaoDeCnpj(cnpj=cnpj);
        if valido:
            resposta = f"O cnpj é válido";
        else:
            resposta = f"O cnpj é inválido";
        bot.reply_to(mensagem,resposta);

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