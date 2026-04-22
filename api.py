from fastapi import FastAPI
from controller.cotacao_controller import router as cotacao_router

app = FastAPI()

app.include_router(cotacao_router)


#matar aplicacao: pkill -f uvicorn
#matar manual: lsof -i :8001
#pelo PID: kill -9 9843
#subir aplicação: uvicorn api:app --reload --port 8001