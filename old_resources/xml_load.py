import xml.etree.ElementTree as ET
import re



class xml_load:
	def __init__(self,name):
		self.parts_list,self.parts_quantity = self.parts_load(name)
		self.model_dict    = self.model_dict_make(self.parts_list)
		self.assembly_list = self.assembly_load(name)
		self.quantity_dict = self.quantity_dict_make(self.assembly_list)
		self.views_list,self.shot_list = self.view_load(name)
		self.maxrank       = self.maxrank_load(name)
		self.apt_list      = self.assemble_parts_load(name,self.maxrank)

	def assembly_load(self,name):
		# part_list
		# 0 name
		# 1 rank
		# 2 type (0:part 1:screw)
		# 3 origin(trans)
		# 4 origin(rotate)
		# 5 diff
		# 6 view
		parts_list=[]
		try:
			tree=ET.parse(name)
		except:
			print("xml file not found")
			return []

		root=tree.getroot()
		elem1=root.find("assembly")

		for i in list(elem1):
			iname  = i.find("name").text
			irank  = int(i.find("rank").text)
			itype  = int(i.find("type").text)

			tmp1=re.split(" +",i.find("origin").attrib["xyz"])
			itmp1=[int(j) for j in tmp1]
	 		
			tmp3=re.split(" +",i.find("origin").attrib["r_axis"])
			itmp3=[int(j) for j in tmp3]
	 
			tmp4=re.split(" +",i.find("diff").attrib["xyz"])
			itmp4=[int(j) for j in tmp4]
	 		
			newitem=[iname,irank,itype,itmp1[0:3],itmp3[0:4],itmp4[0:3]]
			parts_list.append(newitem)
	
		return parts_list

	def view_load(self,name):
		# view_list
		# 0 rank
		# 1 shot
		# 2 from_x
		# 3 from_y
		# 4 from_z
		# 5 to_x
		# 6 to_y
		# 7 to_z
		# 8 angle
		view_list=[]
		shot_list=[]
		try:
			tree=ET.parse(name)
		except:
			print("xml file not found")
			return []

		root=tree.getroot()
		elem1=root.find("views")

		for i in list(elem1):
			rank_number=int(i.get("rank"))
			shot_number=0
			for j in list(i):
				item_list=j.items()
				newitem=[0,0,200,0,0,0,0,0,30]
				newitem[0]=rank_number
				newitem[1]=shot_number
				for k in item_list:
					if k[0]=="from":
						tmp=re.split(" +",k[1])
						itmp=[int(l) for l in tmp]
						newitem[2:5]=itmp[0:3]
		 			elif k[0]=="to":
						tmp=re.split(" +",k[1])
						itmp=[int(l) for l in tmp]
						newitem[5:8]=itmp[0:3]
		 			elif k[0]=="angle":
						irank=int(k[1])
						newitem[8]=irank
				view_list.append(newitem)
				shot_number+=1
			shot_list.append(shot_number)
		return view_list,shot_list
	
	def maxrank_load(self,name):
		try:
			tree=ET.parse(name)
		except:
			print("xml file not found")
			return 0

		root=tree.getroot()
		elem1=root.find("assembly")

		maxrank=0
		for i in list(elem1):
			irank  = int(i.find("rank").text)
			if maxrank<irank:
				maxrank=irank
	
		return maxrank

	def parts_load(self,name):
		# part_list
		# 0 name
		# 1 model
		# 2 type
		# 3 data
		# 4 comment
		# 5 view
		parts_list=[]
		try:
			tree=ET.parse(name)
		except:
			print("xml file not found")
			return []

		root=tree.getroot()
		elem1=root.find("parts")

		pt_quantity=0
		for i in list(elem1):
			iname  = i.find("name").text
			imodel = i.find("model").text
			itype  = i.find("type").text
			idata  = i.find("data").text
			icomment  = i.find("comment").text
			iview  = i.find("view")

			view_list=iview.items()
			newview=[0,0,200,0,0,0,0,0,30]
			for k in view_list:
				if k[0]=="from":
					tmp=re.split(" +",k[1])
					itmp=[int(l) for l in tmp]
					newview[0:3]=itmp[0:3]
	 			elif k[0]=="to":
					tmp=re.split(" +",k[1])
					itmp=[int(l) for l in tmp]
					newview[3:6]=itmp[0:3]
	 			elif k[0]=="angle":
					irank=int(k[1])
					newview[6]=irank

			newitem=[iname,imodel,itype,idata,icomment,newview]
			parts_list.append(newitem)
			pt_quantity+=1
	
		return parts_list,pt_quantity

	def assemble_parts_load(self,name,max_rank):
		apt_list=[]
		for i in range(max_rank):
			# in every item
			# part_list
			# 0 name
			# 1 quantiry
			parts_dict={}
			try:
				tree=ET.parse(name)
			except:
				print("xml file not found")
				return []

			root=tree.getroot()
			elem1=root.find("assembly")

			for j in list(elem1):
				jname  = j.find("name").text
				jrank = int(j.find("rank").text)
				
				if jrank==i:
					if not jname in parts_dict:
						parts_dict[jname]=1
					else:
						parts_dict[jname]+=1

			apt_list.append(parts_dict)

		return apt_list

	def model_dict_make(self,parts_list):
		model_dict={}
		for pt in parts_list:
			if not pt[0] in model_dict: 
				model_dict[pt[0]]=pt[1]
		return model_dict

	def quantity_dict_make(self,assembly_list):
		quantity_dict={}
		for asm in assembly_list:
			if not asm[0] in quantity_dict: 
				quantity_dict[asm[0]]=1
			else:
				quantity_dict[asm[0]]+=1
		return quantity_dict

#if __name__ == '__main__':
#	print xml_load("data1.xml")


