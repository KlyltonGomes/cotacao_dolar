from service.cotacao_service import CotacaoCsvWriter, CotacaoService
from repository.cotacao_repository import Conectar_bd


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

    # salva no banco
    repository = Conectar_bd()
    salvou = repository.salvar_bd(data, valor, origem, created_at)

    # só salva no CSV se salvou no banco
    if not salvou:
        print("Registro já existe, não será salvo no CSV.")
        return

    csv_writer = CotacaoCsvWriter()
    csv_writer.salvar(data, valor, origem, created_at)


if __name__ == "__main__":
    iniciar_programa()