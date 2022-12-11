#  Analyze list of subfolders to find Extra files in folder using date from file name when date is less than the selected date start
#  Folder format C:\CTAT_BI\Position\AAA\AAA-2022-11-09-P.csv     AAA = facility name as subfolder name   in list site  [AAA BBB CCC]
#  File format   AAA-2022-11-09_P.csv   strip YYYY MM DD         AAA = facility name in file name  _P for Position _D History 
import os
import shutil
from datetime import datetime

zSource = "Z:/CTAT_BI/Position/"
zDestination ="Z:/CTAT_BI/zPosition/"

site = ['A11','A80','A90','ABE','ABI','ABQ','ACT','ACY','AGS','ALB','ALO','AMA','ASE','AUS','AVL','AVP','AZO','BFL','BGM','BGR','BHM','BIL','BIS','BNA','BOI','BTR','BTV',\
        'BUF','C90','CAE','CHA','CHS','CID','CKB','CLE','CLT','CMH','CMI','COS','CPR','CRP','CRW','CVG','D01','D10','D21','DAB','DLH','DSM','ELM','ELP','EUG','EVV','F11',\
        'FAI','FAR','FAT','FAY','FLO','FSD','FSM','FWA','GEG','GGG','GPT','GRB','GSO','GSP','GTF','HSV','HTS','HUF','I90','ICT','ILM','IND','JAX','L30','LBB','LCH','LEX',\
        'LFT','LIT','M03','M98','MAF','MCI','MDT','MGM','MIA','MKE','MLI','MLU','MOB','MSN','MSY','MWH','MYR','N90','NCT','OKC','ORF','P31','P50','P80','PCT','PHL','PIT',\
        'PVD','PWM','R90','RDG','RDU','RFD','ROA','ROC','ROW','RST','RSW','S46','S56','SAT','SAV','SBA','SBN','SCT','SDF','SGF','SHV','SUX','SYR','T75','TLH','TOL','TPA',\
        'TRI','TUL','TYS','U90','Y90','YNG']
      

i = int(0)                                                                                                              # counter check each facility in list site   
while i < len(site):                                                                                                # counter to check each facility in list site
    shutil.copy(zSource+"{}\{}-2022-01-01_P.csv".format(site[i],site[i]),zDestination+"{}\{}-2022-01-01_P.csv".format(site[i],site[i]))
    shutil.copy(zSource+"{}\{}-2022-01-02_P.csv".format(site[i],site[i]),zDestination+"{}\{}-2022-01-02_P.csv".format(site[i],site[i]))
    i +=1                                                                                                           # incremenmt site counter     
    
print("Done")    