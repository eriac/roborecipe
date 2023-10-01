#!/usr/bin/python3
from roborecipe.PartsPageGenerator import * 
from roborecipe.AssemblyAnalyzer import * 
from roborecipe.PartImageGenerator import * 


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


    for item in acl.getQuantityList(ComponentCategoryEnum.SCREW):
        # image
        mpis = MechanicalPartsImageSource()
        mpis.mesh_file_path = item[0].rigit_body.mesh_filepath
        print(mpis.mesh_file_path)
        mpis.view_from = [item[0].view_from.x , item[0].view_from.y, item[0].view_from.z]
        mpis.view_to = [item[0].view_to.x , item[0].view_to.y, item[0].view_to.z]

        mpig = MechanicalPartsImageGenerator(mpis)
        mpig.save_image('test_image.png')

        # html
        mpd = MechanicalPartsPageData()
        mpd.title = item[0].id.getName() 
        mpd.overwiew_image = "test_image.png"
        mpd.description = item[0].description
        mpd.product_name = item[0].product.name
        mpd.product_url = item[0].product.url
        mpd.distributor_name = item[0].distributor_name
        mpd.distributor_url = item[0].distributor_url
        mpd.distributor_price = item[0].distributor_price


        mpg = MechanicalPartsPageGenerator(mpd)
        mpg.write('generate_index.html')
        break

        # name_body = item[0].id.getName()
        # name_link = item[0].id.getName() + '.html'
        # td.mechanical_purchased.add_line(ComponentTableLine(name_body,name_link,item[1],10,item[0].description))

