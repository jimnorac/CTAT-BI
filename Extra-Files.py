#  Analyze list of subfolders to find Extra files in folder using date from file name when date is less than the selected date start
#  Folder format C:\CTAT_BI\Position\AAA\AAA-2022-11-09-P.csv     AAA = facility name as subfolder name   in list site  [AAA BBB CCC]
#  File format   AAA-2022-11-09_P.csv   strip YYYY MM DD         AAA = facility name in file name  _P for Position _D History 
import os
from datetime import datetime

DriveIn = 'Z'                       # Drive to check
DriveOut = 'C'                      # Drive to place output file = DriveOut:\CTAT_BI\_Missing_Files.txt
start_date = "1/1/2019"             # end_date = "11/30/2099"

site = ['A11','A80','A90','ABE','ABI','ABQ','ACT','ACY','AGS','ALB','ALO','AMA','ASE','AUS','AVL','AVP','AZO','BFL','BGM','BGR','BHM','BIL','BIS','BNA','BOI','BTR','BTV',\
        'BUF','C90','CAE','CHA','CHS','CID','CKB','CLE','CLT','CMH','CMI','COS','CPR','CRP','CRW','CVG','D01','D10','D21','DAB','DLH','DSM','ELM','ELP','EUG','EVV','F11',\
        'FAI','FAR','FAT','FAY','FLO','FSD','FSM','FWA','GEG','GGG','GPT','GRB','GSO','GSP','GTF','HSV','HTS','HUF','I90','ICT','ILM','IND','JAX','L30','LBB','LCH','LEX',\
        'LFT','LIT','M03','M98','MAF','MCI','MDT','MGM','MIA','MKE','MLI','MLU','MOB','MSN','MSY','MWH','MYR','N90','NCT','OKC','ORF','P31','P50','P80','PCT','PHL','PIT',\
        'PVD','PWM','R90','RDG','RDU','RFD','ROA','ROC','ROW','RST','RSW','S46','S56','SAT','SAV','SBA','SBN','SCT','SDF','SGF','SHV','SUX','SYR','T75','TLH','TOL','TPA',\
        'TRI','TUL','TYS','U90','Y90','YNG']

i = int(0)                                                                                                              # counter check each facility in list site   
start = datetime.strptime(start_date,'%m/%d/%Y').date()                                                                 # convert string start_date to date time
with open(DriveOut+":\CTAT_BI\_Extra_Files.txt",'w') as outfile:                                                        # open output file
    while i < len(site):                                                                                                # counter to check each facility in list site
        in_path = DriveIn+":/CTAT_BI/Position/{}/".format(site[i])                                                      # set path for facility using site[i]
        os.chdir(in_path)                                                                                               # change to facility folder
        for in_file in os.listdir():                                                                                    # loop through each file in folder
            csv_file,extension = os.path.splitext(in_file)                                                              # split file name from extenstion
            file_date = csv_file[4]+csv_file[5]+csv_file[6]+csv_file[7]+"-"+csv_file[9]+csv_file[10]+"-"+csv_file[12]+csv_file[13]
            zfile_date = datetime.strptime(file_date,'%Y-%m-%d').date()                                                 # load zfile_date with datetime extracted date
            if zfile_date < start:                                                                                      # compare is derived file_date less than start date
                file_string =site[i]+"  Extra Position Files > "+str(file_date)+"\n"                                    # if yes build string with extra date
                outfile.write(file_string)                                                                              # load extra date string to file
                print(site[i],"  Extra Position File  > ",file_date)                                                    # display extra date message
        i +=1                                                                                                           # incremenmt site counter     

    i = int(0)                                                                                                          # reset site counter to 0 to check History folder
    while i < len(site):                                                                                                # same logic as Position to check History subfolders
        in_path = DriveIn+":/CTAT_BI/History/{}/".format(site[i])
        os.chdir(in_path)
        for in_file in os.listdir():
            csv_file,extension = os.path.splitext(in_file)
            file_date = csv_file[4]+csv_file[5]+csv_file[6]+csv_file[7]+"-"+csv_file[9]+csv_file[10]+"-"+csv_file[12]+csv_file[13]
            zfile_date = datetime.strptime(file_date,'%Y-%m-%d').date()
            if zfile_date < start:    
                file_string =site[i]+"  Extra History Files  > "+str(file_date)+"\n"
                outfile.write(file_string)
                print(site[i],"  Extra History File  > ",file_date)
        i +=1 
print("Done")    