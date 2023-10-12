#!/usr/bin/python3

import collections
import networkx as nx
import copy

from roborecipe.data_type import *
from roborecipe.ComponentLoader import *

class QuantityItem:
    def __init__(self, comp, quantity):
        self.comp = comp
        self.quantity = quantity

class AssemblyDependencyAnalyzer:
    def __init__(self, component_list, top_assembly_id):
        self.component_list = component_list
        # dependency
        el = self._get_edge_list(top_assembly_id)
        self.dependency_list = self._get_dependency_order(el)
        # quantity
        self.assembly_list = self._get_assembly_list(top_assembly_id)

    def get_list(self):
        quantity_dir = collections.Counter(self.assembly_list)
        asm_list = []
        for comp in self.dependency_list:
            if comp.category.is_assembly():
                asm_list.append(QuantityItem(comp, quantity_dir[comp.id]))
        return asm_list

    def get_pkg_name_set(self):
        pkg_name_list = []
        for comp_id in self.assembly_list:
            pkg_name_list.append(comp_id.pkg_name)
        return set(pkg_name_list)

    def get_m_datetime(self):
        m_datetime_list = []
        for comp_id in self.assembly_list:
            comp = self.component_list.getComponent(comp_id)
            m_datetime_list.append(comp.m_datetime)
        return max(m_datetime_list)

    def _get_edge_list(self, component_id, parent=None):
        edge_list = []
        comp = self.component_list.getComponent(component_id)
        if comp is None:
            RED = '\033[31m'
            END = '\033[0m'
            print(RED + component_id.getName() + ' is empty' + END)
            return edge_list
        if parent is not None:
            edge_list.append([parent, comp])
        if comp.category.is_assembly():
            for step in comp.procedure_list:
                for c in step.component_list:
                    el = self._get_edge_list(c.id, comp)
                    edge_list.extend(el)
        return edge_list

    def _get_dependency_order(self, edge_list):
        graph = nx.DiGraph()
        for e in edge_list:
            graph.add_edge(e[1], e[0])
        T = nx.topological_sort(graph)
        return list(T)

    def _get_assembly_list(self, component_id):
        asm_list = []
        comp = self.component_list.getComponent(component_id)
        if comp is None:
            RED = '\033[31m'
            END = '\033[0m'
            print(RED + component_id.getName() + ' is empty' + END)
            return edge_list

        asm_list.append(comp.id)
        if comp.category.is_assembly():
            for step in comp.procedure_list:
                for c in step.component_list:
                    l = self._get_assembly_list(c.id)
                    asm_list.extend(l)
        return asm_list

class AssemblyTreeItem:
    def __init__(self, id, step_no, comp_no):
        self.id = id
        self.step_no = step_no
        self.comp_no = comp_no
    def __repr__(self):
        return self.id.getName()+'['+str(self.step_no)+','+str(self.comp_no)+']'

class AssemblyDisplayObject:
    def __init__(self, comp, step_no, transform, move):
        self.comp = comp
        self.step_no = step_no
        self.transform = transform
        self.move = move
    def __repr__(self):
        return '[' + str(self.step_no) + '] ' + self.comp.id.getName() + ' ' + str(self.transform) + ' ' + str(self.move)

