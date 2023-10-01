#!/usr/bin/python3

import os
import sys
import pathlib
import argparse

# lib
from roborecipe.XmlParser import *
from roborecipe.TreeAnalyzer import *
from roborecipe.DirectorySearch import *
from roborecipe.HtmlGenerator import *
from roborecipe.ViewListGenerator import *

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("command", help="sub command (list/generate)", type=str)
    parser.add_argument('option', nargs='*', default="")
    parser.add_argument("-d", "--directory", help="target directory")
    parser.add_argument("-o", "--output", help="output directory")
    parser.add_argument('-t', '--top_level_only', help='generate top level image only', action='store_true')
    args = parser.parse_args()

    target_directory = getTargetDirectory(args.directory)
    print('target directory: ' + str(target_directory))
    output_directory = getTargetDirectory(args.output)
    print('output directory: ' + str(output_directory))

    if args.command == "list":
        ds = DirectorySearch(target_directory)
        print("### package ###")
        for p in ds.getPackagePathList():
            print(p)
        print("### component ###")
        for c in ds.getComponentPathPairList():
            print(c[1])

    elif args.command == "generate":
        print("### generate ###")
        if len(args.option) != 2:
            print("tree must be 2 option")
            exit()
        pkg_name = args.option[0]
        type_name = args.option[1]
        generateInstruction(target_directory,output_directory, pkg_name, type_name, args.top_level_only)

    else:
        print("command error")

if __name__ == '__main__':
    main()
