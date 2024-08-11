# px41cx-utility
Python program to add ROM images to an existing PX41CX firmware and/or modify other firmware options.

The PX41CX is a modern replica of the class HP-41CX programmable calculator released in the 1980s. The implementation runs the original
HP-41CX ROM by implementing an emulator of the HP Nut processor. The PX41CX also supports up to 12 optional ROM modules which are encapsulated within
the PX41CX Intel HEX format firmware file. These modules can be virtually plugged in and ejected from the PX41CX menu system as required.

| ROM         | Page        | Bank     | Bank Group | Module Group | Name   | Description |
|-------------|-------------|----------|------------|--------------|--------|-------------|
| 0           | 0           | 1        | 0          | 0            | XNUT0  | Reserved - OS |
| 1           | 1           | 1        | 0          | 0            | XNUT1  | Reserved - OS |
| 2           | 2           | 1        | 0          | 0            | XNUT2  | Reserved - OS |
| 3           | 3           | 1        | 1          | 0            | CXFUN0 | Reserved - OS |
| 4           | 5           | 1        | 1          | 0            | TIMER  | Reserved - OS |
| 5           | 5           | 2        | 1          | 0            | CXFUN1 | Reserved - OS |
| 6           | 8           | 1        | 2          | 1            | AdvL1  | Default - Available |
| 7           | 9           | 1        | 2          | 1            | AdvU1  | Default - Available |
| 8           | 9           | 2        | 2          | 1            | AdvU2  | Default - Available |
| 9           | a           | 1        | 0          | 2            | Math1D  | Default - Available |
| 10          | b           | 1        | 0          | 3            | Stat1B  | Default - Available |
| 11          | c           | 1        | 0          | 4            | Financ  | Default - Available |
| 12          | d           | 1        | 0          | 5            | Zenrom  | Default - Available |
| 13          | e           | 1        | 0          | 9            | Games1  | Default - Available |
| 14          | f           | 1        | 0          | 10            | Circui  | Default - Available |
| 15          | f           | 1        | 0          | 11            | Survey  | Default - Available |
| 16          | e           | 1        | 0          | 12            | PPCL R  | Default - Available |
| 17          | f           | 1        | 0          | 12            | PPCU R  | Default - Available |

ROM locations 0 through 5 are reserved for the HP-41CX operating system. The remaining ROM locations 6 through 17 are available for the firmware default builtin ROMs or they can be replaced with the specific modules the user wishes to use. Adding or updating a ROM location requires specifying the ROM location, ROM filename, 41CX page the module is to be loaded into, the page bank, the bank group and the module group. The module group keeps multiple pages 
from a single module together so they are all plugged into the PX41CX at the same time.

Although ROM modules can be builtin to the PX41CX firmware from the source code, this does not provide a method for the end user to easily modify the available ROM modules. As the HP 41C series includes hundreds of optional HP, 3rd party and community developed ROM modules there needs to be a relatively easy way to modify the PX41CX ROM modules available without the firmware being custom built to meet thousands of different possible configurations.

This program allows HP 41C series ROMs to be added or merged into an existing PX41CX firmware to produce a new firmware file that can be flashed onto the PX41CX.

The PX41CX includes a number of other options that can be configured in the firmware including:
- 4 lines of 31 characters of custom text which is displayed in the Info menu
- a simple BMP image that is displayed when the calculator is powered off

The program does some simple error checking, however, knowledge of the HP 41C series memory space and requirements for the modules to be used is required.

ROM file archives that are regularly updated are available at: https://systemyde.com/hp41/archive.html

