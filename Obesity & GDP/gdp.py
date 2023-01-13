import pandas as pd
import numpy as np

df_gdp = pd.read_csv("gdp.csv", decimal =".")
df_gdp

df_gdp.info()
df_gdp.sum().isnull()
df_gdp.head(5)
df_gdp.tail(5)
df_gdp.columns

df_gdp["Year"] = df_gdp["Year"].apply(lambda x: int(x.split("/")[-1]))
df_gdp[" GDP_pp "].iloc[0]

float(df_gdp[" GDP_pp "].iloc[0].split()[0])
df_gdp["gdp_pp"] = df_gdp[" GDP_pp "].apply(lambda x: float(x.split()[0].replace(",","")))
df_gdp["gdp_pp"]

del df_gdp[" GDP_pp "]
df_gdp

df_gdp.groupby("Country")["Year"].min()
df_gdp.groupby("Country")["Year"].max()

df_gdp.groupby("Country")["Year"].min().value_counts()
df_gdp.groupby("Country")["Year"].min()[df_gdp.groupby("Country")["Year"].min() == 1991]


df_gdp[df_gdp["Year"]< 2000].max()
df_gdp_start = df_gdp[df_gdp["Year"] == 1901]
df_gdp_end = df_gdp[df_gdp["Year"] == 1996]

((df_gdp_end.groupby("Region")["gdp_pp"].mean() / df_gdp_start.groupby("Region")["gdp_pp"].mean() - 1) * 100).sort_values()

arr_year = np.arange(df_gdp["Year"].min(), df_gdp["Year"].max())
df_all_years = pd.DataFrame(arr_year, columns=["Year"])
df_all_years.index = df_all_years["Year"]

df_years_off = ~df_all_years["Year"].isin(df_gdp["Year"])
df_years_off

df_years_off = df_all_years.loc[df_years_off].index
df_years_off

df_gdp = df_gdp.sort_values(["Country","Year"])
df_gdp

df_gdp["variation_gdp"] = df_gdp["gdp_pp"] - df_gdp["gdp_pp"].shift(1)
df_gdp["variation_year"] = df_gdp["Year"] - df_gdp["Year"].shift(1)
df_gdp["gdp_year"] = (df_gdp["variation_gdp"] / df_gdp["variation_year"]).shift(-1)
df_gdp

df_gdp["next_year"] = df_gdp["Year"].shift(-1)
del df_gdp["variation_gdp"], df_gdp["variation_year"]
df_gdp

df_new_data = pd.DataFrame()

for idx, row in df_gdp.iterrows():
    if row["Year"] == 2011:
        continue

    years_to_add = df_years_off[(df_years_off < row["next_year"]) & (df_years_off > row["Year"])]
    for new_year in years_to_add:
        add_row = row.copy()
        add_row["gdp_pp"] = (new_year - add_row["Year"]) * add_row["gdp_year"] + add_row["gdp_pp"]
        add_row["Year"] = new_year
        add_row["Kind"] = "estimated"
        df_new_data = pd.concat([df_new_data, add_row.to_frame().transpose()])

df_new_data

df_gdp = pd.concat([df_gdp, df_new_data])
df_gdp

df_gdp.sort_values(["Country", "Year"], inplace=True)
df_gdp

df_gdp.index = df_gdp["Year"]
df_gdp

df_gdp["Kind"].fillna("real", inplace=True)
df_gdp

import matplotlib.pyplot as plt

fix , ax = plt.subplots(figsize=(20,5))
country = "Brazil"
df_gdp[(df_gdp["Kind"] == "real") & (df_gdp["Country"] == country)].plot(kind="scatter", y="gdp_pp", x="Year",ax=ax)
df_gdp[(df_gdp["Kind"] == "estimated") & (df_gdp["Country"] == country)].plot(kind="scatter", y="gdp_pp", x="Year",ax=ax,color="orange")
