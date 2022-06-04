#-----------------------
# BIBLIOTECAS
#-----------------------
import re
import time
import telebot
import threading
from login import senhas # minha pasta pessoal de senhas
from rastreador import Rastreio
from banco import DataBaseSqlite
from verificador import Verificadores
#-----------------------
# CONSTANTES
#-----------------------
TEMPO_MAXIMO = 2;
#-----------------------
# CLASSES
#-----------------------
#-----------------------
# FUNÇÕES
#-----------------------
def pegar_digitos(mensagem:str) -> str:
    temp = '';
    for caracter in mensagem:
        if(caracter.isdigit()):
            temp += caracter;
    return temp;

def banco(  rastreador:Rastreio,bot:telebot.TeleBot,
            db:DataBaseSqlite)->None:
    while True:
        tempo_banco = db.validar_rastreio();
        if(tempo_banco == -1):
            tempo           = TEMPO_MAXIMO * 60;
            tempo_de_espera = tempo;
            if tempo_de_espera > 0:
                time.sleep(tempo_de_espera);
        elif((tempo_banco/60) >= TEMPO_MAXIMO):
            dados = db.atualiza_rastreio();
            if(dados != []):
                id_user          = str(dados[0]);
                codigo           = str(dados[1]);
                informacoes      = str(dados[2]);
                nome             = str(dados[3]).title();
                nova_informacoes = rastreador.rastrear(codigo=codigo);
                if(nova_informacoes != ""):
                    if(informacoes.upper() != nova_informacoes.upper()):
                        resposta = (f"Temos atualizações da sua "
                                    f"encomenda \n\n{nova_informacoes}"
                                    f"Encomenda: {codigo} {nome}");
                        bot.send_message(id_user,resposta);
                        informacoes = nova_informacoes;
                tupla = (id_user,codigo,informacoes);
                db.update_rastreio(tupla=tupla);
        else:
            tempo           = TEMPO_MAXIMO * 60;
            tempo_de_espera = tempo - tempo_banco;
            if(tempo_de_espera > 0):
                time.sleep(tempo_de_espera);

