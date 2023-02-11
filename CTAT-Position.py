# CTAT-Position   Version 2022-12-04

import pandas as pd
import time
import os
from datetime import datetime,date,timedelta
from CTAT_BI_Functions import (get_eTime, get_hour,get_airport,get_position,get_eTime,get_hh_mm,get_LTime,get_LTime2)

DriveIn = "D"                              # DriveIn   FTP\AcHistory-XXX
DriveOut = "D"                             # DriveOut  CTAT_BI\Position-XXX
b_days=int(3)                              # default b_days value                            
#base_name = "File Modified Date"          # default base_name option is File Modified Date  
base_name = "Date in the File Name"        # Use this one when creating baseline to start from date in file name not the file modified date

header_names = ['Callsign','Date','Time','UTC_Date','UTC_Time','Category','Type','Msg','Rules','Airport','Alt','Bcn','Scr1','Scr2','ADE','Psn','Position','APO','Twr',\
                'Rdr','Area','Airspace','Entry','Exit','Hdg','Spd','RY','WC','TA','X','Y','Fnct','S1','S2','S3','F1','F2','X2','AA','CM','M8','M9','M2','sTime','eTime',\
                'eTime2','60Min','30Min','15Min','Year','Month','Day','Leg','Leg_Time','Leg_Time2','hTime','hTime2','end60','end30','end15']

site = ['A11','A80','A90','ABE','ABI','ABQ','ACT','ACY','AGS','ALB','ALO','AMA','ASE','AUS','AVL','AVP','AZO','BFL','BGM','BGR','BHM','BIL','BIS','BNA','BOI','BTR','BTV',\
        'BUF','C90','CAE','CHA','CHS','CID','CKB','CLE','CLT','CMH','CMI','COS','CPR','CRP','CRW','CVG','D01','D10','D21','DAB','DLH','DSM','ELM','ELP','EUG','EVV','F11',\
        'FAI','FAR','FAT','FAY','FLO','FSD','FSM','FWA','GEG','GGG','GPT','GRB','GSO','GSP','GTF','HSV','HTS','HUF','I90','ICT','ILM','IND','JAN','JAX','L30','LBB','LCH',\
        'LEX','LFT','LIT','M03','M98','MAF','MCI','MDT','MGM','MIA','MKE','MLI','MLU','MOB','MSN','MSY','MWH','MYR','N90','NCT','OKC','ORF','P31','P50','P80','PBI','PCT',\
        'PHL','PIT','PVD','PWM','R90','RDG','RDU','RFD','ROA','ROC','ROW','RST','RSW','S46','S56','SAT','SAV','SBA','SBN','SCT','SDF','SGF','SHV','SUX','SYR','T75','TLH',\
        'TOL','TPA','TRI','TUL','TYS','U90','Y90','YNG']
site = ['A11','N90','PWM']


lsite = len(site)

#  Comment this out to eliminate User input   select Number of Days and/or Single Site
# ###############################################################################################################
# while True:
#   try:  
#     x_days = int(input("Select Enter to process 3 Days       or    Enter the Number of Back Days to process:  " ))
#     if x_days >=1 and x_days <= 1500:
#       b_days = int(x_days)
#       break
#   except:
#     break
   
# while True:
#   try:  
#     xsite = (input("Select Enter to process ALL Sites    or    Enter the 3 alpha/numeric site ID:          " ))        
#     if len(xsite) == 3:   
#       site = [xsite[0]+xsite[1]+xsite[2]]
#       lsite = 0  
#       break
#   except:
#     brea
#   else:
#     break
# #################################################################################################################

