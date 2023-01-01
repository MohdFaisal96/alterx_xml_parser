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

# valid_element_types=["Sort","MultiRowFormula","Join","Union","GenerateRows","AppendFields","Formula","Sample","AlteryxSelect","TextInput","TextToColumns","DbFileInput","DbFileOutput","Filter","CrossTab"]
valid_element_types=["Sort","MultiRowFormula","Join","Union","GenerateRows","CrossTab","Unique","Summarize","AppendFields","Formula","Sample","AlteryxSelect","TextInput","TextToColumns","DbFileInput","DbFileOutput","Filter"]
output_df=pd.DataFrame()


def return_dict(element,filename):
    element_df=getattr(sys.modules[__name__], element)(filename)
    return element_df


for filename in os.listdir("input"):
    input_file = filename
    DOMTree = minidom.parse(input_file)
    origins = DOMTree.getElementsByTagName("Origin")
    destinations=DOMTree.getElementsByTagName("Destination")
    base_df={}
    origin_list=[]
    destination_list=[]
    node_plugin_list=[]
    for origin in origins:
        origin_list.append(origin.getAttribute("ToolID"))
    for destination in destinations:
        destination_list.append(destination.getAttribute("ToolID"))
    origin_dest_list=list(zip(origin_list,destination_list))
    node_df= pd.DataFrame(origin_dest_list, columns=['Source Node', 'Target Node'])

    nodes = DOMTree.getElementsByTagName("Node")
    for node in nodes:
        node_index=node.getAttribute("ToolID")
        gui_settings=node.getElementsByTagName("GuiSettings")
        for gui_setting in gui_settings:
            full_plugin_name=gui_setting.getAttribute("Plugin")
            plugin_name_level_1 = (full_plugin_name[full_plugin_name.find('.', 1, len(full_plugin_name) - 1) + 1:])
            plugin_name_level_2 = (plugin_name_level_1[plugin_name_level_1.find('.', 2, len(plugin_name_level_1) - 1) + 1:])
            node_plugin_list.append([str(node_index),str(plugin_name_level_2)])
    plugin_df=pd.DataFrame(node_plugin_list, columns=['Node', 'Plugin'])
    base_df = pd.merge(node_df, plugin_df, how="inner", left_on=['Source Node'], right_on=['Node'])
    base_df = pd.merge(base_df, plugin_df, how="inner", left_on=['Target Node'], right_on=['Node'])
    # print(base_df)

    base_df=base_df[['Source Node', 'Plugin_x', 'Target Node', 'Plugin_y']]
    base_df.rename(columns={'Plugin_x': 'Source Plugin', 'Plugin_y': 'Target Plugin'}, inplace=True)
    base_df.to_csv("Output.csv")
    for index in base_df.index:
        src_full_plugin_name=base_df['Source Plugin'][index]
        src_plugin_name_level_1 = (src_full_plugin_name[src_full_plugin_name.find('.', 1, len(src_full_plugin_name) - 1) + 1:])
        src_plugin_name_level_2 = (src_plugin_name_level_1[src_plugin_name_level_1.find('.', 2, len(src_plugin_name_level_1) - 1) + 1:])
        tgt_full_plugin_name = base_df['Target Plugin'][index]
        tgt_plugin_name_level_1 = (tgt_full_plugin_name[tgt_full_plugin_name.find('.', 1, len(tgt_full_plugin_name) - 1) + 1:])
        tgt_plugin_name_level_2 = (tgt_plugin_name_level_1[tgt_plugin_name_level_1.find('.', 2, len(tgt_plugin_name_level_1) - 1) + 1:])
        if(src_plugin_name_level_2 in valid_element_types):
            base_df_slice=base_df.loc[base_df['Source Node'] == base_df['Source Node'][index]]
            src_df=return_dict(src_plugin_name_level_2,filename)
            src_df=src_df.loc[src_df['ToolID'] == base_df['Source Node'][index]]
            # tgt_df=return_dict(tgt_plugin_name_level_2,filename)
            # tgt_df = tgt_df.loc[tgt_df['ToolID'] == base_df['Target Node'][index]]
            # print("Source------------")
            # print(src_df)
            # print("Target----------")
            # print(tgt_df)
            # print("Base_Source------------")
            merged_df_slice = pd.merge(base_df_slice, src_df, how="inner", left_on=['Source Node'], right_on=['ToolID'])
            # merged_df_slice = pd.merge(merged_df_slice, tgt_df, how="inner", left_on=['Target Node'], right_on=['ToolID'])
            # print(merged_df_slice)
            # merged_df_slice.drop(['Filename','ToolID','Plugin'],inplace=True,axis=1)
            print(merged_df_slice)
            merged_df_slice.to_csv('test.csv', mode='a', header=False, index=False)
            # output_df=pd.concat([output_df,base_df_slice])
            # output_df = pd.concat([output_df, merged_df_slice])
            # print(output_df)
        else:
            base_df_slice = base_df.loc[base_df['Source Node'] == base_df['Source Node'][index]]
            base_df_slice.to_csv('test.csv', mode='a', header=False, index=False)
            # base_df = pd.merge(base_df_slice, tgt_df, how="inner", left_on=['Source Node'], right_on=['ToolID'])
            # merged_src_tgt_df=pd.merge(src_df, tgt_df, how="inner", left_on=['Source Node'], right_on=['Node'])
    test_df = pd.read_csv("test.csv", names=["Source Node","Source Plugin","Target Node","Target Plugin","FileName","ToolID","Plugin","FieldName","Rename_or_Destination","CreateFieldName","UpdateFieldName","LeftJoinField","RightJoinField","Expression_1","Expression_2","Expression_3","GroupBy","SortOrder","UpdateField","MultifileValue","HeaderField","DataField","IsSelected","NoOfRows","NumFields","ErrorHandlingText"])
    test_df['FileName']=str(filename)
    test_df=test_df[["FileName","Source Node","Source Plugin","Target Node","Target Plugin","ToolID","Plugin","FieldName","Rename_or_Destination","CreateFieldName","UpdateFieldName","LeftJoinField","RightJoinField","Expression_1","Expression_2","Expression_3","GroupBy","SortOrder","UpdateField","MultifileValue","HeaderField","DataField","IsSelected","NoOfRows","NumFields","ErrorHandlingText"]]
    test_df.to_csv("test2.csv")
    test_df.to_excel("Final_Output_Merged.xlsx", sheet_name="Output", index=False)
    test_df.to_csv("test3.csv")


    #

    # test_df=pd.read_csv('test.csv')
    #
    #
    # print(test_df['RowType'])
    # test_df.to_csv('test.csv',header=True)
