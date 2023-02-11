# CTAT-History.py    Version 2022-12-4 

import pandas as pd
import os
from datetime import datetime,date,timedelta,time
from CTAT_BI_Functions import (get_alpha,get_hour,get_airport,get_leading_zero)

DriveIn = "Z"                              # DriveIn   FTP\AcHistory-XXX
DriveOut = "E"                             # DriveOut  CTAT_BI\Position-XXX
b_days=int(3)                              # default b_days value                            
#base_name = "File Modified Date"          # default base_name option is File Modified Date  
base_name = "Date in the File Name"        # Use this one when creating baseline to start from date in file name not the file modified date

header_names = ['Callsign','Date','Time','UTC_Date','UTC_Time','Category','Type','Msg','Rules','Airport','Alt','Bcn','Scr1','Scr2','ADE','Position','APO','Twr','Rdr',\
                'Area','Airspace','Entry','Exit','Hdg','Spd','Runway','WC','TA','X','Y','Fnct','S1','S2','S3','F1','F2','X2','AA','CM','Year','Month','Day',"Hour",\
                'CSAlpha','Beacon']

site = ['A11','A80','A90','ABE','ABI','ABQ','ACT','ACY','AGS','ALB','ALO','AMA','ASE','AUS','AVL','AVP','AZO','BFL','BGM','BGR','BHM','BIL','BIS','BNA','BOI','BTR','BTV',\
        'BUF','C90','CAE','CHA','CHS','CID','CKB','CLE','CLT','CMH','CMI','COS','CPR','CRP','CRW','CVG','D01','D10','D21','DAB','DLH','DSM','ELM','ELP','EUG','EVV','F11',\
        'FAI','FAR','FAT','FAY','FLO','FSD','FSM','FWA','GEG','GGG','GPT','GRB','GSO','GSP','GTF','HSV','HTS','HUF','I90','ICT','ILM','IND','JAN','JAX','L30','LBB','LCH',\
        'LEX','LFT','LIT','M03','M98','MAF','MCI','MDT','MGM','MIA','MKE','MLI','MLU','MOB','MSN','MSY','MWH','MYR','N90','NCT','OKC','ORF','P31','P50','P80','PBI','PCT',\
        'PHL','PIT','PVD','PWM','R90','RDG','RDU','RFD','ROA','ROC','ROW','RST','RSW','S46','S56','SAT','SAV','SBA','SBN','SCT','SDF','SGF','SHV','SUX','SYR','T75','TLH',\
        'TOL','TPA','TRI','TUL','TYS','U90','Y90','YNG']
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
#     break
#   else:
#     break
# ###############################################################################################################    

i=int(0)                                                                    # set counter to zero to look at all facilities
t_start = datetime.today()                                                  # Date for screen output to track processing
t_processing =datetime.today().strftime("%H:%M:%S")                         # Start Time
t_date = datetime.today().strftime("%m-%d-%y")                              # Start Date
start_processing = "{}          Processing >  {}".format(t_processing,site) # Start Time processing selected site
print(f"\n\nInPath > {DriveIn}:\FTP\AcHistory     OutPath > {DriveOut}:\CTAT_BI")
print(f"Processing {lsite} site(s)  Files within {b_days} day(s) of {base_name}\n")
print(site)
print("\nFacility    Start Time          End Time             Elapsed            Progress")

