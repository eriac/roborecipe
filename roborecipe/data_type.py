#!/usr/bin/python3

import math

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