def app(verificador:Verificadores,rastreador:Rastreio,
        bot:telebot.TeleBot,db:DataBaseSqlite)->None:
    regex = (   r'/rastrear|'
                r'/listar|'
                r'/encomendas|'
                r'/deletar|'
                r'/cpf|'
                r'/cnpj');
    regex_opcoes = re.compile(regex,re.MULTILINE | re.IGNORECASE);
    
    def verificar(mensagem):
        guardar_mensagens(mensagem);
        [isTrue,nome] = validar(regex=regex_opcoes,
                        mensagem=mensagem.text);
        nome = str(nome).upper();
        if(isTrue):
            # Rastrear
            if(nome == "/Rastrear".upper()):
                rastrear_encomendas(mensagem);
                return False;
            # Listar
            if(nome == "/Listar".upper()):
                listar_encomendas(mensagem);
                return False;
            # Encomendas
            if(nome == "/Encomendas".upper()):
                buscar_encomendas(mensagem);
                return False;
            # Deletar
            if(nome == "/Deletar".upper()):
                deletar_encomendas(mensagem);
                return False;
            # CPF
            if(nome == "/CPF".upper()):
                verificar_cpf(mensagem);
                return False;
            # CNPJ
            if(nome == "/CNPJ".upper()):
                verificar_cnpj(mensagem);
                return False;
        return True;
    
    def validar(regex:re,mensagem) -> list:
        dados = regex.findall(mensagem);
        if(dados == []):
            return [False,''];
        return [True,dados[0]];

    def rastrear_encomendas(mensagem):
        dados   = str(mensagem.text);
        id_user = str(mensagem.chat.id);

        regex = (   r'(?P<Codigo>[a-z]{2}[0-9]{9}[a-z]{2})'
                    r'(?:\n)*(?:.[^a-z0-9])*(?:\s)*(?:\n)*'
                    r'(?P<Nome>.{1,30})*(?:\n)*');
        dados = re.findall(regex,dados,re.MULTILINE | re.IGNORECASE);
        if(dados != []):
            dados = dados[0];
            if(len(dados) < 2):
                regex = r'(?P<Codigo>[a-z]{2}[0-9]{9}[a-z]{2})(?:\n)*';
                regex_find = re.findall(regex,dados,re.MULTILINE | 
                                        re.IGNORECASE);
                if(regex_find == []):
                    resposta = f"Dados Inválidos";
                    bot.reply_to(mensagem,resposta);
                    return;
                else:
                    codigo   = dados[0];
                    nome     = '';
            else:
                codigo   = dados[0];
                nome     = str(dados[1]).title();
            codigo   = str(codigo).upper();
            resposta = f"Procurando encomenda";
            bot.reply_to(mensagem,resposta);
            informacoes = rastreador.rastrear(codigo=codigo);
            if(informacoes != ''):
                resposta = f"{informacoes}Encomenda: {codigo} {nome}";
                bot.reply_to(mensagem,resposta);
                # ('id_user','codigo','nome_rastreio','informacoes');
                tupla = (id_user,codigo,nome,informacoes);
                db.insert_rastreio(tupla=tupla);
                return;
            resposta = (    f"Infelizmente {nome} "
                            f"{codigo} não foi encontrada.");
            bot.reply_to(mensagem,resposta);
            informacoes = str(informacoes);
            tupla = (id_user,codigo,nome,informacoes);
            db.insert_rastreio(tupla=tupla);
            return;
        resposta = f"Dados Inválidos";
        bot.reply_to(mensagem,resposta);
    
    def buscar_encomendas(mensagem):
        resposta = f"Procurando encomendas";
        bot.reply_to(mensagem,resposta);

        id_user  = str(mensagem.chat.id);
        resposta = (f"Tu tens 📦 "
                    f"{len(db.select_rastreio(id_user=id_user))} "
                    f"encomendas guardadas");
        bot.reply_to(mensagem,resposta);
        for informacoes, nome, codigo in db.select_rastreio(
                                            id_user=id_user):
            resposta = f"{informacoes}Encomenda: {codigo} {nome}";
            bot.send_message(id_user,resposta);
    
    def listar_encomendas(mensagem):
        resposta = f"Procurando encomendas";
        bot.reply_to(mensagem,resposta);
        id_user  = str(mensagem.chat.id);
        resposta = (f"Tu tens "
                    f"{len(db.select_rastreio(id_user=id_user))} "
                    f"encomendas guardadas\n");
        for _ ,nome ,codigo in db.select_rastreio(id_user=id_user):
            resposta += f"📦 {codigo} {nome}\n";
        bot.send_message(mensagem.chat.id,resposta);
    
    def deletar_encomendas(mensagem):
        id_user = str(mensagem.chat.id);
        dados   = mensagem.text;
        regex   = r'(?P<Codigo>[a-z]{2}[0-9]{9}[a-z]{2})';
        dados   = re.findall(regex,dados,re.MULTILINE | re.IGNORECASE);
        if(dados != []):
            dados    = dados[0];
            codigo   = str(dados).upper();
            resposta = f"Procurando encomenda para remover";
            bot.reply_to(mensagem,resposta);
            if(db.delete_rastreio(id_user=id_user,codigo=codigo)):
                resposta = f"Encomenda Deletada";
                bot.reply_to(mensagem,resposta);
                return;
            else:
                resposta = f"Encomenda não existente";
                bot.reply_to(mensagem,resposta);
                return;
        resposta = f"Dados Inválidos";
        bot.reply_to(mensagem,resposta);
    
    def verificar_cpf(mensagem):
        dados   = str(mensagem.text);
        dados   = pegar_digitos(dados);
        id_user = str(mensagem.chat.id);

        regex = r'(?P<CPF_sem_pontos>[0-9]{11})(?:\n)*'; 
        dados = re.findall(regex,dados,re.MULTILINE | re.IGNORECASE);
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
    
    def verificar_cnpj(mensagem):
        dados   = str(mensagem.text);
        dados   = pegar_digitos(dados);
        id_user = str(mensagem.chat.id);
        
        regex = r'(?P<CNPJ_sem_pontos>[0-9]{14})(?:\n)*';
        dados = re.findall(regex,dados,re.MULTILINE | re.IGNORECASE);
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

    def guardar_mensagens(mensagem):
        id_user = str(mensagem.chat.id);
        tupla   = (id_user,str(mensagem));
        db.insert_mensagem(tupla=tupla);

    @bot.message_handler(func=verificar)
    def responder(mensagem):
        texto =("Escolha uma opção para continuar:"
                "\nPara rastrear sua encomenda:\n"
                '/rastrear "código" - "Nome do Produto"\n'
                '\nPara ver suas encomendas guardadas:\n'
                '/encomendas\n'
                '\tCom esse tu vê todas as informações\n'
                '/listar\n'
                '\tCom esse tu vê só o codigo de rastreio e o nome\n\n'
                'Para deletar uma encomenda guardada:\n'
                '/deletar "código"\n\n'
                'Para verificar cpf ou cnpj:\n'
                '/cpf "o cpf da consulta"\n'
                '/cnpj "o cnpj da consulta"\n\n'
                'Se responder qualquer outra coisa não vai funcionar');
        bot.reply_to(mensagem, texto);
    bot.polling();
#-----------------------
# MAIN()
#-----------------------
if __name__ == '__main__':
    db          = DataBaseSqlite()
    bot         = telebot.TeleBot(senhas.CHAVE_API);
    rastreador  = Rastreio();
    verificador = Verificadores();
    # Cria a Thread
    thread_app     =    threading.Thread(target=app, 
                        args=(verificador,rastreador,bot,db,));
    thread_banco   =    threading.Thread(target=banco, 
                        args=(rastreador,bot,db,));
    # Inicia a Thread
    thread_app.start();
    time.sleep(5);
    thread_banco.start();
    # Aguarda finalizar a Thread
    thread_banco.join();
    thread_app.join();
#-----------------------