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

# transform
class Point:
	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.x = x
		self.y = y
		self.z = z
	def __add__(self, other):
		p =Point()
		p.x = self.x + other.x
		p.y = self.y + other.y
		p.z = self.z + other.z
		return p

	def __repr__(self) -> str:
		return "("+str(self.x)+","+str(self.y)+","+str(self.z)+")"

class Quaternion:
	def __init__(self, roll=0.0, pitch=0.0, yaw=0.0):
		self.roll = roll
		self.pitch = pitch
		self.yaw = yaw

	def __mul__(self, other): # TODO
		output = Quaternion()
		output.roll = self.roll + other.roll
		output.pitch = self.pitch + other.pitch
		output.yaw = self.yaw + other.yaw
		return output

	def __repr__(self) -> str:
		return "("+str(self.roll)+","+str(self.pitch)+","+str(self.yaw)+")"

	def getRPY(self):
		return [self.roll, self.pitch, self.yaw]

class Transform:
	def __init__(self, x=0.0, y=0.0, z=0.0, roll=0, pitch=0, yaw=0):
		self.position = Point(x, y, z)
		self.rotation = Quaternion(roll, pitch, yaw)

	def __mul__(self, other):
		output = Transform()
		output.position = self.position + other.position
		output.rotation = self.rotation * other.rotation #TODO
		return output

	def __repr__(self) -> str:
		return "tf " + str(self.position) + " " + str(self.rotation)

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
		self.transform = Transform()
		self.move = Point()

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

