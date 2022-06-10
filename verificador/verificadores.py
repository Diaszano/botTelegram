#-----------------------
# BIBLIOTECAS
#-----------------------
#-----------------------
# CONSTANTES
#-----------------------
#-----------------------
# CLASSES
#-----------------------
class Verificadores:
    """Verificadores
        
        Classe Verificadores.
    """
    @staticmethod
    def CNPJ(cnpj:str = '00.000.000/0000-00') -> bool:
        """Verificador CNPJ
        
        Aqui verificamos se o cnpj é válido.
        """
        cnpjo = [int(char) for char in cnpj if char.isdigit()];
        cnpj  = cnpjo[:12];
        prod  = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
        
        while len(cnpj) < 14:
            valor = sum([x*y for (x, y) in zip(cnpj, prod)])%11;
            if valor > 1:
                resto = 11 - valor;
            else:
                resto = 0;
            cnpj.append(resto);
            prod.insert(0, 6);
        if cnpj == cnpjo:
            return True;
        return False;
    
    @staticmethod
    def CPF(cpf:str = '000.000.000-00') -> bool:
        """Verificador CPF
        
        Aqui verificamos se o cpf é válido.
        """
        cpf_novo = [int(char) for char in cpf if char.isdigit()];
        if len(cpf_novo) != 11 or cpf_novo == cpf_novo[::-1]:
            return False;
        for i in range(9, 11):
            valor  = sum((cpf_novo[num] * 
                        ((i + 1) - num) for num in range(0, i)));
            digito = ((valor * 10) % 11) % 10;
            if digito != cpf_novo[i]:
                return False;
        return True;
#-----------------------
# FUNÇÕES()
#-----------------------
#-----------------------
# Main()
#-----------------------
if(__name__ == "__main__"):
    pass; 
#-----------------------