class AssemblyTreeAnalyzer:
    def __init__(self, component_list, top_assembly_id):
        self.component_list = component_list
        self.tree_list = self._get_transform_tree(top_assembly_id)
        self.step_view_list = self._extract_step_view_list(top_assembly_id)

    def get_position_list(self):
        output_list = []
        for item_list in self.tree_list:
            transform = Transform()
            for item in item_list:
                assembly_item = self.component_list.getComponent(item.id)
                if (assembly_item is not None) and (item.step_no is not None) and (item.comp_no is not None):
                    asm_transform = assembly_item.procedure_list[item.step_no].component_list[item.comp_no].transform
                    transform = asm_transform * transform; 

            top_asm_item = item_list[-1]
            top_assemnly_item = self.component_list.getComponent(top_asm_item.id)
            move = top_assemnly_item.procedure_list[top_asm_item.step_no].component_list[top_asm_item.comp_no].move
            tip_item = item_list[0]
            output_list.append(AssemblyDisplayObject(self.component_list.getComponent(item_list[0].id), top_asm_item.step_no, transform, move))
        return output_list

    def get_quantity_list(self, category_enum):
        part_list = []
        for item_id_list in self.tree_list:
            comp = self.component_list.getComponent(item_id_list[0].id)
            if comp.category.value == category_enum:
                part_list.append(comp)
        quantity_dir = collections.Counter(part_list)

        part_list = []
        for comp in quantity_dir:
            part_list.append(QuantityItem(comp, quantity_dir[comp]))
        def key_func(obj):
            return obj.comp.id.getName()
        return sorted(part_list, key=key_func)

    def get_step_view_list(self):
        return self.step_view_list

    def _get_transform_tree(self, component_id):
        output_list = []
        parent_comp = self.component_list.getComponent(component_id)
        if parent_comp is None:
            RED = '\033[31m'
            END = '\033[0m'
            print(RED + component_id.getName() + ' is empty' + END)
            return output_list
        if parent_comp.category.is_assembly():
            output_list = []
            for step_no, step in enumerate(parent_comp.procedure_list):
                for comp_no, comp in enumerate(step.component_list):
                    sub_list = self._get_transform_tree(comp.id)
                    current_item = AssemblyTreeItem(parent_comp.id, step_no, comp_no)
                    for item_list in sub_list:
                        item_list.append(current_item)
                    output_list.extend(sub_list)
            return output_list
        else:
            return [[AssemblyTreeItem(parent_comp.id, None, None)]]

    def _extract_step_view_list(self, component_id):
        output_list = []
        parent_comp = self.component_list.getComponent(component_id)
        if parent_comp is None:
            RED = '\033[31m'
            END = '\033[0m'
            print(RED + component_id.getName() + ' is empty' + END)
            return output_list
        for step in parent_comp.procedure_list:
            output_list.append(step.view_list)
        return output_list

if __name__ == '__main__':
    component_path_list = [
        ComponentPathItem('screw_m3', '/home/ubuntu/workspace/roborecipe/sample/screw_m3', '/home/ubuntu/workspace/roborecipe/sample/screw_m3/roborecipe/pan_10.yaml'),
        ComponentPathItem('screw_m3', '/home/ubuntu/workspace/roborecipe/sample/screw_m3', '/home/ubuntu/workspace/roborecipe/sample/screw_m3/roborecipe/hollow_spacer_20.yaml'),
        ComponentPathItem('sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project/roborecipe/bar_plate.yaml'),
        ComponentPathItem('sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project/roborecipe/base_plate.yaml'),
        ComponentPathItem('sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project/roborecipe/side_asm.yaml'),
        ComponentPathItem('sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project/roborecipe/main_asm.yaml'),
    ]

    cll = ComponentListLoader()
    for path_item in component_path_list:
        cll.load(path_item)

    ada = AssemblyDependencyAnalyzer(cll, ComponentIdentifier('sample_project', 'main_asm'))

    print('#### Assembly ####')
    for item in ada.get_list():
        print(item.comp.id.getName(), item.quantity)

    ata = AssemblyTreeAnalyzer(cll, ComponentIdentifier('sample_project', 'main_asm'))

    print('#### Screw ####')
    for item in ata.get_quantity_list(ComponentCategoryEnum.SCREW):
        print(item.comp.id.getName(), item.quantity)
    print('#### LaserCut ####')
    for item in ata.get_quantity_list(ComponentCategoryEnum.LASER_CUT):
        print(item.comp.id.getName(), item.quantity)
    print('#### END ####')


    for item in ata.get_position_list():
        print(item.step_no,item.comp.rigit_body.mesh_filepath)

    for view_list in ata.get_step_view_list():
        print(view_list)