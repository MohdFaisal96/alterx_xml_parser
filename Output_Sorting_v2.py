import xml.dom.minidom as minidom
import os
import pandas as pd
import sys
import numpy as np
import pyexcel
from Sort import Sort
from MultiRowFormula import MultiRowFormula
from Joiner import Join
from Union import Union
from GenerateRows import GenerateRows
from AppendFields_Alteryx import AppendFields
from Formula_Alteryx import Formula
from Sample_Alteryx import Sample
from Select_Alteryx import AlteryxSelect
from TextInput_Alteryx import TextInput
from TextToColumns_Alteryx import TextToColumns
from Altryx_DB_file_input_V01 import DbFileInput
from Altryx_DB_file_output_V01 import DbFileOutput
from Altryx_DB_Filter import Filter
from cross_tab import CrossTab
from Unique import Unique
from Summarize import Summarize

valid_element_types=["Sort","MultiRowFormula","Join","Union","GenerateRows","CrossTab","Unique","Summarize","AppendFields","Formula","Sample","AlteryxSelect","TextInput","TextToColumns","DbFileInput","DbFileOutput","Filter"]

def return_dict(element,filename):
    if(str(element) in valid_element_types):
        element_df=getattr(sys.modules[__name__], element)(filename)
    else:
        element_df=pd.DataFrame(data=[['','','','','','','','','','','','','','','','','','','','','','','','']],columns=['FileName','ToolID','Plugin','FieldName','Rename_or_Destination','CreateFieldName','UpdateFieldName','LeftJoinField','RightJoinField','Expression_1','Expression_2','Expression_3','GroupBy','SortOrder','UpdateField','MultifileValue','HeaderField','DataField','IsSelected','NoOfRows','NumFields','ErrorHandlingText',"PreSQL","PostSQL"])
    return element_df

def create_linked_list(linkage_df,curr_src,target_list,list):
    curr_df=linkage_df[linkage_df['Source Node'] == curr_src]
    linkage_df = linkage_df.drop_duplicates()
    # linkage_df.to_csv('Linkage.csv', mode='a', header=False, index=False)
    for index in curr_df.index:
        list.append([curr_df['Source Node'][index], curr_df['Target Node'][index]])
        # if(str(curr_df['Target Node'][index]) not in target_list):
        create_linked_list(linkage_df, curr_df['Target Node'][index], target_list,list)

def append_to_linked_list(list,detailed_df,target_list,filename):
    # print(list)
    for src_target in list:
        # print(detailed_df[detailed_df['Source Node']==src_target[0]])
        if(str(src_target[1]) not in target_list):
            new_df = detailed_df[detailed_df['Source Node'] == src_target[0]]
            new_df.to_csv('New.csv', mode='a', header=False, index=False)
        else:
            new_df = detailed_df[detailed_df['Source Node'] == src_target[0]]
            new_df.to_csv('New.csv', mode='a', header=False, index=False)
            target_subset=detailed_df[detailed_df['Target Node']==src_target[1]]
            target_plugin = target_subset[['Target Plugin','Target Link']].drop_duplicates()
            for index in target_plugin.index:
                target_df=return_dict(str(target_plugin['Target Plugin'][index]), filename)
                target_df.drop('FileName',inplace=True,axis=1)
                target_df.to_csv('Outputdbfile.csv',mode='a',header=True,index=True)
                base_target_slice=pd.DataFrame(data=[[filename,str(src_target[1]),str(target_plugin['Target Plugin'][index]),'','NA','NA','NA']],columns=[str(filename),str(src_target[1]),str(target_plugin['Target Plugin'][index]),str(target_plugin['Target Link'][index]),"NA","NA","NA"])
                merged_target_slice=pd.merge(base_target_slice,target_df,left_on=str(src_target[1]),right_on="ToolID")
                # merged_target_slice=merged_target_slice.drop(['Filename'],inplace=True,axis=1)
                merged_target_slice.to_csv('New.csv', mode='a', header=False, index=True)
                # print(target_df)
    sorted_df=pd.read_csv("New.csv",
                    names=["Input File Name","Source ID","Source Plugin","Source Link","Target ID","Target Plugin","Target Link","Plugin", "ToolID","FieldName","Rename_or_Destination","CreateFieldName","UpdateFieldName","LeftJoinField","RightJoinField","Expression_1","Expression_2","Expression_3","GroupBy","SortOrder","UpdateField","MultifileValue","HeaderField","DataField","IsSelected","NoOfRows","NumFields","ErrorHandlingText","PreSQL","PostSQL"],keep_default_na=False)
    sorted_df=sorted_df.drop_duplicates(keep="first")
    sorted_df['Target Plugin'].replace("", "*Missing*", inplace=True)
    sorted_df.drop(['Plugin', 'ToolID'], inplace=True, axis=1)
    return sorted_df
    # sorted_df.to_excel(writer, sheet_name='Output')
    # sorted_df.to_excel(filename.replace("yxmd","xlsx",1), sheet_name="Output", index=False)

def sort_output(filename1,filename2,xmlfilename):
    source_list = []
    target_list=[]
    linkage_df = pd.read_csv(filename1)
    detailed_df = pd.read_csv(filename2)
    # source_df=input_df['Source Node']-input_df['Target Node']
    source_df=linkage_df[~linkage_df["Source Node"].astype(str).isin(linkage_df["Target Node"].astype(str))]
    target_df=linkage_df[~linkage_df["Target Node"].astype(str).isin(linkage_df["Source Node"].astype(str))]
    # print(source_df)
    # print(target_df)
    for index in target_df.index:
        target_list.append(str(target_df['Target Node'][index]))

    for index in source_df.index:
        source_list.append(source_df['Source Node'][index])

    list = []
    for source in source_list:
        create_linked_list(linkage_df,source,target_list,list)
    list2=[]

    sorted_df=append_to_linked_list(list,detailed_df,target_list,xmlfilename)
    sorted_df['Source Link'].replace('Output','',inplace=True)
    sorted_df['Target Link'].replace('Input', '', inplace=True)
    for index in sorted_df.index:
        # print(str(sorted_df['Source Link'][index]))

        if(str(sorted_df['Target Link'][index]) in ["Output","Input","Targets"] ):
            sorted_df['Target Link'][index]=""
    # print(sorted_df[sorted_df['Source Link']=='Output'])
    writer = pd.ExcelWriter(xmlfilename.replace("yxmd","xlsx",1))

    sorted_df.to_excel(writer, sheet_name='Output',index=False)
    chain_df=sorted_df[["Input File Name","Source ID","Source Plugin","Source Link","Target ID","Target Plugin","Target Link"]].drop_duplicates()
    chain_df=chain_df[chain_df['Target ID']!='NA']
    chain_df.to_csv("Sorted_Chain.csv")


    chain_df.to_excel(writer, sheet_name='Lineage', index=False)
    writer.save()


sort_output("Output.csv","test3.csv","08_Belvidere_Data_Normalization for Mendix V6.yxmd")