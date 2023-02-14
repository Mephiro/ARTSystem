from datetime import datetime
import subprocess
import signal
import os
import sys
import time

def sigterm_handler(signal, frame):
    print('Exiting...')
    os.close(fifo)
    os.close(date_fifo)
    if(gnuradio):
    	os.killpg(os.getpgid(gnuradio.pid), signal.SIGTERM)
    if(tracker):
    	os.killpg(os.getpgid(tracker.pid), signal.SIGTERM)
    sys.exit(0)

def ParsingPasses():
    #Appel system de APIUpdater.sh
    os.system('/home/pi/Dev/n2yoAPI/APIUpdate.sh')
    # Parsing du fichier de passage généré par l'API (C'est de la merde et je m'en branle)
    Passes = open("/home/pi/Dev/n2yoAPI/Passes_time.txt","r")
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

signal.signal(signal.SIGTERM, sigterm_handler)

#Appel de la fonction de mort pour initialiser chaque variable
NOAA15_start_time,NOAA15_stop_time,NOAA18_start_time,NOAA18_stop_time,NOAA19_start_time,NOAA19_stop_time = ParsingPasses()

#Si noTracking est passé en argument le programme n'appele pas la fonction Tracker.py
if(len(sys.argv)>1):
    noTracking = sys.argv[1]
else:
    noTracking = 'Off'

print( "\033[2J")
print("\033[1;1H")
while (1):    
    #Recherche de la prochaine date/heure de passage et du satellite concerné
    nexttime = NOAA15_start_time[0]
    sat='N15'
    if (nexttime > NOAA18_start_time[0]):
        nexttime == NOAA18_start_time[0]
        sat='N18'
    if (nexttime > NOAA19_start_time[0]):
        sat='N19'

    #Fixation du prochain passage avant attente
    if (sat=='N15'):
        set_start_time = NOAA15_start_time.pop(0)
        set_stop_time = NOAA15_stop_time.pop(0)
    elif (sat=='N18'):
        set_start_time = NOAA18_start_time.pop(0)
        set_stop_time = NOAA18_stop_time.pop(0)
    else:
        set_start_time = NOAA19_start_time.pop(0)
        set_stop_time = NOAA19_stop_time.pop(0)
        
    #Affichage du prochain passage
    print('next satellite : '+sat)
    print('next start : '+str(set_start_time))
    print('next stop : '+str(set_stop_time))
    
    if(noTracking != 'noTracking'):
        #Mise a jour du prochain azimuth pour le reglage du rotor
        tracker = subprocess.Popen('python3 -u /home/pi/Dev/NOAAScheduler/Tracker.py '+sat+' Date', stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
        fifo = os.open('/home/pi/Dev/NOAAScheduler/az_alt.fifo', os.O_RDONLY)
        date_fifo = os.open('/home/pi/Dev/NOAAScheduler/date.fifo', os.O_WRONLY)
        os.write(date_fifo,bytes(str(set_start_time),'utf-8'))
        os.close(date_fifo)
        next_az_str = str(os.read(fifo,50))[2:-1]
        os.close(fifo)
        next_az = round(float(next_az_str),3)
        
        #Affichage du prochain azimuth si tracking activé
        print('next azimuth : '+str(next_az))
    print('')

    #Waiting for the time to start the recording
    while(datetime.now()<set_start_time):
        print(str(datetime.now())[:-7]+' | Waiting...',end='\r')
        time.sleep(1)
    print('')
        
    if(noTracking != 'noTracking'):
    	tracker = subprocess.Popen('python3 -u /home/pi/Dev/NOAAScheduler/Tracker.py '+sat, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
    	fifo = os.open("/home/pi/Dev/NOAAScheduler/az_alt.fifo", os.O_RDONLY)

    #Appel du script GnuRadio pour le temps d'apparition du satellite
    gnuradio = subprocess.Popen('python -u /home/pi/Dev/GR_NOAA_script/decodeur_NOAA'+sat[1:]+'_WAV.py', stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
		
    #Waiting for the time to stop the recording
    while(datetime.now()<set_stop_time):
        if(noTracking != 'noTracking'):
            az_alt_str = os.read(fifo,50)
            az_alt = str(az_alt_str).split()
            SAT_AZ = round(float(az_alt[0][2:]),3)
            SAT_ALT = round(float(az_alt[1]),3)
            ROT_AZ = float(az_alt[2])
            ROT_ALT = float(az_alt[3][:-1])
            print(sat+" azimuth : "+str(SAT_AZ)+" | Rotor azimuth : "+str(ROT_AZ))
            print(sat+" elevation : "+str(SAT_ALT)+" | Rotor elevation : "+str(ROT_ALT),end='\r')
            print("\033[2A")
        else:
            print(str(datetime.now())[:-7]+' | Capturing...',end='\r')
            time.sleep(1)
    print('')

    #Stop script GR NOAA
    print('Stopping...')
    os.close(fifo)
    os.killpg(os.getpgid(gnuradio.pid), signal.SIGTERM)
    if(tracker):	
    	os.killpg(os.getpgid(tracker.pid), signal.SIGTERM)
    time.sleep(1)

    #Decodage de l'image
    print('Decoding...')
    aptdec_a = subprocess.Popen('/home/pi/Dev/aptdec/build/aptdec -i a -d /home/pi/Pictures -o picture_'+sat+'_'+str(datetime.now())+'_channelA.png \
        /home/pi/Dev/GR_NOAA_script/record.wav', stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
    aptdec_p = subprocess.Popen('/home/pi/Dev/aptdec/build/aptdec -i p -d /home/pi/Pictures -o picture_'+sat+'_'+str(datetime.now())+'_color.png \
        -p /home/pi/Dev/aptdec/palettes/WXtoImg-'+sat+'-HVC.png /home/pi/Dev/GR_NOAA_script/record.wav', stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
    aptdec_t = subprocess.Popen('/home/pi/Dev/aptdec/build/aptdec -i t -d /home/pi/Pictures -o picture_'+sat+'_'+str(datetime.now())+'_temp.png \
        /home/pi/Dev/GR_NOAA_script/record.wav', stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)

    exit_codes = [process.wait() for process in (aptdec_a, aptdec_p, aptdec_t)]
    print('Images done !')
    print('')
    
    #Appel de la fonction pour reinitialiser toutes les dates
    NOAA15_start_time,NOAA15_stop_time,NOAA18_start_time,NOAA18_stop_time,NOAA19_start_time,NOAA19_stop_time = ParsingPasses()

    time.sleep(1)
