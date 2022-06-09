"""Classe abstrata da Conexão com o banco"""
#-----------------------
# BIBLIOTECAS
#-----------------------
from typing import Union
from datetime import datetime
from abc import ABC, abstractmethod
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class DataBase(ABC):
    # -----------------------
    # Criação e conexão
    # -----------------------
    @abstractmethod
    def _conexao(self):
        """Conexão

        Aqui faremos a conexão com  o banco de dados
        """
        pass;
    # -----------------------
    # CRUD
    # -----------------------
    # Create
    @abstractmethod
    def _insert(self,comando:str,tupla:tuple) -> None:
        """Insert

        Aqui faremos o insert no banco de dados
        """
        pass;
    # Read
    @abstractmethod
    def _select(self,comando:str) -> list:
        """Select

        Aqui faremos o select no banco de dados
        """
        pass;
    # Update
    @abstractmethod
    def _update(self,comando:str) -> None:
        """Update

        Aqui faremos o update no banco de dados
        """
        pass;
    # Delete
    @abstractmethod
    def _delete(self,comando:str) -> None:
        """Delete

        Aqui faremos o delete no banco de dados
        """
        pass;
    # -----------------------
    # CPF
    # -----------------------
    def insert_cpf(self,tupla:tuple=[]) -> None:
        """Insert CPF

        Aqui salvaremos os CPFs que os users pesquisarem
        """
        comando:str = ( " INSERT INTO solicitacao_cpf "
                        " (id_user, id_cpf, dia) "
                        " VALUES(%s,%s,now()) ");
        if(not isinstance(tupla,tuple)):
            return;
        elif(len(tupla) != 3):
            return;
        
        id_user:str = tupla[0];
        cpf:str     = tupla[1];
        status:str  = tupla[2];

        [isTrue,id_cpf] = self._verifica_cpf(cpf=cpf)
        if(not isTrue):
            comando2:str     = (" INSERT INTO cpf "
                                " (CPF, status)"
                                " VALUES(%s,%s)");
            nova_tupla:tuple = (cpf,status);
            self._insert(comando=comando2,tupla=nova_tupla);
            while id_cpf == '':
                [isTrue,id_cpf] = self._verifica_cpf(cpf=cpf);
        tupla = (id_user,id_cpf);
        self._insert(comando=comando,tupla=tupla);

    def _verifica_cpf(self,cpf:str='') -> list:
        """Verifica CPF

        Aqui verificaremos se já existe o cpf solicitado
        """
        if((cpf == '') or (not isinstance(cpf,str))):
            return [False, ''];
        comando:str = ( f"SELECT id FROM cpf "
                        f"WHERE CPF='{cpf}' ");
        id_cpf:list = self._select(comando=comando);
        if(id_cpf == []):
            return [False,''];
        id_cpf:str = id_cpf[0][0];
        return [True,id_cpf];
    # -----------------------    
    # CNPJ
    # -----------------------
    def insert_cnpj(self,tupla:tuple=[]) -> None:
        """Insert CNPJ

        Aqui salvaremos os CNPJs que os users pesquisarem
        """
        comando:str = ( " INSERT INTO solicitacao_cnpj "
                        " (id_user, id_cnpj, dia) "
                        " VALUES(%s,%s,now()) ");

        if(not isinstance(tupla,tuple)):
            return;
        elif(len(tupla) != 3):
            return;
        
        id_user:str = tupla[0];
        cnpj:str    = tupla[1];
        status:str  = tupla[2];

        [isTrue,id_cnpj] = self._verifica_cnpj(cnpj=cnpj)
        if(not isTrue):
            comando2:str     = (" INSERT INTO cnpj "
                                " (CNPJ, status)"
                                " VALUES(%s,%s)");
            nova_tupla:tuple = (cnpj,status);

            self._insert(comando=comando2,tupla=nova_tupla);

            while id_cnpj == '':
                [isTrue,id_cnpj] = self._verifica_cnpj(cnpj=cnpj);

        tupla = (id_user,str(id_cnpj));
        self._insert(comando=comando,tupla=tupla);
    
    def _verifica_cnpj(self,cnpj:str='') -> list:
        """Verifica CNPJ

        Aqui verificaremos se já existe o cnpj solicitado
        """
        if((cnpj == '') or (not isinstance(cnpj,str))):
            return [False, ''];
        comando:str  = (f"SELECT id FROM cnpj "
                        f"WHERE CNPJ='{cnpj}' ");
        id_cnpj:list = self._select(comando=comando);
        if(id_cnpj == []):
            return [False,''];
        id_cnpj:str = id_cnpj[0][0];
        return [True,id_cnpj];
    # -----------------------    
    # RASTREIO
    # -----------------------
    def insert_rastreio(self,tupla:tuple=[]) -> None:
        """Inserir rastreio

        Aqui faremos a inserção do Rastreio no banco de dados
        tupla = ('id_user','codigo','nome_rastreio', 'informacoes')"""
        
        if(not isinstance(tupla,tuple)):
            return;
        elif(len(tupla) != 4):
            # Exemplo de o que deveria vir
            # tupla = ( 'id_user',       'codigo',
            #           'nome_rastreio', 'informacoes');
            return;
        
        comando:str = ( " INSERT INTO solicitacao_rastreio "
                        " (id_user, id_rastreio, nome_rastreio) "
                        " VALUES(%s, %s, %s)");
        
        id_user:str         = tupla[0];
        codigo:str          = tupla[1];
        nome_rastreio:str   = tupla[2];
        informacao:str      = tupla[3];

        [isTrue,id_rastreio] = self._verifica_rastreio(
                                codigo=codigo);
        
        if(isTrue):
            if(self._verifica_user_rastreio(id_user=id_user,
                id_rastreio=str(id_rastreio))):
                return;
        
        while id_rastreio == '':
            comando2:str = (" INSERT INTO rastreio "
                            " (codigo, informacoes, atualizacao)"
                            " VALUES(%s,%s,now())");
            nova_tupla:tuple = (codigo,informacao);
            self._insert(comando=comando2,tupla=nova_tupla);
            [isTrue,id_rastreio] = self._verifica_rastreio(
                                    codigo=codigo);
        nova_tupla:tuple = (id_user,id_rastreio,nome_rastreio);
        
        self._insert(comando=comando,tupla=nova_tupla);
    
    def _verifica_user_rastreio(self,id_user:str='',
                                id_rastreio:str='')->bool:
        """verificar User Rastreio

        Aqui faremos a verificação do user com o rastreio solicitado
        """
        if((id_user == '') or (not isinstance(id_user,str))):
            return False;
        if((id_rastreio == '') or (not isinstance(id_rastreio,str))):
            return False;
        
        comando:str      = (f" SELECT * "
                            f" FROM solicitacao_rastreio "
                            f" WHERE id_rastreio= "
                            f" '{id_rastreio}' AND "
                            f" id_user='{id_user}'");
        retorno = self._select(comando=comando);
        if(retorno == []):
            return False;
        return True;

    def _verifica_rastreio(self,codigo:str='') -> list:
        """verificar Rastreio

        Aqui faremos a verificação do Rastreio no banco de 
        dados e veremos se já existe este rastreio e se até 
        mesmo o user já inseriu esse rastreio, mas se não 
        existir esse rastreio ele insere no banco
        """
        if((codigo == '') or (not isinstance(codigo,str))):
            return [False, ''];
        
        comando:str      = (f" SELECT id "
                            f" FROM rastreio "
                            f" WHERE codigo='{codigo}'");
        id_rastreio:list = self._select(comando=comando);

        if(id_rastreio == []):
            return [False, ''];

        id_rastreio:str  = id_rastreio[0][0];
        return [True,id_rastreio];
    
    def select_rastreio(self,id_user:str='') -> list:
        """Select Rastreio

        Aqui pegaremos todos os rastreios do user
        """
        if((id_user == '') or (not isinstance(id_user,str))):
            return [];
        comando:str = ( f" SELECT informacoes, nome_rastreio, "
                        f" codigo FROM solicitacao_rastreio, "
                        f" rastreio WHERE rastreio.id = "
                        f" solicitacao_rastreio.id_rastreio"
                        f" AND {id_user} = "
                        f" solicitacao_rastreio.id_user"
                        f" ORDER BY id_rastreio DESC ");
        return self._select(comando=comando);

    def delete_rastreio(self,id_user:str='',codigo:str='') -> bool:
        """Delete Rastreio

        Aqui deletaremos o rastreio atribuído ao user
        """
        if((id_user == '') or (not isinstance(id_user,str))):
            return False;
        if((codigo == '') or (not isinstance(codigo,str))):
            return False;
        comando:str = ( f" DELETE FROM solicitacao_rastreio "
                        f" WHERE id_user='{id_user}' "
                        f" AND id_rastreio=(SELECT id "
                        f" FROM rastreio WHERE "
                        f" codigo='{codigo}') ");
        [isTrue,id_rastreio] = self._verifica_rastreio(
                                codigo=codigo);
        if(not isTrue):
            return False;
        if(not self._verifica_user_rastreio(id_user=id_user,
            id_rastreio=str(id_rastreio))):
            return False;
        self._delete(comando=comando);
        return True;

    def atualiza_rastreio(self) -> list:
        """Atualiza Rastreio

        Aqui veremos se o rastreio precisa ser atualizado e quem
        fez a solicitação desse rastreio
        """
        comando:str = ( f" SELECT id, codigo, informacoes"
                        f" FROM rastreio ORDER BY "
                        f" atualizacao LIMIT 1");
        dados:list  = self._select(comando=comando);
        if(dados != []):
            id_rastreio = str(dados[0][0]);
            codigo      = str(dados[0][1]);
            informacoes = str(dados[0][2]);
            
            comando = ( f" SELECT id_user, nome_rastreio "
                        f" FROM solicitacao_rastreio "
                        f" WHERE id_rastreio = "
                        f" {id_rastreio}");
                
            users:list = self._select(comando=comando);

            return [codigo,informacoes,users];
        return [];
    
    def validar_rastreio(self) -> Union[int,float]:
        """Validar Rastreio

        Aqui veremos quanto tempo faz que não atualizamos as
        informações dos rastreios
        """
        comando = ( f" SELECT TIMESTAMPDIFF(SECOND, "
                    f" atualizacao,now()) from rastreio "
                    f" ORDER BY atualizacao LIMIT 1 ");
        dados = self._select(comando=comando);
        if(dados != []):
            data = float(dados[0][0]);
            return data;
        return -1;

    def update_rastreio(self,tupla:tuple=[]) -> None:
        """Update Rastreio

        Aqui faremos a atualização das informações do rastreio
        no banco de dados
        \ntupla = ('codigo', 'informacoes',);
        """

        if(not isinstance(tupla,tuple)):
            return;
        elif(len(tupla) != 2):
            return;

        codigo      = tupla[0];
        informacoes = tupla[1];

        if((codigo == '') or (not isinstance(codigo,str))):
            return;
        if(not isinstance(informacoes,str)):
            return;
        
        comando = ( f" UPDATE rastreio "
                    f" SET atualizacao=now(), " 
                    f" informacoes='{informacoes}' "
                    f" WHERE codigo='{codigo}'");
        self._update(comando=comando);
    # -----------------------
    # Mensagens
    # -----------------------
    def insert_mensagem(self,tupla:tuple=[]) -> None:
        """Insert Mensagem

        Aqui salvaremos a mensagem que o user nos enviou como
        uma forma de segurança contra algum possível ato
        criminoso. 
        """
        comando:str = ( 
            " INSERT INTO mensagem "
            " (id_user, dia, log_mensagem) "
            " VALUES(%s,now(),%s) ");
        if(not isinstance(tupla,tuple)):
            return;
        elif(len(tupla) != 2):
            # Exemplo de o que deveria vir
            # tupla = ('id_user', 'mensagem');
            return;
        self._insert(comando=comando,tupla=tupla);
    # -----------------------
    # Horário do Remédio
    # -----------------------
    def insert_hora_do_remedio(self,tupla:tuple=[]) -> bool:
        """Insert Horário do Remédio

        :param  - tupla:tuple(id_user,hora,nome)
        :return - None 
        
        Aqui nós iremos fazer a inserção do horário do remédio
        do cliente.
        """
        retorno:bool = False;

        if(not isinstance(tupla,tuple)):
            return retorno;
        elif(len(tupla) != 3):
            return retorno;
        
        id_user     :str = str(tupla[0]);
        hora        :str = str(tupla[1]);
        nome_remedio:str = str(tupla[2]);

        if(id_user == ''):
            return retorno;
        if(hora == ''):
            return retorno;

        id_hora:str = self._pega_id_hora_do_remedio(hora=hora);

        if(int(id_hora) <= 0):
            return retorno;

        tupla_insert  :tuple = (id_user,id_hora,nome_remedio,);
        comando_insert:str   = (
            "INSERT INTO solicitacao_hora_do_remedio"
            "(id_user, id_hora, nome_remedio)"
            "VALUES(%s,%s,%s)"
        );
        
        tupla_verifica  :tuple  = (id_user,id_hora,);
        retorno_verifica:bool   = self._verifica_user_hora_do_remedio(
                                    tupla=tupla_verifica);

        if(retorno_verifica):
            return retorno;
        retorno = True;
        self._insert(
            comando=comando_insert,
            tupla=tupla_insert
        );
        return retorno;
    
    def _verifica_user_hora_do_remedio(self,tupla:tuple=[]) -> bool:
        """Verifica user Horário do Remédio

        :param  - tupla:tuple(id_user,id_hora)
        :return - bool 
        
        Aqui nós iremos verificar se o cliente já não tem a 
        solicitação nesse mesmo horário.
        """
        if(not isinstance(tupla,tuple)):
            return True;
        elif(len(tupla) != 2):
            return True;
        
        id_user:str = str(tupla[0]);
        id_hora:str = str(tupla[1]);
        
        if((not isinstance(id_user,str)) or (id_user == '')):
            return True;
        if((not isinstance(id_hora,str)) or (id_hora == '')):
            return True;

        comando_select:str = (
            f" SELECT * "
            f" FROM solicitacao_hora_do_remedio "
            f" WHERE id_user = '{id_user}' "
            f" AND id_hora = '{id_hora}'"
        );

        retorno_select:list = self._select(comando=comando_select);

        if(retorno_select == []):
            return False;
        return True;
    
    def _pega_id_hora_do_remedio(self,hora:str,cria:bool=True
                                ) -> Union[str,int]:
        """Pega ID da Hora do Remédio

        :param  - hora:str  hora do remédio do cliente
        :param  - cria:bool Verifica se precisa criar o horário 
        :return - ID:( str | int ) 
        
        Aqui nós iremos pegar o id da hora do remédio, mas 
        se não existir então vamos criar o id.
        """
        if((not isinstance(hora,str)) or (hora == '')):
            return -1;
        
        comando_select:str = (
            f" SELECT id "
            f" FROM hora_do_remedio "
            f" WHERE hora = '{hora}' "
        );

        retorno_select:list = self._select(comando=comando_select);
        
        if(retorno_select == []):
            if(not cria):
                return -1;
            comando_insert:str = (
                " INSERT INTO hora_do_remedio "
                " (hora, atualizacao) "
                " VALUES(%s,%s) "
            );
            data        :str   = '0000:00:00';
            tupla_insert:tuple = (hora,data,);
            
            self._insert(
                comando=comando_insert,
                tupla=tupla_insert
            );
            return self._pega_id_hora_do_remedio(hora=hora);
        return retorno_select[0][0];
    
    def verifica_hora_do_remedio(self) -> list:
        """Verifica Hora do Remédio

        :param  - hora:str hora atual
        :return - [ID,nome_remedio]*n:list
        
        Aqui nós iremos verificar se tem algum remédio no banco
        que precisa ser atualizado.
        """
        retorno:list = []; 

        hora:str = datetime.today().strftime('%H:%M');
        dia :str = datetime.today().strftime('%Y:%m:%d');

        comando_select:str = (
            f" SELECT id "
            f" FROM hora_do_remedio "
            f" WHERE atualizacao < '{dia}' "
            f" AND hora = '{hora}' "
        );

        retorno_select:list = self._select(comando=comando_select);

        if(retorno_select != []):
            id_hora       :str = retorno_select[0][0];
            comando_update:str = (
                f" UPDATE hora_do_remedio "
                f" SET atualizacao='{dia}' "
                f" WHERE id ='{id_hora}' "
            );

            self._update(comando=comando_update);
            
            comando_select = (
                f" SELECT id_user, nome_remedio "
                f" FROM solicitacao_hora_do_remedio "
                f" WHERE id_hora = '{id_hora}' "
            );
            retorno = self._select(comando=comando_select);
        return retorno;
    
    def delete_hora_do_remedio(self,tupla:tuple=[]) -> bool:
        """Delete Hora do Remédio

        :param  - tupla:tuple = (id_user,hora)
        :return - bool 
        
        Aqui nós iremos deletar um horário do remédio do user que 
        solicitar.
        """
        retorno:bool = False;

        if(not isinstance(tupla,tuple)):
            return retorno;
        elif(len(tupla) != 2):
            return retorno;

        id_user:str = str(tupla[0]);
        hora   :str = str(tupla[1]);

        if(id_user == ''):
            return retorno;
        if(id_hora == ''):
            return retorno;

        id_hora:str = self._pega_id_hora_do_remedio(
            hora=hora,
            cria=False
        );

        if(int(id_hora) <= 0):
            return retorno;

        tupla_verifica  :tuple  = (id_user,id_hora,);
        retorno_verifica:bool   = self._verifica_user_hora_do_remedio(
                                    tupla=tupla_verifica);

        if(retorno_verifica):
            comando_delete:str = (
                f" DELETE FROM "
                f" solicitacao_hora_do_remedio "
                f" WHERE id_hora = '{id_hora}' "
            );
            self._delete(comando=comando_delete);
            retorno = True;
        return retorno;
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