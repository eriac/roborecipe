#!/usr/bin/python3
from jinja2 import Template
from roborecipe.data_type import * 

class HtmlParchageItem:
    def __init__(self):
        self.id = ComponentIdentifier()
        self.quantity = 0
        self.price_value = 0
        self.price_unit = 'yen'
        self.distributor = 'http:/aaa.bbb'
        self.description = 'description'

class HtmlComponentItem:
    def __init__(self, pkg = "unknown", type = "unknown", quantity = 0):
        self.id = ComponentIdentifier(pkg, type)
        self.quantity = quantity
    def increaseQuantity(self):
        self.quantity += 1

class HtmlAssemblyStep:
    def __init__(self):
        self.seq_no = 0
        self.component_list = []
        self.image_path_list = []

class HtmlAssemblyItem:
    def __init__(self):
        self.name = "unknown"
        self.quantity = 0
        self.step_list = []

class Cost:
    def __init__(self):
        self.value = 0
        self.uni = "yen"

class HtmlGenerator:
    def __init__(self):
        self.template_path = ""
        self.title = "roborecipe"
        self.part_list = []
        self.assembly_list = []
        self.total_cost = Cost()
    def generate(self, output_path):
        with open(self.template_path) as f:
            template = Template(f.read())
            ren_s = template.render(tittle=self.title, part_list=self.part_list, assembly_list=self.assembly_list, total_cost=self.total_cost)

        with open(output_path, mode='w') as f:
            f.write(ren_s)
        print('write ' + output_path)

if __name__ == '__main__':
    html_generator = HtmlGenerator()
    html_generator.template_path = 'templates/index.html'

    p1 = HtmlParchageItem()
    p1.id = ComponentIdentifier('p1', 't1')
    p1.quantity = 1
    p2 = HtmlParchageItem()
    p2.id = ComponentIdentifier('p2', 't2')
    p2.quantity = 2
    html_generator.part_list = [p1, p2]



    a1 = HtmlAssemblyItem()
    a1.name = "A1"
    a1.quantity = 1
    a1_1 = HtmlAssemblyStep()
    a1_1.seq_no = 1
    a1_1.component_list.append(HtmlComponentItem("p1", "t1", 1))
    a1_1.component_list.append(HtmlComponentItem("p2", "t2", 2))
    a1_1.image_path_list.append("../image/assemble_0_0.gif")
    a1.step_list.append(a1_1)

    a1_2 = HtmlAssemblyStep()
    a1_2.seq_no = 2
    a1_2.component_list.append(HtmlComponentItem("p1", "t1", 1))
    a1_2.component_list.append(HtmlComponentItem("p2", "t2", 2))
    a1_2.image_path_list.append("../image/assemble_1_0.gif")
    a1_2.image_path_list.append("../image/assemble_1_1.gif")
    a1.step_list.append(a1_2)

    a2 = HtmlAssemblyItem()
    a2.name = "A2"
    a2.quantity = 2

    html_generator.assembly_list =[a1, a2] 

    html_generator.generate('generate_index.html')