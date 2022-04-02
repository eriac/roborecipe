#!/usr/bin/python3

import argparse
import os
import pathlib
from glob import glob
import os
import sys
import networkx as nx

# lib
import parse

def getTargetDirectory(target):
    output = pathlib.Path(target).resolve()
    return output


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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("command", help="sub command (list/tree/generate)", type=str)
    parser.add_argument('option', nargs='*', default="")
    parser.add_argument("-d", "--directory", help="target directory")
    parser.add_argument("-o", "--output", help="output directory")
    args = parser.parse_args()

    target_directory = getTargetDirectory(args.directory)
    
    # get package list
    package_list = parse.get_package_list(str(target_directory))

    # get component list
    component_list = []
    for p in package_list:
        component_list.extend(parse.get_component_list(p))

    if args.command == "list":
        print("### package ###")
        print_package_list(package_list)
        print("### component ###")
        print_component_list(component_list)
    elif args.command == "show":
        print("### show ###")
        if len(args.option) != 2:
            print("tree must be 2 option")
            exit()
        pkg_name = args.option[0]
        comp_name = args.option[1]
        comp = get_component(component_list, pkg_name, comp_name)
        if comp is None:
            print("not found " + pkg_name + "/" + comp_name)
            exit()
        
        show_msg = comp.show()
        print(show_msg)

    elif args.command == "tree":
        print("### tree ###")
        if len(args.option) != 2:
            print("tree must be 2 option")
            exit()
        pkg_name = args.option[0]
        comp_name = args.option[1]
        print_component_tree(component_list, pkg_name, comp_name)

    elif args.command == "order":
        print("### order ###")
        if len(args.option) != 2:
            print("order must be 2 option")
            exit()
        pkg_name = args.option[0]
        comp_name = args.option[1]
        depend_list = get_depend_list(component_list, pkg_name, comp_name)
        for c in depend_list:
            print(c.getFullName())

    else:
        print("command error")