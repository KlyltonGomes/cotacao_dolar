from service.cotacao_service import CotacaoCsvWriter, CotacaoService
from repository.cotacao_repository import Conectar_bd
from util.enviar_bucket import enviar_para_bucket
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
    repository = Conectar_bd()
    salvou = repository.salvar_bd(data, valor, origem, created_at)

    if not salvou:
        print("Registro já existe, não será salvo no CSV.")
        return

    # CSV
    csv_writer = CotacaoCsvWriter()
    csv_writer.salvar(data, valor, origem, created_at)

    # Bucket
    enviar_para_bucket(
        caminho_csv,
        "meu-bucket",
        "cotacao/cotacao.csv"
    )


if __name__ == "__main__":
    iniciar_programa()