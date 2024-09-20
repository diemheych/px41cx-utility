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
#                          [-eng | -fre | -spa | -ger | -ita | -por]
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
# either version 3 of the License, or (at your option) any later version.
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
FW_VERSION = b'VER: '
DATE_ENG = b'JAN\x00FEB\x00MAR\x00APR\x00MAY\x00JUN\x00JUL\x00AUG\x00SEP\x00OCT\x00NOV\x00DEC\x00SUN\x00MON\x00TUE\x00WED\x00THU\x00FRI\x00SAT\x00'
DAY_ENG = b'SUN\x00MON\x00TUE\x00WED\x00THU\x00FRI\x00SAT\x00'
MONTH_ENG = b'JAN\x00FEB\x00MAR\x00APR\x00MAY\x00JUN\x00JUL\x00AUG\x00SEP\x00OCT\x00NOV\x00DEC\x00'
DATE_FRE = b'JAN\x00FEV\x00MAR\x00AVR\x00MAI\x00JUN\x00JUL\x00AOU\x00SEP\x00OCT\x00NOV\x00DEC\x00DIM\x00LUN\x00MAR\x00MER\x00JEU\x00VEN\x00SAM\x00'
DAY_FRE = b'DIM\x00LUN\x00MAR\x00MER\x00JEU\x00VEN\x00SAM\x00'
MONTH_FRE = b'JAN\x00FEV\x00MAR\x00AVR\x00MAI\x00JUN\x00JUL\x00AOU\x00SEP\x00OCT\x00NOV\x00DEC\x00'
DATE_SPA = b'ENE\x00FEB\x00MAR\x00ABR\x00MAY\x00JUN\x00JUL\x00AGO\x00SEP\x00OCT\x00NOV\x00DEC\x00DOM\x00LUN\x00MAR\x00MIE\x00JUE\x00VIE\x00SAB\x00'
DAY_SPA = b'DOM\x00LUN\x00MAR\x00MIE\x00JUE\x00VIE\x00SAB\x00'
MONTH_SPA = b'ENE\x00FEB\x00MAR\x00ABR\x00MAY\x00JUN\x00JUL\x00AGO\x00SEP\x00OCT\x00NOV\x00DEC\x00'
DATE_GER = b'JAN\x00FEB\x00MAR\x00APR\x00MAI\x00JUN\x00JUL\x00AUG\x00SEP\x00OKT\x00NOV\x00DEZ\x00SON\x00MON\x00DIE\x00MIT\x00DON\x00FRE\x00SAM\x00'
DAY_GER = b'SON\x00MON\x00DIE\x00MIT\x00DON\x00FRE\x00SAM\x00'
MONTH_GER = b'JAN\x00FEB\x00MAR\x00APR\x00MAI\x00JUN\x00JUL\x00AUG\x00SEP\x00OKT\x00NOV\x00DEZ\x00'
DATE_ITA = b'GEN\x00FEB\x00MAR\x00APR\x00MAG\x00GIU\x00LUG\x00AGO\x00SET\x00OTT\x00NOV\x00DIC\x00DOM\x00LUN\x00MAR\x00MER\x00GIO\x00VEN\x00SAB\x00'
DAY_ITA = b'DOM\x00LUN\x00MAR\x00MER\x00GIO\x00VEN\x00SAB\x00'
MONTH_ITA = b'GEN\x00FEB\x00MAR\x00APR\x00MAG\x00GIU\x00LUG\x00AGO\x00SET\x00OTT\x00NOV\x00DIC\x00'
DATE_POR = b'JAN\x00FEV\x00MAR\x00ABR\x00MAI\x00JUN\x00JUL\x00AGO\x00SET\x00OCT\x00NOV\x00DEZ\x00DOM\x00SEG\x00TER\x00QUA\x00QUI\x00SEX\x00SAB\x00'
DAY_POR = b'DOM\x00SEG\x00TER\x00QUA\x00QUI\x00SEX\x00SAB\x00'
MONTH_POR = b'JAN\x00FEV\x00MAR\x00ABR\x00MAI\x00JUN\x00JUL\x00AGO\x00SET\x00OCT\x00NOV\x00DEZ\x00'

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
        print("Error opening ROM file:",filename)
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
group = parser.add_mutually_exclusive_group()
group.add_argument("-eng", action="store_true",help="Set date strings to English")
group.add_argument("-fre", action="store_true",help="Set date strings to French")
group.add_argument("-spa", action="store_true",help="Set date strings to Spanish")
group.add_argument("-ger", action="store_true",help="Set date strings to German")
group.add_argument("-ita", action="store_true",help="Set date strings to Italian")
group.add_argument("-por", action="store_true",help="Set date strings to Portuguese")


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
    if (version := ih.find(FW_VERSION)) != -1:
        print(ih.getsz(version).decode('utf-8'))

    for a in range(ROM_MAP_SIZE):
        page, bank, group, modgroup = get_rom(ih, a)
        if page != 255:
            print_rom(ih, a)
    if ih.getsz(USER1).decode('unicode_escape').isprintable():
        print("User 1: '",ih.getsz(USER1).decode('unicode_escape'),"'",sep="")
    else:
        print("User 1: '",repr(ih.getsz(USER1))[2:-1],"'",sep="")
    if ih.getsz(USER2).decode('unicode_escape').isprintable():
        print("User 2: '",ih.getsz(USER2).decode('unicode_escape'),"'",sep="")
    else:
        print("User 2: '",repr(ih.getsz(USER2))[2:-1],"'",sep="")
    if ih.getsz(USER3).decode('unicode_escape').isprintable():
        print("User 3: '",ih.getsz(USER3).decode('unicode_escape'),"'",sep="")
    else:
        print("User 3: '",repr(ih.getsz(USER3))[2:-1],"'",sep="")
    if ih.getsz(USER4).decode('unicode_escape').isprintable():
        print("User 4: '",ih.getsz(USER4).decode('unicode_escape'),"'",sep="")
    else:
        print("User 4: '",repr(ih.getsz(USER4))[2:-1],"'",sep="")
    if ih.find(DATE_ENG) != -1:
        date_fmt = "English"
    elif ih.find(DATE_FRE) != -1:
        date_fmt = "French"
    elif ih.find(DATE_SPA) != -1:
        date_fmt = "Spanish"
    elif ih.find(DATE_GER) != -1:
        date_fmt = "German"
    elif ih.find(DATE_ITA) != -1:
        date_fmt = "Italian"
    elif ih.find(DATE_POR) != -1:
        date_fmt = "Portuguese"
    elif ih.find(DAY_ENG) != -1:
        date_fmt = "English"
    elif ih.find(DAY_FRE) != -1:
        date_fmt = "French"
    elif ih.find(DAY_SPA) != -1:
        date_fmt = "Spanish"
    elif ih.find(DAY_GER) != -1:
        date_fmt = "German"
    elif ih.find(DAY_ITA) != -1:
        date_fmt = "Italian"
    elif ih.find(DAY_POR) != -1:
        date_fmt = "Portuguese"
    else:
        date_fmt = "Unknown"
    print("Date Format: ",date_fmt)
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

