from flask import Flask,render_template
import json
import pandas as pd
import numpy as np
import math

app=Flask(__name__)



linkage_df = pd.read_csv("Sorted_Chain.csv")
# print(linkage_df)
source_df=linkage_df[~linkage_df["Source ID"].astype(str).isin(linkage_df["Target ID"].astype(str))]
source_node_list=[]
for index in source_df.index:
    # print(source_df['Source ID'][index])
    source_node_list.append(str(source_df['Source ID'][index]))

print(source_node_list)
node_list=[]
# print(source_df)
for index in source_df.index:
    if(np.isnan(source_df['Source Link'][index])):
        node_list.append({'Name': str(source_df['Source ID'][index])+"_"+str(source_df['Source Plugin'][index]),"Caption":str(int(source_df['Source ID'][index]))+"_"+str(source_df['Source Plugin'][index])})
    else:
        node_list.append({'Name': str(source_df['Source ID'][index])+"_"+str(source_df['Source Plugin'][index]),"Caption":str(source_df['Source Link'][index])+" "+str(int(source_df['Source ID'][index]))+"_"+str(source_df['Source Plugin'][index])})

# print(node_list)
connector_list = []



for index in linkage_df.index:

    if (str(linkage_df['Target Link'][index])=="nan"):
        node_list.append({"Name": str(int(linkage_df['Target ID'][index]))+"_"+str(linkage_df['Target Plugin'][index]), "ReportingPerson": str(int(linkage_df['Source ID'][index]))+"_"+str(linkage_df['Source Plugin'][index]),"Caption":str(int(linkage_df['Target ID'][index]))+"_"+str(linkage_df['Target Plugin'][index])})
    else:
        node_list.append({"Name": str(int(linkage_df['Target ID'][index]))+"_"+str(linkage_df['Target Plugin'][index]), "ReportingPerson": str(int(linkage_df['Source ID'][index]))+"_"+str(linkage_df['Source Plugin'][index]),"Caption":str(linkage_df['Target Link'][index])+" "+str(int(linkage_df['Target ID'][index]))+"_"+str(linkage_df['Target Plugin'][index])})

# print(node_list)
print(node_list)

@app.route('/')
def home():

    Data_nodes =[{"Name": "Steve-Ceo"},
	{"Name": "Kevin-Manager", "ReportingPerson": "Steve-Ceo"},
	{"Name": "Peter-Manager", "ReportingPerson": "Steve-Ceo"},
	{"Name": "John- Manager", "ReportingPerson": "Peter-Manager"},
	{"Name": "Mary-CSE ", "ReportingPerson": "Peter-Manager"},
	{"Name": "Jim-CSE ", "ReportingPerson": "Kevin-Manager"},
	{"Name": "Martin-CSE", "ReportingPerson": "Kevin-Manager"}]
    connectors=connector_list
    return render_template('/Flowchart2.html',Data_nodes=node_list)

if __name__ == '__main__':
   app.run()