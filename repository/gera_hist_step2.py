from pathlib import Path
import pandas as pd


df = pd.read_csv("repository/dataset_cotacao_tratado.csv")

values = []

for _, row in df.iterrows():
    linha = f"('{row['DATA_COTACAO']}', {row['COTACAO_VALOR']}, '{row['ORIGEM']}', '{row['SIGLA']}', '{row['CREATED_AT']}')"
    values.append(linha)

sql = """
INSERT INTO DATASET_COTACAO (
    DATA_COTACAO,
    VALOR_COTACAO,
    ORIGEM,
    SIGLA_COTACAO,
    CREATED_AT
)
VALUES
""" + ",\n".join(values) + ";"

with open("insert_cotacao.sql", "w") as f:
    f.write(sql)

print("SQL gerado com sucesso: insert_cotacao.sql")