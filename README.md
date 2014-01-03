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
After changing, a restart is necessary
```
sudo /etc/init.d/PIRMotion.sh restart
```

 * Which IO pin to plug into (default is 22)
 * port to run on (default 80)
 * username and password (default "username" and "password")
 * the amount of rolling hours displayed on the chart (default: 24)
 * a few chart titles