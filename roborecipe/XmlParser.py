#!/usr/bin/python3

import os
from glob import glob
import xml.etree.ElementTree as ET
import pathlib
from roborecipe.data_type import *

class PackageParser:
	def __init__(self, path):
		self.path = path
		tree = ET.parse(str(pathlib.Path(path).resolve()))
		self.root = tree.getroot()
	def getName(self):
		return self.root.find("name").text
	def getDirPath(self):
		return str(pathlib.Path(self.path+"/..").resolve())

class PartConverter:
    def __init__(self):
        None

class ComponentParser:
	def __init__(self, pkg_path, component_path):
		pp = PackageParser(pkg_path)
		pkg_name = pp.getName()
		pkg_dir = pp.getDirPath()
		try:
			tree = ET.parse(str(pathlib.Path(component_path).resolve()))
		except:
			RED = '\033[31m'
			END = '\033[0m'
			print(RED + "parse error: " + component_path + END)
			return
		root = tree.getroot()

		if root.tag == 'part':
			self.component = self.ParsePart(pkg_name, pkg_dir, root)
		elif root.tag == 'assembly':
			self.component = self.ParseAssembly(pkg_name, root)
		else:
			self.component = DataComponent()

	def ParsePart(self, pkg_name, pkg_dir, root):
		component_name = root.find("name").text

		if root.find("stl_file") is not None:
			stl_file_name = pkg_dir+"/"+root.find("stl_file").text
		else:
			stl_file_name = ""


		if root.find("price") is not None:
			price = float(root.find("price").text)
		else:
			price = 0.0

		if root.find("distributor") is not None:
			distributor = root.find("distributor").text
		else:
			distributor = ''

		if root.find("description") is not None:
			description = root.find("description").text
		else:
			description = ''

		part = DataPart()
		part.id = ComponentIdentifier(pkg_name, component_name)
		part.price_value = price
		part.price_unit = "yen"
		part.distributor = distributor
		part.description = description
		part.stl_path = stl_file_name
		return part

	def ParseAssembly(self, pkg_name, root):
		component_name = root.find("name").text
		asm = DataAssembly()
		asm.id = ComponentIdentifier(pkg_name, component_name)
		for s in root.iter("step"):
			step = DataAssemblyStep()
			# parse components
			for c in s.iter("component"):
				child = DataAssemblyStepChild()
				child.id = ComponentIdentifier(c.attrib["pkg"], c.attrib["type"])
				child.transform = self.GetTransform(c)
				child.move = self.GetMove(c)
				step.child_list.append(child)
			# parse view
			for c in s.iter("view"):
				look_from = c.attrib["from"].split(' ')
				look_at = c.attrib["to"].split(' ')
				view = DataAssemblyView()
				view.look_at = [float(look_at[0]), float(look_at[1]), float(look_at[2])]
				view.look_from = [float(look_from[0]), float(look_from[1]), float(look_from[2])]
				step.view_list.append(view)

			asm.step_list.append(step)
		return asm

	def GetTransform(self, element):
		xyz = element.find("origin").attrib["xyz"].split(' ')
		rpy = element.find("origin").attrib["rpy"].split(' ')
		return Transform(float(xyz[0]), float(xyz[1]), float(xyz[2]), float(rpy[0]), float(rpy[1]), float(rpy[2]))

	def GetMove(self, element):
		xyz = element.find("move").attrib["xyz"].split(' ')
		return Point(float(xyz[0]), float(xyz[1]), float(xyz[2]))

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

