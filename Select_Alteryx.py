import xml.etree.ElementTree as ET
import csv
import os
import pandas as pd
import numpy as np


FieldName=''
Rename_or_Destination=''
CreateFieldName=''
UpdateFieldName=''
LeftJoinField=''
LeftJoinField=''
RightJoinField=''
Expression_1=''
Expression_2=''
Expression_3=''
GroupBy=''
SortOrder=''
UpdateField=''
MultifileValue=''
HeaderField=''
DataField=''
IsSelected=''
NoOfRows=''
NumFields=''
ErrorHandlingText=''


def AlteryxSelect(filename):
    df=pd.DataFrame()
    tree = ET.parse(filename)
    for i in tree.iter():
        if(i.tag=='Node'): 
            ToolID=i.attrib.get("ToolID")
            if(len(list(filter(lambda x:x.tag=='GuiSettings',list(i.iter()))))>0):
                ss=filter(lambda x:x.tag=='GuiSettings',list(i.iter()))
                result=list(ss)
                plugin=result[0].attrib.get("Plugin")
                if(str(plugin)!='None' and 'AlteryxSelect' in plugin):
                    if(len(list(filter(lambda x:x.tag=='EngineSettings',list(i.iter()))))>0):
                        ss=filter(lambda x:x.tag=='EngineSettings',list(i.iter()))
                        result=list(ss)
                        EngineDll=result[0].attrib.get("EngineDll")
                        displaymode=result[0].attrib.get("DisplayMode")
                        EngineDllEntryPoint=result[0].attrib.get("EngineDllEntryPoint")
                    if(len(list(filter(lambda x:x.tag=='OrderChanged',list(i.iter()))))>0):
                        ss=filter(lambda x:x.tag=='OrderChanged',list(i.iter()))
                        result=list(ss)
                        OrderChanged_Value=result[0].attrib.get("value")
                    if(len(list(filter(lambda x:x.tag=='CommaDecimal',list(i.iter()))))>0):
                        ss=filter(lambda x:x.tag=='CommaDecimal',list(i.iter()))
                        result=list(ss)
                        CommaDecimal_Value=result[0].attrib.get("value")
                    if(len(list(filter(lambda x:x.tag=='Annotation',list(i.iter()))))>0):
                        ss=filter(lambda x:x.tag=='Annotation',list(i.iter()))
                        result=list(ss)
                        Annotation_Value=result[0].attrib.get("DisplayMode")
                    if(len(list(filter(lambda x:x.tag=='DefaultAnnotationText',list(i.iter()))))>0):
                    
                        ss=filter(lambda x:x.tag=='DefaultAnnotationText',list(i.iter()))
                        result=list(ss)
                        DefaultAnnotationText_Value=result[0].text
                    for j in i.iter():
                        #print(j.tag)
                        if(j.tag=='Position'):
                            x_pos=j.attrib.get("x")
                            y_pos=j.attrib.get("y")
                    ss=filter(lambda x:x.tag=='SelectField',list(i.iter()))
                    result=list(ss)
                    
                    for data_index in range(0,len(result)):
                        field_name=result[data_index].attrib.get("field")
                        field_isselected=result[data_index].attrib.get("selected")
                        field_renamed=result[data_index].attrib.get("rename")
                        df=df.append(pd.DataFrame({'Filename':filename.rsplit('/')[-1].replace('.XML',''),  
                                                   'ToolID': ToolID,
                                                    'Plugin': plugin,                   
                                                    'FieldName':str(field_name),
                                                    'Rename_or_Destination':str(field_renamed),
                                                    'CreateFieldName':str(CreateFieldName),
                                                    'UpdateFieldName':str(UpdateFieldName),
                                                    'LeftJoinField':str(LeftJoinField),
                                                    'RightJoinField':str(RightJoinField),
                                                    'Expression_1':str(Expression_1),
                                                    'Expression_2':str(Expression_2),
                                                    'Expression_3':str(Expression_3),
                                                    'GroupBy':str(GroupBy),
                                                    'SortOrder':str(SortOrder),
                                                    'UpdateField':str(UpdateField),
                                                    'MultifileValue':str(MultifileValue),
                                                    'HeaderField':str(HeaderField),
                                                    'DataField':str(DataField),
                                                    'IsSelected':str(field_isselected),
                                                    'NoOfRows':str(NoOfRows),
                                                    'NumFields':str(NumFields),
                                                    'ErrorHandlingText':str(ErrorHandlingText),

                                                                                        }, index=[0]))

    df.fillna(value=pd.np.nan, inplace=True)
    df=df.replace(np.NaN,"")

    return df
