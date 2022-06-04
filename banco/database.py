"""Classe abstrata da Conexão com o banco"""
#-----------------------
# BIBLIOTECAS
#-----------------------
from typing import Union
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
        pass;
    # -----------------------
    # CRUD
    # -----------------------
    # Create
    @abstractmethod
    def _insert(self,comando:str,tupla:tuple) -> None:
        pass;
    # Read
    @abstractmethod
    def _select(self,comando:str) -> list:
        pass;
    # Update
    @abstractmethod
    def _update(self,comando:str) -> None:
        pass;
    # Delete
    @abstractmethod
    def _delete(self,comando:str) -> None:
        pass;
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
        if(self._verifica_cpf(id_user=id_user,cpf=cpf)):
            return;
        self._insert(comando=comando,tupla=tupla);

    def _verifica_cpf(self,id_user:str='',cpf:str='') -> bool:
        if((id_user == '') or (not isinstance(id_user,str))):
            return False;
        if((cpf == '') or (not isinstance(cpf,str))):
            return False;
        comando = ( f"SELECT * FROM cpf "
                    f"WHERE id_user='{id_user}' "
                    f"AND CPF='{cpf}' ");
        if(self._select(comando=comando) == []):
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
        if(self._verifica_cnpj(id_user=id_user,cnpj=cnpj)):
            return;
        self._insert(comando=comando,tupla=tupla);
    
    def _verifica_cnpj(self,id_user:str='',cnpj:str='') -> bool:
        if((id_user == '') or (not isinstance(id_user,str))):
            return False;
        if((cnpj == '') or (not isinstance(cnpj,str))):
            return False;
        comando = ( f" SELECT * FROM cnpj "
                    f" WHERE id_user='{id_user}' "
                    f" AND CNPJ='{cnpj}' ");
        if(self._select(comando=comando) == []):
            return False;
        return True;
    # -----------------------    
    # RASTREIO
    # -----------------------
    def insert_rastreio(self,tupla:tuple=[]) -> None:
        """Inserir rastreio
        
        tupla = ('id_user','codigo','nome_rastreio', 'informacoes')"""
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
        if(self._verifica_rastreio(id_user=id_user,codigo=codigo)):
            return;
        self._insert(comando=comando,tupla=tupla);
    
    def _verifica_rastreio(self,id_user:str='',codigo:str='') -> bool:
        if((id_user == '') or (not isinstance(id_user,str))):
            return False;
        if((codigo == '') or (not isinstance(codigo,str))):
            return False;
        comando = ( f" SELECT * "
                    f" FROM encomenda "
                    f" WHERE id_user='{id_user}' "
                    f" AND codigo='{codigo}'");
        if(self._select(comando=comando) == []):
            return False;
        return True;
    
    def select_rastreio(self,id_user:str='') -> list:
        if((id_user == '') or (not isinstance(id_user,str))):
            return [];
        comando = ( f" SELECT informacoes, nome_rastreio, "
                    f" codigo FROM encomenda  "
                    f" WHERE id_user='{id_user}' "
                    f" ORDER BY id DESC ");
        return self._select(comando=comando);

    def delete_rastreio(self,id_user:str='',codigo:str='') -> bool:
        if((id_user == '') or (not isinstance(id_user,str))):
            return False;
        if((codigo == '') or (not isinstance(codigo,str))):
            return False;
        comando = ( f" DELETE FROM encomenda "
                    f" WHERE id_user='{id_user}' "
                    f" AND codigo='{codigo}' ");
        if(self._verifica_rastreio(id_user=id_user,codigo=codigo)):
            self._delete(comando=comando);
            return True;
        return False;
    
    def atualiza_rastreio(self) -> list:
        comando = ( f" SELECT id_user, codigo, "
                    f" informacoes, nome_rastreio "
                    f" FROM encomenda ORDER BY dia "
                    f" LIMIT 1");
        dados = self._select(comando=comando);
        if(dados != []):
            id_user = str(dados[0][0]);
            codigo  = str(dados[0][1]);
            info    = str(dados[0][2]);
            nome    = str(dados[0][3]);
            return [id_user,codigo,info,nome];
        return [];
    
    def validar_rastreio(self) -> Union[int,float]:
        comando = ( f" SELECT TIMESTAMPDIFF(SECOND, dia,now()) "
                    f" from encomenda "
                    f" ORDER BY dia LIMIT 1 ");
        dados = self._select(comando=comando);
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
        self._update(comando=comando);
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
        self._insert(comando=comando,tupla=tupla);
#-----------------------
# FUNÇÕES
#-----------------------
#-----------------------
# MAIN()
#-----------------------
if(__name__ == "__main__"):
    pass;
#-----------------------