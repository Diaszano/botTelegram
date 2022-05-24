#-----------------------
# BIBLIOTECAS
#-----------------------
import mysql.connector
#-----------------------
# CLASSES
#-----------------------
class DataBase():
    def __init__(self,host:str='',user:str='',password:str='',database:str='')->None:
        self.host = host;
        self.user = user;
        self.password = password;
        self.database = database;

    def conexao(self,host:str='',user:str='',password:str='',database:str='')->list:
        if(host != ''):
            self.host = host;
        if(user != ''):
            self.user = user;
        if(password != ''):
            self.password = password;
        if(database != ''):
            self.database = database;
        if((self.host == '') or (self.user == '') or (self.password == '') or (self.database == '')):
                print("Está faltando argumentos na conexão, faça novamente!");
                return [None,None];
        else:
            cnxn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            );
            cursor = cnxn.cursor();
            return [cnxn,cursor];
    # -----------------------
    # CPF
    # -----------------------
    def insert_cpf(self,comando:str='',tupla=[]) -> None:
        if(comando == ''):
            comando =   """ 
                            INSERT INTO bot_telegram.cpf
                            (id_user, dia, CPF, status)
                            VALUES(%s,now(),%s,%s)
                        """;
        if(tupla == []):
            tupla = ('id_user', 'CPF', 'status', 'dia');
            return;
        if(self.verifica_cpf(id_user=tupla[0],CPF=tupla[1])):
            return;
        try:
            [cnxn,cursor] = self.conexao();
            cursor.execute(comando, tupla);
            cnxn.commit();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
            

    def verifica_cpf(self,comando:str='',id_user:str='',CPF:str='') -> bool:
        if(id_user == '' or CPF == ''):
            return False;
        if(comando == ''):
            comando =   f""" 
                            SELECT * FROM bot_telegram.cpf
                            WHERE id_user='{id_user}' AND CPF LIKE '{CPF}%'
                        """;
        try:
            [cnxn,cursor] = self.conexao();
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
            comando =   """ 
                            INSERT INTO bot_telegram.cnpj
                            (id_user, dia, CNPJ, status)
                            VALUES(%s,now(),%s,%s)
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
                            SELECT * FROM bot_telegram.cnpj
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
                            FROM bot_telegram.encomenda
                            WHERE id_user='{id_user}' 
                            AND
                            codigo='{codigo}'
                        """;
        try:
            [cnxn,cursor] = self.conexao();
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
            comando =   """ 
                            INSERT INTO bot_telegram.encomenda
                            (id_user, codigo, nome_rastreio, dia, informacoes)
                            VALUES(%s,%s,%s,now(),%s)
                        """;
        if(tupla == []):
            tupla = ('id_user','codigo','nome_rastreio','dia','informacoes');
        if(self.verifica_rastreio(id_user=tupla[0],codigo=tupla[1])):
            return;
        try:
            [cnxn,cursor] = self.conexao();
            cursor.execute(comando, tupla);
            cnxn.commit();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
            
        
    
    def delete_rastreio(self,comando:str='',id_user:str='',codigo:str='') -> None:
        if(id_user == '' or codigo == ''):
            return;
        if(comando == ''):
            comando =   f""" 
                            DELETE FROM bot_telegram.encomenda
                            WHERE id_user='{id_user}' AND codigo='{codigo}'
                        """;
        try:
            [cnxn,cursor] = self.conexao();
            cursor.execute(comando);
            cnxn.commit();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
            
        

    def select_rastreio(self,comando:str='',id_user:str='') -> list:
        if(comando == ''):
            comando =   f"SELECT informacoes, nome_rastreio, codigo FROM bot_telegram.encomenda  WHERE id_user='{id_user}' ORDER BY id DESC";
        try:
            [cnxn,cursor] = self.conexao();
            cursor.execute(comando);
            data = cursor.fetchall();
            cursor.close();
            return data;
        except mysql.connector.Error as error:
            print("Falha do comando", error);
            return [];
        
    
    def atualiza_rastreio(self,comando:str='') -> list:
        if(comando == ''):
            comando =   f'SELECT id_user, codigo, informacoes, nome_rastreio FROM encomenda ORDER BY dia LIMIT 1';
        try:
            [cnxn,cursor] = self.conexao();
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
            comando =   f'SELECT TIMESTAMPDIFF(SECOND, dia,NOW()) from bot_telegram.encomenda ORDER BY dia LIMIT 1';
        try:
            [cnxn,cursor] = self.conexao();
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
    
    def update_rastreio(self,id_user:str='',codigo:str='',comando:str='',informacoes:str='') -> bool:
        if(comando == ''):
            comando =   f"""    UPDATE encomenda
                                SET dia=now(), 
                                informacoes='{informacoes}'
                                WHERE id_user='{id_user}' AND codigo='{codigo}'
                        """;
        try:
            [cnxn,cursor] = self.conexao();
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
            comando =   (
                            "INSERT INTO bot_telegram.mensagem "
                            "(id_user, dia, log_mensagem) "
                            "VALUES(%s,now(),%s) "
                        );
        if(tupla == []):
            tupla = ('id_user', 'dia', 'mensagem');
            return;
        try:
            [cnxn,cursor] = self.conexao();
            cursor.execute(comando, params=tupla);
            cnxn.commit();
            cursor.close();
        except mysql.connector.Error as error:
            print("Falha do comando", error);
#-----------------------
# MAIN()
#-----------------------
if(__name__ == "__main__"):
    pass;
#-----------------------