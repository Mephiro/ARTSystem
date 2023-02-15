#!/usr/bin/python3 -u
from datetime import datetime
from Predict import ParsingPasses
import subprocess
import signal
import os
import sys
import time

Path = '/home/pi/Dev/ARTSystem'
Picture_path = '/home/pi/Pictures'

def sigterm_handler(signal, frame):
    print('Exiting...')
    os.close(fifo)
    os.close(date_fifo)
    if(gnuradio):
    	os.killpg(os.getpgid(gnuradio.pid), signal.SIGTERM)
    if(tracker):
    	os.killpg(os.getpgid(tracker.pid), signal.SIGTERM)
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

#Appel de la fonction ParsingPasses pour initialiser les prochains passages de satellites
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
        tracker = subprocess.Popen('python3 -u '+Path+'/NOAAScheduler/Tracker.py '+sat+' Date', stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
        fifo = os.open(Path+'/NOAAScheduler/az_alt.fifo', os.O_RDONLY)
        date_fifo = os.open(Path+'/NOAAScheduler/date.fifo', os.O_WRONLY)
        os.write(date_fifo,bytes(str(set_start_time),'utf-8'))
        os.close(date_fifo)
        next_az_str = str(os.read(fifo,50))[2:-1]
        os.close(fifo)
        next_az = round(float(next_az_str),3)
        
        #Affichage du prochain azimuth si tracking activé
        print('next azimuth : '+str(next_az))
    print('')

    #Waiting for the next satellite to fly-by and start the recording
    while(datetime.now()<set_start_time):
        print(str(datetime.now())[:-7]+' | Waiting...',end='\r')
        time.sleep(1)
    print('')
        
    if(noTracking != 'noTracking'):
    	tracker = subprocess.Popen('python3 -u '+Path+'/NOAAScheduler/Tracker.py '+sat, stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
    	fifo = os.open(Path+'/NOAAScheduler/az_alt.fifo', os.O_RDONLY)

    #Appel du script GnuRadio pour le temps d'apparition du satellite
    gnuradio = subprocess.Popen('python -u '+Path+'/GR_NOAA_script/decodeur_NOAA'+sat[1:]+'_WAV.py', stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
		
    #Waiting end of satellite fly-by and stop the recording
    #If Rot2proG enable it shows the satellite azimuth/elevation and the current azimuth/elevation of the rotor
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
    os.killpg(os.getpgid(gnuradio.pid), signal.SIGTERM)
    if(noTracking != 'noTracking'):
        os.close(fifo)
        os.killpg(os.getpgid(tracker.pid), signal.SIGTERM)
    time.sleep(1)

    #Decodage de l'image
    print('Decoding...')
    aptdec_a = subprocess.Popen(Path+'/aptdec/build/aptdec -i a -d '+Picture_path+' -o picture_'+sat+'_'+str(set_start_time)+'_channelA.png ' \
        +Path+'/GR_NOAA_script/record.wav', stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
    aptdec_p = subprocess.Popen(Path+'/aptdec/build/aptdec -i p -d '+Picture_path+' -o picture_'+sat+'_'+str(set_start_time)+'_color.png \
        -p '+Path+'/aptdec/palettes/WXtoImg-'+sat+'-HVC.png '+Path+'/GR_NOAA_script/record.wav', stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)
    aptdec_t = subprocess.Popen(Path+'/aptdec/build/aptdec -i t -d '+Picture_path+' -o picture_'+sat+'_'+str(set_start_time)+'_temp.png ' \
        +Path+'/GR_NOAA_script/record.wav', stdout=subprocess.PIPE,shell=True, preexec_fn=os.setsid)

    exit_codes = [process.wait() for process in (aptdec_a, aptdec_p, aptdec_t)]
    print('Images done !')
    print('')
    
    #Appel de la fonction ParsingPasses pour reinitialiser toutes les dates
    NOAA15_start_time,NOAA15_stop_time,NOAA18_start_time,NOAA18_stop_time,NOAA19_start_time,NOAA19_stop_time = ParsingPasses()

    time.sleep(1)
