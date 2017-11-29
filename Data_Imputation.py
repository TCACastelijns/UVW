# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 11:19:07 2017

@author: s157084
"""
import pandas as pd
import numpy as np




#Inpute Sessions ID values

def impute_sessionsID_NA(df,time_Session_min = 15):
    """
    Impute values of Sessions ID that are empty. It takes into consideration the complete time and start time of two between two activities tofill forward
    
    :param 
        df = data frame
        time_Session_min = min time between two activities to be considered part of the same session
        
    :return: df_imputed
    """
    users = df['case'].unique()
    control = 0
    count_input = 0
    esp_cases = ['File Complaint', 'Question', 'Werkmap message']
    for user in users:
        temp_df = df[df['case'] == user]
        #only for even_log that
        if (temp_df['sessionid'].isnull().sum() >1):
            if time_Session_min == np.inf:
                temp_df['sessionid'] = temp_df['sessionid'].fillna(method='ffill')
                
            else:
                for t in range(1,len(temp_df)):
                    event_time_min = (temp_df['startTime'].iloc[t] - temp_df['completeTime'].iloc[t - 1]).total_seconds() / 60
                    if((event_time_min < time_Session_min) | (temp_df['event'].iloc[t] in esp_cases)) & (pd.isnull(temp_df['sessionid'].iloc[t])):
                        temp_df['sessionid'].iloc[t] = temp_df['sessionid'].iloc[t-1]
                        count_input = count_input+1
                        print(count_input)
             
        if control == 0:
            df_ans = temp_df
            control = 1
        else:
            df_ans = pd.concat([df_ans,temp_df],axis=0)
    text = str(count_input) + ' has been imputed values '        
    print(text)
    return df_ans
    

#Read the data
df=pd.read_csv('Log.csv')
df['startTime'] = pd.to_datetime(df['startTime'])
df['completeTime'] = pd.to_datetime(df['completeTime'])
df['event_time_min'] = (df['completeTime'] - df['startTime']).dt.total_seconds() / 60

#Call the impute funtion
df_ans = impute_sessionsID_NA(df.copy())
df_ans.to_csv('Data/log_imputed_complete.csv',index=False)  
df_ans = df_ans[(pd.isnull(df_ans['sessionid']) == False)]  
df_ans.to_csv('Data/log_imputed.csv',index=False)      
        
        
    
    
    

