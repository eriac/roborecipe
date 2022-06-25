#!/usr/bin/python3

import argparse
import os
import pathlib
from glob import glob
import os
import sys
import networkx as nx

# lib
from roborecipe import parse

from XmlParser import *
from TreeAnalyzer import *
from DirectorySearch import *
from HtmlGenerator import *
from ViewListGenerator import *

def getTargetDirectory(target):
    if target is None:
        output = pathlib.Path('').resolve()
    else:
        output = pathlib.Path(str(target)).resolve()
    return output

def generateInstruction(target_directory,output_directory, pkg_name, type_name):
    os.makedirs(output_directory, exist_ok=True)

    ds = DirectorySearch(target_directory)
    path_pair_list = ds.getComponentPathPairList()
    component_list = ComponentListParser(path_pair_list).getList()
    ta = TreeAnalyzer(component_list, ComponentIdentifier(pkg_name, type_name))

    html_generator = HtmlGenerator()
    html_generator.template_path = 'templates/index.html'
    html_generator.title = ComponentIdentifier(pkg_name, type_name).getName()

    ## part list
    ql = ta.getQuantityList()
    for comp in ql:
        if type(comp) is DataPart:
            print(comp.id.getName(), ql[comp])
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
                print(image_file)
                s1.image_path_list.append(image_file)
            a1.step_list.append(s1)
            seq_no += 1
        html_generator.assembly_list.append(a1) 

    html_generator.generate(str(output_directory)+"/g_index.html")

    ## asm image
    rt = RenderTree(component_list, dl)
    vlg = ViewListGenerator(dl, rt)
    render_view_list = vlg.GetViewList(str(output_directory))
    ig = ImageGenerator(sys.argv)
    ig.renderViewList(render_view_list) # TODO force finish

def print_package_list(package_list):
    for p in package_list:
        print(p.name, p.path)

def print_component_list(component_list):
    for p in component_list:
        print(p.getStr())

def get_component(component_list, pkg_name, comp_name):
    for c in component_list:
        if c.package_name == pkg_name and c.component_name == comp_name:
            return c
    return None

def print_target_component_tree(component_list, target_component, level):
    spaces = "  " * level
    print(spaces + target_component.getFullName())

    if type(target_component) == parse.Assembly:
        for i in target_component.component_list:
            component = get_component(component_list, i.package_name, i.component_name)
            if component is None:
                print(i.package_name + " " + i.component_name + " is None")
                continue
            print_target_component_tree(component_list, component, level+1)


def print_component_tree(component_list, pkg_name, comp_name):
    root_component = get_component(component_list, pkg_name, comp_name)
    if root_component is None:
        print(pkg_name + " " + comp_name + " is None")
    print_target_component_tree(component_list, root_component, 0)

    # stack = [root_component, 0]

    # spaces = "  " * len(stack)
    # print(spaces + root_component.getFullName())
    # if type(root_component) == parse.Assembly:
    #     stack.append(0)
    #     target_list = root_component.component_list
    #     for i in target_list:
    #         component = get_component(component_list, i.package_name, i.component_name)
    #         if component is None:
    #             print(i.package_name + " " + i.component_name + " is None")

    #         spaces = "  " * len(stack)
    #         print(spaces + component.getFullName())

def get_target_component_tree(component_list, target_component, level):
    spaces = "  " * level
    # print("#" + spaces + target_component.getFullName())

    part_list = []
    part_list.append(target_component)
    if type(target_component) == parse.Assembly:
        for i in target_component.component_list:
            component = get_component(component_list, i.package_name, i.component_name)
            if component is None:
                print(i.package_name + " " + i.component_name + " is None")
                continue
            part_list.extend(get_target_component_tree(component_list, component, level+1))
    
    return part_list


def print_component_quantity(component_list, pkg_name, comp_name):
    root_component = get_component(component_list, pkg_name, comp_name)
    if root_component is None:
        print(pkg_name + " " + comp_name + " is None")
    part_list = get_target_component_tree(component_list, root_component, 0)

    quantity_dir = {}
    for p in part_list:
        if (p in quantity_dir):
            quantity_dir[p] = quantity_dir[p] + 1
        else:
            quantity_dir[p] = 1

    for i in quantity_dir:
        component = i
        quantity = quantity_dir[i]
        print(component.getFullName() + " " + str(quantity))


def get_edge_list(component_list, graph, component):
    if type(component) == parse.Assembly:
        for c in component.component_list:
            sub = get_component(component_list, c.package_name, c.component_name)
            if sub is None:
                continue
            graph.add_edge(component, sub)
            get_edge_list(component_list, graph, sub)

def get_depend_list(component_list, pkg_name, comp_name):
    root_component = get_component(component_list, pkg_name, comp_name)
    if root_component is None:
        print(pkg_name + " " + comp_name + " is None")

    graph = nx.DiGraph()
    get_edge_list(component_list, graph, root_component)
 
    T = nx.dfs_tree(graph, source=root_component)
    return list(T)

def get_quantity_dir(component_list, pkg_name, comp_name):
    quantity_dir = {}

    root_component = get_component(component_list, pkg_name, comp_name)
    if root_component is None:
        print(pkg_name + " " + comp_name + " is None")

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


    # # get package list
    # package_list = parse.get_package_list(str(target_directory))

    # # get component list
    # component_list = []
    # for p in package_list:
    #     component_list.extend(parse.get_component_list(p))

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

    # elif args.command == "show":
    #     print("### show ###")
    #     if len(args.option) != 2:
    #         print("tree must be 2 option")
    #         exit()
    #     pkg_name = args.option[0]
    #     comp_name = args.option[1]
    #     comp = get_component(component_list, pkg_name, comp_name)
    #     if comp is None:
    #         print("not found " + pkg_name + "/" + comp_name)
    #         exit()
        
    #     show_msg = comp.show()
    #     print(show_msg)


    # elif args.command == "tree":
    #     print("### tree ###")
    #     if len(args.option) != 2:
    #         print("tree must be 2 option")
    #         exit()
    #     pkg_name = args.option[0]
    #     comp_name = args.option[1]
    #     print_component_tree(component_list, pkg_name, comp_name)

    # elif args.command == "quantity":
    #     print("### quantity ###")
    #     if len(args.option) != 2:
    #         print("tree must be 2 option")
    #         exit()
    #     pkg_name = args.option[0]
    #     comp_name = args.option[1]
    #     print_component_quantity(component_list, pkg_name, comp_name)

    # elif args.command == "order":
    #     print("### order ###")
    #     if len(args.option) != 2:
    #         print("order must be 2 option")
    #         exit()
    #     pkg_name = args.option[0]
    #     comp_name = args.option[1]
    #     depend_list = get_depend_list(component_list, pkg_name, comp_name)
    #     for c in depend_list:
    #         print(c.getFullName())

    else:
        print("command error")

if __name__ == '__main__':
    main()