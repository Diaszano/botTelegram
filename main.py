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
# CONSTANTES
#-----------------------
TEMPO_MAXIMO = 2;
#-----------------------
# FUNÇÕES()
#-----------------------
def banco(db:DataBase=DataBase(),rastreador:Rastreio=Rastreio(),bot:telebot.TeleBot = telebot.TeleBot(senhas.CHAVE_API))->None:
    while True:
        tempo_banco = db.validar_rastreio();
        if((tempo_banco) == -1):
            tempo           = TEMPO_MAXIMO * 60;
            tempo_de_espera = tempo;
            if tempo_de_espera > 0:
                time.sleep(tempo_de_espera);
        elif((tempo_banco/60) >= TEMPO_MAXIMO):
            dados = db.atualiza_rastreio();
            if(dados != []):
                id_user          = dados[0];
                codigo           = dados[1];
                informacoes      = str(dados[2]);
                nome             = dados[3];
                nova_informacoes = rastreador.rastrear(codigo=codigo);
                if(nova_informacoes != ""):
                    if(informacoes.upper() != nova_informacoes.upper()):
                        resposta = f"Temos atualizações da sua encomenda \n\n{nova_informacoes}Encomenda: {codigo} {nome}";
                        bot.send_message(id_user,resposta);
                        informacoes = nova_informacoes;
                db.update_rastreio(id_user=id_user,codigo=codigo,informacoes=informacoes);
        else:
            tempo           = TEMPO_MAXIMO * 60;
            tempo_de_espera = tempo - tempo_banco;
            if tempo_de_espera > 0:
                time.sleep(tempo_de_espera);

