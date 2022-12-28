


import pandas as pd


df1_data = pd.read_csv('gasolina_2000+.csv', index_col=0)
df2_data = pd.read_csv('gasolina_2010+.csv', index_col=0)

df_data = pd.concat([df1_data,df2_data])

df_data.head()
df_data.tail()
df_data.info
df_data.dtypes
df_data.shape

type(df_data["DATA INICIAL"].iloc[2])

df_data["DATA INICIAL"] = pd.to_datetime(df_data["DATA INICIAL"])
df_data["DATA FINAL"] = pd.to_datetime(df_data["DATA FINAL"])
df_data.dtypes

df_data["ANO-MES"] = df_data["DATA FINAL"].apply(lambda x: "{}".format(x.year)) + df_data["DATA FINAL"].apply(lambda x: "-{:02d}".format(x.month))

df_data["PRODUTO"].value_counts()

df_gasolina_comum = df_data[df_data["PRODUTO"] == "GASOLINA COMUM"]

df_data[df_data["ANO-MES"] == '2008-08']["PREÇO MÉDIO REVENDA"].mean()
df_gasolina_comum[df_gasolina_comum["ANO-MES"] == '2008-08']["PREÇO MÉDIO REVENDA"].mean()

df_data[(df_data["ANO-MES"] == '2014-05') & (df_data["ESTADO"] == 'SAO PAULO')]["PREÇO MÉDIO REVENDA"].mean()
df_gasolina_comum[(df_gasolina_comum["ANO-MES"] == '2014-05') & (df_gasolina_comum["ESTADO"] == 'SAO PAULO')]["PREÇO MÉDIO REVENDA"].mean()


df_data[df_data["PREÇO MÉDIO REVENDA"] > 5][["ESTADO", "ANO-MES", "PREÇO MÉDIO REVENDA"]].head(5)
df_gasolina_comum[df_gasolina_comum["PREÇO MÉDIO REVENDA"] > 5][["ESTADO", "ANO-MES", "PREÇO MÉDIO REVENDA"]].head(5)

df_media_sul = df_gasolina_comum[(df_gasolina_comum["DATA FINAL"].apply(lambda x: x.year) == 2012)]
df_media_sul[df_media_sul["REGIÃO"] == "SUL"]["PREÇO MÉDIO REVENDA"].mean()



