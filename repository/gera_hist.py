import pandas as pd

# ler arquivo original
df = pd.read_csv("../BD_HIST_COTACAO.csv", sep=";")

# guardar controle de origem
df["ORIGEM"] = "API"

# tratamento
df["DATA_COTACAO"] = pd.to_datetime(df["DATA_COTACAO"], dayfirst=True)
df["COTACAO_VALOR"] = df["COTACAO_VALOR"].str.replace(",", ".").astype(float)

# ordenar e indexar
df = df.sort_values("DATA_COTACAO").set_index("DATA_COTACAO")

# criar calendário contínuo (preencher datas faltantes)
df_full = df.asfreq("D")

# preencher valores e sigla
df_full["COTACAO_VALOR"] = df_full["COTACAO_VALOR"].ffill()
df_full["SIGLA"] = df_full["SIGLA"].ffill()

# origem: API ou FALLBACK
df_full["ORIGEM"] = df_full["ORIGEM"].fillna("FALLBACK")

# reset index
df_full = df_full.reset_index()

# formatar data
df_full["DATA_COTACAO"] = df_full["DATA_COTACAO"].dt.strftime("%Y-%m-%d")

# created_at
df_full["CREATED_AT"] = df_full["DATA_COTACAO"]

# salvar CSV final
df_full.to_csv("dataset_cotacao_tratado.csv", index=False)

print("✅ CSV gerado: dataset_cotacao_tratado.csv")