from service.cotacao_service import CotacaoCsvWriter, CotacaoService
from repository.cotacao_repository import Conectar_bd
#from util.enviar_bucket import enviar_para_bucket
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
caminho_csv = BASE_DIR / "repository" / "data_base" / "cotacao.csv"


def iniciar_programa():
    print("--- CONSULTA PTAX DOLAR ---")

    service = CotacaoService()
    resultado = service.obter_valor_dolar()

    if not resultado["sucesso"]:
        print(f"Atenção: {resultado['mensagem']}")
        return

    valor = resultado["valor"]
    data = resultado["data"]
    created_at = resultado["created_at"]
    origem = resultado["origem"]

    print(f"Valor: R$ {valor:.4f}")
    print(f"Info: {resultado['mensagem']}")

    # banco
    cotacao_repository = Conectar_bd()
    salvou = cotacao_repository.salvar_bd(data, valor, origem, created_at)

    if salvou:
        print("Cotação salva no banco")
    else:
        print("Registro já existe no banco (ok).")

    # CSV
    csv_writer = CotacaoCsvWriter()

    if not csv_writer.data_existe(data):
        csv_writer.salvar(data, valor, origem, created_at)
    else:
        print("Data já existe no CSV.")

    # Bucket
    """ enviar_para_bucket(
        caminho_csv,
        "meu-bucket",
        "cotacao/cotacao.csv"
    ) """


if __name__ == "__main__":
    iniciar_programa()