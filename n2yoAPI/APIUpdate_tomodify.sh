#!/bin/bash

#Put your API from n2yo.com into the 'YOUR-API-KEY' field and rename the file APIUpdate.sh
APIKey=YOUR-API-KEY
Path=/home/pi/Dev/ARTSystem

curl -s 'https://api.n2yo.com/rest/v1/satellite/radiopasses/33591/44.821781/-0.56531/20/2/40/&apiKey='$APIKey -o $Path'/n2yoAPI/NOAA19.json' & >&- 2>&-
curl -s 'https://api.n2yo.com/rest/v1/satellite/radiopasses/28654/44.821781/-0.56531/20/2/40/&apiKey='$APIKey -o $Path'/n2yoAPI/NOAA18.json' & >&- 2>&-
curl -s 'https://api.n2yo.com/rest/v1/satellite/radiopasses/25338/44.821781/-0.56531/20/2/40/&apiKey='$APIKey -o $Path'/n2yoAPI/NOAA15.json' & >&- 2>&-
wait

python3 -u $Path/n2yoAPI/APIParser.py

curl -s 'https://api.n2yo.com/rest/v1/satellite/tle/25338&apiKey='$APIKey -o $Path'/NOAAScheduler/N15_TLE.json' & >&- 2>&-
curl -s 'https://api.n2yo.com/rest/v1/satellite/tle/28654&apiKey='$APIKey -o $Path'/NOAAScheduler/N18_TLE.json' & >&- 2>&-
curl -s 'https://api.n2yo.com/rest/v1/satellite/tle/33591&apiKey='$APIKey -o $Path'/NOAAScheduler/N19_TLE.json' & >&- 2>&-
wait
