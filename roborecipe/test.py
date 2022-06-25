#!/usr/bin/python3

from XmlParser import *
from TreeAnalyzer import *
from DirectorySearch import *
from ImageGenerator import *
from StlLoader import *

import os

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

	ta = TreeAnalyzer(component_list, ComponentIdentifier('sample_project', 'main_asm'))

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
	render_target_component = dl[-1]

	render_list = rt.GetItemListWithTransform(render_target_component.id)
	print("#### RenderList ####")


	component_output_dir ="/home/ubuntu/roborecipe/out"+"/"+render_target_component.id.pkg_name+'/'+render_target_component.id.type_name
	os.makedirs(component_output_dir, exist_ok=True)

	render_view_list=[]
	for step_seq_no in range(len(render_target_component.step_list)):
		step_render_list = []
		for i in render_list:
			print(i.component.id.getName())
			print(i.component.stl_path)
			print(i.GetWholeTransform())
			print(i.step)
			if i.step <= step_seq_no:
				p1 = PartSource()
				p1.triangles = StlLoader(i.component.stl_path).get_triangles()
				wtr=i.GetWholeTransform()
				p1.position = [wtr.position.x,wtr.position.y,wtr.position.z]
				p1.rotation = wtr.rotation.getRPY()
				if i.step == step_seq_no:
					p1.move = i.move
				step_render_list.append(p1)

		for view_seq_no in range(len(render_target_component.step_list[step_seq_no].view_list)):
			view_data = render_target_component.step_list[step_seq_no].view_list[view_seq_no]
		
			render_view = ViewSource()
			render_view.output_filepath = component_output_dir + '/asm_'+str(step_seq_no)+'_'+str(view_seq_no)+'.gif'
			render_view.step=step_seq_no
			render_view.part_list = step_render_list
			render_view.look_from = view_data.look_from
			render_view.look_at = view_data.look_at
			render_view.step=10
			render_view_list.append(render_view)

	ig = ImageGenerator(sys.argv)
	ig.renderViewList(render_view_list)
