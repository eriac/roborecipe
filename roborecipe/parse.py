#!/usr/bin/python3

import os
from glob import glob
import xml.etree.ElementTree as ET
import pathlib

class Package:
	def __init__(self, path):
		self.name = ""
		self.path = ""
		self.valid = False
		self.load(path)

	def load(self, path):
		self.path = path
		tree = ET.parse(path)
		root = tree.getroot()
		if root.tag != 'package':
			print("root tag name is not package " + path)
			return

		n = root.find("name")
		if n is None:
			print("not have name tag " + path)
			return

		self.name = n.text
		self.valid = True

def get_package_list(target_directory):
	path_list=glob(target_directory + '/*/package.xml', recursive = True)

	package_list = []
	for p in path_list:
		p_class = Package(p)
		if p_class.valid:
			package_list.append(p_class)
	return package_list


class Component:
	def __init__(self, package_name, path):
		self.package_name = package_name
		self.component_name = ""
		self.initial_char = "C"
		self.path = path
		self.valid = False
		self.tree = None

		tree = ET.parse(path)
		root = tree.getroot()

		n = root.find("name")
		if n is None:
			print("not have name tag ", path)
			return
		self.component_name = n.text

		self.tree = tree
		self.valid = True

	def getFullName(self):
		return self.package_name + "/" + self.component_name

	def getStr(self):
		return "[" + self.initial_char + "]" + self.package_name + "/" + self.component_name + " " + self.path

	def show(self):
		output = ""
		output += "component " + self.package_name + "/" + self.component_name
		return output


class Part(Component):
	def __init__(self, package_name, path):
		super().__init__(package_name, path)
		self.initial_char = "P"

	def show(self):
		output = ""
		output += "part " + self.package_name + "/" + self.component_name
		return output

class AsmItem:
	def __init__(self, tree):
		self.package_name = ""
		self.component_name = ""
		self.valid = False
		self.load(tree)

	def load(self, tree):
		pn = tree.find("package")
		if pn is None:
			print("no package tag")
		self.package_name = pn.text

		cn = tree.find("component")
		if cn is None:
			print("no component tag")
		self.component_name = cn.text

		self.valid = True

	def print(self, prefix):
		print(prefix+" "+self.pkg_name+" "+self.component_name)

class Assembly(Component):
	def __init__(self, package_name, path):
		super().__init__(package_name, path)
		self.initial_char = "A"
		self.component_list = []

		# get list
		comp_list = self.tree.find("list")
		if comp_list is None:
			print("list tag not exists")
			return

		for c in comp_list:
			item = AsmItem(c)
			if item.valid:
				self.component_list.append(item)

	def show(self):
		output = ""
		output += "assembly " + self.package_name + "/" + self.component_name + "\n"
		output += "list:"
		for c in self.component_list:
			output += "\n  " + c.package_name + "/" + c.component_name
		return output

	# def print(self, prefix):
	# 	print(prefix + "asm  name: " + self.name)
	# 	for item in self.list:
	# 		item.print(prefix+'  ')

	# def print(self):
	# 	print('#### package ####')
	# 	print('name: ' + self.name)
	# 	for p in self.part_list:
	# 		p.print("  ")

	# def get(self, name):
	# 	output = None
	# 	for part in self.part_list:
	# 		if part.name == name:
	# 			output = part
	# 	for asm in self.asm_list:
	# 		if asm.name == name:
	# 			output = asm
	# 	return output

def get_type(path):
	tree = ET.parse(path)
	root = tree.getroot()
	return root.tag

def get_component_list(package):
	package_path = package.path
	ex = os.path.isfile(package_path)
	assert ex, "package.xml not exists"

	package_dir = str(pathlib.Path(package_path+"/..").resolve())
	component_path_list = glob(package_dir + '/*/*.roborecipe', recursive = True)

	component_list = []
	for p in component_path_list:
		roborecipe_type = get_type(p)
		if roborecipe_type == 'part':
			part = Part(package.name, p)
			if part.valid:
				component_list.append(part)
		elif roborecipe_type == 'assembly':
			asm = Assembly(package.name, p)
			if asm.valid:
				component_list.append(asm)
		else:
			print("root tag is unknown: " + roborecipe_type)
	return component_list


# class MetaPackage:
# 	def __init__(self, path):
# 		self.list = []
# 		self.load(path)

# 	def load(self, path):
# 		pkgs=glob(path + '/*/', recursive = True)
# 		for p in pkgs:
# 			ex = os.path.isfile(p+'package.xml')
# 			print(p, ex)
# 			p_class = Package(p)
# 			self.list.append(p_class)

# 	def print(self):
# 		for p in self.list:
# 			p.print()

# 	def get_pkg(self, name):
# 		output = None
# 		for pkg in self.list:
# 			if pkg.name == name:
# 				output = pkg
# 		return output

# 	def get(self, pkg_name, comp_name):
# 		pkg = self.get_pkg(pkg_name)
# 		if pkg is None:
# 			return None
# 		return pkg.get(comp_name)

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
	