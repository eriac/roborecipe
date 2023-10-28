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

# newlib
from roborecipe.DirectoryLoader import * 
from roborecipe.AssemblyAnalyzer import * 
from roborecipe.TopPageGenerator import * 
from roborecipe.PartsPageGenerator import *
from roborecipe.PartImageGenerator import *


def getTargetDirectory(target, default = ''):
    if target is None:
        output = pathlib.Path(default).resolve()
    else:
        output = pathlib.Path(str(target)).resolve()
    return output

def getCurrentDirectory():
    return str(pathlib.Path(__file__+'/..').resolve())

def output_list_data(target_directory):
    dl = DirectoryLoader(target_directory)
    component_path_list = []
    for component in dl.get_component_path_list(): 
        component_path_list.append(component)

    cll = ComponentListLoader()
    for path_item in component_path_list:
        cll.load(path_item)

    for comp in cll.getList():
        print(comp.id.getName())


def generateInstruction(target_directory, output_directory, pkg_name, type_name, top_level_only):
    # clear_panda3d_cashe()
    print(pkg_name, type_name)

    dl = DirectoryLoader(target_directory)
    out_ds = OutputDirectorySearch(output_directory)
    component_path_list = []
    for component in dl.get_component_path_list(): 
        component_path_list.append(component)

    cll = ComponentListLoader()
    for path_item in component_path_list:
        cll.load(path_item)

    top_assembly_id = ComponentIdentifier(pkg_name, type_name)
    ata = AssemblyTreeAnalyzer(cll, top_assembly_id)
    ada = AssemblyDependencyAnalyzer(cll, top_assembly_id)

    # top page
    tg = TopPageGenerator(top_assembly_id, ata, ada)
    tg.write(output_directory)

    # package copy
    used_pkg_name_set = ada.get_pkg_name_set()
    dl.copy_resouces_dir(used_pkg_name_set, output_directory)

    # part page (screw)
    for item in ata.get_quantity_list(ComponentCategoryEnum.SCREW):
        # image
        mpig = MechanicalPartsImageGenerator(item.comp)
        if out_ds.need_update_image(mpig.get_pkg_name(), mpig.get_m_datetime()):
            mpig.write(output_directory)
        else:
            print('skip image')

        # html
        mpg = MechanicalPartsPageGenerator(item.comp)
        mpg.write(output_directory)

    # part page (mechanical)
    for item in ata.get_quantity_list(ComponentCategoryEnum.MECHANICAL_ITEN):
        # image
        mpig = MechanicalPartsImageGenerator(item.comp)
        if out_ds.need_update_image(mpig.get_pkg_name(), mpig.get_m_datetime()):
            mpig.write(output_directory)
        else:
            print('skip image')

        # html
        mpg = MechanicalPartsPageGenerator(item.comp)
        mpg.write(output_directory)

    # part page (laser_cut)
    for item in ata.get_quantity_list(ComponentCategoryEnum.LASER_CUT):
        # image
        mpig = MechanicalPartsImageGenerator(item.comp)
        if out_ds.need_update_image(mpig.get_pkg_name(), mpig.get_m_datetime()):
            mpig.write(output_directory)
        else:
            print('skip image')

        # html
        mpg = ProcessPartsPageGenerator(item.comp)
        mpg.write(output_directory)

    # part page (3d_print)
    for item in ata.get_quantity_list(ComponentCategoryEnum.PRINT_3D):
        # image
        mpig = MechanicalPartsImageGenerator(item.comp)
        if out_ds.need_update_image(mpig.get_pkg_name(), mpig.get_m_datetime()):
            mpig.write(output_directory)
        else:
            print('skip image')

        # html
        mpg = ProcessPartsPageGenerator(item.comp)
        mpg.write(output_directory)

    # part page (order)
    for item in ata.get_quantity_list(ComponentCategoryEnum.ORDER):
        # image
        mpig = MechanicalPartsImageGenerator(item.comp)
        if out_ds.need_update_image(mpig.get_pkg_name(), mpig.get_m_datetime()):
            mpig.write(output_directory)
        else:
            print('skip image')

        # html
        mpg = ProcessPartsPageGenerator(item.comp)
        mpg.write(output_directory)

    # part page (electrical)
    for item in ata.get_quantity_list(ComponentCategoryEnum.ELECTRIC_ITEM):
        # image
        mpig = MechanicalPartsImageGenerator(item.comp)
        if out_ds.need_update_image(mpig.get_pkg_name(), mpig.get_m_datetime()):
            mpig.write(output_directory)
        else:
            print('skip image')

        # html
        mpg = MechanicalPartsPageGenerator(item.comp)
        mpg.write(output_directory)

    # part page (board)
    for item in ata.get_quantity_list(ComponentCategoryEnum.BOARD):
        # image
        mpig = MechanicalPartsImageGenerator(item.comp)
        if out_ds.need_update_image(mpig.get_pkg_name(), mpig.get_m_datetime()):
            mpig.write(output_directory)
        else:
            print('skip image')

        # html
        mpg = ProcessPartsPageGenerator(item.comp)
        mpg.write(output_directory)

    # part page (assembly)
    for item in ada.get_list():
        # image
        ata = AssemblyTreeAnalyzer(cll, item.comp.id)
        aig = AssemblyImageGenerator(item.comp, ata.get_position_list(), ata.get_step_view_list())
        asm_m_datetime = AssemblyDependencyAnalyzer(cll, item.comp.id).get_m_datetime()

        if out_ds.need_update_image(aig.get_pkg_name(), asm_m_datetime):
            aig.write(output_directory)
        else:
            print('skip image')

        # html
        apg = AssemblyPageGenerator(item.comp)
        apg.write(output_directory)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("command", help="sub command (list/generate)", type=str)
    parser.add_argument('option', nargs='*', default="")
    parser.add_argument("-d", "--directory", help="target directory")
    parser.add_argument("-o", "--output", help="output directory")
    parser.add_argument('-t', '--top_level_only', help='generate top level image only', action='store_true')
    args = parser.parse_args()

    target_directory = getTargetDirectory(args.directory, '')
    print('target directory: ' + str(target_directory))
    output_directory = getTargetDirectory(args.output, 'out')
    print('output directory: ' + str(output_directory))

    if args.command == "list":
        output_list_data(target_directory)

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
