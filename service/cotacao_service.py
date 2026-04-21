from datetime import datetime
import os
import csv
from requests import get
from repository.cotacao_repository import Conectar_bd
from util.tratamento_dado import Tratamento
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
caminho_csv = BASE_DIR / "repository" / "data_base" / "cotacao.csv"


class CotacaoService:
    def __init__(self):
        self.tratamento = Tratamento()

    def obter_valor_dolar(self):
        try:
            url_final = self.tratamento.processar()
            response = get(url_final)

            hoje = datetime.now().strftime("%Y-%m-%d")
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # API
            if response.status_code == 200:
                dados = response.json()

                if dados.get("value"):
                    cotacao = dados["value"][0]
                    data_hora = cotacao["dataHoraCotacao"]

                    return {
                        "sucesso": True,
                        "valor": cotacao["cotacaoVenda"],
                        "data": datetime.fromisoformat(data_hora).strftime("%Y-%m-%d"),
                        "origem": "API",
                        "created_at": agora,
                        "mensagem": "Obtido via API"
                    }

            # FALLBACK
            repository = Conectar_bd()
            ultimo = repository.buscar_ultimo_registro()

            if ultimo:
                row = ultimo[0]
                valor = row[1] if not isinstance(row, dict) else row["VALOR_COTACAO"]

                return {
                    "sucesso": True,
                    "valor": valor,
                    "data": hoje,
                    "origem": "FALLBACK",
                    "created_at": agora,
                    "mensagem": "Fallback com último valor válido"
                }

            return {
                "sucesso": False,
                "mensagem": "Sem dados na API e no banco"
            }

        except Exception as e:
            return {
                "sucesso": False,
                "mensagem": f"Erro interno no Service: {e}"
            }


class CotacaoCsvWriter:

    def salvar(self, data, valor, origem, created_at):
        arquivo_existe = os.path.exists(caminho_csv)

        with open(caminho_csv, "a", newline="") as file:
            writer = csv.writer(file)

            if not arquivo_existe:
                writer.writerow([
                    "DATA_COTACAO",
                    "VALOR_COTACAO",
                    "ORIGEM",
                    "SIGLA_COTACAO",
                    "CREATED_AT"
                ])

            writer.writerow([data, valor, origem, "USD", created_at])

        print("✔ Registro salvo no CSV")

        return True