import xml.dom.minidom as minidom
import pandas as pd

def GenerateRows(filename):
    createfield_name=""
    createfield_type=""
    createfield_size=""
    exp_init=""
    exp_cond = ""
    exp_loop = ""
    upd_field = ""
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
        if(plugin_name_level_2=="GenerateRows"):
            createfield_name = node.getElementsByTagName("CreateField_Name")[0].firstChild.nodeValue
            updatefield_name=''
            if(node.getElementsByTagName("UpdateField_Name")[0].firstChild is not None):
                updatefield_name = node.getElementsByTagName("UpdateField_Name")[0].firstChild.nodeValue
            createfield_type = node.getElementsByTagName("CreateField_Type")[0].firstChild.nodeValue
            createfield_size= node.getElementsByTagName("CreateField_Size")[0].firstChild.nodeValue
            exp_init = node.getElementsByTagName("Expression_Init")[0].firstChild.nodeValue
            exp_cond = node.getElementsByTagName("Expression_Cond")[0].firstChild.nodeValue
            exp_loop = node.getElementsByTagName("Expression_Loop")[0].firstChild.nodeValue
            update_fields=node.getElementsByTagName("UpdateField")
            for update_field in update_fields:
                upd_field=update_field.getAttribute("value")
                list_row.append([str(filename),str(tool_id),str(full_plugin_name),"","",str(createfield_name),str(updatefield_name),"","",str(exp_cond),str(exp_init),str(exp_loop),"","","","","","","","","",""])
    generaterows_df=pd.DataFrame(data=list_row,columns=["FileName","ToolID","Plugin","FieldName","Rename_or_Destination","CreateFieldName","UpdateFieldName","LeftJoinField","RightJoinField","Expression_1","Expression_2","Expression_3","GroupBy","SortOrder","UpdateField","MultifileValue","HeaderField","DataField","IsSelected","NoOfRows","NumFields","ErrorHandlingText"])
    return generaterows_df.drop_duplicates()

# GenerateRows("02_BELVDR_Data_Load_API V3.yxmd").to_csv("GenerateRows.csv",index=False)