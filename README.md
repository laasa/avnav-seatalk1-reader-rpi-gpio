# avnav-seatalk1-reader-rpi-gpio


# General

The plugin read seatalk 1 protocol via configured GPIO on Raspberry Pi.

It is widely based on the
- seatalk remote plugin (https://github.com/wellenvogel/avnav-seatalk-remote-plugin),
- more nmea plugin (https://github.com/kdschmidt1/avnav-more-nmea-plugin) and
-  (https://github.com/Thomas-GeDaD/Seatalk1-Raspi-reader).

There exist the way to activate the GPIO plugin in openplotter/signalk base on 'Seatalk1 Raspi Reader'.
But especially for beginners like me it's possibly a bit to complicate to get knowledge 
- which software serve the hardware, 
- which one is storing the value and 
- what is the way to get these values in avnav.
It takes a bit of time to understand the powerful ideas of multiplexing between all the software in openplotter family.
To get in touch with avnav plugin programming and python and to have simple and short data ways.
Especially the last thing could be interesting: To have the most current 'depth below transducer' value and not the 2 seconds old one.

# Parameter

- GPIO pin on raspberry (default is GPIO4 on pin 7)
- Inverted flag (default is on)

# Details

# Hardware needs
It is strongly commended to use optocoupler between seatalk 1 level and Raspberry Pi inputs.

I have used the circuit suggested here: https://pysselilivet.blogspot.com/2020/06/seatalk1-to-nmea-0183-converter-diy.html

![grafik](https://user-images.githubusercontent.com/98450191/153387500-d0d51e84-01ea-464c-9ae9-742f282d7829.png)


# Installation

To install this plugin please 
- create directory '/usr/lib/avnav/plugins/avnav-seatalk1-reader-rpi-gpio' and 
- and copy the file plugin.py to this directory.

# Known issues