while i < len(site):  
  s_site = datetime.today()                                           # load current date time
  s_time =s_site.strftime("%H:%M:%S.%f")                              # strip time in H:M:S.f for print display
  in_path = DriveIn+":/FTP/AcHistory/{}/".format(site[i])             # set variable with Input Data path 
  out_path = DriveOut+":/CTAT_BI/History/{}/".format(site[i])         # set variable with Output data path  
  back_date = date.today() - timedelta(b_days)                        # days to process timedelta(b_days) = value from`` last b_days default
  os.chdir(in_path)                                                   # Load each file in identified in site folder
  for in_file in os.listdir():                                        # eg FAR_CountOps_AcHistory_2022-09-06_Lcl.csv  s
    csv_file,extension = os.path.splitext(in_file)                    #    |||                    |||| || ||  < strip file name from extension shown below
    FAC = csv_file[0]+csv_file[1]+csv_file[2]                         #    FAR                    |||| || ||  < Facility ID 
    zyear = csv_file[23]+csv_file[24]+csv_file[25]+csv_file[26]       #                           2022 || ||  < load into data frame df['Year']
    zmonth = csv_file[28]+csv_file[29]                                #                                09 ||  < Load into data frame df['Month']
    zday = csv_file[31]+csv_file[32]                                  #                                   06  < Use to build zdate
    zdate = zmonth+'-'+zday+'-'+zyear                                 # 09-06-2022                            < Date from File name
    out_file = FAC+'-'+zyear+'-'+zmonth+'-'+zday+'_D.csv'             # FAR-2022-09-06_D.csv                  < Output file name.csv
    file_date = datetime.strptime(zdate, "%m-%d-%Y").date()           # 09-06-2022                            < string to date type compare if file should be processed
    zmonth = file_date.strftime('%b')                                 # convert zmonth to MMM format          < Load into data frame df['Day']
    zday =file_date.strftime('%a')                                    # convert zday to Day of Week           < Load into data frame df['Day']
    m_time =os.path.getmtime(in_file)                                 # get file modified date time of input file as a float
    m_time_s = str(datetime.fromtimestamp(m_time))                    # convert modified date time from float to datetime then to string
    myear = m_time_s[0]+m_time_s[1]+m_time_s[2]+m_time_s[3]           # extract when File was modified Year
    mmonth = m_time_s[5]+m_time_s[6]                                  #                                Month
    mday = m_time_s[8]+m_time_s[9]                                    #                                Day of Week     
    mdate = mmonth+'-'+mday+'-'+myear                                 # string mm-dd-yyyy
    modified_date = datetime.strptime(mdate, "%m-%d-%Y").date()       # date class YYYY-MM-DD
    base_date = modified_date                                         # set base_date to file modified data
    if base_name == "Date in the File Name":                          # switch between date in file name and file modified date   base_name flag at top of script
      base_date = file_date                                           # 
    if base_date >= back_date:                                        # Continue when file or modified date is not more than b_days before current date  
      with open(in_file, 'r') as csv_file:                            # read all Folder files that pass date check
          df = pd.read_csv(csv_file,header=None,skiprows=1,names=header_names,low_memory=False)  # WARNING APPEARS problem with low_memory for large sites
          df.dropna(axis='index',how = 'any', subset=['Callsign','Category','Rules', 'ADE'],inplace = True)    # drop row with Na or NaN in Callsign Category Rules or ADE          
          df['Year'] = zyear                                          # Data Frame load Year                     need better solution than don't display warning option
          df['Month'] = zmonth                                        #                 Month
          df['Day'] = zday                                            #                 Day of Week
          df['Beacon'] = df['Bcn'].apply(get_leading_zero)            #                 Beacon as 4 character string with leading zeros
          df['Hour'] = df['Time'].apply(get_hour)                     #                 Hour as Integer
          df['CSAlpha'] = df['Callsign'].apply(get_alpha)             #                 Leading Alha from callsign
          df['Airport'] = df['Airport'].apply(get_airport)            #                 3 character aiport but change OVR to dot (.)
          df.drop(columns=['UTC_Date','UTC_Time','Alt','Bcn','APO','Hdg','Msg','Spd','WC','TA','X','Y','S3','F1','F2','X2','Fnct','AA','CM'],inplace=True)             
        
          zfilter= (df['Twr']=='A') | (df['Twr']== 'C') | (df['Twr'] == 'E') | (df['Twr']=='F') | (df['Twr']== 'G') | \
                   (df['Rdr']=='A') | (df['Rdr']== 'B') | (df['Rdr'] == 'C') | (df['Rdr']=='E') | (df['Rdr']== 'G') | (df['Rdr']=='H') | (df['Rdr']== 'I') | \
                   (df['Rdr']=='K') | (df['Rdr']=='M') | (df['Rdr']=='O')| \
                   (df['Area']=='A') | (df['Area']=='B') | (df['Area'] == 'C') | (df['Area']=='E') | (df['Area']== 'G') | (df['Area']=='H') | (df['Area']== 'I') | \
                   (df['Area']=='K') | (df['Area']=='M') | (df['Area']=='O')
          df1 = df[zfilter]                                           # keep only rows where at least one count column TWR RDR or Area is not Null
          if len(df1) >= 1:                                           # only create file that have data beyond the header (can cause Power BI issues)
            df1.to_csv(out_path+out_file,index=False)                 # ouput prepped and written to csv file
  s_time =s_site.strftime("%H:%M:%S.%f")                              # Start Time processing Facility folder s_site set when entering Folder (line 22)
  e_site = datetime.today()                                           # End   Time processing Facility folder
  e_time =e_site.strftime("%H:%M:%S.%f")    
  dif_time = e_site - s_site                                          # Elapsed time processing facility folder
  dif_time.total_seconds()    
  print(site[i],"       ",s_time,"   ",e_time,"    ",dif_time,"   ",i+1," of ",len(site),)
  i=i+1
t_end = datetime.today()
t1 =t_start.strftime("%H:%M:%S")                                      # Time Stamp for complete process
t2 =t_end.strftime("%H:%M:%S")
t_dif = t_end - t_start
t_dif = (str(t_dif))[:-4]
print("______________________________________________________________________________________")
print("Total      ",t1,"          ",t2,"           ",t_dif, "        END")