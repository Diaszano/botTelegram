"""Conexão com o Banco de Dados SqLite"""
#-----------------------
# BIBLIOTECAS
#-----------------------
import os
import sqlite3
from datetime import datetime
#-----------------------
# CLASSES
#-----------------------
class DataBaseSqlite():
    def __init__(self) -> None:
        caminho = os.path.dirname(os.path.realpath(__file__));
        pasta   = os.path.join(caminho,"data");
        arquivo    = "rastreador.db";
        if(not(os.path.exists(pasta))):
            os.mkdir(pasta);
        self.nome = os.path.join(pasta,arquivo);
        self.__create_table();
        self.__create_index();
    # -----------------------
    # OUTROS
    # -----------------------
    def __conexao(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.nome);
        return connection;
    
    @staticmethod
    def __dif_minutos(date1)->float:
        data_agora = datetime.now();
        date2      = data_agora.strftime('%Y-%m-%d %H:%M:%S');
        d1         = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S');
        d2         = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S');
        resultado  = d2-d1;
        segundos   = resultado.total_seconds();
        segundos   = float(segundos);
        return segundos;
    
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
            self.__execute_create(comando=comando);
        
    def __execute_create(self,comando:str):
        try:
            Connection = self.__conexao();
            cursor = Connection.cursor();
            cursor.execute(comando);
            Connection.commit();
            cursor.close();
        except sqlite3.Error as error:
            print("Falha do comando", error);
            if Connection:
                Connection.close();
        finally:
            if Connection:
                Connection.close();
    # -----------------------
    # CPF
    # -----------------------
    def creat_table_cpf(self,comando:str='') -> None:
        if(comando == ''):
            comando =   """ CREATE TABLE IF NOT EXISTS cpf(
                            id              INTEGER primary key autoincrement,
                            id_user         TEXT NOT NULL,
                            CPF             TEXT NOT NULL,
                            status          TEXT NOT NULL,
                            dia             TEXT NOT NULL)
                        """;
        self.creat_table(comando=comando);
    
    def insert_cpf(self,comando:str='',tupla=[]) -> None:
        if(comando == ''):
            comando =   """ 
                            INSERT INTO cpf
                            (id_user, CPF, status, dia)
                            VALUES(?, ?, ?,(SELECT DATETIME('now','localtime')))
                        """;
        if(tupla == []):
            tupla = ('id_user', 'CPF', 'status', 'dia');
            return;
        if(self.verifica_cpf(id_user=tupla[0],CPF=tupla[1])):
            return;
        try:
            self.conexao();
            Connection = self.connection;
            cursor = Connection.cursor();
            cursor.execute(comando, tupla);
            Connection.commit();
            cursor.close();
        except sqlite3.Error as error:
            print("Falha do comando", error);
            if Connection:
                Connection.close();
        finally:
            if Connection:
                Connection.close();

    def verifica_cpf(self,comando:str='',id_user:str='',CPF:str='') -> bool:
        if(id_user == '' or CPF == ''):
            return False;
        if(comando == ''):
            comando =   f""" 
                            SELECT * FROM cpf
                            WHERE id_user='{id_user}' AND CPF LIKE '{CPF}%'
                        """;
        try:
            self.conexao();
            Connection = self.connection;
            cursor = Connection.cursor();
            cursor.execute(comando);
            if cursor.fetchall() != []:
                cursor.close();
                return True;
            cursor.close();
            return False;
        except sqlite3.Error as error:
            print("Falha do comando", error);
            if Connection:
                Connection.close();
            return False;
        finally:
            if Connection:
                Connection.close();
    # -----------------------    
    # CNPJ
    # -----------------------
    def creat_table_cnpj(self,comando:str='') -> None:
        if(comando == ''):
            comando =   """ CREATE TABLE IF NOT EXISTS cnpj(
                            id              INTEGER primary key autoincrement,
                            id_user         TEXT NOT NULL,
                            CNPJ            TEXT NOT NULL,
                            status          TEXT NOT NULL,
                            dia             TEXT NOT NULL)
                        """;
        self.creat_table(comando=comando);
    
    def insert_cnpj(self,comando:str='',tupla=[]) -> None:
        if(comando == ''):
            comando =   """ 
                            INSERT INTO cnpj
                            (id_user, CNPJ, status, dia)
                            VALUES(?, ?, ?,(SELECT DATETIME('now','localtime')))
                        """;
        if(tupla == []):
            tupla = ('id_user', 'CNPJ', 'status', 'dia');
            return;
        if(self.verifica_cnpj(id_user=tupla[0],CNPJ=tupla[1])):
            return;
        self.insert_cpf(comando=comando,tupla=tupla);

    def verifica_cnpj(self,comando:str='',id_user:str='',CNPJ:str='') -> bool:
        if(id_user == '' or CNPJ == ''):
            return False;
        if(comando == ''):
            comando =   f""" 
                            SELECT * FROM cnpj
                            WHERE id_user='{id_user}' AND CNPJ LIKE '{CNPJ}%'
                        """;
        return self.verifica_cpf(comando=comando,id_user=id_user,CPF=CNPJ);
    # -----------------------    
    # RASTREIO
    # -----------------------
    def verifica_rastreio(self,comando:str='',id_user:str='',codigo:str='') -> bool:
        if(id_user == '' or codigo == ''):
            return False;
        if(comando == ''):
            comando =   f""" 
                            SELECT *
                            FROM encomenda
                            WHERE id_user='{id_user}' 
                            AND
                            codigo='{codigo}'
                        """;
        try:
            self.conexao();
            Connection = self.connection;
            cursor = Connection.cursor();
            cursor.execute(comando);
            tmp = cursor.fetchall();
            if tmp != []:
                cursor.close();
                return True;
            cursor.close();
            return False;
        except sqlite3.Error as error:
            print("Falha do comando", error);
            if Connection:
                Connection.close();
            return False;
        finally:
            if Connection:
                Connection.close();
    
    def insert_rastreio(self,comando:str='',tupla=[]) -> None:
        if(comando == ''):
            comando =   """ 
                            INSERT INTO encomenda
                            (id_user, codigo, nome_rastreio, 'data', informacoes)
                            VALUES(?, ?, ?,(SELECT DATETIME('now','localtime')), ?)
                        """;
        if(tupla == []):
            tupla = ('id_user','codigo','nome_rastreio','data','informacoes');
        if(self.verifica_rastreio(id_user=tupla[0],codigo=tupla[1])):
            return;
        try:
            self.conexao();
            Connection = self.connection;
            cursor = Connection.cursor();
            cursor.execute(comando, tupla);
            Connection.commit();
            cursor.close();
        except sqlite3.Error as error:
            print("Falha do comando", error);
            if Connection:
                Connection.close();
        finally:
            if Connection:
                Connection.close();
    
    def delete_rastreio(self,comando:str='',id_user:str='',codigo:str='') -> None:
        if(id_user == '' or codigo == ''):
            return;
        if(comando == ''):
            comando =   f""" 
                            DELETE FROM encomenda
                            WHERE id_user='{id_user}' AND codigo='{codigo}'
                        """;
        try:
            self.conexao();
            Connection = self.connection;
            cursor = Connection.cursor();
            cursor.execute(comando);
            Connection.commit();
            cursor.close();
        except sqlite3.Error as error:
            print("Falha do comando", error);
            if Connection:
                Connection.close();
        finally:
            if Connection:
                Connection.close();

    def select_rastreio(self,comando:str='',id_user:str='') -> list:
        if(comando == ''):
            comando =   f"SELECT informacoes, nome_rastreio, codigo FROM encomenda  WHERE id_user='{id_user}' ORDER BY id";
        try:
            self.conexao();
            Connection = self.connection;
            cursor     = Connection.cursor();
            cursor.execute(comando);
            data = cursor.fetchall();
            cursor.close();
            return data;
        except sqlite3.Error as error:
            print("Falha do comando", error);
            if Connection:
                Connection.close();
                return [];
        finally:
            if Connection:
                Connection.close();
    
    def atualiza_rastreio(self,comando:str='') -> list:
        if(comando == ''):
            comando =   f'SELECT id_user, codigo, informacoes, nome_rastreio FROM encomenda ORDER BY data LIMIT 1';
        try:
            self.conexao();
            Connection = self.connection;
            cursor     = Connection.cursor();
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
        except sqlite3.Error as error:
            print("Falha do comando", error);
            if Connection:
                Connection.close();
                return [];
        finally:
            if Connection:
                Connection.close();

    def validar_rastreio(self,comando:str='') -> float:
        if(comando == ''):
            comando =   f'SELECT data FROM encomenda ORDER BY data LIMIT 1';
        try:
            self.conexao();
            Connection = self.connection;
            cursor     = Connection.cursor();
            cursor.execute(comando);
            data = cursor.fetchall();
            if data != []:
                data = str(data[0][0]);
                data = self.dif_minutos(data);
                cursor.close();
                return data;
            cursor.close();
            return -1;
        except sqlite3.Error as error:
            print("Falha do comando", error);
            if Connection:
                Connection.close();
                return -1;
        finally:
            if Connection:
                Connection.close();
    
    def update_rastreio(self,id_user:str='',codigo:str='',comando:str='',informacoes:str='') -> bool:
        if(comando == ''):
            comando =   f""" UPDATE encomenda
                            SET 'data'=(SELECT DATETIME('now','localtime')), 
                            informacoes='{informacoes}'
                            WHERE id_user='{id_user}' AND codigo='{codigo}'
                        """;
        try:
            self.conexao();
            Connection = self.connection;
            cursor     = Connection.cursor();
            cursor.execute(comando);
            Connection.commit();
            cursor.close();
        except sqlite3.Error as error:
            print("Falha do comando", error);
            if Connection:
                Connection.close();
        finally:
            if Connection:
                Connection.close();
    # -----------------------
    # Mensagens
    # -----------------------
    def creat_table_mensagem(self,comando:str='') -> None:
        if(comando == ''):
            comando =   """ CREATE TABLE IF NOT EXISTS mensagem(
                            id              INTEGER primary key autoincrement,
                            id_user         TEXT NOT NULL,
                            dia             TEXT NOT NULL,
                            mensagem        BLOB NOT NULL)
                        """;
        self.creat_table(comando=comando);

    def insert_mensagem(self,comando:str='',tupla=[]) -> None:
        if(comando == ''):
            comando =   """ 
                            INSERT INTO mensagem
                            (id_user, dia, mensagem)
                            VALUES(?, (SELECT DATETIME('now','localtime')), ?)
                        """;
        if(tupla == []):
            tupla = ('id_user', 'dia', 'mensagem');
            return;
        try:
            self.conexao();
            Connection = self.connection;
            cursor = Connection.cursor();
            cursor.execute(comando, tupla);
            Connection.commit();
            cursor.close();
        except sqlite3.Error as error:
            print("Falha do comando", error);
            if Connection:
                Connection.close();
        finally:
            if Connection:
                Connection.close();
#-----------------------
# MAIN()
#-----------------------
if(__name__ == "__main__"):
    pass;
#-----------------------