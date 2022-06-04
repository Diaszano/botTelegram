"""Conexão com o Banco de Dados SqLite"""
#-----------------------
# BIBLIOTECAS
#-----------------------
import os
import sys
import sqlite3
from typing import Union
from threading import Lock
from .database import DataBase
from datetime import datetime
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class DataBaseSqlite(DataBase):
    def __init__(self) -> None:
        caminho = os.path.dirname(os.path.realpath('~/'));
        pasta   = os.path.join(caminho,"data");
        arquivo = "rastreador.db";
        if(not(os.path.exists(pasta))):
            os.mkdir(pasta);
        self.nome = os.path.join(pasta,arquivo);
        self.lock = Lock();
        self.__create_table();
        self.__create_index();
    # -----------------------
    # Funções estáticas
    # -----------------------
    @staticmethod
    def _dif_segundos(data:str) -> Union[int,float]:
        if((data == '') or (not isinstance(data,str))):
            return -1;
        data_agora = datetime.now();
        date2      = data_agora.strftime('%Y-%m-%d %H:%M:%S');
        d1         = datetime.strptime(data,'%Y-%m-%d %H:%M:%S');
        d2         = datetime.strptime(date2,'%Y-%m-%d %H:%M:%S');
        resultado  = d2-d1;
        segundos   = resultado.total_seconds();
        segundos   = float(segundos);
        return segundos;
    
    @staticmethod
    def __corrigir_comando(comando:str) -> str:
        now     = "(SELECT DATETIME('now','localtime'))";
        comando = comando.replace('%s','?');
        comando = comando.replace('now()',now);
        return comando;
    # -----------------------
    # Criação e conexão
    # -----------------------
    def _conexao(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.nome);
        return connection;
    
    def __create_index(self) -> None:
        comandos = [
            # Tabela das mensagem
            (   " CREATE INDEX IF NOT EXISTS "
                " index_mensagem_id_user "
                " ON mensagem(id_user)"),
            (   " CREATE INDEX IF NOT EXISTS "
                " index_mensagem_dia "
                " ON mensagem(dia)"),
            # Tabela dos CNPJs
            (   " CREATE INDEX IF NOT EXISTS "
                " index_cnpj_id_user "
                " ON cnpj(id_user)"),
            (   " CREATE INDEX IF NOT EXISTS "
                " index_cnpj_CNPJ "
                " ON cnpj(CNPJ)"),
            (   " CREATE INDEX IF NOT EXISTS "
                " index_cnpj_status "
                " ON cnpj(status)"),
            # Tabela dos CPFs
            (   " CREATE INDEX IF NOT EXISTS "
                " index_cpf_id_user "	
                " ON cpf(id_user)"),
            (   " CREATE INDEX IF NOT EXISTS "
                " index_cpf_CPF "
                " ON cpf(CPF)"),
            (   " CREATE INDEX IF NOT EXISTS "
                " index_cpf_status "
                " ON cpf(status)"),
            # Tabela das Encomendas
            (   " CREATE INDEX IF NOT EXISTS "
                " index_encomenda_id_user "
                " ON encomenda(id_user)"),
            (   " CREATE INDEX IF NOT EXISTS "
                " index_encomenda_codigo "
                " ON encomenda(codigo)")
        ];
        for comando in comandos:
            self.__execute_create(comando=comando);
    
    def __create_table(self) -> None:
        comandos = [
            # Tabela das Mensagens
            (   " CREATE TABLE IF NOT EXISTS mensagem( "
                " id			INTEGER PRIMARY KEY AUTOINCREMENT, "
                " id_user 		INTEGER NOT NULL, "
                " dia 			TEXT	NOT NULL, "
                " log_mensagem 	TEXT 	NOT NULL) "),
            # Tabela dos CNPJs
            (   " CREATE TABLE IF NOT EXISTS cnpj( "
                " id		INTEGER PRIMARY KEY AUTOINCREMENT, "
                " id_user 	INTEGER NOT NULL, "
                " dia 		TEXT	NOT NULL, "
                " CNPJ		TEXT	NOT NULL, "
                " status	TEXT	NOT NULL) "),
            # Tabela dos CPFs
            (   "CREATE TABLE IF NOT EXISTS cpf( "
                " id		INTEGER PRIMARY KEY AUTOINCREMENT, "
                " id_user 	INTEGER NOT NULL, "
                " dia 		TEXT	NOT NULL, "
                " CPF		TEXT	NOT NULL, "
                " status	TEXT	NOT NULL) "),
            # Tabela das Encomendas
            (   "CREATE TABLE IF NOT EXISTS encomenda( "
                " id			INTEGER PRIMARY KEY AUTOINCREMENT, "
                " id_user 		INTEGER NOT NULL, "
                " codigo		TEXT	NOT NULL, "
                " nome_rastreio	TEXT	NOT NULL, "
                " dia 			TEXT	NOT NULL, "
                " informacoes   TEXT 	NOT NULL) ")
        ];
        for comando in comandos:
            if(self.__execute_create(comando=comando) == False):
                sys.exit(0);
        
    def __execute_create(self,comando:str) -> Union[None,bool]:
        retorno:bool = False;
        self.lock.acquire();
        try:
            cnxn   = self._conexao();
            cursor = cnxn.cursor();
            cursor.execute(comando);
            cnxn.commit();
            retorno = True;
        except sqlite3.Error as error:
            print("Falha do comando", error);
        finally:
            if cursor:
                cursor.close();
            if cnxn:
                cnxn.close();
            self.lock.release();
            return retorno;
    # -----------------------
    # CRUD
    # -----------------------
    # Create
    def _insert(self,comando:str,tupla:tuple) -> None:
        self.lock.acquire();
        comando = self.__corrigir_comando(comando=comando);
        try:
            cnxn   = self._conexao();
            cursor = cnxn.cursor();
            cursor.execute(comando, tupla);
            cnxn.commit();
        except sqlite3.Error as error:
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
        comando = self.__corrigir_comando(comando=comando);
        retorno:list = [];
        try:
            cnxn   = self._conexao();
            cursor = cnxn.cursor();
            cursor.execute(comando);
            retorno = cursor.fetchall();
        except sqlite3.Error as error:
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
        comando = self.__corrigir_comando(comando=comando);
        try:
            cnxn   = self._conexao();
            cursor = cnxn.cursor();
            cursor.execute(comando);
            cnxn.commit();
        except sqlite3.Error as error:
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
        comando = self.__corrigir_comando(comando=comando);
        try:
            cnxn   = self._conexao();
            cursor = cnxn.cursor();
            cursor.execute(comando);
            cnxn.commit();
        except sqlite3.Error as error:
            print("Falha do comando", error);
        finally:
            if cursor:
                cursor.close();
            if cnxn:
                cnxn.close();
            self.lock.release();
    # -----------------------    
    # RASTREIO
    # -----------------------
    def validar_rastreio(self) -> Union[int,float]:
        comando = ( f" SELECT dia FROM encomenda "
                    f" ORDER BY dia LIMIT 1");
        dados = self._select(comando=comando);
        if(dados != []):
            data = str(dados[0][0]);
            dif  = self._dif_segundos(data);
            return dif;
        return -1;
    # -----------------------
#-----------------------
# FUNÇÕES
#-----------------------
#-----------------------
# MAIN()
#-----------------------
if(__name__ == "__main__"):
    pass;
#-----------------------