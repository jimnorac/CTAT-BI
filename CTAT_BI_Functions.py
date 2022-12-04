from datetime import datetime, timedelta
import math
import time

def get_hour(zIn):
  zOut = str(zIn).split(":",1)[0]  
  return zOut

def get_hh_mm(zIn):
  zOut = str(zIn).split(":",2)
  return zOut[0] +":" +zOut[1]

def get_eTime(zIn):
  zOut = str(zIn)
  return zOut

def get_floor30(zIn):
  delta = timedelta(minutes =15)
  zOut = datetime.min + math.floor((zIn - datetime.min)/delta) * delta  
  return zOut

def get_floor15(zIn):
  zOut = datetime.min + round((zIn - datetime.min)/15) *15  
  return zOut

def get_LTime(zIn):
  zOut = str(zIn).split(" ",2)
  return zOut[2]

def get_LTime2(zIn):  
  zOut = str(zIn).split(" ",2)
  if (zOut[0] == "0"):
     zOut = str(zIn).split(" ",2)      
  zOut = str(zIn).split(",",2)   
  return zOut[0:5]

def get_alpha(zIn):
  z=1
  zOut = zIn[0] 
  while z < len(zIn):
    if(zIn[z] != '0' and zIn[z] !='1' and zIn[z] !='2' and zIn[z] !='3'and zIn[z] !='4'and zIn[z] !='5'and zIn[z] !='6'and zIn[z] !='7'and zIn[z] !='8'and zIn[z] !='9'):
      zOut  = zOut +zIn[z]
      z=z+1
    else:
      z=len(zIn)
  return zOut

def get_airport(zIn):
  zOut = zIn
  if zIn == "Ovr":
    zOut = "."
  return zOut  

def get_leading_zero(zIn):
  zOut = str(zIn)
  zOut = str(zIn).zfill(4)    
  return(zOut)

def get_position(zIn):
  zOut = str(zIn)
  if zOut[-1] == "C":
    zOut = '.'  
  if (len(zOut) <= 1):    
    zOut = '.'
  if ((zOut=='01') | (zOut=='02')| (zOut=='03')| (zOut=='04')| (zOut=='05')| (zOut=='06')| (zOut=='07')| (zOut=='08')| (zOut=='09')):
    zOut = '.'   
  if len(zOut) == 2:
    if zOut[-2] == '0':
      zOut = '.'
  return zOut

#  LenzOut = len(zOut)
#  LenzIn = len(zIn)
#    print(f"Stop Len zIn  {LenzOut}  - {LenzIn}      {zhold}  ** {zOut} ",end='')
#    time.sleep(.25)
