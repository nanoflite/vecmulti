import argparse
import glob
import os
import sys
from itertools import chain, product
from os.path import basename, splitext
from shutil import copyfile
from string import ascii_uppercase

import serial


def tell(args, message):
    if args.verbose:
        print(message)


def bar(value, end_value, bar_length):
    percent = float(value) / end_value
    hashes = "#" * int(round(percent * bar_length))
    spaces = " " * (bar_length - len(hashes))
    sys.stdout.write("\rLoading: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
    sys.stdout.flush()


def load(args):
    port = "/dev/ttys0" if args.port is None else args.port
    size = os.stat(args.rom).st_size
    tell(args, "Loader")
    tell(args, " file: %s" % args.rom)
    tell(args, " port: %s" % port)
    tell(args, "Open serial port")
    ser = serial.Serial(port, 115200)
    tell(args, "Writing ROM file")
    ser.write(b"s")
    with open(args.rom, "rb") as rom:
        i = 0
        while True:
            byte = rom.read(1)
            if not byte:
                break
            ser.write(b"@")
            ser.write(byte)
            verify = ser.read(1)
            if verify != byte:
                print("error:%d" % i)
            i += 1
            tell(args, "%d/%d" % (i, size))
            if args.progress:
                bar(i, size, 40)
    ser.write(b"y")
    ser.close()
    if args.progress:
        sys.stdout.write("\n")
    tell(args, "Done")


def generate_menu_name():
    while True:
        for p in product(ascii_uppercase, repeat=2):
            yield "%s.men" % "".join(p)


def menu(args):
    tell(args, "Make menu")
    tell(args, " from:    %s" % args.source)
    tell(args, " to:      %s" % args.destination)

    tell(args, "Deleting existing files")
    for game in glob.iglob("%s/*.men" % args.destination):
        tell(args, " remove '%s'" % game)
        os.remove(game)

    tell(args, "Create destination files")
    menu_names = generate_menu_name()
    entries = []
    for game in sorted(chain(glob.iglob("%s/*.bin" % args.source), glob.iglob("%s/*.BIN" % args.source))):
        menu_name = next(menu_names)
        tell(args, " %s --> %s/%s" % (game, args.destination, menu_name))
        copyfile(game, "%s/%s" % (args.destination, menu_name))
        entries.append(splitext(basename(game))[0])

    tell(args, "Create index file")
    with open("%s/Titles.rtf" % args.destination, "w") as index:
        high, low = divmod(len(entries), 0x100)
        index.write("%c%c%c" % (high, low, 13))
        for game in entries:
            index.write("|%s|%c" % (game.ljust(13, " ")[:13], 13))

    tell(args, "Done")


def build_parser():
    parser = argparse.ArgumentParser(prog="vecmulti")
    parser.add_argument("--verbose", help="Show what is going on.", action="store_true")
    subparsers = parser.add_subparsers(help="command help", dest="command", required=True)

    parser_load = subparsers.add_parser("load", help="Load a program into the the Vectrex using the VecMulti dev mode.")
    parser_load.add_argument("--port", help="Specify connection port.")
    parser_load.add_argument("--progress", help="Show a progress bar.", action="store_true")
    parser_load.add_argument("rom", help="ROM file to upload to Vectrex.")
    parser_load.set_defaults(func=load)

    parser_menu = subparsers.add_parser("menu", help="Create a menu to use on the VecMulti cartridge.")
    parser_menu.add_argument("source", help="Source folder containing games (*.bin files).")
    parser_menu.add_argument("destination", help="Destination folder.")
    parser_menu.set_defaults(func=menu)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)