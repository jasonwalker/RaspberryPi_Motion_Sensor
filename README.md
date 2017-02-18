# Passive IR Motion Detector

## A web server running on Raspberry Pi displaying a chart showing motion

## Hardware Setup
This is tested on Raspberry Pi running Raspbian.
Attach motion sensor (e.g. [this](http://www.adafruit.com/products/189)) to a Raspberry Pi.

 * power goes to pin #2
 * ground goes to pin #6
 * data goes to pin #22 (aka GPIO 25)

## Software Setup

 * Create a directory named PIR in /usr/local/bin
```
sudo mkdir /usr/local/bin/PIR
```
 * _from with the project directory_ Copy this project into the new directory 
```
sudo cp -r * /usr/local/bin/PIR
```
* Create a subdirectory named "js" in /usr/local/bin/PIR/static to hold Javascript libraries
```
sudo mkdir /usr/local/bin/PIR/static/js
```
* Pull down the two Javascript libraries we use, Jquery and Highcharts and copy them into the 'static/js' directory
```
sudo wget -P /usr/local/bin/PIR/static/js http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js http://code.highcharts.com/highcharts.js
```
 * make main file executable
```
sudo chmod +x /usr/local/bin/PIR/PirWeb.py
```
 * move startup file to correct location
```
sudo mv /usr/local/bin/PIR/PIRMotion.sh to /etc/init.d/
```
 * make startup file executable
```
sudo chmod +x /etc/init.d/PIRMotion.sh
```
 * make server start after booting
```
sudo update-rc.d PIRMotion.sh defaults
```
 * start server now (or reboot)
```
sudo /etc/init.d/PIRMotion.sh start
```

## Viewing the data
Open a browser and go to your Raspberry Pi's IP address.  It will take a minute to display data.

## Changing the configuration
You can change various features in the file /usr/local/bin/PIR/Config.py.


 * Which IO pin to plug into (default is 22)
 * port to run on (default 80)
 * username and password (default "username" and "password")
 * the amount of rolling hours displayed on the chart (default: 24)
 * a few chart titles
 * certificate and private key if using HTTPS
 
 After changing, a restart is necessary
```
sudo /etc/init.d/PIRMotion.sh restart
```

## WIFI dropping out
Wifi has been shutting down after a few weeks for me.  To correct this:
 * Create and edit a new file in /etc/modprobe.d/8192cu.conf
 * sudo vim /etc/modprobe.d/8192cu.conf
 * paste the following lines in
```
# Disable power saving
options 8192cu rtw_power_mgnt=0 rtw_enusbss=1 rtw_ips_mode=1
```
 * reboot
 
[this fix is from Adafruit](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-3-network-setup/test-and-configure#fixing-wifi-dropout-issues))
