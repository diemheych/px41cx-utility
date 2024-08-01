#
# px41cx_roms.py - load ROM files into PX41CX firmware and map to memory pages and
#                  set options
#
#
# Usage: px41cx_utility.py [-h] [-m]
#                          [-06 romfile page bank bankgroup modgroup]
#                          [-07 romfile page bank bankgroup modgroup]
#                          [-08 romfile page bank bankgroup modgroup]
#                          [-09 romfile page bank bankgroup modgroup]
#                          [-10 romfile page bank bankgroup modgroup]
#                          [-11 romfile page bank bankgroup modgroup]
#                          [-12 romfile page bank bankgroup modgroup]
#                          [-13 romfile page bank bankgroup modgroup]
#                          [-14 romfile page bank bankgroup modgroup]
#                          [-15 romfile page bank bankgroup modgroup]
#                          [-16 romfile page bank bankgroup modgroup]
#                          [-17 romfile page bank bankgroup modgroup]
#                          [-u1 "custom string line 1"]
#                          [-u2 "custom string line 2"]
#                          [-u3 "custom string line 3"}
#                          [-u4 "custom string line 4"]
#                          [-b BMPFILE]
#                          infile [outfile]
#
#
# The PX41CX firmware includes space for 18 x 4Kb word ROMs from 0 to 17. Locations
# 0 through 5 are reserved for the 41CX operating system ROMs. ROMs 6 through 17 are
# available for the user to load additional ROMs.
#
# For each required ROM location specify a ROM file, 41CX page, bank, bank group and
# module group.
#
# Custom information can also be specified which will be displayed in the PX41CX
# Info menu.
#
# A simple splash screen can also be added from a monochrome (1 bit) BMP. The screen
# resolution is 250 x 122 pixels.
# 
# By default the new ROM options replace all existing firmware ROMs (6-17) in the
# outfile firmware. The merge option (-m or --merge) merges/replaces the new ROMs
# with the existing ROMs in the infile firmware.
#

#
# Copyright (c) 2024 Darren Hosking @calculatorclique https://github.com/diemheych
# 
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.
#
import argparse
from intelhex import IntelHex

ROM_MAP = 0xf800
ROM_MAP_SIZE = 18
ROM_MAP_ENTRY = 4
ROM_NAMES = 0xf848
# ROM name length including null
NAME_LEN = 7
ROM_LOCATION = [0x8000, 0x9400, 0xab00, 0xbc00, 0xd000, 0xe400, 0x10000, 0x11400, 0x12800, 0x13c00, 0x15000, 0x16400, 0x18000, 0x19400, 0x1a800, 0x1bc00, 0x1d000, 0x1e400]
#USER1 = 0xf926
USER1 = 0xf8c6
USER2 = USER1 + 0x20
USER3 = USER2 + 0x20
USER4 = USER3 + 0x20
SPLASH = 0x1f800
MAGIC1 = 0x0c
MAGIC2 = 0x94
IMAGE_SIZE = 2048
WIDTH = 250
HEIGHT = 122

def set_rom(hex, rom, page, bank, bankgroup, modgroup):
    hex[ROM_MAP + ROM_MAP_ENTRY * rom + 0] = page
    hex[ROM_MAP + ROM_MAP_ENTRY * rom + 1] = bank
    hex[ROM_MAP + ROM_MAP_ENTRY * rom + 2] = bankgroup
    hex[ROM_MAP + ROM_MAP_ENTRY * rom + 3] = modgroup

def get_rom(hex, rom):
    return hex[ROM_MAP + ROM_MAP_ENTRY * rom + 0],hex[ROM_MAP + ROM_MAP_ENTRY * rom + 1],hex[ROM_MAP + ROM_MAP_ENTRY * rom + 2], hex[ROM_MAP + ROM_MAP_ENTRY * rom + 3]

def print_rom(hex, rom):
    print("ROM[","{:02d}".format(rom),"]: Page: ","{:01x}".format(hex[ROM_MAP + ROM_MAP_ENTRY * rom + 0])," Bank: ",hex[ROM_MAP + ROM_MAP_ENTRY * rom + 1]+1," Bank Group: ",hex[ROM_MAP + ROM_MAP_ENTRY * rom + 2]," Mod Group: ","{:02d}".format(hex[ROM_MAP + ROM_MAP_ENTRY * rom + 3])," ",get_name(hex, rom),sep="")
#    print("ROM[","{:02d}".format(rom),"]: Page: ","{:02d}".format(hex[ROM_MAP + ROM_MAP_ENTRY * rom + 0])," Bank: ",hex[ROM_MAP + ROM_MAP_ENTRY * rom + 1]," Group: ",hex[ROM_MAP + ROM_MAP_ENTRY * rom + 2]," ",get_name(hex, hex[ROM_MAP + ROM_MAP_ENTRY * rom + 0]),sep="")

