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