def app(db:DataBase=DataBase(),verificador:Verificadores=Verificadores(),rastreador:Rastreio=Rastreio(),bot:telebot.TeleBot = telebot.TeleBot(senhas.CHAVE_API))->None:
    @bot.message_handler(commands=["rastrear","RASTREAR"])
    def rastrear(mensagem):
        dados = mensagem.text;
        id_user  = mensagem.chat.id;
        tupla = (id_user,str(mensagem));
        db.insert_mensagem(tupla=tupla);
        dados = re.findall(   r'(?P<Codigo>[a-z]{2}[0-9]{9}[a-z]{2})(?:\n)*(?:.[^a-z0-9])*(?:\s)*(?:\n)*(?P<Nome>.*)(?:\n)*'
                                    ,dados,re.MULTILINE | re.IGNORECASE);
        if(dados != []):
            dados = dados[0];
            if(len(dados) != 2):
                if(re.findall(r'(?P<Codigo>[a-z]{2}[0-9]{9}[a-z]{2})(?:\n)*',dados,re.MULTILINE | re.IGNORECASE) == []):
                    resposta = f"Dados Inválidos";
                    bot.reply_to(mensagem,resposta);
                    return;
                else:
                    codigo   = dados[0];
                    nome     = '';
            else:
                codigo   = dados[0];
                nome     = dados[1];

            codigo   = str(codigo).upper();
            resposta = f"Procurando encomenda";
            bot.reply_to(mensagem,resposta);
            informacoes = rastreador.rastrear(codigo=codigo); # ----
            if(informacoes != ''):
                resposta = f"{informacoes}Encomenda: {codigo} {nome}";
                bot.reply_to(mensagem,resposta);
                # ('id_user','codigo','nome_rastreio','informacoes');
                tupla = (id_user,codigo,nome,informacoes);
                db.insert_rastreio(tupla=tupla);
                return;
            resposta = f"Infelizmente {nome} {codigo} não foi encontrada."
            bot.reply_to(mensagem,resposta);
            tupla = (id_user,codigo,nome,informacoes);
            db.insert_rastreio(tupla=tupla);
            return;
        resposta = f"Dados Inválidos";
        bot.reply_to(mensagem,resposta);
    
    @bot.message_handler(commands=["encomendas","ENCOMENDAS"])
    def atualizar_encomendas(mensagem):
        resposta = f"Procurando encomendas";
        bot.reply_to(mensagem,resposta);
        id_user  = mensagem.chat.id;
        tupla = (id_user,str(mensagem));
        db.insert_mensagem(tupla=tupla);
        resposta = f"Tu tens 📦 {len(db.select_rastreio(id_user=id_user))} encomendas guardadas";
        bot.reply_to(mensagem,resposta);
        for informacoes, nome, codigo in db.select_rastreio(id_user=id_user):
            resposta = f"{informacoes}Encomenda: {codigo} {nome}";
            bot.reply_to(mensagem,resposta);

    @bot.message_handler(commands=["LISTAR","listar"])
    def listar_encomendas(mensagem):
        resposta = f"Procurando encomendas";
        bot.reply_to(mensagem,resposta);
        id_user  = mensagem.chat.id;
        tupla = (id_user,str(mensagem));
        db.insert_mensagem(tupla=tupla);
        resposta = f"Tu tens {len(db.select_rastreio(id_user=id_user))} encomendas guardadas\n";
        comando  = f"SELECT codigo, nome_rastreio FROM encomenda WHERE id_user='{id_user}' ORDER BY id";
        for informacoes, nome in db.select_rastreio(comando=comando):
            resposta += f"📦 {informacoes} {nome}\n";
        bot.send_message(mensagem.chat.id,resposta);

    @bot.message_handler(commands=["deletar","DELETAR"])
    def deletar_encomendas(mensagem):
        id_user  = mensagem.chat.id;
        tupla = (id_user,str(mensagem));
        db.insert_mensagem(tupla=tupla);
        dados = mensagem.text;
        dados = re.findall(   r'(?P<Codigo>[a-z]{2}[0-9]{9}[a-z]{2})'
                                    ,dados,re.MULTILINE | re.IGNORECASE);
        if(dados != []):
            dados    = dados[0];
            codigo   = str(dados).upper();
            resposta = f"Procurando encomenda para remover";
            bot.reply_to(mensagem,resposta);
            if(db.verifica_rastreio(id_user=id_user,codigo=codigo)):
                db.delete_rastreio(id_user=id_user,codigo=codigo);
                resposta = f"Encomenda Deletada";
                bot.reply_to(mensagem,resposta);
                return;
        resposta = f"Dados Inválidos";
        bot.reply_to(mensagem,resposta);

    @bot.message_handler(commands=["cpf","CPF"])
    def cpf_funcao(mensagem):
        dados = str(mensagem.text);
        dados = dados.replace('.','').replace('-','').replace('/','');
        id_user  = mensagem.chat.id;
        tupla = (id_user,str(mensagem));
        db.insert_mensagem(tupla=tupla);
        dados = re.findall(   r'(?P<CPF_sem_pontos>[0-9]{11})(?:\n)*'
                                    ,dados,re.MULTILINE | re.IGNORECASE);
        if(dados != []):
            cpf    = dados[0];
            cpf    = str(cpf);
            valido = verificador.CPF(cpf);
            if valido:
                resposta = f"O cpf é válido";
                valido   = f'True';
            else:
                resposta = f"O cpf é inválido";
                valido   = f'False';
            tupla = (id_user,cpf,valido);
            db.insert_cpf(tupla=tupla);
            bot.reply_to(mensagem,resposta);
            return;
        resposta = f"Infelizmente solicitação inválida";
        bot.reply_to(mensagem,resposta);
    
    @bot.message_handler(commands=["cnpj","CNPJ"])
    def cnpj_funcao(mensagem):
        dados   = str(mensagem.text);
        dados   = dados.replace('.','').replace('-','').replace('/','');
        id_user  = mensagem.chat.id;
        tupla = (id_user,str(mensagem));
        db.insert_mensagem(tupla=tupla);
        dados   = re.findall(   r'(?P<CNPJ_sem_pontos>[0-9]{14})(?:\n)*'
                                    ,dados,re.MULTILINE | re.IGNORECASE);
        if(dados != []):
            cnpj    = dados[0];
            cnpj    = str(cnpj);
            valido = verificador.CNPJ(cnpj=cnpj);
            if valido:
                resposta = f"O cnpj é válido";
                valido   = f'True';
            else:
                resposta = f"O cnpj é inválido";
                valido   = f'False';
            tupla = (id_user,cnpj,valido);
            db.insert_cnpj(tupla=tupla);
            bot.reply_to(mensagem,resposta);
            return;
        resposta = f"Infelizmente solicitação inválida";
        bot.reply_to(mensagem,resposta);
    
    def verificar(mensagem):
        id_user  = mensagem.chat.id;
        tupla = (id_user,str(mensagem));
        db.insert_mensagem(tupla=tupla);
        return True;

    @bot.message_handler(func=verificar)
    def responder(mensagem):
        texto = str("Escolha uma opção para continuar:" +
                "\nPara rastrear sua encomenda:\n" +
                '/rastrear "código" - "Nome do Produto"\n'+
                '\nPara ver suas encomendas guardadas:\n'+
                '/encomendas\n'+
                '   Com esse tu vê todas as informações\n'+
                '/listar\n'+
                '   Com esse tu vê só o codigo de rastreio e o nome\n\n'+
                'Para deletar uma encomenda guardada:\n'+
                '/deletar "código"\n\n'+
                'Para verificar cpf ou cnpj:\n'+
                '/cpf "o cpf da consulta"\n'+
                '/cnpj "o cnpj da consulta"\n\n'+
                'Se responder qualquer outra coisa não vai funcionar');
        bot.reply_to(mensagem, texto);
    bot.polling();
#-----------------------
# MAIN()
#-----------------------
if __name__ == '__main__':
    db          = DataBase();
    verificador = Verificadores();
    rastreador  = Rastreio();
    bot         = telebot.TeleBot(senhas.CHAVE_API);
    db.creat_table();
    db.creat_table_cpf();
    db.creat_table_cnpj();
    db.creat_table_mensagem();
    # Cria a Thread
    thread_banco = threading.Thread(target=banco, args=(db,rastreador,bot,));
    thread_app   = threading.Thread(target=app, args=(db,verificador,rastreador,bot,));
    # Inicia a Thread
    thread_banco.start();
    thread_app.start();
    # Aguarda finalizar a Thread
    thread_banco.join();
    thread_app.join();
#-----------------------