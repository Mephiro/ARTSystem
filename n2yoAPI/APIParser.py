import datetime
Path = '/home/pi/Dev/ARTSystem'
#Ouverture des fichers obtenus par l'API
NOAA15_file = open(Path+'/n2yoAPI/NOAA15.json','r')
NOAA18_file = open(Path+'/n2yoAPI/NOAA18.json','r')
NOAA19_file = open(Path+'/n2yoAPI/NOAA19.json','r')
#Ouverture du fichiers de sortie
Passes_time = open(Path+'/n2yoAPI/Passes_time.txt','w')


def NOAA(NOAA_file):
    NOAA_str = NOAA_file.read()

    #Parsing des fichiers
    NOAA_1 = NOAA_str.split('}')
    NOAA_passes = int(NOAA_1[0].split(':')[-1])
    
    #Parsing each passe
    if(NOAA_passes>0):
        NOAA_sep = NOAA_1[1:NOAA_passes+1]
        NOAA_sep[0] =  NOAA_sep[0].split('[')[1]

    NOAA_infos=[]
    for i in range(NOAA_passes):
        NOAA_infos.append(NOAA_sep[i].split(','))

    #Extraction time for GnuRadio script
    UNIX_start_time = []
    UNIX_stop_time = []
    for i in range(NOAA_passes):
        for j in range(len(NOAA_infos[i])):
            if(NOAA_infos[i][j].find('startUTC')>0):
                UNIX_start_time.append(NOAA_infos[i][j].split(':')[1])
            if(NOAA_infos[i][j].find('endUTC')>0):
                UNIX_stop_time.append(NOAA_infos[i][j].split(':')[1])
                
    #Converting UNIX time to local time
    Start_time = []
    Stop_time = []
    for i in range(NOAA_passes):
        Start_time.append(datetime.datetime.fromtimestamp(int(UNIX_start_time[i])))
        Stop_time.append(datetime.datetime.fromtimestamp(int(UNIX_stop_time[i])))
    return Start_time,Stop_time

NOAA15_start, NOAA15_stop = NOAA(NOAA15_file)
NOAA18_start, NOAA18_stop = NOAA(NOAA18_file)
NOAA19_start, NOAA19_stop = NOAA(NOAA19_file)
if (len(NOAA15_start)>0):
    print('NOAA15',file=Passes_time)
    for i in range(len(NOAA15_start)):
        print(str(NOAA15_start[i])+';'+str(NOAA15_stop[i]),end=',',file=Passes_time)
    print('',file=Passes_time)
if (len(NOAA18_start)>0):
    print('NOAA18',file=Passes_time)
    for i in range(len(NOAA18_start)):
        print(str(NOAA18_start[i])+';'+str(NOAA18_stop[i]),end=',',file=Passes_time)
    print('',file=Passes_time)
if (len(NOAA19_start)>0):
    print('NOAA19',file=Passes_time)
    for i in range(len(NOAA19_start)):
        print(str(NOAA19_start[i])+';'+str(NOAA19_stop[i]),end=',',file=Passes_time)
Passes_time.close()
NOAA19_file.close()
NOAA18_file.close()
NOAA15_file.close()
