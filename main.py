from service.cotacao_service import CotacaoService
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

    print(f"Valor: R$ {valor:.4f}")
    print(f"Info: {resultado['mensagem']}")

    repository = Conectar_bd()
    repository.salvar_bd(data, valor , created_at)



if __name__ == "__main__":
    iniciar_programa()