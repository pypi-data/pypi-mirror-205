#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Auther : MR_GT

import sys
import requests
from .utils import *




def Main():
    color()

    try: Commands = sys.argv[1]
    except IndexError: Commands = False

    try: CommandArguments = sys.argv[2:]
    except IndexError: CommandArguments = False

    try: Arguments = sys.argv[3:]
    except IndexError: Arguments = ""

    if (Commands):
        # install
        if (Commands == "i") or (Commands == "-i") or (Commands == "--i") or (Commands == "install") or (Commands == "-install") or (Commands == "--install") or (Commands == "--clone") or (Commands == "--clone") or (Commands == "--clone"):
            if (Internet):
                if (len(CommandArguments) != 1):
                    print(f"\n{magenta}[{white}!{magenta}] {white}The install command requires 1 argument, but {len(CommandArguments)} were provided"), exit()
                else:
                    Install(CommandArguments[0])
                    version = requests.get("https://raw.githubusercontent.com/GreyTechno/gtf/main/.info").json()["version"]
                    if (__VERSION__ != version):
                        print(f"\n{magenta}[{white}!{magenta}] {white}A new release of GTF is available: {blue}{__VERSION__} {red}➟  {yellow}{version}")
                        print(f"{magenta}[{white}!{magenta}] {white}To update, run {red}➟  {yellow}gtf --update{reset}")
                        exit()
            else: print(f"{magenta}[{white}!{magenta}] {white}Check your internet connection...{reset}"), exit()
        # run
        elif (Commands == "r") or (Commands == "-r") or (Commands == "--r") or (Commands == "run") or (Commands == "-run") or (Commands == "--run") or (Commands == "--start") or (Commands == "--start") or (Commands == "--start"):
            Run(CommandArguments[0], Arguments)
        # uninstall
        elif (Commands == "remove") or (Commands == "-remove") or (Commands == "--remove") or (Commands == "uninstall") or (Commands == "-uninstall") or (Commands == "--uninstall"):
            if (len(CommandArguments) != 1):
                print(f"\n{magenta}[{white}!{magenta}] {white}The uninstall command requires 1 argument, but {len(CommandArguments)} were provided"), exit()
            else:
                Uninstall(CommandArguments[0])
        # self update
        elif (Commands == "gtf.update") or (Commands == "-gtf.update") or (Commands == "--gtf.update"):
            if (Internet): Update()
            else: print(f"{magenta}[{white}!{magenta}] {white}Check your internet connection...{reset}"), exit()
        # download
        elif (Commands == "d") or (Commands == "-d") or (Commands == "--d") or (Commands == "download") or (Commands == "-download") or (Commands == "--download"):
            if (len(CommandArguments) != 1):
                print(f"\n{magenta}[{white}!{magenta}] {white}The download command requires 1 argument, but {len(CommandArguments)} were provided"), exit()
            else:
                Download(CommandArguments[0])
        # list of installed programs
        elif (Commands == "l") or (Commands == "-l") or (Commands == "--l") or (Commands == "list") or (Commands == "-list") or (Commands == "--list"):
            List()
        # version
        elif (Commands == "v") or (Commands == "-v") or (Commands == "--v") or (Commands == "version") or (Commands == "-version") or (Commands == "--version"):
            Version()
        # help
        elif (Commands == "h") or (Commands == "-h") or (Commands == "--h") or (Commands == "help") or (Commands == "-help") or (Commands == "--help"):
            Help()
        else: Help()
    else:
        Help()


if (__name__ == "__main__"):
    Main()
