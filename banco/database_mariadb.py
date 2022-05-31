"""Conexão com o Banco de Dados MariaDB"""
#-----------------------
# BIBLIOTECAS
#-----------------------
import mysql.connector
from .database_sqlite import DataBaseSqlite
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class DataBaseMariaDB():
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, '__is_alive'):
    #         cls.__is_alive = super().__new__(cls,*args, **kwargs);
    #     return cls.__is_alive;

    def __init__(   self,host:str='',user:str='',
                    password:str='',database:str='')->None:
        self.__host     = host;
        self.__user     = user;
        self.__password = password;
        self.__database = database;
        self.__lite     = DataBaseSqlite();
    
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
    # CPF
    # -----------------------
    def insert_cpf(self,comando:str='',tupla=[]) -> None:
        if(comando == ''):
            comando = ( "INSERT INTO cpf "
                        "(id_user, dia, CPF, status) "
                        "VALUES(%s,now(),%s,%s) ");
        if(tupla == []):
            tupla = ('id_user', 'CPF', 'status', 'dia');
            return;
        if(self.__verifica_cpf(id_user=tupla[0],CPF=tupla[1])):
            return;
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando, tupla);
            cnxn.commit();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
            
    def __verifica_cpf( self,comando:str='',id_user:str=''
                        ,CPF:str='') -> bool:
        if(id_user == '' or CPF == ''):
            return False;
        if(comando == ''):
            comando = ( f"SELECT * FROM cpf "
                        f"WHERE id_user='{id_user}' "
                        f"AND CPF LIKE '{CPF}%'");
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando);
            if cursor.fetchall() != []:
                cursor.close();
                return True;
            cursor.close();
            return False;
        except mysql.connector.Error as error:
            print("Falha do comando", error);
            return False;
    # -----------------------    
    # CNPJ
    # -----------------------
    def insert_cnpj(self,comando:str='',tupla=[]) -> None:
        if(comando == ''):
            comando = ( " INSERT INTO cnpj "
                        " (id_user, dia, CNPJ, status) "
                        " VALUES(%s,now(),%s,%s)");
        if(tupla == []):
            tupla = ('id_user', 'CNPJ', 'status', 'dia');
            return;
        if(self.__verifica_cnpj(id_user=tupla[0],CNPJ=tupla[1])):
            return;
        self.insert_cpf(comando=comando,tupla=tupla);

    def __verifica_cnpj(self,comando:str='',id_user:str='',
                        CNPJ:str='') -> bool:
        if(id_user == '' or CNPJ == ''):
            return False;
        if(comando == ''):
            comando = ( f" SELECT * FROM cnpj "
                        f" WHERE id_user='{id_user}' "
                        f" AND CNPJ LIKE '{CNPJ}%' ");
        return self.__verifica_cpf( comando=comando,id_user=id_user,
                                    CPF=CNPJ);
    # -----------------------    
    # RASTREIO
    # -----------------------
    def verifica_rastreio(  self,comando:str='',id_user:str='',
                            codigo:str='') -> bool:
        if(id_user == '' or codigo == ''):
            return False;
        if(comando == ''):
            comando = ( f" SELECT * "
                        f" FROM encomenda "
                        f" WHERE id_user='{id_user}' "
                        f" AND codigo='{codigo}'");
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando);
            tmp = cursor.fetchall();
            if tmp != []:
                cursor.close();
                return True;
            cursor.close();
            return False;
        except mysql.connector.Error as error:
            print("Falha do comando", error);
            return False;
    
    def insert_rastreio(self,comando:str='',tupla=[]) -> None:
        if(comando == ''):
            comando = ( " INSERT INTO encomenda "
                        " (id_user, codigo, nome_rastreio, "
                        " dia, informacoes) VALUES(%s,%s,%s, "
                        " now(),%s)");
        if(tupla == []):
            tupla = (   'id_user','codigo','nome_rastreio',
                        'dia','informacoes');
        if(self.verifica_rastreio(id_user=tupla[0],codigo=tupla[1])):
            return;
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando, tupla);
            cnxn.commit();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
            
    def delete_rastreio(self,comando:str='',id_user:str='',
                        codigo:str='') -> None:
        if(id_user == '' or codigo == ''):
            return;
        if(comando == ''):
            comando = ( f" DELETE FROM encomenda "
                        f" WHERE id_user='{id_user}' "
                        f" AND codigo='{codigo}' ");
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando);
            cnxn.commit();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);

    def select_rastreio(self,comando:str='',id_user:str='') -> list:
        if(comando == ''):
            comando = ( f" SELECT informacoes, nome_rastreio, "
                        f" codigo FROM encomenda  "
                        f" WHERE id_user='{id_user}' "
                        f" ORDER BY id DESC ");
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando);
            data = cursor.fetchall();
            cursor.close();
            return data;
        except mysql.connector.Error as error:

            print("Falha do comando", error);
            return [];
    
    def atualiza_rastreio(self,comando:str='') -> list:
        if(comando == ''):
            comando = ( f" SELECT id_user, codigo, "
                        f" informacoes, nome_rastreio "
                        f" FROM encomenda ORDER BY dia "
                        f" LIMIT 1 ");
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando);
            data = cursor.fetchall();
            if data != []:
                id_user = str(data[0][0]);
                codigo  = str(data[0][1]);
                info    = str(data[0][2]);
                nome    = str(data[0][3]);
                cursor.close();
                return [id_user,codigo,info,nome];
            cursor.close();
            return [];
        except mysql.connector.Error as error:
            print("Falha do comando", error);
            return [];

    def validar_rastreio(self,comando:str='') -> float:
        if(comando == ''):
            comando = ( f" SELECT TIMESTAMPDIFF(SECOND, dia,NOW()) "
                        f" from encomenda "
                        f" ORDER BY dia LIMIT 1 ");
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando);
            data = cursor.fetchall();
            if data != []:
                data = float(data[0][0]);
                cursor.close();
                return data;
            cursor.close();
            return -1;
        except mysql.connector.Error as error:
            print("Falha do comando", error);
            return -1;
    
    def update_rastreio(self,id_user:str='',codigo:str='',
                        comando:str='',informacoes:str='') -> bool:
        if(comando == ''):
            comando = ( f" UPDATE encomenda "
                        f" SET dia=now(), " 
                        f" informacoes='{informacoes}' "
                        f" WHERE id_user='{id_user}' "
                        f" AND codigo='{codigo}' ");
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando);
            cnxn.commit();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
    # -----------------------
    # Mensagens
    # -----------------------
    def insert_mensagem(self,comando:str='',tupla=[]) -> None:
        if(comando == ''):
            comando = ( "INSERT INTO mensagem "
                        "(id_user, dia, log_mensagem) "
                        "VALUES(%s,now(),%s) ");
        if(tupla == []):
            tupla = ('id_user', 'dia', 'mensagem');
            return;
        try:
            [cnxn,cursor] = self.__conexao();
            cursor.execute(comando, params=tupla);
            cnxn.commit();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# MAIN()
#-----------------------
if(__name__ == "__main__"):
    pass;
#-----------------------