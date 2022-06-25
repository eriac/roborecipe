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

def getTargetDirectory(target):
    if target is None:
        output = pathlib.Path('').resolve()
    else:
        output = pathlib.Path(str(target)).resolve()
    return output

def getCurrentDirectory():
    return str(pathlib.Path(__file__+'/..').resolve())

def generateInstruction(target_directory,output_directory, pkg_name, type_name):
    os.makedirs(output_directory, exist_ok=True)

    ds = DirectorySearch(target_directory)
    path_pair_list = ds.getComponentPathPairList()
    component_list = ComponentListParser(path_pair_list).getList()
    ta = TreeAnalyzer(component_list, ComponentIdentifier(pkg_name, type_name))

    html_generator = HtmlGenerator()
    html_generator.template_path = getCurrentDirectory() +'/templates/index.html'
    html_generator.title = ComponentIdentifier(pkg_name, type_name).getName()

    ## part list
    ql = ta.getQuantityList()
    for comp in ql:
        if type(comp) is DataPart:
            p1 = HtmlParchageItem()
            p1.id = comp.id
            p1.quantity = ql[comp]
            html_generator.part_list.append(p1)

    ## asm list
    dl = ta.getDependOrderList()
    for comp in dl:
        if type(comp) is not DataAssembly:
            continue
        a1 = HtmlAssemblyItem()
        a1.name = comp.id.getName()
        a1.quantity = ql[comp]
        seq_no = 0
        for s in comp.step_list:
            s1 = HtmlAssemblyStep()
            s1.seq_no = seq_no+1
            for child in s.child_list:
                s1.component_list.append(HtmlComponentItem(child.id.pkg_name, child.id.type_name, 1))
            for view_seq_no in range(len(s.view_list)):
                image_file = str(comp.id.pkg_name)+'/'+str(comp.id.type_name)+'/asm_'+str(seq_no)+'_'+str(view_seq_no)+'.gif'
                s1.image_path_list.append(image_file)
            a1.step_list.append(s1)
            seq_no += 1
        html_generator.assembly_list.append(a1) 

    html_generator.generate(str(output_directory)+"/index.html")

    ## asm image
    rt = RenderTree(component_list, dl)
    vlg = ViewListGenerator(dl, rt)
    render_view_list = vlg.GetViewList(str(output_directory))
    ig = ImageGenerator(sys.argv)
    ig.renderViewList(render_view_list) # TODO force finish

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("command", help="sub command (list/generate)", type=str)
    parser.add_argument('option', nargs='*', default="")
    parser.add_argument("-d", "--directory", help="target directory")
    parser.add_argument("-o", "--output", help="output directory")
    args = parser.parse_args()

    target_directory = getTargetDirectory(args.directory)
    print('target directory: ' + str(target_directory))
    output_directory = getTargetDirectory(args.output)
    print('target directory: ' + str(output_directory))

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
        generateInstruction(target_directory,output_directory, pkg_name, type_name)

    else:
        print("command error")

if __name__ == '__main__':
    main()