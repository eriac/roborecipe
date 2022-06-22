#!/usr/bin/python3

# common
class ComponentIdentifier:
	def __init__(self, pkg = "unknown", type = "unknown"):
		self.pkg_name = pkg
		self.type_name = type
	def getName(self):
		return self.pkg_name + "/" + self.type_name
	def __eq__(self, other):
		if not isinstance(other, ComponentIdentifier):
			return NotImplemented
		return self.pkg_name == other.pkg_name and self.type_name == other.type_name    

# component internal data
class DataComponent:
	def __init__(self, pkg="unknown", type="unknown", pkg_path="", cmp_path=""):
		self.initial_char = "C"
		self.id = ComponentIdentifier(pkg, type)
		self.pkg_path = pkg_path
		self.cmp_path = cmp_path

class DataPart(DataComponent):
	def __init__(self, pkg="unknown", type="unknown", pkg_path="", cmp_path=""):
		super().__init__(pkg, type, pkg_path, cmp_path)
		self.initial_char = "P"
		self.price_value = 0
		self.price_unit = "yen"
		self.url = 'http:/sample.com/sample.html'
		self.description = "description"
		self.stl_path = ""

class DataAssemblyStepChild:
	def __init__(self):
		self.id = ComponentIdentifier()
		self.position = [0,0,0]
		self.move = [0,0,0]

class DataAssemblyView:
	def __init__(self):
		self.look_at = [0,0,0]
		self.look_from = [0,0,0]

class DataAssemblyStep:
	def __init__(self):
		self.view_list = []
		self.child_list = []

class DataAssembly(DataComponent):
	def __init__(self, pkg="unknown", type="unknown", pkg_path="", cmp_path=""):
		super().__init__(pkg, type, pkg_path, cmp_path)
		self.initial_char = "A"
		self.step_list = []
