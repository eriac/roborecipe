#!/usr/bin/python3
from roborecipe.TopPageGenerator import * 
from roborecipe.AssemblyAnalyzer import * 


if __name__ == '__main__':
    component_path_list = [
        ComponentPathItem('screw_m3', '/home/ubuntu/workspace/roborecipe/sample/screw_m3', '/home/ubuntu/workspace/roborecipe/sample/screw_m3/roborecipe/pan_10.yaml'),
        ComponentPathItem('screw_m3', '/home/ubuntu/workspace/roborecipe/sample/screw_m3', '/home/ubuntu/workspace/roborecipe/sample/screw_m3/roborecipe/hollow_spacer_20.yaml'),
        ComponentPathItem('sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project/roborecipe/bar_plate.yaml'),
        ComponentPathItem('sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project/roborecipe/base_plate.yaml'),
        ComponentPathItem('sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project/roborecipe/side_asm.yaml'),
        ComponentPathItem('sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project', '/home/ubuntu/workspace/roborecipe/sample/sample_project/roborecipe/main_asm.yaml'),
    ]

    cll = ComponentListLoader()
    for path_item in component_path_list:
        cll.load(path_item)

    top_assembly_id = ComponentIdentifier('sample_project', 'main_asm')
    acl = AssemblyComponentListAnalyzer(cll, top_assembly_id)

    td = TopPageData()
    td.title = top_assembly_id.getName()

    for item in acl.getQuantityList(ComponentCategoryEnum.SCREW):
        name_body = item[0].id.getName()
        name_link = item[0].id.getName() + '.html'
        td.mechanical_purchased.add_line(ComponentTableLine(name_body,name_link,item[1],10,item[0].description))

    for item in acl.getQuantityList(ComponentCategoryEnum.LASER_CUT):
        name_body = item[0].id.getName()
        name_link = item[0].id.getName() + '.html'
        td.laser_cut.add_line(ComponentTableLine(name_body,name_link,item[1],20,item[0].description))

    for item in acl.getAssemblyDependencyList():
        name_body = item[0].id.getName()
        name_link = item[0].id.getName() + '.html'
        td.assembly.add_line(ComponentTableLine(name_body,name_link,item[1],0,item[0].description))


    tg = TopPageGenerator(td)
    tg.write('generate_index.html')