i=int(0)                                                                           # set counter to zero to look at all facilities
t_start = datetime.today()                                                  # Date for screen output to track processing
t_processing =datetime.today().strftime("%H:%M:%S")                         # Start Time
t_date = datetime.today().strftime("%m-%d-%y")                              # Start Date
start_processing = "{}          Processing >  {}".format(t_processing,site) # Start Time processing selected site
print("\n\n")                                                             # TESTING clean display screen
print(f"InPath > {DriveIn}:\FTP\AcHistory     OutPath > {DriveOut}:\CTAT_BI\Position\  ")
print(f"Processing >> {lsite} site(s)  Files within >> {b_days} day(s) of >>> {base_name}\n")
# print(site)
print("\nFacility    Start Time          End Time             Elapsed            Progress")
#print("\nFacility    Start Time          End Time             Elapsed            Progress      Processing File")
#        print(f"{site[i]}         {s_time}                                                           {in_file} ",end='\r')
while i < len(site):  
    s_site = datetime.today()                                               # load current date time
    s_time =s_site.strftime("%H:%M:%S.%f")                                  # strip time in H:M:S.f for print display
    in_path = DriveIn+":/FTP/AcHistory/{}/".format(site[i])                 # Input Data path 
    out_path = DriveOut+":/CTAT_BI/Position/{}/".format(site[i])            # Output data path  
    back_date = date.today() - timedelta(b_days)                            # days to process timedelta(b_days) = value from`` last b_days default
    os.chdir(in_path)                                                       # Load each file in identified in site folder
    for in_file in os.listdir():                                        # eg FAR_CountOps_AcHistory_2022-09-06_Lcl.csv  s
      csv_file,extension = os.path.splitext(in_file)                    #    |||                    |||| || ||  < strip file name from extension shown below
      FAC = csv_file[0]+csv_file[1]+csv_file[2]                         #    FAR                    |||| || ||  < Facility ID 
      zyear = csv_file[23]+csv_file[24]+csv_file[25]+csv_file[26]       #                           2022 || ||  < load into data frame df['Year']
      zmonth = csv_file[28]+csv_file[29]                                #                                09 ||  < Load into data frame df['Month']
      zday = csv_file[31]+csv_file[32]                                  #                                   06  < Use to build zdate
      zdate = zmonth+'-'+zday+'-'+zyear                                 # 09-06-2022                            < Date from File name
      out_file = FAC+'-'+zyear+'-'+zmonth+'-'+zday+'_P.csv'             # FAR-2022-09-06_D.csv                  < Output file name.csv
      file_date = datetime.strptime(zdate, "%m-%d-%Y").date()           # 09-06-2022                            < convert from string to date type to compare if file should be processed
      zmonth = file_date.strftime('%b')                                 # convert zmonth to Mmm format          < Load into data frame df['Day']
      zday =file_date.strftime('%a')                                    # convert zday to Day of Week           < Load into data frame df['Day']
      m_time =os.path.getmtime(in_file)                                 # get modified date time of input file float
      m_time_s = str(datetime.fromtimestamp(m_time))                    # convert modified date time from float to datetime then to string
      myear = m_time_s[0]+m_time_s[1]+m_time_s[2]+m_time_s[3]           # extract when File was modified Year
      mmonth = m_time_s[5]+m_time_s[6]                                  #                                Month
      mday = m_time_s[8]+m_time_s[9]                                    #                                Day of Week     
      mdate = mmonth+'-'+mday+'-'+myear                                 # string mm-dd-yyyy
      m_date = datetime.strptime(mdate, "%m-%d-%Y").date()              # date class YYYY-MM-DD      
      base_date = m_date                                                # account for loading base_date using either file modified data or date stripped from file name
      if base_name == "Date in the File Name":                          # set the print screen to display the type base date selected
        base_date = file_date    
      if base_date >= back_date:                                        # Continue when file or modified date is not more that b_days before current date  
            with open(in_file, 'r') as csv_file:                           # read all files that passed date check from if file_date or modified  >= back_date:                
                df = pd.read_csv(csv_file,header=None,skiprows=1,names=header_names,low_memory=False)
                df.dropna(axis='index',how = 'any', subset=['Callsign','Category','Rules', 'ADE'],inplace = True)    # drop row with Na or NaN in Callsign Category Rules or ADE          
                df['sTime'] = df['Time']                                      # Load Data Frame sTime with Time
                df['Year'] = zyear                                            #
                df['Month'] = zmonth                                          #
                df['Day'] = zday                                              #
                df['Airport'] = df['Airport'].apply(get_airport)              # If Airport OVR change to period
                df['Position'] = df['Psn'].apply(get_position)                # Prepare for filter identfy TRACON positions single charcter and when right most chacter is a C to period
                df['60Min'] = df['Time'].apply(get_hour)                      # Function   Strip hour from sTime
                      
                df['xTime'] = pd.to_datetime(df['Time'])
                df['xMin'] = df['xTime'].dt.floor('30T')
                df['30Min'] = df['xMin'].dt.strftime("%H:%M")
                df['x30'] = df['30Min'].apply(get_eTime)
                
                df['xMin'] = df['xTime'].dt.floor('15T')
                df['15Min'] = df['xMin'].dt.strftime("%H:%M")
                df['x15'] = df['15Min'].apply(get_eTime)

                df['Position'] = df['Psn'].apply(get_position)                # Prepare for filter identfy TRACON positions single charcter and when right most chacter is a C to period
                df.sort_values(by=['Callsign','Date','sTime'],inplace=True)   # Sort Data Frame
                df['hTime'] = df['Time'].shift(1).apply(get_eTime)            # get absolute value of time in row above
                df['M8'] = ((df['Callsign']!=df['Callsign'].shift()) | (df['Psn']!=df['Psn'].shift()) | ((df['ADE']!=df['ADE'].shift()) &  (df['ADE']!='E')  &  (df['ADE'].shift()!='E')) | (df['Msg'].shift(1)=="TRM"))
                df['M9'] = ((df['Callsign'] == df['Callsign'].shift()) & (df['Position'] == '.')  &  (df['Position'].shift() != '.') & ((df['ADE'] == 'D')  &  (df['ADE'].shift() == 'D')))
                df.iloc[-1,0] = 'X'                                                                                   # Set Callsing[-1] last row to 'X' to hold eTime before filter
                zfilter= (df['M8'] == True ) | (df['Callsign'] == 'X')
                df = df[zfilter]                                                                                      # KEEP just rows that met conditions and remove not needed columns
                df['M2'] = ((df['Callsign'] == df['Callsign'].shift(-1)) & ((df['Position'] != '.')  &  (df['Position'].shift(1) == '.'))  & ((df['ADE'] == 'D')  &  (df['ADE'].shift(-1) == 'D')))
                df['hTime2'] = df['hTime'].shift(-1).apply(get_eTime)                                                 # get absolute value of time in row above
                df['eTime'] = df['hTime'].shift(-1).apply(get_eTime)                                                  # After filter get end time from hTime
