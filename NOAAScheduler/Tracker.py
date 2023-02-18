import ephem
import signal
from datetime import datetime
import time
import sys
import subprocess
import numpy as np
import os
import pytz
from Rotor import Rot2proG

local = pytz.timezone("Europe/Paris")
Rotor = Rot2proG('/dev/ttyUSB0')
Path = '/home/pi/Dev/ARTSystem'

def sigterm_handler(signal, frame):
    Rotor.stop()
    os.close(fifo)
    os.close(date_fifo)
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

#Loading TLE
if len(sys.argv) < 2:
    sys.exit(0)

sat = str(sys.argv[1])
TLE_file = open(Path+'/NOAAScheduler/'+sat+'_TLE.json','r')
TLE = TLE_file.readlines()
lines = str(TLE).split(',')[4].split('r')
line1 = lines[0][lines[0].find('1'):lines[0].find('\\')]
line2 = lines[1][lines[1].find('2'):lines[1].find('"')]
TLE_file.close()

NOAA = ephem.readtle(sat,line1,line2)

#GPS observer location
BOD = ephem.Observer()
BOD.lat, BOD.lon, BOD.elevation = '44:48:58.5','-0:34:25.5',20
BOD.pressure, BOD.temperature = 1010,25

fifo = os.open(Path+'/NOAAScheduler/az_alt.fifo', os.O_WRONLY)

if len(sys.argv) > 2:
    Mode = sys.argv[2]
else:
    Mode = ''

if (Mode=='Date'):
    date_fifo = os.open(Path+'/NOAAScheduler/date.fifo', os.O_RDONLY)
    next_date = os.read(date_fifo,50)
    os.close(date_fifo)

    next_date_str = datetime.strptime(str(next_date)[2:-1],'%Y-%m-%d %H:%M:%S')
    local_dt = local.localize(next_date_str, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    BOD.date = utc_dt
    NOAA.compute(BOD)
    next_az = NOAA.az*180/np.pi

    #Reglage de la prochaine position + attente que la position soit atteinte
    Rotor.set(round(next_az,1),0.0)
    Rotor_az, Rotor_alt, ph = Rotor.status()
    while((np.abs(Rotor_az-round(next_az,1)) > 0.2) or (Rotor_alt>0.2)):
        time.sleep(1)
        Rotor_az, Rotor_alt, ph = Rotor.status()
    os.write(fifo,bytes(str(next_az),'utf-8'))
    os.close(fifo)
    sys.exit(0)
else:
    #Compute current satellite position
    while(1):
        BOD.date = datetime.utcnow()
        NOAA.compute(BOD)
        current_az, current_alt = NOAA.az*180/np.pi, NOAA.alt*180/np.pi
        Rotor.set(round(current_az,1),round(current_alt,1))
        Rotor_az, Rotor_alt, ph = Rotor.status()
        #Ecriture des valeurs obtenue dans la fifo
        os.write(fifo,bytes(str(current_az)+' '+str(current_alt)+' '+str(Rotor_az)+' '+str(Rotor_alt),'utf-8'))
        time.sleep(1)
