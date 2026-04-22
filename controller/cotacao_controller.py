from fastapi import APIRouter
from repository.cotacao_repository import Conectar_bd
from service.cotacao_service import CotacaoService

router = APIRouter()

@router.get("/cotacao/hoje")
def cotacao_hoje():
    service = CotacaoService()
    resultado = service.obter_valor_dolar()

    if not resultado["sucesso"]:
        return {"erro": resultado["mensagem"]}

    return {
        "data": resultado["data"],
        "valor_dolar": resultado["valor"]
        #,"origem": resultado["origem"]

    }

@router.get("/cotacao/{data}")
def cotacao_por_data(data: str):
    repository = Conectar_bd()

    resultado = repository.buscar_por_data(data)

    if not resultado:
        return {"erro": "Data não encontrada"}

    # ajuste dependendo do retorno (tuple ou dict)
    row = resultado[0]

    return {
        "data": resultado[0],
        "valor_dolar": resultado[1],
        #"origem": resultado[2]
    }