"""Conexão com o Banco de Dados MariaDB"""
#-----------------------
# BIBLIOTECAS
#-----------------------
import mysql.connector
from threading import Lock
from .database import DataBase
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class DataBaseMariaDB(DataBase):
    def __init__(   self,host:str='',user:str='',
                    password:str='',database:str='')->None:
        self._host     = host;
        self._user     = user;
        self._password = password;
        self._database = database;
        self.lock      = Lock();
    # -----------------------
    # Criação e conexão
    # -----------------------
    def _conexao(self,host:str='',user:str='',
                password:str='',database:str='')->list:
        if(host != ''):
            self._host = host;
        if(user != ''):
            self._user = user;
        if(password != ''):
            self._password = password;
        if(database != ''):
            self._database = database;
        if( (self._host == '') or (self._user == '') or
            (self._password == '') or (self._database == '')):
            mensagem = ("Está faltando argumentos na "
                        "conexão, faça novamente!");
            print(mensagem);
            return [None,None];
        else:
            cnxn = mysql.connector.connect(
                host=self._host,
                user=self._user,
                password=self._password,
                database=self._database,
            );
            cursor = cnxn.cursor();
            return [cnxn,cursor];
    # -----------------------
    # CRUD
    # -----------------------
    # Create
    def _insert(self,comando:str,tupla:tuple) -> None:
        self.lock.acquire();
        try:
            [cnxn,cursor] = self._conexao();
            cursor.execute(comando, tupla);
            cnxn.commit();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
        finally:
            if cursor:
                cursor.close();
            if cnxn:
                cnxn.close();
            self.lock.release();
    # Read
    def _select(self,comando:str) -> list:
        self.lock.acquire();
        retorno:list = [];
        try:
            [cnxn,cursor] = self._conexao();
            cursor.execute(comando);
            retorno = cursor.fetchall();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
        finally:
            if cursor:
                cursor.close();
            if cnxn:
                cnxn.close();
            self.lock.release();
            return retorno;
    # Update
    def _update(self,comando:str) -> None:
        self.lock.acquire();
        try:
            [cnxn,cursor] = self._conexao();
            cursor.execute(comando);
            cnxn.commit();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
        finally:
            if cursor:
                cursor.close();
            if cnxn:
                cnxn.close();
            self.lock.release();
    # Delete
    def _delete(self,comando:str) -> None:
        self.lock.acquire();
        try:
            [cnxn,cursor] = self._conexao();
            cursor.execute(comando);
            cnxn.commit();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
        finally:
            if cursor:
                cursor.close();
            if cnxn:
                cnxn.close();
            self.lock.release();
#-----------------------
# FUNÇÕES
#-----------------------
#-----------------------
# MAIN()
#-----------------------
if(__name__ == "__main__"):
    pass;
#-----------------------