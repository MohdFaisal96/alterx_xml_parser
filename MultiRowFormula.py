import xml.dom.minidom as minidom
import pandas as pd

def MultiRowFormula(filename):
    createfield_name=""
    createfield_type=""
    createfield_size=""
    updatefield_name=""
    other_rows = ""
    expression = ""
    upd_field = ""
    field_name = ""
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
        if(plugin_name_level_2=="MultiRowFormula"):
            createfield_name = node.getElementsByTagName("CreateField_Name")[0].firstChild.nodeValue
            createfield_type = node.getElementsByTagName("CreateField_Type")[0].firstChild.nodeValue
            createfield_size= node.getElementsByTagName("CreateField_Size")[0].firstChild.nodeValue
            if(node.getElementsByTagName("UpdateField_Name")[0].firstChild is not None):
                updatefield_name = node.getElementsByTagName("UpdateField_Name")[0].firstChild.nodeValue
            other_rows = node.getElementsByTagName("OtherRows")[0].firstChild.nodeValue
            expression = node.getElementsByTagName("Expression")[0].firstChild.nodeValue
            update_fields=node.getElementsByTagName("UpdateField")
            fields=node.getElementsByTagName("Field")
            numrows=node.getElementsByTagName("NumRows")
            for update_field in update_fields:
                upd_field=update_field.getAttribute("value")
                for numrow in numrows:
                    NumRow = numrow.getAttribute("value")
                    field_name=""
                    for field in fields:
                        if(field_name==""):
                            field_name=field_name+str(field.getAttribute("field"))
                        else:
                            field_name = field_name + ", "+str(field.getAttribute("field"))
                    list_row.append([str(filename),str(tool_id),str(full_plugin_name),"","",str(createfield_name),str(updatefield_name),"","",str(expression),"","",str(field_name),"",str(upd_field),"","","","","","",""])
    multirowformula_df=pd.DataFrame(data=list_row,columns=["FileName","ToolID","Plugin","FieldName","Rename_or_Destination","CreateFieldName","UpdateFieldName","LeftJoinField","RightJoinField","Expression_1","Expression_2","Expression_3","GroupBy","SortOrder","UpdateField","MultifileValue","HeaderField","DataField","IsSelected","NoOfRows","NumFields","ErrorHandlingText"])
    return multirowformula_df.drop_duplicates()

# MultiRowFormula("C:/Users/angangupta4/Downloads/Alteryx/input/08_Belvidere_Data_Normalization for Mendix V6.yxmd").to_csv("MultipleRowFormxula.csv",index=False)