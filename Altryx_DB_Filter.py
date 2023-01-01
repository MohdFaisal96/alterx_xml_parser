import xml.dom.minidom as minidom
import pandas as pd


def Filter(filename):
    FileName = ""
    ToolID = ""
    Plugin = ""
    FieldName = ""
    Rename_or_Destination = ""
    CreateFieldName = ""
    UpdateFieldName = ""
    LeftJoinField = ""
    RightJoinField = ""
    Expression_1 = ""
    Expression_2 = ""
    Expression_3 = ""
    GroupBy = ""
    SortOrder = ""
    UpdateField = ""
    MultifileValue = ""
    HeaderField = ""
    DataField = ""
    IsSelected = ""
    NoOfRows = ""
    NumFields = ""
    ErrorHandlingText = ""
    DOMTree = minidom.parse(filename)
    Node = DOMTree.getElementsByTagName("Node")
    list_row=[]
    for node in Node:
        GuiSettings=node.getElementsByTagName("GuiSettings")
        child=node.childNodes.item(1)
        ToolID=child.getAttribute("Plugin")
        plugin_name_level_1 = (ToolID[ToolID.find('.', 1, len(ToolID) - 1) + 1:])
        Plugin = (plugin_name_level_1[plugin_name_level_1.find('.', 2, len(plugin_name_level_1) - 1) + 1:])

        ToolID=node.getAttribute("ToolID")
        if(Plugin=="Filter"):
         for GuiSetting in GuiSettings:

             if node.getElementsByTagName("Expression")==[]:
                Expression_1=''
             else:
                 Expression_1 = node.getElementsByTagName("Expression")[0].firstChild.nodeValue
             if node.getElementsByTagName("Mode") == []:
                 Expression_2=''
             else:
                 Expression_2 = node.getElementsByTagName("Mode")[0].firstChild.nodeValue

             if node.getElementsByTagName("Operator") == []:
                 Operator=''
             else:
                 Operator = node.getElementsByTagName("Operator")[0].firstChild.nodeValue
             if node.getElementsByTagName("Field") == []:
                 Field=''
             else:
                 Field = node.getElementsByTagName("Field")[0].firstChild.nodeValue

             Expression_3= Operator+" "+Field


             list_row.append([str(filename), ToolID, Plugin, FieldName, Rename_or_Destination, CreateFieldName,
                                 UpdateFieldName, LeftJoinField, RightJoinField, Expression_1, Expression_2,
                                 Expression_3, GroupBy, SortOrder, UpdateField, MultifileValue, HeaderField,
                                 DataField, IsSelected, NoOfRows, NumFields, ErrorHandlingText])

    Filter_df = pd.DataFrame(data=list_row,columns=['FileName','ToolID','Plugin','FieldName','Rename_or_Destination','CreateFieldName','UpdateFieldName','LeftJoinField','RightJoinField','Expression_1','Expression_2','Expression_3','GroupBy','SortOrder','UpdateField','MultifileValue','HeaderField','DataField','IsSelected','NoOfRows','NumFields','ErrorHandlingText'])

    return Filter_df.drop_duplicates()

# Filter("C:/Users/kanish/Desktop/UNDIAL FI/Altryx FI/Abhishek_Doc/08_Belvidere_Data_Normalization for Mendix V6.yxmd").to_csv("Filter_new.csv",index=False)








