#-----------------------
# BIBLIOTECAS
#-----------------------
import re
import telebot
import requests
from login import senhas as dz
#-----------------------
# FUNÇÕES
#-----------------------
def rastrearEncomendaBanco(codigo:str = '',idUser:str = '',novo:bool = False)-> bool:
    print('\noi\n');
    return False;

def rastrearEncomendaNova(codigo:str = '',idUser:str = '') -> bool or list:
    if not(rastrearEncomendaBanco(codigo=codigo,idUser=idUser,novo=True)):
        url = f'https://proxyapp.correios.com.br/v1/sro-rastro/{codigo}';
        informacoes = requests.get(url);
        informacoes = str(informacoes.text);
        print(informacoes);
        informacoes = re.findall('(?P<Eventos>\"eventos\"\:)(?P<Dados_Eventos>\[.*?\])', informacoes, re.MULTILINE | re.IGNORECASE);
        if informacoes != []:
            informacoes    = str(informacoes);
            informacoes    = re.findall('(?P<Eventos>\{\"codigo\"\:.*?\.png\"\})*', informacoes, re.MULTILINE | re.IGNORECASE);
            resultados = [valor for valor in informacoes if valor != ''];
            return limparMensagem(eventos=resultados);
        else:
            return False;

def limparMensagem(eventos:list = []) -> list:
    rastreio = '';
    for resultado in eventos:
        dia       = '';
        tipo      = '';
        local     = '';
        destino   = '';
        detalhe   = '';
        descricao = '';
        if 'descricao' in resultado:
            temp      = re.findall('((\"descricao\"\:)(\".*?\"))', resultado, re.MULTILINE | re.IGNORECASE);
            temp      = str(temp[0][2]);
            temp      = temp.replace('"','');
            descricao = temp;
        if 'detalhe' in resultado:
            temp    = re.findall('((\"detalhe\"\:)(\".*?\"))', resultado, re.MULTILINE | re.IGNORECASE);
            temp    = temp[0][2];
            temp    = temp.replace('"','');
            detalhe = temp;
        if 'dtHrCriado' in resultado:
            temp = re.findall('((\"dtHrCriado\"\:)(\".*?\"))', resultado, re.MULTILINE | re.IGNORECASE);
            temp = temp[0][2]
            temp = temp.replace('"','');
            dia  = temp;
        if 'tipo' in resultado:
            tipo = re.findall('((\"tipo\"\:)(\"[^0-9]*?\"))', resultado, re.MULTILINE | re.IGNORECASE);
            if tipo != []:
                temp = re.findall('(?:\"unidade\"\:\{\"endereco\"\:\{"cidade"\:)(\".*?\"),(?:\"uf\"\:)(\".*?\")', resultado, re.MULTILINE | re.IGNORECASE);
                if temp != []:
                    temp        = temp[0];
                    [cidade,uf] = [temp[0],temp[1]];
                    uf          = uf.replace('"','');
                    cidade      = cidade.replace('"','');
                    local       = f'[{cidade}/{uf}]';
                else:
                    temp  = re.findall('(?:\"unidade\"\:\{\"codSro\"\:\".*?\"(?:\,)\"endereco\"\:\{\}\,\"nome"\:)(\".*?\")', resultado, re.MULTILINE | re.IGNORECASE);
                    if temp != []:
                        temp  = temp[0].replace('"','');
                        local = f'[{temp}]';
        if '' in resultado:
            temp  = re.findall('(?:\"unidadeDestino\"\:\{\"endereco\"\:\{\"cidade\":)(\".*?\")(?:,\"uf\"\:)(\".*?\")', resultado, re.MULTILINE | re.IGNORECASE);
            if temp != []:
                temp        = temp[0];
                [cidade,uf] = [temp[0],temp[1]];
                uf          = uf.replace('"','');
                cidade      = cidade.replace('"','');
                destino     = f' para [{cidade}/{uf}]';
        rastreio += f'[{limpaData(dia)}] - {descricao} {local}{destino}\n{detalhe}\n\n'
    print(rastreio);
    return rastreio;

def limpaData(data:str='')->str:
    ano = data[:4];
    mes = data[5:7];
    dia = data[8:10];
    hora= data[11:];
    mensagem = f"{dia}/{mes}/{ano} - {hora}";
    return mensagem;

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
        else:
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