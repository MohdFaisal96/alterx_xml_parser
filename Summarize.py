import os
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET 
import pandas as pd
import itertools

def Summarize(filename):

    _FileName = ''
    _ToolID = ''
    _Plugin = ''
    _FieldName = ''
    _Rename_or_Destination = ''
    _CreateFieldName = ''
    _UpdateFieldName = ''
    _LeftJoinField = ''
    _RightJoinField = ''
    _Expression_1 = ''
    _Expression_2 = ''
    _Expression_3 = ''
    _GroupBy = ''
    _SortOrder = ''
    _UpdateField = ''
    _MultifileValue = ''
    _HeaderField = ''
    _DataField = ''
    _IsSelected = ''
    _NoOfRows = ''
    _NumFields = ''
    _ErrorHandlingText = ''

    Plugin_value = "Summarize"
    file = os.path.splitext(os.path.basename(filename))[0]
    field_name=""
    list_row=[]

    DOMTree = minidom.parse(filename)
    Node = DOMTree.getElementsByTagName("Node")
    for node in Node:
        GuiSettings=node.getElementsByTagName("GuiSettings")
        child=node.childNodes.item(1)
        full_plugin_name=child.getAttribute("Plugin")
        tool_id=node.getAttribute("ToolID")
        if Plugin_value in full_plugin_name:

            summ_flds = node.getElementsByTagName("SummarizeField")
            for s in summ_flds:

                field_name = s.getAttribute("field")
                action_name = s.getAttribute("action")
                rename_name = s.getAttribute("rename")
                list_row.append([str(file),str(tool_id),str(full_plugin_name),str(field_name),str(rename_name),
                                str(_CreateFieldName),str(_UpdateFieldName),str(_LeftJoinField),
                                str(_RightJoinField),str(action_name),str(_Expression_2),str(_Expression_3),
                                str(_GroupBy),str(_SortOrder),str(_UpdateField),str(_MultifileValue),str(_HeaderField),
                                str(_DataField),str(_IsSelected),str(_NoOfRows),str(_NumFields),str(_ErrorHandlingText)])
    
    
    
    unique_df=pd.DataFrame(data=list_row,columns=["FileName","ToolID","Plugin","FieldName",
            "Rename_or_Destination","CreateFieldName","UpdateFieldName","LeftJoinField",
            "RightJoinField","Expression_1","Expression_2","Expression_3","GroupBy","SortOrder",
            "UpdateField","MultifileValue","HeaderField","DataField","IsSelected","NoOfRows","NumFields",
            "ErrorHandlingText"])
    return unique_df.drop_duplicates()


# if __name__ == "__main__":
#     file_input = "08_Belvidere_Data_Normalization V15 Weekly.yxmd"
#     filename = os.path.abspath(os.path.join(file_input))
#     Summarize_Tx(filename).to_csv("Summarize_new.csv",index=False)
#
#
#
#



