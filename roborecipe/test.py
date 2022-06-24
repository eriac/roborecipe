#!/usr/bin/python3

from XmlParser import *
from TreeAnalyzer import *
from DirectorySearch import *
from ImageGenerator import *
from StlLoader import *


if __name__ == '__main__':
	# path_pair_list = [
	# 	['../sample/srs007/package.xml', '../sample/srs007/main_asm/assemble.roborecipe'],
	# 	['../sample/srs007/package.xml', '../sample/srs007/base_asm/assemble.roborecipe'],
	# 	['../sample/pololu/package.xml', '../sample/pololu/4691_37mm_motor/description.roborecipe'],
	# 	['../sample/iso_screw_m3/package.xml', '../sample/iso_screw_m3/pan_12/part.roborecipe']
	# ]

	ds = DirectorySearch('../sample')
	path_pair_list = ds.getComponentPathPairList()

	component_list = ComponentListParser(path_pair_list).getList()
	# print("#### component list ####")
	# for c in component_list:
	# 	print(c.id.getName())

	ta = TreeAnalyzer(component_list, ComponentIdentifier('sample_project', 'side_asm'))

	print("#### quantity ####")
	ql = ta.getQuantityList()
	for c in ql:
		print(c.id.getName(), ql[c])

	print("#### depend order ####")
	dl = ta.getDependOrderList()
	for c in dl:
		print(c.id.getName())

	print("#### RenderList ####")
	rt = RenderTree(component_list, dl)
	list = rt.GetItemListWithTransform(dl[-1].id)
	print("#### RenderList ####")

	view1 = ViewSource()
	view1.output_filepath = "/home/ubuntu/roborecipe/out.png"
	view1.step=0
	view1.look_from = [70,0,-50]
	view1.look_at = [0,0,-10]

	for i in list:
		print(i.component.id.getName())
		print(i.component.stl_path)
		print(i.GetWholeTransform())

		p1 = PartSource()
		p1.triangles = StlLoader(i.component.stl_path).get_triangles()
		wtr=i.GetWholeTransform()
		p1.position = [wtr.position.x,wtr.position.y,wtr.position.z]
		view1.part_list.append(p1)

	ig = ImageGenerator(sys.argv)
	ig.renderViewList([view1])
