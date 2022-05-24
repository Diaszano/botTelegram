#-----------------------
# BIBLIOTECAS
#-----------------------
import re
import requests
from database import DataBase
#-----------------------
# CLASSES
#-----------------------
class Rastreio:
    def __init__(self)->None:
        pass;
    def rastrear(self,codigo:str='')->str:
        if(len(codigo) != 13):
            return '';
        codigo = re.findall(r'(?P<Codigo>[a-z]{2}[0-9]{9}[a-z]{2})',codigo,re.MULTILINE | re.IGNORECASE);
        if(codigo != []):
            codigo = codigo[0];
            url         = f'https://proxyapp.correios.com.br/v1/sro-rastro/{codigo}';
            informacoes = requests.get(url);
            informacoes = str(informacoes.text);
            informacoes = re.findall(r'(?P<Eventos>\"eventos\"\:)(?P<Dados_Eventos>\[.*?\])', informacoes, re.MULTILINE | re.IGNORECASE);
            if informacoes != []:
                informacoes = str(informacoes);
                informacoes = re.findall(r'(?P<Eventos>\{\"codigo\"\:.*?\.png\"\})*', informacoes, re.MULTILINE | re.IGNORECASE);
                informacoes = [valor for valor in informacoes if valor != ''];
                informacoes = self.limparMensagem(eventos=informacoes);
                return informacoes;
        return '';
    
    def limparMensagem(self,eventos:list = []) -> list:
        rastreio          = [];
        re_data           = re.compile(r'((\"dtHrCriado\"\:)(\".*?\"))', re.MULTILINE | re.IGNORECASE);
        re_tipo           = re.compile(r'((\"tipo\"\:)(\"[^0-9]*?\"))', re.MULTILINE | re.IGNORECASE);
        re_detalhe        = re.compile(r'((\"detalhe\"\:)(\".*?\"))', re.MULTILINE | re.IGNORECASE);
        re_descricao      = re.compile(r'((\"descricao\"\:)(\".*?\"))', re.MULTILINE | re.IGNORECASE);
        re_unidade_1      = re.compile(r'(?:\"unidade\"\:\{\"endereco\"\:\{"cidade"\:)(\".*?\"),(?:\"uf\"\:)(\".*?\")', re.MULTILINE | re.IGNORECASE);
        re_unidade_2      = re.compile(r'(?:\"unidade\"\:\{\"codSro\"\:\".*?\"(?:\,)\"endereco\"\:\{\}\,\"nome"\:)(\".*?\")', re.MULTILINE | re.IGNORECASE);
        re_unidadeDestino = re.compile(r'(?:\"unidadeDestino\"\:\{\"endereco\"\:\{\"cidade\":)(\".*?\")(?:,\"uf\"\:)(\".*?\")', re.MULTILINE | re.IGNORECASE);
        
        for resultado in eventos:
            dia       = '';
            tipo      = '';
            local     = '';
            destino   = '';
            detalhe   = '';
            descricao = '';
            if 'descricao' in resultado:
                temp      = re_descricao.findall(resultado);
                temp      = str(temp[0][2]);
                temp      = temp.replace('"','');
                descricao = temp;
            if 'detalhe' in resultado:
                temp    = re_detalhe.findall(resultado);
                temp    = temp[0][2];
                temp    = temp.replace('"','');
                detalhe = f'\n{temp}';
            if 'dtHrCriado' in resultado:
                temp = re_data.findall(resultado);
                temp = temp[0][2]
                temp = temp.replace('"','');
                dia  = temp;
            if 'tipo' in resultado:
                tipo = re_tipo.findall(resultado);
                if tipo != []:
                    temp = re_unidade_1.findall(resultado);
                    if temp != []:
                        temp        = temp[0];
                        [cidade,uf] = [temp[0],temp[1]];
                        uf          = uf.replace('"','');
                        cidade      = cidade.replace('"','');
                        local       = f'[{cidade}/{uf}]';
                    else:
                        temp  = re_unidade_2.findall(resultado);
                        if temp != []:
                            temp  = temp[0].replace('"','');
                            local = f'[{temp}]';
            if 'unidadeDestino' in resultado:
                temp  = re_unidadeDestino.findall(resultado);
                if temp != []:
                    temp        = temp[0];
                    [cidade,uf] = [temp[0],temp[1]];
                    uf          = uf.replace('"','');
                    cidade      = cidade.replace('"','');
                    destino     = f' para [{cidade}/{uf}]';
            rastreio.append(f'[{self.limpaData(dia)}] - {descricao} {local}{destino}{detalhe}\n\n\n');
        rastreio_str = '';
        tamanho_rastreio = len(rastreio)-1;
        for i in range(tamanho_rastreio+1):
            rastreio_str += rastreio[tamanho_rastreio - i];
        return rastreio_str;

    def limpaData(self,data:str='')->str:
        ano      = data[:4];
        mes      = data[5:7];
        dia      = data[8:10];
        hora     = data[11:];
        mensagem = f"{dia}/{mes}/{ano} - {hora}";
        return mensagem;
#-----------------------
# Main()
#-----------------------    
if __name__ == '__main__':
    correios = Rastreio()
    resposta = correios.rastrear('');
    tupla = ('05','','Celular',resposta)
    #       ('id_user','codigo','nome_rastreio','data','informacoes');
    print(resposta);
    db = DataBase();
    db.creat_table();
    db.insert(comando_tuple=tupla);
    # db.upadate(id_user='05',codigo='',mensagem=resposta)
#-----------------------    