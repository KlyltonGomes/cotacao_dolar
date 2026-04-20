from repository.conector_sql import SQLiteConnector
import os

class Conectar_bd:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))        
        self.db_path = os.path.join(base_dir, "repository", "data_base", "bd_cotacao.db")
        self.db = SQLiteConnector(self.db_path)

    def salvar_bd(self, data, valor, created_at):
        try:
            self.db.conectar()

            self.db.executar("""
            CREATE TABLE IF NOT EXISTS DATASET_COTACAO (
                DATA_COTACAO TEXT PRIMARY KEY,
                VALOR_COTACAO REAL,
                SIGLA_COTACAO TEXT,
                CREATED_AT TEXT
            )
            """)

            existe = self.db.consultar(
                "SELECT 1 FROM DATASET_COTACAO WHERE DATA_COTACAO = ?",
                (data,)
            )

            if not existe:
                self.db.executar(
                    "INSERT INTO DATASET_COTACAO VALUES (?, ?, ?, ?)",
                    (data, valor, "USD", created_at)
                )
                print("✔ Cotação salva no banco")
            else:
                print("⚠ Cotação já existe no banco")

        finally:
            self.db.fechar()

        




