from datetime import datetime
from requests import get
from repository.cotacao_repository import Conectar_bd
from util.tratamento_dado import Tratamento


class CotacaoService:
    def __init__(self):
        self.tratamento = Tratamento()

    def obter_valor_dolar(self):
        try:
            url_final = self.tratamento.processar()
            response = get(url_final)

            hoje = datetime.now().strftime("%Y-%m-%d")
            agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # =========================
            # ✔ 1. API (dia útil)
            # =========================
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

            # =========================
            # ❌ 2. FALLBACK (fim de semana/feriado)
            # =========================
            repository = Conectar_bd()
            ultimo = repository.buscar_ultimo_registro()

            if ultimo:
                row = ultimo[0]

                valor = row[1] if not isinstance(row, dict) else row["VALOR_COTACAO"]

                return {
                    "sucesso": True,
                    "valor": valor,
                    "data": hoje,  # 👈 REGISTRA HOJE
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