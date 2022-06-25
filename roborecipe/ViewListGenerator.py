#!/usr/bin/python3

import os
from roborecipe.data_type import *
from roborecipe.ImageGenerator import *
from roborecipe.StlLoader import *

class ViewListGenerator:
	def __init__(self, dl, rt):
		self.dl = dl
		self.rt = rt
	def GetViewList(self, output_dir):
		render_view_list=[]

		for render_target_component in self.dl:
			if type(render_target_component) is not DataAssembly:
				continue

			render_list = self.rt.GetItemListWithTransform(render_target_component.id)

			component_output_dir = output_dir+"/"+render_target_component.id.pkg_name+'/'+render_target_component.id.type_name
			os.makedirs(component_output_dir, exist_ok=True)

			for step_seq_no in range(len(render_target_component.step_list)):
				step_render_list = []
				for i in render_list:
					# print(i.component.id.getName())
					# print(i.component.stl_path)
					# print(i.GetWholeTransform())
					# print(i.step)
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
		return render_view_list

if __name__ == '__main__':
	from XmlParser import *
	from TreeAnalyzer import *
	from DirectorySearch import *
	from ImageGenerator import *
	from StlLoader import *

	ds = DirectorySearch('../sample')
	path_pair_list = ds.getComponentPathPairList()

	component_list = ComponentListParser(path_pair_list).getList()

	ta = TreeAnalyzer(component_list, ComponentIdentifier('sample_project', 'main_asm'))

	print("#### quantity ####")
	ql = ta.getQuantityList()
	for c in ql:
		print(c.id.getName(), ql[c])

	print("#### depend order ####")
	dl = ta.getDependOrderList()

	print("#### RenderList ####")
	rt = RenderTree(component_list, dl)

	vlg = ViewListGenerator(dl, rt)
	output_dir ="/home/ubuntu/roborecipe/out"
	render_view_list = vlg.GetViewList(output_dir)

	ig = ImageGenerator(sys.argv)

	ig.renderViewList(render_view_list)
