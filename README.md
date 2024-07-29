# px41cx-utility
Python program to add ROM images to an existing PX41CX firmware and/or modify other firmware options.

The PX41CX is a modern replica of the class HP-41CX programmable calculator released in the 1980s. The implementation runs the original
HP-41CX ROM by implementing an emulator of the original HP Nut processor. The PX41CX also supports up to 12 optional ROM modules which are encapsulated within
the PX41CX Intel HEX format firmware file. These modules can be virtually plugged in and ejected from the PX41CX menu system as required.

Although ROM modules can be builtin to the PX41CX firmware from the source code, this does not provide a method for the end user to easily modify the available ROM modules. As the HP 41C series includes hundreds of optional HP, 3rd party and user community developed ROM modules there needs to be a relatively easy way to modify the PX41CX ROM modules available without the firmware being custom built to meet thousands of different possible configurations.

This program allows HP 41C series ROMs to be added or merged into an existing PX41CX firmware to produce a new firmware file that can be flashed onto the PX41CX.

The PX41CX includes a number of other options that can be configured in the firmware including:
- 4 lines of 32 characters of custom text which is displayed in the Info menu
- a simple BMP image that is displayed when the calculator is powered off

The program does some simple error checking, however, knowledge of the HP 41C series memory space and requirements for the modules to be used is required.

# Installation
The program requires Python 3 and the intelhex module which can be found at: https://pypi.org/project/intelhex/
# Examples
To view the loaded modules and configured options of an existing PX41CX firmware
