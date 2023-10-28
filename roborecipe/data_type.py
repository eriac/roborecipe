#!/usr/bin/python3

import math
from enum import Enum
import colorsys 

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
	def __hash__(self):
		return hash((self.pkg_name, self.type_name))

class ComponentCategoryEnum(Enum):
	UNKNOWN = 0
	# to make instruction steps
	ASSEMBLY = 1
	# harnes_connection related
	HARNESS = 2
	BOARD = 3
	ELECTRIC_ITEM = 4
	# rigit body related
	MECHANICAL_ITEN = 5
	SCREW = 6
	PRINT_3D = 7
	LASER_CUT = 8
	ORDER = 9

class ComponentCategory:
	def __init__(self, category_str):
		if category_str == 'assembly':
			self.value = ComponentCategoryEnum.ASSEMBLY
		elif category_str == 'screw':
			self.value = ComponentCategoryEnum.SCREW
		elif category_str == 'mechanical':
			self.value = ComponentCategoryEnum.MECHANICAL_ITEN
		elif category_str == 'laser_cut':
			self.value = ComponentCategoryEnum.LASER_CUT
		elif category_str == 'electric':
			self.value = ComponentCategoryEnum.ELECTRIC_ITEM
		elif category_str == '3d_print':
			self.value = ComponentCategoryEnum.PRINT_3D
		elif category_str == 'order':
			self.value = ComponentCategoryEnum.ORDER
		elif category_str == 'board':
			self.value = ComponentCategoryEnum.BOARD
		elif category_str == 'harness':
			self.value = ComponentCategoryEnum.HARNESS
		else:
			self.value = ComponentCategoryEnum.UNKNOWN

	def is_assembly(self):
		return (self.value == ComponentCategoryEnum.ASSEMBLY)

	def get_color(self, focused):
		if focused:
			s = 1.0
			v = 1.0
		else:
			s = 0.5
			v = 0.5

		if self.value == ComponentCategoryEnum.SCREW:
			h = 0.66
		elif self.value == ComponentCategoryEnum.LASER_CUT:
			h = 0.1
		elif self.value == ComponentCategoryEnum.ELECTRIC_ITEM:
			h = 0.3
		elif self.value == ComponentCategoryEnum.PRINT_3D:
			h = 0.4
		else:
			h = 0.0
			s = 0.0

		rgb = colorsys.hsv_to_rgb(h, s, v)
		return (rgb[0], rgb[1], rgb[2], 1.0)

class ComponentCommon:
	def __init__(self, pkg_base_path, yaml_obj):
		self.description = yaml_obj['description']
		self.image_list = []
		if 'image_list' in yaml_obj:
			self.image_list = yaml_obj['image_list']

class RigitBody:
	def __init__(self, pkg_base_path, yaml_obj):
		self.mesh_filepath = pkg_base_path + '/' + yaml_obj['mesh']['path']
		self.view = View(yaml_obj['view'])

class View:
	def __init__(self, yaml_obj):
		from_obj = yaml_obj['from']
		self.from_point = Point(from_obj['x'], from_obj['y'], from_obj['z'])
		to_obj = yaml_obj['to']
		self.to_point = Point(to_obj['x'], to_obj['y'], to_obj['z'])
	def __repr__(self):
		return 'view(' + str(self.from_point) + '->' + str(self.to_point) + ')'

class Product:
	def __init__(self, yaml_obj):
		self.name = yaml_obj['name']
		self.url = yaml_obj['url']

class Distributor:
	def __init__(self, yaml_obj):
		self.name = yaml_obj['name']
		self.url = yaml_obj['url']
		self.price = yaml_obj['price']

class Process:
	def __init__(self, pkg_base_path, yaml_obj):
		self.data_filepath = pkg_base_path + '/' + yaml_obj['data']['path']
		self.material = yaml_obj['material']
		self.cost = yaml_obj['cost']	