#                df['eTime2'] = df['hTime2'].shift(-1).apply(get_eTime)
                df['eTime2'] = ''                
                df['end60'] = df['eTime'].apply(get_hour)                           # Function   Strip hour from sTime    df['60Min'] = df['Time'].apply(lambda x: str(x).split(":",1)[0])    # Lambda     Strip hour from sTime

                df['xTime'] = pd.to_datetime(df['Time'])
                df['xMin'] = df['xTime'].dt.floor('30T')
                df['end30'] = df['xMin'].dt.strftime("%H:%M")
                                
                df['xMin'] = df['xTime'].dt.floor('15T')
                df['end15'] = df['xMin'].dt.strftime("%H:%M")
                df['x15'] = df['15Min'].apply(get_eTime)
                
                df.drop(columns=['UTC_Date','UTC_Time','Msg','Alt','Bcn','Scr1','Scr2','APO','Twr','Rdr','Area','Airspace','Entry','Exit','Hdg','Spd','RY','WC','TA','X','Y','S1','S2','S3','F1','F2','X2','Fnct','AA','CM'],inplace = True)
                df.drop(df.tail(1).index,inplace=True)                                                                # Drop last row
                df['Leg'] = 1                                                                                         # Set to 1 to identify Number of Legs not Buckets
                LTime = ((pd.to_datetime(df['eTime'])) -(pd.to_datetime(df['sTime'])))
                df['Leg_Time'] = LTime.apply(get_LTime)
#                LTime2 = ((pd.to_datetime(df['eTime2'])) -(pd.to_datetime(df['sTime'])))
#                df['Leg_Time2'] = LTime2.apply(get_LTime2)
                df['Leg_Time2'] =''
                df.drop(columns=['M8','M9','hTime','hTime2'],inplace = True)
                zfilter= (df['Position'] != '.')
                df = df[zfilter]             
