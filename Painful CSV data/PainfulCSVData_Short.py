# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 11:36:48 2020

@author: Kieran Blacker
"""
import pandas as pd
df = pd.read_csv("DC-2019.csv")
df2 = df.pivot_table(index='id', columns=["determinand.notation"], values="result")
df2 = df2.reset_index(drop=True)
pointID = df["sample.samplingPoint.notation"]
df2 = df2.join(pointID)
df2c = df2.groupby(['sample.samplingPoint.notation']).sum(min_count=1)
dfc = df.drop_duplicates(subset='sample.samplingPoint.notation')
dfc = dfc.set_index('sample.samplingPoint.notation')
merge = dfc.join(df2c)
merge.to_csv("DC-2019_formatted.csv")