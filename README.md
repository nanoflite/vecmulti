VecMulti tool
=============

With this tool you can control your VecMulti cartridge.
Is has support for building a menu and uploading programs over serial.

Build a menu
------------

 $> vecmulti menu source destination

Upload a program over the development connection
------------------------------------------------

 $> vecmulti load --port /dev/cu.SLAB_USBtoUART --progress test/in/Wormhole.bin

Connecting a serial to USB cable
 
 [--- top of pcb ---]
                x - GND
                x - PC RX
                x - PC TX
                x
 
Install
-------

You need to have Python and pyserial installed.

Author
------

Johan Van den Brande
 


