# Open Sesame

This project enables the RPi to auto-connect to Monash WiFi including signing in using your Authcate User and Password.

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

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Deployment

Add additional notes about how to deploy this on a live system

## Additional Notes
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

-----------------------------------------
### How to Change Timezone

sudo raspi-config
4 Localisation Options > I2 Change Timezone > Asia > Kuala Lumpur

4 Localisation Options > I3 Change Keyboard Layout > MODEL-XXXX Keyboard > Other > English (US) > English (US) > The default for the keyboard layout > No compose key > No

## Authors

Chin Er Win

## License

This project is unlicensed

## Acknowledgments
