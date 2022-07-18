#!/usr/bin/python3

import collections
import networkx as nx
import copy

from roborecipe.data_type import *

class TreeAnalyzer:
    def __init__(self, component_list, top_assembly_id):
        self.component_list = component_list
        self.top_assembly_id = top_assembly_id

    def getQuantityList(self):
        dl = self._getDuplicateList(self.top_assembly_id)
        return collections.Counter(dl)

    def getDependOrderList(self):
        el = self._getEdgeList(self.top_assembly_id)
        return self._getDependOrder(el)

    def _getDuplicateList(self, component_id):
        part_list = []
        comp = self._getItemFromComponentList(component_id)
        if type(comp) is DataPart:
            part_list.append(comp)
        elif type(comp) is DataAssembly:
            part_list.append(comp)
            for s in comp.step_list:
                for c in s.child_list:
                    l = self._getDuplicateList(c.id)
                    part_list.extend(l)
        return part_list

    def _getItemFromComponentList(self, id):
        for c in self.component_list:
            if c.id == id:
                return c
        return None

    def _getEdgeList(self, component_id, parent=None):
        edge_list = []
        comp = self._getItemFromComponentList(component_id)
        if parent is not None:
            edge_list.append([parent, comp])
        if type(comp) is DataAssembly:
            for s in comp.step_list:
                for c in s.child_list:
                    el = self._getEdgeList(c.id, comp)
                    edge_list.extend(el)
        return edge_list

    def _getDependOrder(self, edge_list):
        graph = nx.DiGraph()
        for e in edge_list:
            graph.add_edge(e[1], e[0])

        top_comp = self._getItemFromComponentList(self.top_assembly_id)
        T = nx.topological_sort(graph)
        return list(T)

class ItemWithTransformList:
    def __init__(self, component, transform_list=[]):
        self.component = component
        self.transform_list = transform_list
        self.step = 0
        self.move = [0, 0, 0]
    def AddParentTransform(self, transform):
        self.transform_list.insert(0, transform)
    def GetWholeTransform(self):
        output = Transform()
        for t in self.transform_list:
            output = output * t
        return output

class RenderTree:
    def __init__(self, component_list, depend_list):
        self.component_list = component_list
        self.depend_list = depend_list
        self.iwtl_list_dict = {}
        for comp in depend_list:
            self.iwtl_list_dict[comp] = self._ExpandComponent(comp)

    def GetItemListWithTransform(self, target_id):
        for comp in self.iwtl_list_dict:
            if comp.id == target_id:
                return self.iwtl_list_dict[comp]

    def _ExpandComponent(self, component):
        output_list = []
        if type(component) is DataPart:
            output_list.append(ItemWithTransformList(component, [Transform()]))
        elif type(component) == DataAssembly:
            step_seq_no = 0
            for s in component.step_list:
                for c in s.child_list:
                    child_item_list = self.GetItemListWithTransform(c.id)
                    move = [c.move.x, c.move.y, c.move.z]
                    for ci in child_item_list:
                        new_ci = copy.deepcopy(ci)
                        new_ci.AddParentTransform(c.transform)
                        new_ci.step = step_seq_no
                        new_ci.move = move
                        output_list.append(new_ci)
                step_seq_no += 1
        return output_list

