#!/usr/bin/python3
from jinja2 import Template

path  = 'templates/index.html'
with open(path) as f:
    template = Template(f.read())

class ComponentIdentifier:
    def __init__(self, pkg = "unknown", type = "unknown"):
        self.pkg_name = pkg
        self.type_name = type
    def getName(self):
        return self.pkg_name + "/" + self.type_name

class ParchageItem:
    def __init__(self):
        self.id = ComponentIdentifier()
        self.quantity = 0
        self.price_value = 0
        self.price_unit = "yen"
        self.url = 'http:/aaa.bbb'
        self.description = "description"

p1 = ParchageItem()
p1.id = ComponentIdentifier('p1', 't1')
p1.quantity = 1
p2 = ParchageItem()
p2.id = ComponentIdentifier('p2', 't2')
p2.quantity = 2
part_list = [p1, p2]


class ComponentItem:
    def __init__(self, pkg = "unknown", type = "unknown", quantity = 0):
        self.id = ComponentIdentifier(pkg, type)
        self.quantity = quantity

class AssemblyStep:
    def __init__(self):
        self.seq_no = 0
        self.component_list = []
        self.image_path_list = []

class AssemblyItem:
    def __init__(self):
        self.name = "unknown"
        self.quantity = 0
        self.step_list = []

a1 = AssemblyItem()
a1.name = "A1"
a1.quantity = 1
a1_1 = AssemblyStep()
a1_1.seq_no = 1
a1_1.component_list.append(ComponentItem("p1", "t1", 1))
a1_1.component_list.append(ComponentItem("p2", "t2", 2))
a1_1.image_path_list.append("../image/assemble_0_0.gif")
a1.step_list.append(a1_1)

a1_2 = AssemblyStep()
a1_2.seq_no = 2
a1_2.component_list.append(ComponentItem("p1", "t1", 1))
a1_2.component_list.append(ComponentItem("p2", "t2", 2))
a1_2.image_path_list.append("../image/assemble_1_0.gif")
a1_2.image_path_list.append("../image/assemble_1_1.gif")
a1.step_list.append(a1_2)

a2 = AssemblyItem()
a2.name = "A2"
a2.quantity = 2

assembly_list =[a1, a2] 

ren_s = template.render(tittle='roborecipe', body="<p>body</p>", part_list=part_list, assembly_list=assembly_list)

output_path  = 'generate_index.html'
with open(output_path, mode='w') as f:
    f.write(ren_s)
print('write ' + output_path)