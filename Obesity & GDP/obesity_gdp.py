'''
Obesity Code Starts here
'''
import pandas as pd
import numpy as np

df_obesity = pd.read_csv("obesity_cleaned.csv")

df_obesity.info()
df_obesity.head(5)
df_obesity.tail(5)
df_obesity.dtypes

del df_obesity["Unnamed: 0"]
df_obesity["Obesity"] = df_obesity["Obesity (%)"].apply(lambda x: x.split()[0])

df_obesity["Obesity"]
df_obesity["Obesity"].value_counts()

df_obesity.loc[df_obesity["Obesity"] == "No", "Obesity"] = np.nan
df_obesity["Obesity"] = df_obesity["Obesity"].dropna()
df_obesity
df_obesity["Obesity"].value_counts()

df_obesity["Obesity"] = df_obesity["Obesity"].apply(lambda x: float(x))
df_obesity.info()

## Making the year as inex to better visualize
df_obesity.set_index("Year", inplace=True)
df_obesity

df_obesity[df_obesity.index == 2015].groupby("Sex").mean()

df_obesity_start = df_obesity[df_obesity.index == 1975]
df_obesity_end = df_obesity[df_obesity.index == 2016]

df_obesity_start.set_index("Country", inplace=True)
df_obesity_end.set_index("Country", inplace=True)

df_obesity_growth = df_obesity_end[df_obesity_end["Sex"] == "Both sexes"]["Obesity"] - df_obesity_start[df_obesity_start["Sex"] == "Both sexes"]["Obesity"]
df_obesity_growth
df_obesity_growth.sort_values()
df_obesity_growth.dropna()

df_obesity_growth.head(5)
df_obesity_growth.tail(5) 

df_2015 = df_obesity[df_obesity.index == 2015]
df_2015[df_2015["Obesity"] == df_2015["Obesity"].max()]

df_brazil = df_obesity[df_obesity["Country"] == "Brazil"]
df_brazil

import matplotlib.pyplot as plt

df_brazil[df_brazil["Sex"] == "Female"]["Obesity"] - df_brazil[df_brazil["Sex"] == "Male"]["Obesity"]
(df_brazil[df_brazil["Sex"] == "Female"]["Obesity"] - df_brazil[df_brazil["Sex"] == "Male"]["Obesity"]).plot()

df_both_sex = df_obesity[df_obesity["Sex"] == "Both sexes"]
df_both_sex

df_both_sex.groupby("Year")["Obesity"].mean()
(df_both_sex.groupby("Year")["Obesity"].mean()).plot()


'''
GDP Code Starts here
'''

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

fix , ax = plt.subplots(figsize=(20,5))
country = "Brazil"
df_gdp[(df_gdp["Kind"] == "real") & (df_gdp["Country"] == country)].plot(kind="scatter", y="gdp_pp", x="Year",ax=ax)
df_gdp[(df_gdp["Kind"] == "estimated") & (df_gdp["Country"] == country)].plot(kind="scatter", y="gdp_pp", x="Year",ax=ax,color="orange")


'''
GDP & Obesity together Code Starts here
'''

df_gdp["Year"] = df_gdp["Year"].astype(int)
df_gdp["gdp_pp"] = df_gdp["gdp_pp"].astype(float)

import plotly.express as px

df = px.data.gapminder()
df

'''
There is 2 new columns that will help to combine both and apply to an interactive world map to
better visualize the combination of both codes.

The columns are: iso_alpha and is_num which essentialy returns the country code and each country number.

The objective is to find any correlation between obesity and gdp
'''

dict_iso_alpha =df.set_index("country").to_dict()["iso_alpha"]
dict_num = {j: i for i,j in enumerate(df_gdp["Country"].unique())}

df_gdp["iso_alpha"] = df_gdp["Country"].map(dict_iso_alpha)
df_gdp["iso_num"] = df_gdp["Country"].map(dict_num)

fig = px.choropleth(df_gdp[df_gdp["Kind"]== "real"].reset_index(drop=True), locations="iso_alpha", color="gdp_pp", hover_name="Country", animation_frame="Year")
fig.update_layout(height=600)
fig.show()

df_obesity["country-year"] = df_obesity["Country"] + "-" + df_obesity.reset_index()["Year"].apply(lambda x: str(int(x))).values
dict_obesity_year = df_obesity.set_index("country-year").to_dict()["Obesity"]

df_gdp["country-year"] = df_gdp["Country"] + "-" + df_gdp["Year"].apply(lambda x: str(int(x))).values
df_gdp["Obesity"] = df_gdp["country-year"].map(dict_obesity_year)
df_gdp

df_gdp_clean = df_gdp.dropna()
df_gdp_clean.reset_index(drop=True).groupby("Year")[["Obesity", "gdp_pp"]].mean().corr()