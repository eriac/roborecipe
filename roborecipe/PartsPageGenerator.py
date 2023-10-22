#!/usr/bin/python3
from jinja2 import Template
import pathlib
from roborecipe.data_type import * 
import collections

class MechanicalPartsPageData:
    def __init__(self):
        self.title = ""
        self.overwiew_image = ""
        self.description = ""
        self.product_name = ""
        self.product_url = ""
        self.distributor_list = []

class MechanicalPartsPageGenerator:
    def __init__(self, comp):
        self.comp = comp
        template_filepth = pathlib.Path(__file__).parent / 'templates' / 'mechanical_parts.html'
        file = open(template_filepth)
        self.template = Template(file.read()) 

    def write(self, output_base_dir):
        data = MechanicalPartsPageData()
        data.title = self.comp.id.getName() 
        data.overwiew_image = 'images/' + self.comp.id.type_name + '_rigid_body.png'
        data.image_list = self.comp.common.image_list
        data.description = self.comp.common.description
        data.product_name = self.comp.product.name
        data.product_url = self.comp.product.url
        data.distributor_list = self.comp.distributor_list
        rendered_str = self.template.render(data = data)

        output_path = str(output_base_dir) + '/' + self.comp.id.pkg_name + '/' + self.comp.id.type_name + '.html'
        print('write html ' + output_path)
        with open(output_path, mode='w') as f:
            f.write(rendered_str)


# LaserCut 3Dprint
class ProcessPartsPartsPageData:
    def __init__(self):
        self.title = ""
        self.overwiew_image = ""
        self.image_list = []
        self.description = ""
        self.process_data_file = ""
        self.process_material = ""
        self.process_cost = 0

class ProcessPartsPageGenerator:
    def __init__(self, comp):
        self.comp = comp
        template_filepth = pathlib.Path(__file__).parent / 'templates' / 'process_parts.html'
        file = open(template_filepth)
        self.template = Template(file.read())

    def write(self, output_base_dir):
        data = ProcessPartsPartsPageData()
        data.title = self.comp.id.getName() 
        data.overwiew_image = 'images/' + self.comp.id.type_name + '_rigid_body.png'
        data.image_list = self.comp.common.image_list
        data.description = self.comp.common.description
        data.process_data = self.comp.process.data_filepath
        data.process_material = self.comp.process.material
        data.process_cost = self.comp.process.cost
        rendered_str = self.template.render(data = data)

        output_path = str(output_base_dir) + '/' + self.comp.id.pkg_name + '/' + self.comp.id.type_name + '.html'
        print('write html ' + output_path)
        with open(output_path, mode='w') as f:
            f.write(rendered_str)

# Harness
class HarnessPageData:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.table_title = HarnessTableLineData()
        self.table_content_list = []

class HarnessTableLineData:
    def __init__(self, line = '', end1 = '', end2 = ''):
        self.line = line
        self.end1 = end1
        self.end2 = end2

class HarnessPageGenerator:
    def __init__(self, comp):
        self.comp = comp
        template_filepth = pathlib.Path(__file__).parent / 'templates' / 'harness.html'
        file = open(template_filepth)
        self.template = Template(file.read())

    def write(self, output_base_dir):
        data = HarnessPageData()
        data.title = self.comp.id.getName() 
        data.description = self.comp.common.description
        rendered_str = self.template.render(data = data)

        output_path = str(output_base_dir) + '/' + self.comp.id.pkg_name + '/' + self.comp.id.type_name + '.html'
        print('write html ' + output_path)
        with open(output_path, mode='w') as f:
            f.write(rendered_str)

# assembly
class AssemblyPageData:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.step_list = []

class MechanicalPartsStepItem:
    def __init__(self):
        self.seq_no = 0
        self.component_list = []
        self.image_path_list = []

class MechanicalPartsComponentItem:
    def __init__(self):
        self.name = ""
        self.quantity = 0

class AssemblyPageGenerator:
    def __init__(self, comp):
        self.comp = comp
        template_filepth = pathlib.Path(__file__).parent / 'templates' / 'assembly.html'
        file = open(template_filepth)
        self.template = Template(file.read())

    def write(self, output_base_dir):
        data = AssemblyPageData()
        data.title = self.comp.id.getName()
        data.image_list = self.comp.common.image_list
        data.description = self.comp.common.description
        for step_no, step in enumerate(self.comp.procedure_list):
            step_data = MechanicalPartsStepItem()
            step_data.seq_no = step_no
            comp_id_list = []
            for c in step.component_list:
                comp_id_list.append(c.id)
            quantity_list = collections.Counter(comp_id_list)
            for comp_id in quantity_list:
                comp_data = MechanicalPartsComponentItem()
                comp_data.name = comp_id.getName()
                comp_data.quantity = quantity_list[comp_id]
                step_data.component_list.append(comp_data)
            view_size = len(step.view_list)
            for i in range(view_size):
                step_data.image_path_list.append('images/' + self.comp.id.type_name + '_' + str(step_no) + '_' + str(i) + '.gif')
            data.step_list.append(step_data)
        rendered_str = self.template.render(data = data)

        output_path = str(output_base_dir) + '/' + self.comp.id.pkg_name + '/' + self.comp.id.type_name + '.html'
        print('write html ' + output_path)
        with open(output_path, mode='w') as f:
            f.write(rendered_str)

if __name__ == '__main__':
    mpd = MechanicalPartsPageData()
    mpg = MechanicalPartsPageGenerator(mpd)
    mpg.write('generate_index.html')