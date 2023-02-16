# ARTSystem
Autonomous Receiving and Tracking System for NOAA satellites using SDRPlay RSP1A

## Disclamer

**This project is currently in dev, the rotor control has not been tested in real condition yet.**

The scripts are targeted for Raspberry application but it should be compatible on any device with python3

The gnuradio-compagnion software uses python2.7 for my setup (gnuradio v.3.7). If you have gnuradio on python3 you must change the line 84 in the Scheduler.py script and regenerate each gnuradio script :
> gnuradio = subprocess.Popen('**python** -u $Path/GR_NOAA_script/ ...

## Dependencies

- gnuradio-compagnion (https://www.gnuradio.org/) (tested with v.3.7 only)
- aptdec (https://github.com/Xerbo/aptdec)
- SDRPlay API and gnuradio bloc (https://www.sdrplay.com/) (If you are using another SDR you'll need the specific API and GR bloc)

## First setup

### Modifying APIUpdate_tomodify.sh

Go to ./n2yoAPI and open APIUpdate_tomodify.sh. From there you must replace 'YOUR-API-KEY' field with your API key from n2yo.com

Change the name of the file to APIUpdate.sh for the main script.

### Modifying absolute paths to file

I used absolute path for pretty much everything to be "safe" ~~I guess ??~~. The file concerned by that modification are :
```
n2yoAPI/APIUpdate.sh (or APIUpdate_tomodify.sh)
n2yoAPI/AAPIParser.py
NOAAScheduler/Predict.py
NOAAScheduler/Scheduler.py
NOAAScheduler/Tracker.py
```
On each concerned file a variable Path is declared to set your own Path. Scheduler.py also has a variable for Picture_path.
### Modifying serial port for Rot2proG rotor

All the work here is done by [jaidenfe](https://github.com/jaidenfe/rot2proG). I just remove the stuff I don't need for this project. You can set the serial port for your rotor in the Tracker.py script :

> Rotor = Rot2proG('**/dev/ttyS0**')

### Create fifo for subprocesses

in the folder /NOAAScheduler do :

```
mkfifo az_alt.fifo
chmod 664 az_alt.fifo
mkfifo date.fifo
chmod 664 date.fifo
```

## How to use ?

After setting everything up you just have to launch the Scheduler.py script with :

> ./Scheduler.py

If you don't have a Rot2proG or you have a fixed antenna for receiving you have to launch the script with:

> ./Scheduler.py noTracking

### Modification for another SDR 

If you have another SDR you can open the gr_NOAA.grc file with gnuradio to change the SDR source. You'll have to regenerate all the scripts. For NOAA satellite the frequencies are :

```
NOAA15 : 137.620 MHz
NOAA18 : 137.9125 MHz
NOAA19 : 137.100 MHz
```

## What it does ?

When launching Scheduler.py the script will update all the files needed from n2yoAPI.

From there it will wait for the next satellite to cross the sky with a maximum elevation of at least 40°.

During fly-by the script launches 2 scripts :
- gnuradio script which save audio file of the WFM decoded signal
- tracking script (if tracking enable) which send to the rotor the azimuth/elevation coordinates of the satellite

When Fly-by ends the two previous scripts are closed and aptdec is called to decode the WAV file previously recorded.

By default aptdec saves 3 images to the ~/Pictures folder : the raw channelA, the false colored and the temperature image.

It then updates the files with n2yoAPI and loop to wait for the next passe.

# TODO

- [ ] Test rotor in real condition with tracking activated
- [ ] Update to gnuradio 3.10
- [ ] Merge gnuradio scripts into one for every satellites
- [ ] Add compatibility with bladerf SDR

Everything is a big mess for now but it should works as espected. I will probably clean thing up with the time.