if args['eng'] or args['fre'] or args['spa'] or args['ger'] or args['ita'] or args['por']:
    fw903plus = False
    lang = 0

    if (date_addr := ih.find(DATE_ENG)) != -1:
        fw903plus = True
        lang = 1
    elif (date_addr := ih.find(DATE_FRE)) != -1:
        fw903plus = True
        lang = 2
    elif (date_addr := ih.find(DATE_SPA)) != -1:
        fw903plus = True
        lang = 3
    elif (date_addr := ih.find(DATE_GER)) != -1:
        fw903plus = True
        lang = 4
    elif (date_addr := ih.find(DATE_ITA)) != -1:
        fw903plus = True
        lang = 5
    elif (date_addr := ih.find(DATE_POR)) != -1:
        fw903plus = True
        lang = 6
    elif (date_addr := ih.find(DAY_ENG)) != -1:
        lang = 1
    elif (date_addr := ih.find(DAY_FRE)) != -1:
        lang = 2
    elif (date_addr := ih.find(DAY_SPA)) != -1:
        lang = 3
    elif (date_addr := ih.find(DAY_GER)) != -1:
        lang = 4
    elif (date_addr := ih.find(DAY_ITA)) != -1:
        lang = 5
    elif (date_addr := ih.find(DAY_POR)) != -1:
        lang = 6
    else:
        pass

    if args['eng'] and lang:
        print("Set language: English")
        if fw903plus:
            ih.puts(date_addr, DATE_ENG)
            changed = True
        elif (month_addr := ih.find(MONTH_ENG)) != -1:
            ih.puts(date_addr, DAY_ENG)
            changed = True

    if args['fre'] and lang:
        print("Set language: French")
        if fw903plus:
            ih.puts(date_addr, DATE_FRE)
            changed = True
        elif (month_addr := ih.find(MONTH_FRE)) != -1:
            ih.puts(date_addr, DAY_FRE)
            changed = True

    if args['spa'] and lang:
        print("Set language: Spanish")
        if fw903plus:
            ih.puts(date_addr, DATE_SPA)
            changed = True
        elif (month_addr := ih.find(MONTH_SPA)) != -1:
            ih.puts(date_addr, DAY_SPA)
            changed = True

    if args['ger'] and lang:
        print("Set language: German")
        if fw903plus:
            ih.puts(date_addr, DATE_GER)
            changed = True
        elif (month_addr := ih.find(MONTH_GER)) != -1:
            ih.puts(date_addr, DAY_GER)
            changed = True

    if args['ita'] and lang:
        print("Set language: Italian")
        if fw903plus:
            ih.puts(date_addr, DATE_ITA)
            changed = True
        elif (month_addr := ih.find(MONTH_ITA)) != -1:
            ih.puts(date_addr, DAY_ITA)
            changed = True

    if args['por'] and lang:
        print("Set language: Portuguese")
        if fw903plus:
            ih.puts(date_addr, DATE_POR)
            changed = True
        elif (month_addr := ih.find(MONTH_POR)) != -1:
            ih.puts(date_addr, DAY_POR)
            changed = True
    if not changed:
        print("Error: Date strings not found")

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

