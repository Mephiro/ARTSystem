import os
from datetime import datetime

Path = '/home/pi/Dev/ARTSystem'

def ParsingPasses():
    #Appel system de APIUpdater.sh
    os.system(Path+'/n2yoAPI/APIUpdate.sh')
    #Parsing du fichier de passage généré par l'API
    Passes = open(Path+'/n2yoAPI/Passes_time.txt','r')
    line='0'
    NOAA15_start=[]
    NOAA15_stop=[]
    NOAA18_start=[]
    NOAA18_stop=[]
    NOAA19_start=[]
    NOAA19_stop=[]
    while (len(line) != 0):
        line = Passes.readlines(1)
        if (len(line) != 0):
            line = line[0].strip()
            if (line=='NOAA15'):
                NOAA15_start_stop = Passes.readlines(1)[0].strip().split(',')
                for x in NOAA15_start_stop:
                    if (len(x)>0):
                        temp = x.split(';')
                        NOAA15_start.append(temp[0])
                        NOAA15_stop.append(temp[1])
            if (line=='NOAA18'):
                NOAA18_start_stop = Passes.readlines(1)[0].strip().split(',')
                for x in NOAA18_start_stop:
                    if (len(x)>0):
                        temp = x.split(';')
                        NOAA18_start.append(temp[0])
                        NOAA18_stop.append(temp[1])
            if (line=='NOAA19'):
                NOAA19_start_stop = Passes.readlines(1)[0].strip().split(',')
                for x in NOAA19_start_stop:
                    if (len(x)>0):
                        temp = x.split(';')
                        NOAA19_start.append(temp[0])
                        NOAA19_stop.append(temp[1])
    Passes.close()

    #Transforme tout ça en date pour le PC
    NOAA15_start_time = []
    NOAA15_stop_time = []
    for i in range(len(NOAA15_start)):
        NOAA15_start_time.append(datetime.strptime(NOAA15_start[i],'%Y-%m-%d %H:%M:%S'))
        NOAA15_stop_time.append(datetime.strptime(NOAA15_stop[i],'%Y-%m-%d %H:%M:%S'))

    NOAA18_start_time = []
    NOAA18_stop_time = []
    for i in range(len(NOAA18_start)):
        NOAA18_start_time.append(datetime.strptime(NOAA18_start[i],'%Y-%m-%d %H:%M:%S'))
        NOAA18_stop_time.append(datetime.strptime(NOAA18_stop[i],'%Y-%m-%d %H:%M:%S'))

    NOAA19_start_time = []
    NOAA19_stop_time = []
    for i in range(len(NOAA19_start)):
        NOAA19_start_time.append(datetime.strptime(NOAA19_start[i],'%Y-%m-%d %H:%M:%S'))
        NOAA19_stop_time.append(datetime.strptime(NOAA19_stop[i],'%Y-%m-%d %H:%M:%S'))

    return NOAA15_start_time,NOAA15_stop_time,NOAA18_start_time,NOAA18_stop_time,NOAA19_start_time,NOAA19_stop_time
