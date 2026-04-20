from datetime import date

class Data_api:
    def __init__(self):
        self.data_formatada = ""

    def data_consulta(self):
        # Pegar a data atual
        hoje = date.today()

        # Formatar para o padrão que a API do Banco Central exige (MM-DD-AAAA)
        self.data_formatada = hoje.strftime('%m-%d-%Y')

        return self.data_formatada 
    
    def __str__(self):
        return self.data_formatada 