###########################################################   BUCKET LOGIC
                x=0
                while x < len(df):
                    try:
                        end_60 = datetime.strptime((str(df.iloc[x,12])),'%H:%M:%S')
                    except:
                        end_60 = ""
                    try:
                        end_30 = datetime.strptime((str(df.iloc[x,12])),'%H:%M:%S')
                    except:
                        end_30 = ""
                    try:
                        end_15 = datetime.strptime((str(df.iloc[x,12])),'%H:%M:%S')
                    except:
                        end_15= ''
                    try:
                        start_60 = datetime.strptime((str(df.iloc[x,14])),'%H') + timedelta(minutes = 60)
                    except:
                        start_60 = end_60
                    try:
                        start_30 = datetime.strptime((str(df.iloc[x,15])),'%H:%M') + timedelta(minutes = 30)
                    except:
                        start_30 = end_30
                    try:
                        start_15 = datetime.strptime((str(df.iloc[x,16])),'%H:%M') + timedelta(minutes = 15)
                    except:
                        start_15 = end_15
                    x60Min =''
                    x30Min = ''
                    x15Min =''

                    if ((df.iloc[x,10]) == False):                      # If M2 is False then row is not an eTime2 or Leg_Time2 row
                        df.iloc[x,13] = ""                              # eTime2    NULL
                        df.iloc[x,22] = ""                              # Leg_Time2 NULL
                    else:
                        df.iloc[x,22] =(str(df.iloc[x,22])[-10:-2])     # Change Leg_Time2 to string H:MM:SS format
          
                    z=0
                    while z< 50:                                        # APPEND A NEW ROW
                        x60Min =''
                        x30Min = ''
                        x15Min =''
                        if (start_60)  <= (end_60):
                            load_60 = str(start_60)
                            x60Min = str(load_60[-8:-6])

                        if (start_30)  <= (end_30):
                            load_30 = str(start_30)
                            x30Min = str(load_30[-8:-3])

                        if (start_15)  <= (end_15):
                            load_15 = str(start_15)
                            x15Min = str(load_15[-8:-3])
                        
                        if ((start_60 < end_60) |  (start_30 < end_30) | (start_15 < end_15)):                    
                            
                            xCallsign  = df.iloc[x,0]
                            xDate = df.iloc[x,1]
                            xTime = df.iloc[x,2]
                            xCategory = df.iloc[x,3]
                            xType = df.iloc[x,4]
                            xRules = df.iloc[x,5]
                            xAirport = df.iloc[x,6]
                            xADE = df.iloc[x,7]
                            xPsn = df.iloc[x,8]
                            xPosition = df.iloc[x,9]
                            xM2 = ""
                            xsTime = df.iloc[x,11]
                            xeTime = df.iloc[x,12]
                            xeTime2 = ""
                            xYear = df.iloc[x,17]
                            xMonth = df.iloc[x,18]
                            xDay = df.iloc[x,19]
                            xLeg = ""
                            xLeg_Time = ""
                            xLeg_Time2 = ""
                            xend60 = df.iloc[x,23]
                            xend30 = df.iloc[x,24]
                            xend15 = df.iloc[x,25]
                            dict = {'Callsign' : [xCallsign],'Date':[xDate], 'Time':[xTime],'Category':[xCategory],'Type':[xType],'Rules':[xRules],'Airport':[xAirport],'ADE':[xADE],'Psn':[xPsn],'Position':[xPosition],'M2':[xM2],'sTime':[xsTime],'eTime':[xeTime],'eTime2':[xeTime2],'60Min':[x60Min],'30Min':[x30Min],'15Min':[x15Min],'Year':[xYear],'Month':[xMonth],'Day':[xDay],'Leg':[xLeg],'Leg_Time':[xLeg_Time],'Leg_Time2':[xLeg_Time2],'end60':[xend60],'end30':[xend30],'end15':[xend15]}
                            df2 = pd.DataFrame.from_dict(dict)
                            frames = [df,df2]
                            result = pd.concat(frames)
                            df = result
                            z=z+1
                            start_60 = start_60 + timedelta(minutes=60) 
                            start_30 = start_30 + timedelta(minutes=30)
                            start_15 = start_15 + timedelta(minutes=15)
                            x=x+1  
                        else:
                            z=1000                         
                            x=x+1                    
######################################################################################
            df.drop(columns=['M2','Psn','end60','end30','end15'],inplace = True)
            new_df= df[['Callsign','Category','Type','Rules','Airport','ADE','Position','Date','sTime','eTime','60Min','30Min','15Min','Leg_Time','Leg','Year','Month','Day','eTime2','Leg_Time2']]
            if len(new_df) >= 1:                                # Do not create file if just header and no data
                new_df.to_csv(out_path+out_file,index=False)    # Copy DataFrame to DiveOut format XXX-YYYY-MM-DD-P.csv            
    e_site = datetime.today()
    e_time =e_site.strftime("%H:%M:%S.%f")
    dif_time = e_site - s_site
    dif_time.total_seconds()
    print(f"{site[i]}         {s_time}     {e_time}      {dif_time}     {i+1}   {len(site)}")
#    print(f"{site}         {s_time}     {e_time}      {dif_time}\n\n")
    i=i+1
t_end = datetime.today()
t1 =t_start.strftime("%H:%M:%S")
t2 =t_end.strftime("%H:%M:%S")
t_dif = t_end - t_start
t_dif = (str(t_dif))[:-4]
print("___________________________________________________________________________________________")
print("Total Time ",t1,"          ",t2,"           ",t_dif,"\n\n")
