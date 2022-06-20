#!/usr/bin/python3

class ComponentName:
    def __init__(self):
        self.package_name = ""
        self.item_name = ""
    def __init__(self, pkg_name, item_name):
        self.package_name = pkg_name
        self.item_name = item_name

class TreeComponent:
    def __init__(self):
        self.root_component_name = ComponentName()


class TreeNode:
    def __init__(self):
        self.componentName = ComponentName()
        self.childlen = []
        self.
    
