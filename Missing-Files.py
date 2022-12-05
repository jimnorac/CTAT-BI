#  Analyze list of subfolders to find missing files using date in file name between selected date range
#  File format   date in the file name eg AAA-2022-11-09-P.csv  = YYYY-MM-DD
#  Folder format C:\CTAT_BI\Position\AAA\files     AAA = subfolder check for match in list site  [AAA BBB CCC]
import os
from datetime import date,datetime,timedelta

DriveIn = 'Z'                       # Drive to check
DriveOut = 'C'                      # Drive to place output file = DriveOut:\CTAT_BI\_Missing_Files.txt
Search_Folder = "Position"          # History or Position
start_date = "1/1/2019"             # end_date = "11/30/2099"

site = ['A11','A80','A90','ABE','ABI','ABQ','ACT','ACY','AGS','ALB','ALO','AMA','ASE','AUS','AVL','AVP','AZO','BFL','BGM','BGR','BHM','BIL','BIS','BNA','BOI','BTR','BTV',\
        'BUF','C90','CAE','CHA','CHS','CID','CKB','CLE','CLT','CMH','CMI','COS','CPR','CRP','CRW','CVG','D01','D10','D21','DAB','DLH','DSM','ELM','ELP','EUG','EVV','F11',\
        'FAI','FAR','FAT','FAY','FLO','FSD','FSM','FWA','GEG','GGG','GPT','GRB','GSO','GSP','GTF','HSV','HTS','HUF','I90','ICT','ILM','IND','JAX','L30','LBB','LCH','LEX',\
        'LFT','LIT','M03','M98','MAF','MCI','MDT','MGM','MIA','MKE','MLI','MLU','MOB','MSN','MSY','MWH','MYR','N90','NCT','OKC','ORF','P31','P50','P80','PCT','PHL','PIT',\
        'PVD','PWM','R90','RDG','RDU','RFD','ROA','ROC','ROW','RST','RSW','S46','S56','SAT','SAV','SBA','SBN','SCT','SDF','SGF','SHV','SUX','SYR','T75','TLH','TOL','TPA',\
        'TRI','TUL','TYS','U90','Y90','YNG']
i = int(0)                                                                      # counter check each facility in list site
x = int(0)                                                                      # counter between days
start = datetime.strptime(start_date,'%m/%d/%Y').date()                         # convert string start_date to date time
loop_start = start                                                              # copy start to loop_start for first facility
end = datetime.today().date() - timedelta(2)                                    # end date todays's date - 2 days  
day_dif = abs((end-start).days)                                                 # number of day to check

with open(DriveOut+":\CTAT_BI\_Missing_Files.txt",'w') as outfile:              # open output file
    while i < len(site):                                                        # counter to check each facility in list site
        in_path = DriveIn+":/CTAT_BI/"+Search_Folder+"/{}/".format(site[i])     # set path for facility using site[i]
        os.chdir(in_path)                                                       # change to facility folder
        file_list= []                                                           # build empty list to hold dates from file names in folder
        for in_file in os.listdir():                                            # loop through each file in folder
            csv_file,extension = os.path.splitext(in_file)                      # split file name from extenstion
            file_date = csv_file[4]+csv_file[5]+csv_file[6]+csv_file[7]+"-"+csv_file[9]+csv_file[10]+"-"+csv_file[12]+csv_file[13]
            file_list.append(file_date)                                         # put YYYY-MM-DD from each file in folder in file_list    
        x=0                                                                     # set between start end date counter
        while x < day_dif:                                                      # counter less than integer days between start and end
            if str(loop_start) not in file_list:                                # if start date not in derived date list from file name
                file_string =site[i]+"  Missing Dates > "+str(loop_start)+"\n"  # if missing build string to put in oputput file
                outfile.write(file_string)                                      # Write string with Missing date to output file
                print(site[i],"  Missing Dates > ",loop_start)                  # Display Missing date on screen
            loop_start += timedelta(1)                                          # increment loop_start by one day
            x  += 1                                                             # increment date counter
        i +=1                                                                   # increment site counter
        loop_start = start                                                      # set loop_start back to start for next site loop
print("Done")    