# Open Sesame

Automated login for Monash Malaysia Wi-Fi Portal. The python script is specifically made to run on a Raspberry Pi 3 but can easily be altered to run on any other systems

This project enables the RPi to auto-connect to Monash WiFi including signing in using your Authcate User and Password.

As of 12 March 2018, the program will show "UserWarning: Selenium support for PhantomJS has been deprecated, please use headless versions of Chrome or Firefox instead", this warning can be ignored.

## Getting Started

These instructions will get you a copy of the project up and running on your RPi.

### Prerequisites


1. Equipment Needed
  - Rpi ( I am using RPi3 )
  - Screen ( with Hdmi or get a VGA to Hdmi Converter )
  - Keyboard and Mouse
  - 8/16/32 GB SD Card, class 10 and above for speed (I am using 16GB)
2. Download Image from the * [Official Site](https://www.raspberrypi.org/downloads/raspbian/) (I downloaded RASPBIAN STRETCH WITH DESKTOP)
3. Format the SD card using * [SDFormatter](https://www.sdcard.org/downloads/formatter_4/)
4. Write the downloaded image into the SD Card using * [Win32 Disk Imager](https://sourceforge.net/projects/win32diskimager/)
5. Place the SD card into the Rpi, it should boot with default user "pi" and password "raspberry"
6. Connect to the Monash WiFi, open the browser to https://wifi.monash.edu.my/PortalMain to login.
7. To Run updates, open the Terminal enter in:
```
sudo apt-get update
sudo apt-get dist-upgrade
```

### Installing
These instructions will get you a copy of the project up and running on your RPi.

#### Clone this github

```
git clone https://github.com/Palt0n/open_sesame.git
```

#### Install Selenium

```
sudo pip install selenium
```
If there is an Error:
"
Could not find a version that satisfies the requirement selenium (from versions: )
No Matching distribution found for selenium
"
It is because of ITS, use data

#### Install PhantomJS

Go to https://github.com/fg2it/phantomjs-on-raspberry/tree/master/rpi-2-3/wheezy-jessie/v2.1.1 for the instructions to install PhantomJS

```
sudo apt-get install libfontconfig1 libfreetype6
curl -o /tmp/phantomjs_2.1.1_armhf.deb -sSL https://github.com/fg2it/phantomjs-on-raspberry/releases/download/v2.1.1-wheezy-jessie/phantomjs_2.1.1_armhf.deb
sudo dpkg -i /tmp/phantomjs_2.1.1_armhf.deb
```
Note: Attempted to use chromium but latest version of chromium at this time (12/3/2018) is version 60.0.3112.89. Selenium only works with version 61.0.3163.0 and above

```
sudo apt-get update
sudo apt-get install iceweasel
sudo apt-get install xvfb

sudo pip install selenium
sudo pip install PyVirtualDisplay
sudo pip install xvfbwrapper
```

visit https://github.com/mozilla/geckodriver/releases to download geckodriver-v0.16.1-arm7hf.tar.gz

For my case versions:
Selenium 3.11.0
Mozilla Firefox 52.7.3 
Geckodriver 0.16.1

## Deployment

Change the details to your Monash AuthCate User and Password, the email details are from when you want to know the ip and mac address of the pi.

```
AUTHCATE_USER = '**user**'
AUTHCATE_PASS = '**password**'
EMAIL_FROM = '@gmail.com'
EMAIL_FROM_PASS = 'emailpassword'
EMAIL_TO = '@gmail.com'
```


## Additional Notes

### How to get it to boot on startup

#### Install Xterm
Xterm is a terminal, has additional pop-out functionality from the pre-installed Terminal

```
Sudo apt-get install xterm
```

#### Create startup.py
startup.py will contain a ptyhon command to start open_sesame.py, if you want to run any other scripts, you can add them here 
```
sudo nano startup.py
```
in startup.py enter:
```
import os
os.system('sudo xterm -fn fixed -hold -e sudo python /home/pi/open_sesame/open_sesame_v1_e.py')
```

#### Run startup.py on Start
```
sudo nano ~/.config/lxsession/LXDE-pi/autostart
```
Add python /home/pi/startup.py
```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@point-rpi
@python /home/pi/startup.py
```

### How to Change NTP Server
You will noticed that the RPi cannot sync time when connected to Monash Malaysia WiFi, this is due to ITS blocking the default NTP servers which the RPi (or any computers) need to connect to time sync.
Monash has its own time server at "ntp.monash.edu".
The following steps (according to * [Dropwizard](https://www.linuxquestions.org/questions/linux-newbie-8/where-does-raspbian-stretch-assign-default-ntp-servers-4175618162/)) are to change the NTP server to Monash NTP Servers
```
sudo nano /etc/systemd/timesyncd.conf
```
What you see
```
#NTP=
#FallbackNTP=0.debian.pool.ntp.org 1.debian.pool.ntp.org 2.debian.pool.ntp.org 3.debian.pool.ntp.org
```

Change to (Uncomment "NTP=", add monash time server address)
```
NTP=ntp.monash.edu
```

### How to Change Timezone & Keyboard

sudo raspi-config
4 Localisation Options > I2 Change Timezone > Asia > Kuala Lumpur

4 Localisation Options > I3 Change Keyboard Layout > MODEL-XXXX Keyboard > Other > English (US) > English (US) > The default for the keyboard layout > No compose key > No

### How to forward internet from Conected WiFi to Ethernet Port

https://github.com/arpitjindal97/raspbian-recipes/blob/master/wifi-to-eth-route.sh


## Authors

Chin Er Win

## License

This project is unlicensed

## Acknowledgments

## Additonal Reading
Installing Libraries
https://raspberrypi.stackexchange.com/questions/4941/can-i-run-selenium-webdriver-using-firefox-as-the-browser
http://www.mantonel.com/tutorials/web-scraping-raspberry-pi-and-python
