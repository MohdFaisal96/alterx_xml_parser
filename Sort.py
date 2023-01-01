import xml.dom.minidom as minidom
import pandas as pd

def Sort(filename):
    field_name=""
    order=""
    locale=""
    list_row=[]
    DOMTree = minidom.parse(filename)
    Node = DOMTree.getElementsByTagName("Node")
    for node in Node:
        GuiSettings=node.getElementsByTagName("GuiSettings")
        child=node.childNodes.item(1)
        full_plugin_name=child.getAttribute("Plugin")
        plugin_name_level_1 = (full_plugin_name[full_plugin_name.find('.', 1, len(full_plugin_name) - 1) + 1:])
        plugin_name_level_2 = (plugin_name_level_1[plugin_name_level_1.find('.', 2, len(plugin_name_level_1) - 1) + 1:])
        # print(plugin_name_level_2)
        tool_id=node.getAttribute("ToolID")
        if(plugin_name_level_2=="Sort"):
            sortinfos=node.getElementsByTagName("SortInfo")
            fields=node.getElementsByTagName("Field")
            for sortinfo in sortinfos:
                locale=sortinfo.getAttribute("locale")
                for field in fields:
                    field_name=field.getAttribute("field")
                    order=field.getAttribute("order")
                    list_row.append([str(filename),str(tool_id),str(full_plugin_name),str(field_name),"","","","","","","","","",str(order),"","","","","","","",""])
    sort_df=pd.DataFrame(data=list_row,columns=["FileName","ToolID","Plugin","FieldName","Rename_or_Destination","CreateFieldName","UpdateFieldName","LeftJoinField","RightJoinField","Expression_1","Expression_2","Expression_3","GroupBy","SortOrder","UpdateField","MultifileValue","HeaderField","DataField","IsSelected","NoOfRows","NumFields","ErrorHandlingText"])
    return sort_df.drop_duplicates()

# Sort("C:/Users/angangupta4/Downloads/Alteryx/input/08_Belvidere_Data_Normalization for Mendix V6.yxmd").to_csv("Sort.csv",index=False)