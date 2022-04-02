import requests
import sys
from roborecipe import *

import argparse
import os
import pathlib
from glob import glob
import os
import sys
import networkx as nx

def main() -> None:
    print(sys.argv)

    parser = argparse.ArgumentParser()

    parser.add_argument("command", help="sub command (list/tree/generate)", type=str)
    parser.add_argument('option', nargs='*', default="")
    parser.add_argument("-d", "--directory", help="target directory")
    parser.add_argument("-o", "--output", help="output directory")
    args = parser.parse_args()


    if args.command == "list":
        print("### package ###")
    elif args.command == "show":
        print("### show ###")
    else:
        print("command error")