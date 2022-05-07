#-----------------------
# BIBLIOTECAS
#-----------------------
import re
import time
import telebot
import threading
from login import senhas
from database import DataBase
from rastreador import Rastreio
from verificadores import Verificadores
#-----------------------
# FUNÇÕES()
#-----------------------
# bot.send_message(mensagem.chat.id,resposta);
# 
def banco(db:DataBase=DataBase(),rastreador:Rastreio=Rastreio())->None:
    while True:
        if(db.validar_rastreio() >= 15):
            dados = db.select_rastreio();
            if(dados != []):
                id_user = dados[0];
                codigo  = dados[1];
                info    = dados[2];
                nome    = dados[3];
                novo_info = rastreador.rastrear(codigo=codigo);
                db.update_rastreio(id_user=id_user,codigo=codigo,mensagem=novo_info);
                if(info != novo_info):
                    resposta = f"Temos atualizações da sua encomenda {nome}\n\n{novo_info}Encomenda: {nome}";
                    bot = telebot.TeleBot(senhas.CHAVE_API);
                    bot.send_message(id_user,resposta);
        else:
            time.sleep(30);

def app(db:DataBase=DataBase(),verificador:Verificadores=Verificadores(),rastreador:Rastreio=Rastreio())->None:
    bot = telebot.TeleBot(senhas.CHAVE_API);
    @bot.message_handler(commands=["rastrear"])
    def rastrear(mensagem):
        informacoes = mensagem.text;
        informacoes = re.findall(   r'(?P<Codigo>[a-z]{2}[0-9]{9}[a-z]{2})(?:\n)*(?:.[^a-z0-9])*(?:\s)*(?:\n)*(?P<Nome>.*)(?:\n)*'
                                    ,informacoes,re.MULTILINE | re.IGNORECASE);
        if(informacoes != []):
            informacoes = informacoes[0];
            if(len(informacoes) != 2):
                if(re.findallr(r'(?P<Codigo>[a-z]{2}[0-9]{9}[a-z]{2})(?:\n)*',informacoes,re.MULTILINE | re.IGNORECASE) == []):
                    return;
                else:
                    codigo   = informacoes[0];
                    nome     = '';
            else:
                codigo   = informacoes[0];
                nome     = informacoes[1];
            idUser   = mensagem.chat.id;
            resposta = f"Procurando encomenda";
            bot.reply_to(mensagem,resposta);
            dados = rastreador.rastrear(codigo=codigo);
            if(dados != ''):
                resposta = f"{dados}Encomenda: {nome}";
                bot.reply_to(mensagem,resposta);
                # ('id_user','codigo','nome_rastreio','informacoes');
                tupla = (idUser,codigo,nome,dados);
                db.insert_rastreio(comando_tuple=tupla);
                return;
        resposta = f"Infelizmente {nome} {codigo} não foi encontrada."
        bot.reply_to(mensagem,resposta);
    
    @bot.message_handler(commands=["encomendas"])
    def atualizarEncomendas(mensagem):
        resposta = f"Funcionalidade indisponível";
        bot.reply_to(mensagem,resposta);
    
    @bot.message_handler(commands=["cpf","CPF"])
    def cpf_funcao(mensagem):
        informacoes = str(mensagem.text);
        informacoes = informacoes.replace('.'|'-'|'/','');
        idUser   = mensagem.chat.id;
        informacoes = re.findall(   r'(?P<CPF_sem_pontos>[0-9]{11})(?:\n)*'
                                    ,informacoes,re.MULTILINE | re.IGNORECASE);
        if(informacoes != []):
            cpf    = informacoes[0];
            cpf    = str(cpf);
            valido = verificador.CPF(CPF=cpf);
            if valido:
                resposta = f"O cpf é válido";
                valido   = f'True';
            else:
                resposta = f"O cpf é inválido";
                valido   = f'False';
            tupla = (idUser,cpf,valido);
            db.insert_cpf(comando_tuple=tupla);
            bot.reply_to(mensagem,resposta);
        resposta = f"Infelizmente solicitação inválida";
        bot.reply_to(mensagem,resposta);
    
    @bot.message_handler(commands=["cnpj"])
    def cnpj_funcao(mensagem):
        informacoes = str(mensagem.text);
        informacoes = informacoes.replace('.'|'-'|'/','');
        idUser   = mensagem.chat.id;
        informacoes = re.findall(   r'(?P<CNPJ_sem_pontos>[0-9]{14})(?:\n)*'
                                    ,informacoes,re.MULTILINE | re.IGNORECASE);
        if(informacoes != []):
            cnpj    = informacoes[0];
            cnpj    = str(cnpj);
            cnpj    = cnpj.replace('.','').replace('-','');
            valido = verificador.CNPJ(cnpj=cnpj);
            if valido:
                resposta = f"O cnpj é válido";
                valido   = f'True';
            else:
                resposta = f"O cnpj é inválido";
                valido   = f'False';
            tupla = (idUser,cnpj,valido);
            db.insert_cnpj(comando_tuple=tupla);
            bot.reply_to(mensagem,resposta);
        resposta = f"Infelizmente solicitação inválida";
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
# MAIN()
#-----------------------
if __name__ == '__main__':
    db          = DataBase();
    verificador = Verificadores();
    rastreador  = Rastreio();
    db.creat_table();
    # Cria a Thread
    thread_banco = threading.Thread(target=banco, args=(db,));
    thread_app   = threading.Thread(target=app, args=(db,verificador,rastreador,));
    # Inicia a Thread
    thread_banco.start();
    thread_app.start();
    # Aguarda finalizar a Thread
    thread_banco.join();
    thread_app.join();
#-----------------------