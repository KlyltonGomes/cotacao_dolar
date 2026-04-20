from datetime import datetime
import sys
import os
import json
from requests import get
from util.tratamento_dado import Tratamento
from util.tratamento_data import Data_api
from util.leitor_arquivo import Caminho_arquivo


class CotacaoService:
    def __init__(self):
        # Agora você instancia a classe Tratamento diretamente
        self.tratamento = Tratamento()

    def obter_valor_dolar(self):
        try:
            # 1. Obtém a URL pronta
            url_final = self.tratamento.processar()
            
            # 2. Faz a chamada à API
            response = get(url_final)
            
            if response.status_code == 200:
                dados = response.json()
                
                # 3. Extrai os dados (com o índice [0] que você adicionou, está correto!)
                if dados.get("value"):
                    cotacao = dados["value"][0]
                    valor_venda = cotacao["cotacaoVenda"]
                    data_hora = cotacao["dataHoraCotacao"]
                    
                    data_formatada = datetime.fromisoformat(data_hora).strftime("%Y-%m-%d")
                    data_created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    return {
                            "sucesso": True,
                            "valor": valor_venda,
                            "data": data_formatada,
                            "created_at":data_created_at,
                            "mensagem": f"Cotação obtida em: {data_formatada}"
                        }
                else:
                    return {
                        "sucesso": False, 
                        "mensagem": "Cotação não disponível (Fim de semana/Feriado)."
                    }
            else:
                return {"sucesso": False, "mensagem": f"Erro na API: {response.status_code}"}

        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro interno no Service: {e}"}
        



# execução única
if __name__ == "__main__":
    CotacaoService()