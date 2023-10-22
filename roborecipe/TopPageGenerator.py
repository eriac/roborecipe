#!/usr/bin/python3
from jinja2 import Template
import os
import pathlib

from roborecipe.data_type import * 

class ComponentTableLine:
    def __init__(self, name_body = "", name_link = "", quantity = 0, price = 0, description = ""):
        self.name_body = name_body
        self.name_link = name_link
        self.quantity = quantity
        self.price = price
        self.description = description

class ComponentTable:
    def __init__(self):
        self.list = []
        self.total_price = 0
    def add_line(self, line):
        self.list.append(line)
        self.total_price += line.price * line.quantity

class TopPageData:
    def __init__(self):
        self.title = ""
        self.mechanical_purchased = ComponentTable()
        self.mechanical_fabrication = ComponentTable()
        self.electric_purchased = ComponentTable()
        self.electric_fabrication = ComponentTable()
        self.assembly = ComponentTable()

class TopPageGenerator:
    def __init__(self, comp_id, tree_analyer, dependency_analyzer):
        self.comp_id = comp_id
        self.tree_analyer = tree_analyer
        self.dependency_analyzer = dependency_analyzer

        template_filepth = pathlib.Path(__file__).parent / 'templates' / 'top.html'
        file = open(template_filepth)
        self.template = Template(file.read())

    def write(self, output_base_dir):
        td = TopPageData()
        td.title = self.comp_id.getName()

        mechanical_list = []
        mechanical_list.extend(self.tree_analyer.get_quantity_list(ComponentCategoryEnum.SCREW))
        mechanical_list.extend(self.tree_analyer.get_quantity_list(ComponentCategoryEnum.MECHANICAL_ITEN))
        for item in mechanical_list:
            name_body = item.comp.id.getName()
            name_link = item.comp.id.getName() + '.html'
            price = item.comp.distributor_list[0].price
            td.mechanical_purchased.add_line(ComponentTableLine(name_body,name_link,item.quantity,price,item.comp.common.description))

        fablication_list = []
        fablication_list.extend(self.tree_analyer.get_quantity_list(ComponentCategoryEnum.LASER_CUT))
        fablication_list.extend(self.tree_analyer.get_quantity_list(ComponentCategoryEnum.PRINT_3D))
        fablication_list.extend(self.tree_analyer.get_quantity_list(ComponentCategoryEnum.ORDER))
        for item in fablication_list:
            name_body = item.comp.id.getName()
            name_link = item.comp.id.getName() + '.html'
            price = item.comp.process.cost
            td.mechanical_fabrication.add_line(ComponentTableLine(name_body,name_link,item.quantity,price,item.comp.common.description))

        for item in self.tree_analyer.get_quantity_list(ComponentCategoryEnum.ELECTRIC_ITEM):
            name_body = item.comp.id.getName()
            name_link = item.comp.id.getName() + '.html'
            price = item.comp.distributor_list[0].price
            td.electric_purchased.add_line(ComponentTableLine(name_body,name_link,item.quantity,price,item.comp.common.description))

        for item in self.tree_analyer.get_quantity_list(ComponentCategoryEnum.BOARD):
            name_body = item.comp.id.getName()
            name_link = item.comp.id.getName() + '.html'
            price = item.comp.process.cost
            td.electric_fabrication.add_line(ComponentTableLine(name_body,name_link,item.quantity,price,item.comp.common.description))

        for item in self.dependency_analyzer.get_list():
            name_body = item.comp.id.getName()
            name_link = item.comp.id.getName() + '.html'
            td.assembly.add_line(ComponentTableLine(name_body,name_link,item.quantity,0,item.comp.common.description))

        rendered_str = self.template.render(data = td)

        os.makedirs(output_base_dir, exist_ok = True)
        output_file = str(output_base_dir) + '/index.html'
        with open(output_file, mode='w') as f:
            f.write(rendered_str)
        print('write html ' + output_file)

if __name__ == '__main__':
    td = TopPageData()
    tg = TopPageGenerator(td)
    tg.write('generate_index.html')