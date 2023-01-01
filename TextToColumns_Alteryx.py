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

def TextToColumns(filename):
    df=pd.DataFrame()
    tree = ET.parse(filename)
    for i in tree.iter():
        if(i.tag=='Node'): 
            ToolID=i.attrib.get("ToolID")
            if(len(list(filter(lambda x:x.tag=='GuiSettings',list(i.iter()))))>0):
                ss=filter(lambda x:x.tag=='GuiSettings',list(i.iter()))
                result=list(ss)
                plugin=result[0].attrib.get("Plugin")
                if(str(plugin)!='None' and 'TextToColumns' in plugin):
                    if(len(list(filter(lambda x:x.tag=='EngineSettings',list(i.iter()))))>0):
                        ss=filter(lambda x:x.tag=='EngineSettings',list(i.iter()))
                        result=list(ss)
                        EngineDll=result[0].attrib.get("EngineDll")
                        displaymode=result[0].attrib.get("DisplayMode")
                        EngineDllEntryPoint=result[0].attrib.get("EngineDllEntryPoint")
                    if(len(list(filter(lambda x:x.tag=='Annotation',list(i.iter()))))>0):
                        ss=filter(lambda x:x.tag=='Annotation',list(i.iter()))
                        result=list(ss)
                        Annotation_Value=result[0].attrib.get("DisplayMode")
                    if(len(list(filter(lambda x:x.tag=='DefaultAnnotationText',list(i.iter()))))>0):
                        ss=filter(lambda x:x.tag=='DefaultAnnotationText',list(i.iter()))
                        result=list(ss)
                        DefaultAnnotationText_Value=result[0].text
                    for j in i.iter():
                        if(j.tag=='Position'):
                            x_pos=j.attrib.get("x")
                            y_pos=j.attrib.get("y")
                        elif(j.tag=='NumFields'):
                            no_of_fields=j.attrib.get("value")
                        elif(j.tag=='ErrorHandling'):
                            ErrorHandling_text=j.text
                        elif(j.tag=='RootName'):
                            RootName_text=j.text
                        elif(j.tag=='Delimeters'):
                            Delimeters_value=j.attrib.get("value")
                        elif(j.tag=='Flags'):
                            Flag_value=j.attrib.get("value")
                            df=df.append(pd.DataFrame({
                                                    'Filename':filename.rsplit('/')[-1].replace('.XML',''), 
                                                    'ToolID': ToolID,
                                                    'Plugin': plugin,
                                                    'FieldName':str(RootName_text),
                                                    'Rename_or_Destination':str(Rename_or_Destination),
                                                    'CreateFieldName':str(CreateFieldName),
                                                    'UpdateFieldName':str(UpdateFieldName),
                                                    'LeftJoinField':str(LeftJoinField),
                                                    'RightJoinField':str(RightJoinField),
                                                    'Expression_1':str(Expression_1),
                                                    'Expression_2':str(Delimeters_value),
                                                    'Expression_3':str(Flag_value),
                                                    'GroupBy':str(GroupBy),
                                                    'SortOrder':str(SortOrder),
                                                    'UpdateField':str(UpdateField),
                                                    'MultifileValue':str(MultifileValue),
                                                    'HeaderField':str(HeaderField),
                                                    'DataField':str(DataField),
                                                    'IsSelected':str(IsSelected),
                                                    'NoOfRows':str(NoOfRows),
                                                    'NumFields':str(no_of_fields),
                                                    'ErrorHandlingText':str(ErrorHandling_text),
                                                                    }, index=[0]))
    df.fillna(value=pd.np.nan, inplace=True)
    df=df.replace(np.NaN,"")

    return df