def get_name(hex, num):
    if num == 55:
        return "CXFUNS1"
    else:
        return hex.getsz(ROM_NAMES + num * NAME_LEN).decode('utf-8')

def read_rom(barr, filename):
    loc = 0

    try:
        f = open(filename, "rb")
    except:
        print("Error opening hex file:",args['infile'])
        exit(1)
        
    rom = bytearray(f.read())
    f.close()

    for x in range(256):
        for y in range(0, 32, 2):
            low = rom[x * 32 + y + 1]
            barr[loc] = int(low)
            loc += 1

    for x in range(64):
        for y in range(0, 128, 8):
            high = (rom[x * 128 + y + 6] & 3) << 6
            high |= (rom[x * 128 + y + 4] & 3) << 4
            high |= (rom[x * 128 + y + 2] & 3) << 2
            high |= (rom[x * 128 + y + 0] & 3)
            barr[loc] = int(high)
            loc += 1


def access_bit(data, num):
    base = int(num // 8)
    shift = 7 - int(num % 8)
    return (data[base] >> shift) & 0x1


rom_map = [[0 for _ in range(ROM_MAP_ENTRY)] for _ in range(ROM_MAP_SIZE)]

parser = argparse.ArgumentParser(description='Update ROMs and options in PX41CX Firmware.')
parser.add_argument('infile')
parser.add_argument('outfile',nargs='?')
parser.add_argument('-m','--merge',action='store_true',help="Merge with existing firmware ROMs")
parser.add_argument('-06',dest='rom06',nargs=5,type=str,metavar=('romfile','page','bank','bankgroup','modgroup'))
parser.add_argument('-07',dest='rom07',nargs=5,type=str,metavar=('romfile','page','bank','bankgroup','modgroup'))
parser.add_argument('-08',dest='rom08',nargs=5,type=str,metavar=('romfile','page','bank','bankgroup','modgroup'))
parser.add_argument('-09',dest='rom09',nargs=5,type=str,metavar=('romfile','page','bank','bankgroup','modgroup'))
parser.add_argument('-10',dest='rom10',nargs=5,type=str,metavar=('romfile','page','bank','bankgroup','modgroup'))
parser.add_argument('-11',dest='rom11',nargs=5,type=str,metavar=('romfile','page','bank','bankgroup','modgroup'))
parser.add_argument('-12',dest='rom12',nargs=5,type=str,metavar=('romfile','page','bank','bankgroup','modgroup'))
parser.add_argument('-13',dest='rom13',nargs=5,type=str,metavar=('romfile','page','bank','bankgroup','modgroup'))
parser.add_argument('-14',dest='rom14',nargs=5,type=str,metavar=('romfile','page','bank','bankgroup','modgroup'))
parser.add_argument('-15',dest='rom15',nargs=5,type=str,metavar=('romfile','page','bank','bankgroup','modgroup'))
parser.add_argument('-16',dest='rom16',nargs=5,type=str,metavar=('romfile','page','bank','bankgroup','modgroup'))
parser.add_argument('-17',dest='rom17',nargs=5,type=str,metavar=('romfile','page','bank','bankgroup','modgroup'))
parser.add_argument('-u1',dest='user1',type=str,help="Info menu configurable text line 1")
parser.add_argument('-u2',dest='user2',type=str,help="Info menu configurable text line 2")
parser.add_argument('-u3',dest='user3',type=str,help="Info menu configurable text line 3")
parser.add_argument('-u4',dest='user4',type=str,help="Info menu configurable text line 4")
parser.add_argument('-b',dest='bmpfile',type=str,help="BMP file for splash screen" )

args = vars(parser.parse_args())
arg_count = len(args)

try:
    ih = IntelHex(args['infile'])
except:
    print("Error reading hex file:",args['infile'])
    exit(1)

if ih[0] != MAGIC1 and ih[1] != MAGIC2:
    print("Error:",args['infile']," does not look like PX41CX firmware")
    exit(1)


if (arg_count - list(args.values()).count(None) == 1) or (not args['outfile'] and not args['bmpfile']):
    print("PX41CX Firmware:",args['infile'])
    for a in range(ROM_MAP_SIZE):
        page, bank, group, modgroup = get_rom(ih, a)
        if page != 255:
            print_rom(ih, a)
    print("User 1: '",ih.getsz(USER1).decode('utf-8'),"'",sep="")
    print("User 2: '",ih.getsz(USER2).decode('utf-8'),"'",sep="")
    print("User 3: '",ih.getsz(USER3).decode('utf-8'),"'",sep="")
    print("User 4: '",ih.getsz(USER4).decode('utf-8'),"'",sep="")
    exit(0)

newrom = IntelHex()
#blank = IntelHex()

ba = bytearray(b'\0' * 5120)

changed = False

for key in args:
    if args[key] and key.startswith("rom"):
        num = int(key[-2:])
        romfilename = args[key][0]
        read_rom(ba, romfilename)
        newrom.frombytes(ba, offset=ROM_LOCATION[num])
        ih.merge(newrom, overlap="replace")
        try:
            rom_map[num][0] = int(args[key][1],16)
            rom_map[num][1] = int(args[key][2]) - 1
            rom_map[num][2] = int(args[key][3])
            rom_map[num][3] = int(args[key][4])
            if rom_map[num][0] < 4 or rom_map[num][0] == 5:
                print("Error, OS page",rom_map[num][0],"selected")
                exit(1)
        except ValueError:
            print("Invalid argument:",-num," ".join(args[key]))
            exit(1)
        changed = True
        romname = "{:6.6}".format(romfilename.rsplit('.',1)[0])
        name_addr = ROM_NAMES + num * NAME_LEN
        ih.putsz(name_addr, romname)
    
rom_nonzero = [i for i in rom_map if any(i)]
unique_map = [list(x) for x in set(tuple(x) for x in rom_nonzero)]

if changed and len(rom_nonzero) > len(unique_map):
    print("Duplicate page map - no file output")
    exit(1)
else:
    if changed:
        for n in range(6, ROM_MAP_SIZE):
            if not args['merge'] and not any(rom_map[n]):
                set_rom(ih, n, 255, 255, 255, 255)
#                name_addr = ROM_NAMES + rom_map[n][0] * NAME_LEN
                name_addr = ROM_NAMES + n * NAME_LEN
                ih.putsz(name_addr, "EMPTY ")
            else:
               if any(rom_map[n]):
                   set_rom(ih, n, *rom_map[n])
    else:
        print("No ROM changes")


if args['user1'] != None:
    info = args['user1']
    ih.putsz(USER1, "{:31.31}".format(info))
    changed = True

if args['user2'] != None:
    info = args['user2']
    ih.putsz(USER2, "{:31.31}".format(info))
    changed = True

if args['user3'] != None:
    info = args['user3']
    ih.putsz(USER3, "{:31.31}".format(info))
    changed = True

if args['user4'] != None:
    info = args['user4']
    ih.putsz(USER4, "{:31.31}".format(info))
    changed = True

if args['bmpfile']:

    filename = args['bmpfile']

    try:
        f = open(filename, "rb")
    except:
        print("Error opening BMP file:",filename)
        exit(1)

    bmp = bytearray(f.read())
    f.close()

    if bmp[0] != 0x42 or bmp[1] != 0x4d:
        print("Error not a BMP file:",filename)
        exit(1)

    if bmp[0x1c] != 1:
        print("Error BMP depth not 1:",filename)
        exit(1)

    offset = bmp[11] * 256 + bmp[10]
    width = bmp[19] * 256 + bmp[18]
    width_pad = -(-width//32) * 32
    height = bmp[23] * 256 + bmp[22]

# Display is 250x122

    rleimg = bytearray(b'\x00' * IMAGE_SIZE)
    inverted = bmp[offset-2]
    total_bytes = 0
    for r in range(HEIGHT,0,-1):
        pixel_count = 0
        last_colour = 123
        for c in range(WIDTH):
            colour = access_bit(bmp, 8 * offset + (r-1) * width_pad + c)
            if inverted:
                if colour:
                    colour = 0
                else:
                    colour = 1
            if colour != last_colour:
                if pixel_count > 0:
                    rleimg[total_bytes] = pixel_count
                    total_bytes += 1
                    if total_bytes >= IMAGE_SIZE:
                        break
                if c == 0:
                    rleimg[total_bytes] = colour
                    total_bytes += 1
                pixel_count = 1
                last_colour = colour
            else:
                pixel_count += 1
        if total_bytes >= IMAGE_SIZE:
            break
        rleimg[total_bytes] = pixel_count
        total_bytes += 1
        if total_bytes >= IMAGE_SIZE:
            break

# Padding for display driver

    for r in range(10):
        try:
            rleimg[total_bytes] = 0
            rleimg[total_bytes+1] = 0xfa
            total_bytes += 2
        except:
            break

#    print("Total Bytes:",total_bytes)
#    print(rleimg)
    if total_bytes >= IMAGE_SIZE:
        print("BMP image too complex - not loaded:",filename)
    else:
        changed = True
        newrom.frombytes(rleimg, offset=SPLASH)
        ih.merge(newrom, overlap="replace")
    
####
if changed:
    ih.write_hex_file(args['outfile'], byte_count=16)
else:
    print("No change - no output file created")