class ScrewData:
	def __init__(self, path_item, yaml_obj):
		self.id = ComponentIdentifier(path_item.pkg_name, yaml_obj['name'])
		self.category = ComponentCategory(yaml_obj['category'])
		self.pkg_base_path = path_item.pkg_base_path
		self.m_datetime = path_item.m_datetime
		# common
		self.common = ComponentCommon(path_item.pkg_base_path, yaml_obj['common'])
		# body related
		self.rigit_body = RigitBody(path_item.pkg_base_path, yaml_obj['rigit_body'])
		# product
		self.product = Product(yaml_obj['product'])
		# distributor
		self.distributor_list = []
		for yaml_item in yaml_obj['distributor']:
			self.distributor_list.append(Distributor(yaml_item))

class LaserData:
	def __init__(self, path_item, yaml_obj):
		self.id = ComponentIdentifier(path_item.pkg_name, yaml_obj['name'])
		self.category = ComponentCategory(yaml_obj['category'])
		self.pkg_base_path = path_item.pkg_base_path
		self.m_datetime = path_item.m_datetime

		self.common = ComponentCommon(path_item.pkg_base_path, yaml_obj['common'])
		self.rigit_body = RigitBody(path_item.pkg_base_path, yaml_obj['rigit_body'])
		self.process = Process(path_item.pkg_base_path, yaml_obj['process'])

class Harness:
	def __init__(self, pkg_base_path, yaml_obj):
		self.cost = yaml_obj['cost']
		self.line_kind = yaml_obj['line']['kind']
		self.line_length = yaml_obj['line']['length']
		self.line_name_list = yaml_obj['line']['names']
		self.end1 = HarnessEnd(yaml_obj['end1'])
		self.end2 = HarnessEnd(yaml_obj['end2'])

class HarnessEnd:
	def __init__(self, yaml_obj):
		self.family = yaml_obj['family']
		self.model = yaml_obj['model']
		self.assign_list = yaml_obj['assign']

class HarnessData:
	def __init__(self, path_item, yaml_obj):
		self.id = ComponentIdentifier(path_item.pkg_name, yaml_obj['name'])
		self.category = ComponentCategory(yaml_obj['category'])
		self.pkg_base_path = path_item.pkg_base_path
		self.m_datetime = path_item.m_datetime

		self.common = ComponentCommon(path_item.pkg_base_path, yaml_obj['common'])
		self.harness = Harness(path_item.pkg_base_path, yaml_obj['harness'])

class AssemblyData:
	def __init__(self, path_item, yaml_obj):
		self.id = ComponentIdentifier(path_item.pkg_name, yaml_obj['name'])
		self.category = ComponentCategory(yaml_obj['category'])
		self.pkg_base_path = path_item.pkg_base_path
		self.m_datetime = path_item.m_datetime

		self.common = ComponentCommon(path_item.pkg_base_path, yaml_obj['common'])
		self.procedure_list = []
		for step in yaml_obj['procedure_list']:
			self.procedure_list.append(AssemblyStepData(step))

class AssemblyStepData:
	def __init__(self, yaml_obj):
		self.component_list = []
		for comp in yaml_obj['component_list']:
			self.component_list.append(AssemblyComponentData(comp))
		self.view_list = []
		for view in yaml_obj['view_list']:
			self.view_list.append(View(view))

