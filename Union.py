import xml.dom.minidom as minidom
import pandas as pd

def Union(filename):
    errormode=""
    outputmode=""
    mode=""
    set_op_order=""
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
        if(plugin_name_level_2=="Union"):
            errormode = node.getElementsByTagName("ByName_ErrorMode")[0].firstChild.nodeValue
            outputmode = node.getElementsByTagName("ByName_OutputMode")[0].firstChild.nodeValue
            mode=node.getElementsByTagName("Mode")[0].firstChild.nodeValue
            SetOutputOrders=node.getElementsByTagName("SetOutputOrder")
            for SetOutputOrder in SetOutputOrders:
                set_op_order=SetOutputOrder.getAttribute("value")
                list_row.append([str(filename),str(tool_id),str(full_plugin_name),"","","","","","",str(outputmode),str(mode),"","","","","","","","","","",""])
    union_df=pd.DataFrame(data=list_row,columns=["FileName","ToolID","Plugin","FieldName","Rename_or_Destination","CreateFieldName","UpdateFieldName","LeftJoinField","RightJoinField","Expression_1","Expression_2","Expression_3","GroupBy","SortOrder","UpdateField","MultifileValue","HeaderField","DataField","IsSelected","NoOfRows","NumFields","ErrorHandlingText"])
    return union_df.drop_duplicates()

# Union("02_BELVDR_Data_Load_API V3.yxmd").to_csv("Union.csv",index=False)