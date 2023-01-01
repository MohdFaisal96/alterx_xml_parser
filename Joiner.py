import xml.dom.minidom as minidom
import pandas as pd

def Join(filename):
    left_join_field=""
    right_join_field=""
    OrderChanged=""
    CommaDecimal=""
    field=""
    selected=""
    rename=""
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
        if(plugin_name_level_2=="Join"):
            left_join_field=""
            right_join_field=""
            for GuiSetting in GuiSettings:
                join_info = node.getElementsByTagName("JoinInfo")
                for info in join_info:
                    join_fields=info.getElementsByTagName("Field")
                    for join_field in join_fields:
                        if(info.getAttribute("connection")=="Left"):
                            if(left_join_field==""):
                                left_join_field=left_join_field+str(join_field.getAttribute("field"))
                            else:
                                left_join_field = left_join_field + ", "+str(join_field.getAttribute("field"))
                            # left_join_field=join_field.getAttribute("field")
                        if(info.getAttribute("connection") == "Right"):
                            if(right_join_field==""):
                                right_join_field=right_join_field+str(join_field.getAttribute("field"))
                            else:
                                right_join_field = right_join_field + ", "+str(join_field.getAttribute("field"))
                            # right_join_field=join_field.getAttribute("field")
                order_changes = node.getElementsByTagName("OrderChanged")
                comma_decimals=node.getElementsByTagName("CommaDecimal")
                SelectFields=node.getElementsByTagName("SelectField")
                for order_change in order_changes:
                    OrderChanged=order_change.getAttribute("value")
                for comma_decimal in comma_decimals:
                    CommaDecimal=comma_decimal.getAttribute("value")
                for SelectField in SelectFields:
                    field=SelectField.getAttribute("field")
                    selected=SelectField.getAttribute("selected")
                    rename=SelectField.getAttribute("rename")
                    list_row.append([str(filename),tool_id,full_plugin_name,field,rename,"","",left_join_field,right_join_field,"","","","","","","","","","","","",""])
    joiner_df=pd.DataFrame(data=list_row,columns=["FileName","ToolID","Plugin","FieldName","Rename_or_Destination","CreateFieldName","UpdateFieldName","LeftJoinField","RightJoinField","Expression_1","Expression_2","Expression_3","GroupBy","SortOrder","UpdateField","MultifileValue","HeaderField","DataField","IsSelected","NoOfRows","NumFields","ErrorHandlingText"])

    return joiner_df.drop_duplicates()

# Join("C:/Users/angangupta4/Downloads/Alteryx/input/08_Belvidere_Data_Normalization for Mendix V6.yxmd").to_csv("Joiner.csv",index=False)