#!/usr/bin/python3

import collections
import networkx as nx

from data_type import *

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
            graph.add_edge(e[0], e[1])
    
        top_comp = self._getItemFromComponentList(self.top_assembly_id)
        T = nx.dfs_tree(graph, source=top_comp)
        return list(reversed(list(T)))  
