# avnav-seatalk1-reader-rpi-gpio


# General

The plugin read seatalk 1 protocol via configured GPIO on Raspberry Pi.

It is widely based on the
- seatalk remote plugin (https://github.com/wellenvogel/avnav-seatalk-remote-plugin),
- more nmea plugin      (https://github.com/kdschmidt1/avnav-more-nmea-plugin) and
- Seatalk Raspi Reader  (https://github.com/Thomas-GeDaD/Seatalk1-Raspi-reader).

There exist the way to activate the GPIO plugin in openplotter/signalk base on 'Seatalk1 Raspi Reader'.
But especially for beginners like me it's possibly a bit to complicate to get knowledge 
- which software serve the hardware, 
- which one is storing the value and 
- what is the way to get these values in avnav.

It takes a bit of time to understand the powerful ideas of multiplexing between all the software in openplotter family.
To get in touch with avnav plugin programming and python and to have simple and short data ways I tried another way.
Especially the last thing could be interesting: To have the most current 'depth below transducer' value and not the 2 seconds old one.

# Parameter

- GPIO pin on raspberry (default is GPIO4 on pin 7)
- Inverted flag (default is on)

# Details

# Hardware needs
It is strongly commended to use optocoupler between seatalk 1 level and Raspberry Pi inputs.

I have used the circuit suggested here: https://pysselilivet.blogspot.com/2020/06/seatalk1-to-nmea-0183-converter-diy.html

![grafik](https://user-images.githubusercontent.com/98450191/153389077-942ecb63-cb50-4e82-a864-6e4f0f91789d.png)

I have selected such an 4 channel module like BUCCK_817_4_V1.0 (because need 3 more channels for anchor chain counter).

Inside the Seatalk1 data line I have added an additional Resistor of 1K and couple both signals (Seatalk 1 Data, GND) via pin 1&2 on a 5-pin-socket.
Pin 3,4 and 5 of these socket are used for anchor chain counter (reed contact, up , down).

# Installation

To install this plugin please 
- create directory '/usr/lib/avnav/plugins/avnav-seatalk1-reader-rpi-gpio' and 
- and copy the file plugin.py to this directory.

# Known issues
