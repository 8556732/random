# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 19:26:49 2020

@author: Kieran Blacker

Ensure all files are in same dir as this script
"""
import pandas as pd

# Load csv data

df = pd.read_csv("DC-2019.csv")

'''
This is my data exploration stuff - I have kept my working in this script

Uncomment out to run lines if you want to go through my steps
'''
#df = df.set_index('id')
# print head and summary files, easier than terminal checking, uncomment 
#df.describe().to_csv("DF_Summary-EvaM.csv") # stats for entire dataframe
#df.head(n=10).to_csv("DF_Head-EvaM.csv") # first 10 rows

# Determine list of unique values for determinands:

# first I count the number of unique entries to see if this will work!
#print(len(pd.unique(df["determinand.notation"]))) 
#print(len(pd.unique(df["determinand.label"]))) 
#print(len(pd.unique(df["determinand.definition"]))) 
'''
Ok so this returns [699, 697, 699]

This tells me there are 699 unique dtypes but there are duplicate labels
I'm going to group by notation, so columns will have numerical notation

We also need a unique identifier for each point as the id var contains the 
determinand notation, which doesn't help us. 

So I'm going to multiply easting and northing together, to make a UID

Correction - apparently var "sample.samplingPoint.notation" is the UID

Leaving this in for completeness
'''
#df['UID'] = pd.Series(df['sample.samplingPoint.easting']*df['sample.samplingPoint.northing'])
# This appends the UID column to the dataframe
#print(len(pd.unique(df['UID']))) # check number of unique points = 1695

# Pivot to new dataframe with columns of unique determinand.notation, retain NaN values
df2 = df.pivot_table(index='id', columns=["determinand.notation"], values="result") # this now has text "id" index
# we need to numerically reindex to rejoin the sample ID column back
df2 = df2.reset_index(drop=True)
# we drop the original index
pointID = df["sample.samplingPoint.notation"]
# we add the point ID column back and join frames
df2 = df2.join(pointID)
#df2.head(n=1000).to_csv("DF2_Head-EvaM.csv") # first 1000 rows to check
#print(len(pd.unique(df2['sample.samplingPoint.notation']))) # check it works!

# aggregate and sum determinands, retain nan's by specifying min val to be used
df2c = df2.groupby(['sample.samplingPoint.notation']).sum(min_count=1)
#df2c.head(n=10).to_csv("DF2c_Head-EvaM.csv") # first 10 rows to check

# Ok now to do the same collapse/drop repeat to the original DF and join
dfc = df.drop_duplicates(subset='sample.samplingPoint.notation') # drop all repeats from original
dfc = dfc.set_index('sample.samplingPoint.notation') # set sample id as index for join

merge = dfc.join(df2c)

# save to a csv:
merge.to_csv("DC-2019_formatted.csv")

# to do - remap column names using determinand list and drop dud columns



















