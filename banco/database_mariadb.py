"""Conexão com o Banco de Dados MariaDB"""
#-----------------------
# BIBLIOTECAS
#-----------------------
import mysql.connector
from typing import Union
from threading import Lock
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class DataBaseMariaDB():
    def __init__(   self,host:str='',user:str='',
                    password:str='',database:str='')->None:
        self.__host     = host;
        self.__user     = user;
        self.__password = password;
        self.__database = database;
        self.lock = Lock();
    # -----------------------
    # Criação e conexão
    # -----------------------
    def __conexao(self,host:str='',user:str='',
                password:str='',database:str='')->list:
        if(host != ''):
            self.__host = host;
        if(user != ''):
            self.__user = user;
        if(password != ''):
            self.__password = password;
        if(database != ''):
            self.__database = database;
        if( (self.__host == '') or (self.__user == '') or
            (self.__password == '') or (self.__database == '')):
            mensagem = ("Está faltando argumentos na "
                        "conexão, faça novamente!");
            print(mensagem);
            return [None,None];
        else:
            cnxn = mysql.connector.connect(
                host=self.__host,
                user=self.__user,
                password=self.__password,
                database=self.__database,
            );
            cursor = cnxn.cursor();
            return [cnxn,cursor];
    # -----------------------
    # CRUD
    # -----------------------
    # Create
    def __insert(self,comando:str,tupla:tuple) -> None:
        self.lock.acquire();
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando, tupla);
            cnxn.commit();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
        self.lock.release();
    # Read
    def __select(self,comando:str) -> list:
        self.lock.acquire();
        retorno:list = [];
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando);
            retorno = cursor.fetchall();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
        self.lock.release();
        return retorno;
    # Update
    def __update(self,comando:str) -> None:
        self.lock.acquire();
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando);
            cnxn.commit();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
        self.lock.release();
    # Delete
    def __delete(self,comando:str) -> None:
        self.lock.acquire();
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando);
            cnxn.commit();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
        self.lock.release();
    # -----------------------
    # CPF
    # -----------------------
    def insert_cpf(self,tupla:tuple=[]) -> None:
        comando = ( "INSERT INTO cpf "
                    "(id_user, dia, CPF, status) "
                    "VALUES(%s,now(),%s,%s) ");
        if(not isinstance(tupla,tuple)):
            return;
        elif(len(tupla) != 3):
            # Exemplo de o que deveria vir
            # tupla = ('id_user', 'CPF', 'status',);
            return;
        id_user = tupla[0];
        cpf     = tupla[1];
        if(self.__verifica_cpf(id_user=id_user,cpf=cpf)):
            return;
        self.__insert(comando=comando,tupla=tupla);

    def __verifica_cpf(self,id_user:str='',cpf:str='') -> bool:
        if((id_user == '') or (not isinstance(id_user,str))):
            return False;
        if((cpf == '') or (not isinstance(cpf,str))):
            return False;
        comando = ( f"SELECT * FROM cpf "
                    f"WHERE id_user='{id_user}' "
                    f"AND CPF='{cpf}' ");
        if(self.__select(comando=comando) == []):
            return False;
        return True;
    # -----------------------    
    # CNPJ
    # -----------------------
    def insert_cnpj(self,tupla:tuple=[]) -> None:
        comando = ( " INSERT INTO cnpj "
                    " (id_user, dia, CNPJ, status) "
                    " VALUES(%s,now(),%s,%s)");
        if(not isinstance(tupla,tuple)):
            return;
        elif(len(tupla) != 3):
            # Exemplo de o que deveria vir
            # tupla = ('id_user', 'CNPJ', 'status',);
            return;
        id_user = tupla[0];
        cnpj    = tupla[1];
        if(self.__verifica_cnpj(id_user=id_user,cnpj=cnpj)):
            return;
        self.__insert(comando=comando,tupla=tupla);
    
    def __verifica_cnpj(self,id_user:str='',cnpj:str='') -> bool:
        if((id_user == '') or (not isinstance(id_user,str))):
            return False;
        if((cnpj == '') or (not isinstance(cnpj,str))):
            return False;
        comando = ( f" SELECT * FROM cnpj "
                    f" WHERE id_user='{id_user}' "
                    f" AND CNPJ='{cnpj}' ");
        if(self.__select(comando=comando) == []):
            return False;
        return True;
    # -----------------------    
    # RASTREIO
    # -----------------------
    def insert_rastreio(self,tupla:tuple=[]) -> None:
        comando = ( " INSERT INTO encomenda "
                    " (id_user, codigo, nome_rastreio, "
                    " dia, informacoes) VALUES(%s,%s,%s, "
                    " now(),%s)");
        if(not isinstance(tupla,tuple)):
            return;
        elif(len(tupla) != 4):
            # Exemplo de o que deveria vir
            # tupla = ( 'id_user',       'codigo',
            #           'nome_rastreio', 'informacoes');
            return;
        id_user = tupla[0];
        codigo  = tupla[1];
        if(self.__verifica_rastreio(id_user=id_user,codigo=codigo)):
            return;
        self.__insert(comando=comando,tupla=tupla);
    
    def __verifica_rastreio(self,id_user:str='',codigo:str='') -> bool:
        if((id_user == '') or (not isinstance(id_user,str))):
            return False;
        if((codigo == '') or (not isinstance(codigo,str))):
            return False;
        comando = ( f" SELECT * "
                    f" FROM encomenda "
                    f" WHERE id_user='{id_user}' "
                    f" AND codigo='{codigo}'");
        if(self.__select(comando=comando) == []):
            return False;
        return True;
    
    def select_rastreio(self,id_user:str='') -> list:
        if((id_user == '') or (not isinstance(id_user,str))):
            return [];
        comando = ( f" SELECT informacoes, nome_rastreio, "
                    f" codigo FROM encomenda  "
                    f" WHERE id_user='{id_user}' "
                    f" ORDER BY id DESC ");
        return self.__select(comando=comando);

    def delete_rastreio(self,id_user:str='',codigo:str='') -> bool:
        if((id_user == '') or (not isinstance(id_user,str))):
            return False;
        if((codigo == '') or (not isinstance(codigo,str))):
            return False;
        comando = ( f" DELETE FROM encomenda "
                    f" WHERE id_user='{id_user}' "
                    f" AND codigo='{codigo}' ");
        if(self.__verifica_rastreio(id_user=id_user,codigo=codigo)):
            self.__delete(comando=comando);
            return True;
        return False;
    
    def atualiza_rastreio(self) -> list:
        comando = ( f" SELECT id_user, codigo, "
                    f" informacoes, nome_rastreio "
                    f" FROM encomenda ORDER BY dia "
                    f" LIMIT 1");
        dados = self.__select(comando=comando);
        if(dados != []):
            id_user = str(dados[0][0]);
            codigo  = str(dados[0][1]);
            info    = str(dados[0][2]);
            nome    = str(dados[0][3]);
            return [id_user,codigo,info,nome];
        return [];
    
    def validar_rastreio(self) -> Union[int,float]:
        comando = ( f" SELECT TIMESTAMPDIFF(SECOND, dia,NOW()) "
                    f" from encomenda "
                    f" ORDER BY dia LIMIT 1 ");
        dados = self.__select(comando=comando);
        if(dados != []):
            data = float(dados[0][0]);
            return data;
        return -1;

    def update_rastreio(self,tupla:tuple=[]) -> None:
        if(not isinstance(tupla,tuple)):
            return;
        elif(len(tupla) != 3):
            # Exemplo de o que deveria vir
            # tupla = ('id_user', 'CPF', 'status',);
            return;
        id_user     = tupla[0];
        codigo      = tupla[1];
        informacoes = tupla[2];
        if((id_user == '') or (not isinstance(id_user,str))):
            return;
        if((codigo == '') or (not isinstance(codigo,str))):
            return;
        if((informacoes == '') or (not isinstance(informacoes,str))):
            return;
        comando = ( f" UPDATE encomenda "
                    f" SET dia=now(), " 
                    f" informacoes='{informacoes}' "
                    f" WHERE id_user='{id_user}' "
                    f" AND codigo='{codigo}'");
        self.__update(comando=comando);
    # -----------------------
    # Mensagens
    # -----------------------
    def insert_mensagem(self,tupla:tuple=[]) -> None:
        comando = ( "INSERT INTO mensagem "
                    "(id_user, dia, log_mensagem) "
                    "VALUES(%s,now(),%s) ");
        if(not isinstance(tupla,tuple)):
            return;
        elif(len(tupla) != 2):
            # Exemplo de o que deveria vir
            # tupla = ('id_user', 'mensagem');
            return;
        self.__insert(comando=comando,tupla=tupla);
#-----------------------
# FUNÇÕES
#-----------------------
#-----------------------
# MAIN()
#-----------------------
if(__name__ == "__main__"):
    pass;
#-----------------------