# ATCProgram
Autonomous Tracking and Capturing Program for NOAA satellites

## Disclamer

**This project is currently in dev, the rotor control has not been tested in real condition yet.**

The scripts are targeted for Raspberry application but it should be compatible on any device with python3

The gnu-radio-compagnion software uses python2.7 for my setup (gnu-radio v.3.7). If you have gnu-radio on python3 you must change the line 84 in the Scheduler.py script :
> gnuradio = subprocess.Popen('**python** -u /home/pi/Dev/GR_NOAA_script/ ...

## First setup

### Modifying APIUpdate_tomodify.sh

Go to ./n2yoAPI and open APIUpdate_tomodify.sh. From there you must replace 'YOUR-API-KEY' field with your API key from n2yo.com
Change the name of the file to APIUpdate.sh for the main script.

### Modifying absolute paths to file

I used absolute path for pretty much everything to be "safe" ~~I guess ??~~.
The file concerned by that modification are :
```
n2yoAPI/APIUpdate.sh (or APIUpdate_tomodify.sh)
n2yoAPI/AAPIParser.py
NOAAScheduler/Predict.py
NOAAScheduler/Scheduler.py
NOAAScheduler/Tracker.py
```
### Modifying serial port for Rot2proG rotor

All the work here is done by [jaidenfe](https://github.com/jaidenfe/rot2proG).
I just remove the stuff I don't need for this project. You can set the serial port for your rotor in the Tracker.py script :

> Rotor = Rot2proG('**/dev/ttyS0**')

## How to use ?

After setting everything up you just have to launch the Scheduler.py script with :

> $python3 -u Scheduler.py

If you don't have a Rot2proG or you have a fixed antenna for receiving you have to launch the script with:

> $python3 -u Scheduler.py noTracking

# TODO

- [ ] Switch comments to english
- [ ] Test rotor in real condition with tracking activated

Everything is a big mess for now but it should work as espected. I will probably clean thing up with the time.
