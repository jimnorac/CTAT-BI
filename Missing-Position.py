# Find missing files between dates / file contains a date in the file name eg CCC-2022-11-09-P.csv
# Folder C:\CTAT_BI\Position\AAA\CCC-2022-11-09-P.csv     AAA = subfolders  in list site  [AAA BBB CCC]
import os
from datetime import date,datetime,timedelta

DriveIn = 'Z'
start_date = "1/1/2019"     # end_date = "11/30/2099"

site = ['A11','A80','A90','ABE','ABI','ABQ','ACT','ACY','AGS','ALB','ALO','AMA','ASE','AUS','AVL','AVP','AZO','BFL','BGM','BGR','BHM','BIL','BIS','BNA','BOI','BTR','BTV','BUF','C90','CAE','CHA','CHS','CID','CKB','CLE','CLT','CMH','CMI','COS','CPR','CRP','CRW','CVG','D01','D10','D21','DAB','DLH','DSM','ELM','ELP','EUG','EVV','F11','FAI','FAR','FAT','FAY','FLO','FSD','FSM','FWA','GEG','GGG','GPT','GRB','GSO','GSP','GTF','HSV','HTS','HUF','I90','ICT','ILM','IND','JAX','L30','LBB','LCH','LEX','LFT','LIT','M03','M98','MAF','MCI','MDT','MGM','MIA','MKE','MLI','MLU','MOB','MSN','MSY','MWH','MYR','N90','NCT','OKC','ORF','P31','P50','P80','PCT','PHL','PIT','PVD','PWM','R90','RDG','RDU','RFD','ROA','ROC','ROW','RST','RSW','S46','S56','SAT','SAV','SBA','SBN','SCT','SDF','SGF','SHV','SUX','SYR','T75','TLH','TOL','TPA','TRI','TUL','TYS','U90','Y90','YNG']
i = int(0)       
x = int(0)

start = datetime.strptime(start_date,'%m/%d/%Y').date()
loop_start = start
end = datetime.today().date() - timedelta(2)       # end date todays's date - 2 days  end = datetime.strptime(end_date,'%m/%d/%Y').date()
day_dif = abs((end-start).days)

with open("C:\CTAT_BI\_Position_Missing_Files.txt",'w') as outfile:  
    while i < len(site):
        in_path = DriveIn+":/CTAT_BI/Position/{}/".format(site[i])
        os.chdir(in_path)
        file_list= []
        for in_file in os.listdir():
            csv_file,extension = os.path.splitext(in_file)
            file_date = csv_file[4]+csv_file[5]+csv_file[6]+csv_file[7]+"-"+csv_file[9]+csv_file[10]+"-"+csv_file[12]+csv_file[13]
            file_list.append(file_date)
            x  += 1
        s_start = str(start)
    
        x=0
        while x < day_dif:
            if str(loop_start) not in file_list:    
                file_string =site[i]+"  Missing Dates > "+str(loop_start)+"\n"
                outfile.write(file_string)
                print(site[i],"  Missing Dates > ",loop_start)
            loop_start += timedelta(1)
            x  += 1
        i +=1
        x=0    
        loop_start = start
print("Done")    
