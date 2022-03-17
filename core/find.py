#!/usr/bin/python3

import os
from glob import glob
import xml.etree.ElementTree as ET

class Component:
	def __init__(self, path, package):
		self.name = ""
		self.dir = ""
		self.tree = None
		self.package = package

		tree = ET.parse(path+'description.xml')
		root = tree.getroot()
		n = root.find("name")
		if n is not None:
			self.name = n.text
		self.tree = tree

	def print(self, prefix):
		print(prefix + "name: " + self.name)

class Part(Component):
	def __init__(self, path, package):
		super().__init__(path, package)

	def print(self, prefix):
		print(prefix + "part name: " + self.name)

class AsmItem:
	def __init__(self, tree):
		self.pkg_name = ""
		self.component_name = ""
		self.load(tree)

	def load(self, tree):
		pn = tree.find("pkg")
		if pn is not None:
			self.pkg_name = pn.text

		cn = tree.find("component")
		if cn is not None:
			self.component_name = cn.text

	def print(self, prefix):
		print(prefix+" "+self.pkg_name+" "+self.component_name)

class Assembly(Component):
	def __init__(self, path, package):
		super().__init__(path, package)
		self.list = []

		# get list
		comp_list = self.tree.find("list")
		if  comp_list is not None:
			for c in comp_list:
				asm_item = AsmItem(c)
				self.list.append(asm_item)

	def print(self, prefix):
		print(prefix + "asm  name: " + self.name)
		for item in self.list:
			item.print(prefix+'  ')


class Package:
	def __init__(self, path):
		self.name = ""
		self.part_list = []
		self.asm_list = []
		self.load(path)

	def load(self, path):
		tree = ET.parse(path + 'package.xml')
		root = tree.getroot()
		print(root.tag)

		n = root.find("name")
		if n is not None:
			self.name = n.text

		sub_dir=glob(path + '/*/', recursive = True)
		for p in sub_dir:
			ex = os.path.isfile(p+'description.xml')
			if ex:
				tree = ET.parse(p+'description.xml')
				root = tree.getroot()
				comp_type = root.tag
				print("sub", comp_type)
				if comp_type == "part":
					part_class = Part(p, self)
					self.part_list.append(part_class)
				elif comp_type == "assembly":
					part_class = Assembly(p, self)
					self.part_list.append(part_class)

	def print(self):
		print('#### package ####')
		print('name: ' + self.name)
		for p in self.part_list:
			p.print("  ")

	def get(self, name):
		output = None
		for part in self.part_list:
			if part.name == name:
				output = part
		for asm in self.asm_list:
			if asm.name == name:
				output = asm
		return output

class MetaPackage:
	def __init__(self, path):
		self.list = []
		self.load(path)

	def load(self, path):
		pkgs=glob(path + '/*/', recursive = True)
		for p in pkgs:
			ex = os.path.isfile(p+'package.xml')
			print(p, ex)
			p_class = Package(p)
			self.list.append(p_class)

	def print(self):
		for p in self.list:
			p.print()

	def get_pkg(self, name):
		output = None
		for pkg in self.list:
			if pkg.name == name:
				output = pkg
		return output

	def get(self, pkg_name, comp_name):
		pkg = self.get_pkg(pkg_name)
		if pkg is None:
			return None
		return pkg.get(comp_name)

LIBRARIES_DIR = os.getcwd() + '/sample'

def get_sub():
	print(LIBRARIES_DIR)
	meta_pkg = MetaPackage(LIBRARIES_DIR)
	meta_pkg.print()
	return meta_pkg

def get_list(meta_pkg, pkg_name, component_name):
	part_list = []
	comp = meta_pkg.get(pkg_name, component_name)
	if type(comp) is Part:
		part_list.append(comp)
	elif type(comp) is Assembly:
		for c in comp.list:
			l = get_list(meta_pkg, c.pkg_name, c.component_name)
			part_list.extend(l)

	return part_list

if __name__ == '__main__':
	meta_pkg = get_sub()
	l=get_list(meta_pkg, "srs007", "main_asm")

	part_dict = {}
	for i in l:
		if i not in part_dict:
			part_dict[i]=1
		else:
			part_dict[i]=part_dict[i]+1

	print("##### list #####")
	for d in part_dict:
		print(d.package.name +"/"+ d.name + " " + str(part_dict[d]))

	# print(part_dict)
	