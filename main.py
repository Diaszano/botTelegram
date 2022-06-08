#-----------------------
# BIBLIOTECAS
#-----------------------
import re
import time
import telebot
import threading
from login import senhas
from datetime import datetime
from rastreador import Rastreio
from verificador import Verificadores
from banco import DataBaseSqlite as Sqlite
from banco import DataBaseMariaDB as MariaDB
#-----------------------
# CONSTANTES
#-----------------------
HORA = 20;
TEMPO_MAXIMO = 2;
#-----------------------
# CLASSES
#-----------------------
#-----------------------
# FUNÇÕES
#-----------------------
def pegar_digitos(mensagem:str):
    temp:str = '';
    for caracter in mensagem:
        if(caracter.isdigit()):
            temp += caracter;
    return temp;

def hora_do_remedio(bot:telebot.TeleBot,db:MariaDB) -> None:
    isTrue:bool = True;
    while True:
        hora = int(datetime.today().strftime('%H'));
        if(hora == HORA and isTrue):
            IDs      = senhas.IDs;
            resposta = "Horário do Remédio 😁💊";
            for id_user in IDs:
                bot.send_message(id_user,resposta.title());
            isTrue = False;
            pass;
        elif(hora != HORA):
            isTrue = True;
        time.sleep(30);

def banco(  rastreador:Rastreio,bot:telebot.TeleBot,
            db:MariaDB,bkp:Sqlite)->None:
    while True:
        tempo_banco = db.validar_rastreio();
        if(tempo_banco == -1):
            tempo           = TEMPO_MAXIMO * 60;
            tempo_de_espera = tempo;
            if tempo_de_espera > 0:
                time.sleep(tempo_de_espera);
        elif((tempo_banco/60) >= TEMPO_MAXIMO):
            dados = db.atualiza_rastreio();
            # return [codigo,informacoes,users];
            if(dados != []):
                codigo      = str(dados[0]);
                informacoes = str(dados[1]);
                users:list  = dados[2];

                nova_informacoes = rastreador.rastrear(codigo=codigo);
                
                if(nova_informacoes != ""):
                    if(informacoes.upper() != nova_informacoes.upper()):
                        for id_user, nome in users:
                            resposta = (f"Temos atualizações da sua "
                                        f"encomenda \n\n"
                                        f"{nova_informacoes}"
                                        f"Encomenda: {codigo} {nome}");
                            bot.send_message(id_user,resposta);
                        informacoes = nova_informacoes;
                tupla = (codigo,informacoes);
                db.update_rastreio(tupla=tupla);
                bkp.update_rastreio(tupla=tupla);
        else:
            tempo           = TEMPO_MAXIMO * 60;
            tempo_de_espera = tempo - tempo_banco;
            if(tempo_de_espera > 0):
                time.sleep(tempo_de_espera);

def app(verificador:Verificadores,rastreador:Rastreio,
        bot:telebot.TeleBot,db:MariaDB,bkp:Sqlite)->None:
    regex = (   r'/rastrear|'
                r'/listar|'
                r'/encomendas|'
                r'/deletar|'
                r'/cpf|'
                r'/cnpj|'
                r'/remedio');
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
            if(nome == "/remedio".upper()):
                remedio(mensagem);
                # return False;
        return True;
    
    def validar(regex:re,mensagem) -> list:
        dados = regex.findall(mensagem);
        if(dados == []):
            return [False,''];
        return [True,dados[0]];

    def remedio(mensagem):
        dados = str(mensagem.text);
        regex:str =(r'(?:^\/remedio\s*){1}'
                    r'(?P<horario>[0-9]{2}\:{1}[0-9]{2}){1}'
                    r'(?:\s*\-\s*){0,1}(?P<Nome>.{0,30}){1}');
        dados = re.findall(regex,dados,re.MULTILINE | re.IGNORECASE);
        if(dados == []):
            resposta = f"Dados Inválidos";
            bot.reply_to(mensagem,resposta);
            return;
        dados      = dados[0];
        hora:str   = dados[0];
        nome:str   = dados[1];
        data_agora = datetime.now();
        date2      = data_agora.strftime('%H:%M');
        d2         = datetime.strptime(date2,'%H:%M');
        asa = datetime.strptime(hora,'%H:%M');
        print(f" dados - {dados} \nd1 - {asa} \nd2 - {d2}\n{asa == asa}");

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
                bkp.insert_rastreio(tupla=tupla);
                return;
            resposta = (    f"Infelizmente {nome} "
                            f"{codigo} não foi encontrada.");
            bot.reply_to(mensagem,resposta);
            informacoes = str(informacoes);
            tupla = (id_user,codigo,nome,informacoes);
            db.insert_rastreio(tupla=tupla);
            bkp.insert_rastreio(tupla=tupla);
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
            bkp.insert_cpf(tupla=tupla);
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
            bkp.insert_cnpj(tupla=tupla);
            bot.reply_to(mensagem,resposta);
            return;
        resposta = f"Infelizmente solicitação inválida";
        bot.reply_to(mensagem,resposta);

    def guardar_mensagens(mensagem):
        id_user = str(mensagem.chat.id);
        tupla   = (id_user,str(mensagem));
        db.insert_mensagem(tupla=tupla);
        bkp.insert_mensagem(tupla=tupla);

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
    db          = MariaDB(  host=senhas.host,user=senhas.user,
                            password=senhas.passaword,
                            database=senhas.database);
    bkp         = Sqlite();
    bot         = telebot.TeleBot(senhas.CHAVE_API);
    rastreador  = Rastreio();
    verificador = Verificadores();
    
    # Cria a Thread
    threads_bot:list = [];
    threads_bot.append( threading.Thread(target=app, 
                        args=(verificador,rastreador,bot,db,bkp,),
                        daemon=True));
    threads_bot.append( threading.Thread(target=banco, 
                        args=(rastreador,bot,db,bkp,),
                        daemon=True));
    threads_bot.append( threading.Thread(target=hora_do_remedio,
                        args=(bot,db,),daemon=True));
    # Inicia a Thread
    for t in threads_bot:
        t.start();
    # Aguarda finalizar a Thread
    while True:
        time.sleep(1);
        for t in threads_bot:
            if(not (t.is_alive())):
                raise threading.ThreadError("Thread não deveria ter morrido");
#-----------------------