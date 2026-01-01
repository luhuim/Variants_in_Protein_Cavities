#!/usr/bin/python3
"""
Title: getting a table which include the distribution of amono acids between normal and variant
Date: 2022 December 12
Author: Huimin Lu
"""
# import numpy as np
# from pandas import DataFrame
import pandas as pd
from collections import Counter

f= pd.read_csv("variant_cavity.tsv",sep='\t',index_col=None)

# print(f.info())

full_text=[]#["P01112-G12C","P01112-G12C"]
full_variant=[]#"full_variant" include all substitute[AT,PS]
for i in range(0,len(f["UniprotID"])):
    uniprot=f.loc[i,"UniprotID"]
    text_list=f.loc[i,"Variantion Text"].split(',')
    for x in text_list:
        full_text.append(uniprot+"-"+x)
print("All text", len(full_text))
full_text=set(full_text)#Only leave unique text["P01112-G12C"]
print("Only Unique",len(full_text))

for variant in full_text:
    y=variant.index("-")
    full_variant.append(variant[y+1]+variant[-1])

result=Counter(full_variant)#"result" is a dictionary, key is variant, value is the amount of this variant 
# print(result)

#Making table
amino_acid=["A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","V"]

summary=pd.DataFrame(index=amino_acid, columns=amino_acid)##The summary table is "summary"

for k,v in result.items():
    # print("key",k)
    # print("value",v)
    a=k[0]#front
    b=k[1]#back
    # print("front",a)
    # print("back",b)
    summary[b][a]=v
# print(summary)
summary = summary.fillna(0)#replace all "Nan" with "0"
# print(summary)

#add sum of column and row
#sum that is bottom raw
sum_row=summary.sum()
sum_row.name="sum_row"
# Assign sum of all rows of DataFrame as a new Row
summary = summary.append(sum_row.transpose())

#sum that is last column
#df2 = df.sum(axis=1)
summary["sum_col"]=summary.sum(axis=1)


print(summary)

#Export DataFrame "summary" into excel
#df1.to_excel("output.xlsx") 
summary.to_excel("Variant_Summary.xlsx")




