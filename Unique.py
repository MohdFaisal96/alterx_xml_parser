import os
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET 
import pandas as pd


def Unique(filename):

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
    
    Plugin_value = "Unique"
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
            unique_flds = node.getElementsByTagName("UniqueFields")
            for u in unique_flds:
                fields = u.getElementsByTagName("Field")
                for f in fields:
                    field_name=f.getAttribute("field")
                    list_row.append([str(file),str(tool_id),str(full_plugin_name),str(field_name),
                    str(_Rename_or_Destination),str(_CreateFieldName),str(_UpdateFieldName),str(_LeftJoinField),
                    str(_RightJoinField),str(_Expression_1),str(_Expression_2),str(_Expression_3),
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
#     Unique_Tx(filename).to_csv("unique_new.csv",index=False)
#





