# avnav-seatalk1-reader-rpi-gpio


# General

The plugin read seatalk 1 protocol via configured GPIO on Raspberry Pi.

It is widely based on the
- seatalk remote plugin (https://github.com/wellenvogel/avnav-seatalk-remote-plugin),
- more nmea plugin      (https://github.com/kdschmidt1/avnav-more-nmea-plugin) and
- Seatalk1 to NMEA 0183 (https://github.com/MatsA/seatalk1-to-NMEA0183/blob/master/STALK_read.py).

There exist the way to activate the GPIO plugin in openplotter/signalk base on 'Seatalk1 Raspi Reader'.
But especially for beginners like me it's possibly a bit to complicate to get knowledge 
- which software serve the hardware, 
- which one is storing the value and 
- what is the way to get these values in avnav.

It takes a bit of time to understand the powerful ideas of multiplexing between all the software in openplotter family.
To get in touch with avnav plugin programming and python and to have simple and short data ways I tried another way.
Especially the last thing could be interesting: To have the most current 'depth below transducer' value and not the 2 seconds old one.

# Parameter

- gpio    : Define gpio where the SeaTalk1 (yellow wire) is sensed (default is 4 => GPIO4 on pin 7)
- inverted: Define if input signal shall be inverted 0 => not inverted, 1 => Inverted (default is 1)
- pulldown: Define if using internal RPi pull up/down 0 => No, 1= Pull down, 2=Pull up (default is 2)

# Details

# Hardware needs
It is strongly commended to use optocoupler between seatalk 1 level and Raspberry Pi inputs.

An example for such an circuit is suggested here: https://pysselilivet.blogspot.com/2020/06/seatalk1-to-nmea-0183-converter-diy.html

![grafik](https://user-images.githubusercontent.com/98450191/153389077-942ecb63-cb50-4e82-a864-6e4f0f91789d.png)

When needing more then 1 optical inputs (e.g. 3 for anchor chain counter) it make sense to use an module like BUCCK_817_4_V1.0.

![grafik](https://user-images.githubusercontent.com/98450191/153612895-ecf98fa0-a629-49a6-879c-2184b5e25af8.png)


Inside the Seatalk1 data line I have added an additional Resistor of 1K and couple both signals (Seatalk 1 Data, GND) via pin 1&2 on a 5-pin-socket.
Pin 3,4 and 5 of these socket are used for anchor chain counter (reed contact, up , down).  => https://github.com/laasa/avnav-anchor-chain-counter-rpi-gpio.
The rasperry pi is not fixed build on the boat.

![grafik](https://user-images.githubusercontent.com/98450191/153612948-56a30a7f-bc65-4fc3-87fb-684c5faf281a.png)


# Software installation

To install this plugin please 
- install packages via: sudo apt-get update && sudo apt-get install pigpio python-pigpio python3-pigpio
- start pigpio deamon e.g. via sudo servive pigdiod restart
- create directory '/usr/lib/avnav/plugins/avnav-seatalk1-reader-rpi-gpio' and 
- and copy the file plugin.py to this directory.

# Using in anvav
- STW: value from gps.SEATALK_STW in [m/s]

![grafik](https://user-images.githubusercontent.com/98450191/153569250-92ccd43b-df36-41cf-88ca-6f6340052a29.png)

- DBT: value from gpc.SEATALK_DBT in [m]

![grafik](https://user-images.githubusercontent.com/98450191/153557342-b5453d97-4b93-4f32-a148-b5365c5bd431.png)

# TODOs
- generate NMEA0183 frames (for multiplexing to other openplotter software like signalk) ?
