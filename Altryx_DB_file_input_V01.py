import xml.dom.minidom as minidom
import pandas as pd


def DbFileInput(filename):

    DOMTree = minidom.parse(filename)
    Node = DOMTree.getElementsByTagName("Node")
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
    list_row=[]
    for node in Node:
        GuiSettings=node.getElementsByTagName("GuiSettings")
        child=node.childNodes.item(1)
        ToolID = child.getAttribute("Plugin")
        plugin_name_level_1 = (ToolID[ToolID.find('.', 1, len(ToolID) - 1) + 1:])
        Plugin = (plugin_name_level_1[plugin_name_level_1.find('.', 2, len(plugin_name_level_1) - 1) + 1:])

        ToolID = node.getAttribute("ToolID")
        if(Plugin=="DbFileInput"):

         for GuiSetting in GuiSettings:
            if node.getElementsByTagName("File")==[]:
                Expression_1=''
            else:
             File=node.getElementsByTagName("File")
             for f in File:
                 Expression_1=node.getElementsByTagName("File")[0].firstChild.nodeValue
             if node.getElementsByTagName("Field")==[]:
                 FieldName = ''
                 Expression_2 = ''
                 list_row.append([str(filename), ToolID, Plugin, FieldName, Rename_or_Destination, CreateFieldName,
                                  UpdateFieldName, LeftJoinField, RightJoinField, Expression_1, Expression_2,
                                  Expression_3, GroupBy, SortOrder, UpdateField, MultifileValue, HeaderField,
                                  DataField, IsSelected, NoOfRows, NumFields, ErrorHandlingText])
             Field = node.getElementsByTagName("Field")
             for fld in Field:
                 FieldName=fld.getAttribute("name")
                 Expression_2=fld.getAttribute("source")

                 list_row.append([str(filename), ToolID, Plugin, FieldName, Rename_or_Destination, CreateFieldName,
                                  UpdateFieldName, LeftJoinField, RightJoinField, Expression_1, Expression_2,
                                  Expression_3, GroupBy, SortOrder, UpdateField, MultifileValue, HeaderField,
                                  DataField, IsSelected, NoOfRows, NumFields, ErrorHandlingText])

    DbFileInput_df = pd.DataFrame(data=list_row,columns=['FileName','ToolID','Plugin','FieldName','Rename_or_Destination','CreateFieldName','UpdateFieldName','LeftJoinField','RightJoinField','Expression_1','Expression_2','Expression_3','GroupBy','SortOrder','UpdateField','MultifileValue','HeaderField','DataField','IsSelected','NoOfRows','NumFields','ErrorHandlingText'])

    return DbFileInput_df.drop_duplicates()

# DbFileInput("C:/Users/kanish/Desktop/UNDIAL FI/Altryx FI/Abhishek_Doc/08_Belvidere_Data_Normalization for Mendix V6.yxmd").to_csv("DbFileInput_new.csv",index=False)






