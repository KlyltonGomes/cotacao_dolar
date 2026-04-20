import json
from requests import get
from util.leitor_arquivo import Caminho_arquivo 
from util.tratamento_data import Data_api

class Tratamento:
    def __init__(self):
        self.url_final = ""

    def processar(self):

        leitor =  Caminho_arquivo('config','url.json')
        dados_json = leitor.carregar_arq()

        url_api = dados_json['api']['url_base']
        data_api = Data_api().data_consulta()

        #teste manual
        data_api_ = '04-15-2026'

        self.url_final = f"{url_api}/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data_api_}'&$format=json"
        return self.url_final
    
    def __str__(self):
        return self.url_final
    


if __name__ == "__main__":
    t = Tratamento()
    t.processar()
    print(f"Teste de URL: {t}")

#https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='04-15-2026'&$format=json