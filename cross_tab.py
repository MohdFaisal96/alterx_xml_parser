import os
import xml.dom.minidom as minidom
import pandas as pd

def CrossTab(filename):

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

    Plugin_value = "CrossTab"
    file = os.path.splitext(os.path.basename(filename))[0]
    field_name=""
    appn_list=[]
    appn_list1=[]
    fld_list=[]
    list_row=[]
    sort_list=[]
    DOMTree = minidom.parse(filename)
    Node = DOMTree.getElementsByTagName("Node")
    for node in Node:
        GuiSettings=node.getElementsByTagName("GuiSettings")
        child=node.childNodes.item(1)
        full_plugin_name=child.getAttribute("Plugin")
        tool_id=node.getAttribute("ToolID")
        if Plugin_value in full_plugin_name:
            headinfo=node.getElementsByTagName("HeaderField")
            for h in headinfo:
                header_name=h.getAttribute("field")

            datainfo=node.getElementsByTagName("DataField")
            for d in datainfo:
                data_name=d.getAttribute("field")

            methods=node.getElementsByTagName("Methods")
            for me in methods:
                meth=me.getElementsByTagName("Method")
                sep=me.getElementsByTagName("Separator")[0]
                sep_value=sep.firstChild.data
                fieldsize=node.getElementsByTagName("FieldSize")
                for m,f in zip(meth,fieldsize):
                    method_name=m.getAttribute("method")
                    


            crossinfo=node.getElementsByTagName("GroupFields")
            
            for c in crossinfo:
                fields=c.getElementsByTagName("Field")
                for field in fields:
                    field_name=field.getAttribute("field")
                    appn_list1.append(field_name)
                    fld_list = list(set(appn_list1))
                    fld_elements = str(fld_list)[1:-1]
                MetaInfo = node.getElementsByTagName("MetaInfo")
                for MI in MetaInfo:
                    SortInfo = MI.getElementsByTagName("SortInfo")
                    for SI in SortInfo:
                        field = SI.getElementsByTagName("Field")
                        for f in field:
                            sort_field = f.getAttribute("field")
                            order = f.getAttribute("order")
                            appn_list.append(sort_field+"| Sort Order = "+order)
                            sort_list = list(set(appn_list))
                            sort_elements =  str(sort_list)[1:-1]
                RecordInfo = MI.getElementsByTagName("RecordInfo")
                for RI in RecordInfo:
                    field = RI.getElementsByTagName("Field")
                    for f in field:
                        rec_name = f.getAttribute("name")
                        source = f.getAttribute("source")
                        list_row.append([str(file),str(tool_id),str(full_plugin_name),str(rec_name),
                                        str(_Rename_or_Destination),str(_CreateFieldName),
                                        str(_UpdateFieldName),str(_LeftJoinField),str(_RightJoinField),
                                        str(str(method_name) + "| Separator = " + str(sep_value)),str(fld_elements),str(source),str(_GroupBy),
                                        str(sort_elements),str(_UpdateField),str(_MultifileValue),
                                        str(header_name),str(data_name),str(_IsSelected),str(_NoOfRows),
                                        str(_NumFields),str(_ErrorHandlingText)])                        

                                                        

    sort_df=pd.DataFrame(data=list_row,columns=["FileName","ToolID","Plugin","FieldName",
            "Rename_or_Destination","CreateFieldName","UpdateFieldName","LeftJoinField",
            "RightJoinField","Expression_1","Expression_2","Expression_3","GroupBy","SortOrder",
            "UpdateField","MultifileValue","HeaderField","DataField","IsSelected","NoOfRows","NumFields",
            "ErrorHandlingText"])


    return sort_df.drop_duplicates()


#
#
#
# if __name__ == "__main__":
#     file_input = "08_Belvidere_Data_Normalization for Mendix V6.yxmd"
#     filename = os.path.abspath(os.path.join(file_input))
#     crossTab(filename).to_csv("CrossTab_mendix_v6_new.csv",index=False)
#
# # print("--- %s seconds ---" % (time.time() - start_time))
#