class AssemblyComponentData:
	def __init__(self, yaml_obj):
		self.id  = ComponentIdentifier(yaml_obj['pkg'], yaml_obj['type'])
		ori = yaml_obj['origin']
		self.transform = Transform(ori['x'], ori['y'], ori['z'], ori['roll'], ori['pitch'], ori['yaw'])
		self.move = Point(yaml_obj['move']['x'], yaml_obj['move']['y'], yaml_obj['move']['z'])

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
	def __init__(self, w=1.0, x=0.0, y=0.0, z=0.0): # degree
		self.w = w
		self.x = x
		self.y = y
		self.z = z

	def __mul__(self, other): # TODO
		output = Quaternion()
		output.w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
		output.x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
		output.y = self.w * other.y + self.y * other.w + self.z * other.x - self.x * other.z
		output.z = self.w * other.z + self.z * other.w + self.x * other.y - self.y * other.x
		return output
		# self_rpy = self.getRPY()
		# other_rpy = other.getRPY()
		# output = Quaternion().setRPY(self_rpy[0]+other_rpy[0],self_rpy[1]+other_rpy[1],self_rpy[2]+other_rpy[2])
		# return output

	def __repr__(self) -> str:
		(roll, pitch, yaw) = self.getRPY()
		return "q("+ str(self.w) + ',' + str(self.x) + ',' + str(self.y) + ',' + str(self.z) +") rpy("+str(roll)+","+str(pitch)+","+str(yaw)+")"
		# return "("+str(self.roll)+","+str(self.pitch)+","+str(self.yaw)+")"

	def setRPY(self, roll, pitch, yaw): # degree
		cy = math.cos(yaw*math.pi/180 * 0.5)
		sy = math.sin(yaw*math.pi/180 * 0.5)
		cp = math.cos(pitch*math.pi/180 * 0.5)
		sp = math.sin(pitch*math.pi/180 * 0.5)
		cr = math.cos(roll*math.pi/180 * 0.5)
		sr = math.sin(roll*math.pi/180 * 0.5)
		self.w = cr * cp * cy + sr * sp * sy
		self.x = sr * cp * cy - cr * sp * sy
		self.y = cr * sp * cy + sr * cp * sy
		self.z = cr * cp * sy - sr * sp * cy
		return self

	def getRPY(self): # degree
		q0q0 = self.w * self.w
		q1q1 = self.x * self.x
		q2q2 = self.y * self.y
		q3q3 = self.z * self.z
		q0q1 = self.w * self.x
		q0q2 = self.w * self.y
		q0q3 = self.w * self.z
		q1q2 = self.x * self.y
		q1q3 = self.x * self.z
		q2q3 = self.y * self.z
		roll = math.atan2((2.0 * (q2q3 + q0q1)), (q0q0 - q1q1 - q2q2 + q3q3))
		pitch = -math.asin((2.0 * (q1q3 - q0q2)))
		yaw = math.atan2((2.0 * (q1q2 + q0q3)), (q0q0 + q1q1 - q2q2 - q3q3))
		return [roll*180/math.pi, pitch*180/math.pi, yaw*180/math.pi]

	def setPoint(self, position):
		self.w = 0
		self.x = position.x
		self.y = position.y
		self.z = position.z
		return self

	def getPoint(self):
		return Point(self.x, self.y, self.z)

	def getConj(self):
		return Quaternion(self.w,-self.x,-self.y,-self.z)

class Transform:
	def __init__(self, x=0.0, y=0.0, z=0.0, roll=0, pitch=0, yaw=0):
		self.position = Point(x, y, z)
		self.rotation = Quaternion().setRPY(roll, pitch, yaw)

	def __mul__(self, other):
		output = Transform()
		pos_q = Quaternion().setPoint(other.position)
		conv_pos_q = self.rotation * pos_q * self.rotation.getConj()
		conv_pos = conv_pos_q.getPoint()
		output.position = self.position + conv_pos
		output.rotation = self.rotation * other.rotation
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
		self.price_unit = 'yen'
		self.distributor = ''
		self.description = ''
		self.stl_path = ''

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

if __name__ == '__main__':
	t1 = Transform()
	t1.position.x = 0
	t1.position.y = 0
	t1.position.z = 4
	t1.rotation.setRPY(0,0,-30)

	t2 = Transform()
	t2.position.x = 0
	t2.position.y = 0
	t2.position.z = 4
	t2.rotation.setRPY(180,0,0)

	print(t1*t2)