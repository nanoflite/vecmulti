VecMulti tool
=============

With this tool you can control your VecMulti cartridge.
It has support for building a menu and uploading programs over serial.

```
usage: vecmulti [-h] [--verbose] {load,menu} ...

positional arguments:
  {load,menu}  command help
    load       Load a program into the the Vectrex using the VecMulti dev
               mode.
    menu       Create a menu to use on the VecMulti cartridge.

optional arguments:
  -h, --help   show this help message and exit
  --verbose    Show what is going on.
```

Build a menu
------------

 $> vecmulti menu source destination

Upload a program over the development connection
------------------------------------------------

 $> vecmulti load --port /dev/cu.SLAB_USBtoUART --progress test/in/Wormhole.bin

Connecting a serial to USB cable

 ```
[--- top of pcb ---]
     x - GND
     x - PC RX
     x - PC TX
     x
 ```
 
Install
-------

You need to have Python and pyserial installed.

Author
------

Johan Van den Brande
 


