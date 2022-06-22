#!/usr/bin/python3

import os
from glob import glob
import xml.etree.ElementTree as ET
import pathlib
from data_type import *

class PackageParser:
	def __init__(self, path):
		tree = ET.parse(str(pathlib.Path(path).resolve()))
		self.root = tree.getroot()
	def getName(self):
		return self.root.find("name").text

class PartConverter:
    def __init__(self):
        None

class ComponentParser:
	def __init__(self, pkg_path, component_path):
		pkg_name = PackageParser(pkg_path).getName()
		tree = ET.parse(str(pathlib.Path(component_path).resolve()))
		root = tree.getroot()

		if root.tag == 'part':
			self.component = self.ParsePart(pkg_name, root)
		elif root.tag == 'assembly':
			self.component = self.ParseAssembly(pkg_name, root)
		else:
			self.component = DataComponent()

	def ParsePart(self, pkg_name, root):
		component_name = root.find("name").text

		if root.find("stf_file"):
			stl_file_name = root.find("stf_file").text
		else:
			stl_file_name = ""

		part = DataPart()
		part.id = ComponentIdentifier(pkg_name, component_name)
		part.price_value = 0
		part.price_unit = "yen"
		part.url = 'http:/sample.com/sample.html'
		part.description = "description"
		part.stl_path = stl_file_name
		return part

	def ParseAssembly(self, pkg_name, root):
		component_name = root.find("name").text
		asm = DataAssembly()
		asm.id = ComponentIdentifier(pkg_name, component_name)
		for s in root.iter("step"):
			step = DataAssemblyStep()
			for c in s.iter("component"):
				child = DataAssemblyStepChild()
				child.id = ComponentIdentifier(c.attrib["pkg"], c.attrib["type"])
				step.child_list.append(child)
			asm.step_list.append(step)
		return asm

class ComponentListParser:
	def __init__(self, path_pair_list):
		self.component_list = []
		for pp in path_pair_list:
			self.component_list.append(ComponentParser(pp[0], pp[1]).component)
	def getList(self):
		return self.component_list
			


if __name__ == '__main__':
	path_pair_list = [
		['../sample/srs007/package.xml', '../sample/srs007/main_asm/assemble.roborecipe'],
		['../sample/srs007/package.xml', '../sample/srs007/base_asm/assemble.roborecipe'],
		['../sample/pololu/package.xml', '../sample/pololu/4691_37mm_motor/description.roborecipe'],
		['../sample/iso_screw_m3/package.xml', '../sample/iso_screw_m3/pan_12/part.roborecipe']
	]
	for c in ComponentListParser(path_pair_list).getList():
		print(c.id.getName())

