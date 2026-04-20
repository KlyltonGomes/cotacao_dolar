import json
import os

class Caminho_arquivo:
    def __init__(self, diretorio, arquivo):
        self.diretorio = diretorio
        self.arquivo = arquivo
        # Criamos o caminho já no __init__ para ele estar disponível para a classe toda
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.caminho_completo = os.path.join(self.base_dir, self.diretorio, self.arquivo)

    def carregar_arq(self):
        with open(self.caminho_completo, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __str__(self):
        # Agora o print(d) vai mostrar o caminho do arquivo
        return self.caminho_completo