# Installation
The program requires Python 3 and the intelhex module which can be found at: https://pypi.org/project/intelhex/
# Usage
```
Usage: px41cx_utility.py [-h] [-m]
                         [-06 romfile page bank bankgroup modgroup]
                         [-07 romfile page bank bankgroup modgroup]
                         [-08 romfile page bank bankgroup modgroup]
                         [-09 romfile page bank bankgroup modgroup]
                         [-10 romfile page bank bankgroup modgroup]
                         [-11 romfile page bank bankgroup modgroup]
                         [-12 romfile page bank bankgroup modgroup]
                         [-13 romfile page bank bankgroup modgroup]
                         [-14 romfile page bank bankgroup modgroup]
                         [-15 romfile page bank bankgroup modgroup]
                         [-16 romfile page bank bankgroup modgroup]
                         [-17 romfile page bank bankgroup modgroup]
                         [-u1 USER1] [-u2 USER2] [-u3 USER3] [-u4 USER4]
                         [-b BMPFILE]
                         infile [outfile]

Update ROMs and options in PX41CX Firmware.

positional arguments:
  infile
  outfile
```
# Examples
To view the loaded modules and configured options of an existing PX41CX firmware specify a firmware filename only:
```
python px41cx_utility.py px41cx-fw01.hex 
PX41CX Firmware: px41cx-fw01.hex
ROM[00]: Page: 0 Bank: 1 Bank Group: 0 Mod Group: 00 XNUT0 
ROM[01]: Page: 1 Bank: 1 Bank Group: 0 Mod Group: 00 XNUT1 
ROM[02]: Page: 2 Bank: 1 Bank Group: 0 Mod Group: 00 XNUT2 
ROM[03]: Page: 3 Bank: 1 Bank Group: 1 Mod Group: 00 CXFUN0
ROM[04]: Page: 5 Bank: 1 Bank Group: 1 Mod Group: 00 TIMER 
ROM[05]: Page: 5 Bank: 2 Bank Group: 1 Mod Group: 00 CXFUN1
ROM[06]: Page: 4 Bank: 1 Bank Group: 0 Mod Group: 01 LIBRY4
ROM[07]: Page: 8 Bank: 1 Bank Group: 2 Mod Group: 02 AdvL1 
ROM[08]: Page: 9 Bank: 1 Bank Group: 2 Mod Group: 02 AdvU1 
ROM[09]: Page: 9 Bank: 2 Bank Group: 2 Mod Group: 02 AdvU2 
ROM[10]: Page: 4 Bank: 1 Bank Group: 2 Mod Group: 03 FORTH4
ROM[11]: Page: e Bank: 1 Bank Group: 2 Mod Group: 03 FORTH+
ROM[12]: Page: a Bank: 1 Bank Group: 0 Mod Group: 04 Stat1B
ROM[13]: Page: b Bank: 1 Bank Group: 0 Mod Group: 05 Zenrom
ROM[14]: Page: c Bank: 1 Bank Group: 0 Mod Group: 06 Math1D
ROM[15]: Page: d Bank: 1 Bank Group: 0 Mod Group: 07 Financ
ROM[16]: Page: e Bank: 1 Bank Group: 0 Mod Group: 08 Aviati
ROM[17]: Page: f Bank: 1 Bank Group: 0 Mod Group: 09 Games1
User 1: 'Line 0'
User 2: 'Line 1'
User 3: 'Line 2'
User 4: 'Line 3'
```
User 1 through User 4 are the custom text lines displayed in the PX41CX Info menu.

To replace all user ROMs with the 2 pages of the PPC ROM to be loaded into 41CX pages C and D and store the new firmware in file new-fw.hex:
```
python px41cx_utility.py px41cx-fw01.hex new-fw.hex -06 PPCL.ROM c 1 0 10 -07 PPCU.ROM d 1 0 10
```
To replace the last 2 user ROMs with the 2 pages of the FORTH41 to be loaded into 41CX pages 4 (required) and E and store the new firmware in file new-fw.hex:
```
python px41cx_utility.py px41cx-fw01.hex new-fw.hex -16 FORTH4.ROM 4 1 0 12 -17 FORTH5.ROM e 1 0 12
```
# Sample Power Off Splash Screens
The Splash_Images folder includes some sample BMP images (some shown below) which can be loaded using this utility and displayed when the PX41CX is turned off (if enabled in the configuration menu). Thanks to Pierre (https://clones.phweb.me/index.php?langue=EN) for creating many of these.

![PX](Splash_Images/PX.bmp)
![PX-ML](Splash_Images/PX-MemLost.bmp)
![PX-DARK](Splash_Images/PX-Dark.bmp)
![PX41CX](Splash_Images/px41cx.bmp)
![Robot](Splash_Images/robot.bmp)
![Droid](Splash_Images/droid.bmp)
