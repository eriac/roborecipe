#!/usr/bin/python3

from XmlParser import *
from TreeAnalyzer import *
from DirectorySearch import *

if __name__ == '__main__':
	# path_pair_list = [
	# 	['../sample/srs007/package.xml', '../sample/srs007/main_asm/assemble.roborecipe'],
	# 	['../sample/srs007/package.xml', '../sample/srs007/base_asm/assemble.roborecipe'],
	# 	['../sample/pololu/package.xml', '../sample/pololu/4691_37mm_motor/description.roborecipe'],
	# 	['../sample/iso_screw_m3/package.xml', '../sample/iso_screw_m3/pan_12/part.roborecipe']
	# ]

	ds = DirectorySearch('../sample')
	path_pair_list = ds.getFilePathList()

	component_list = ComponentListParser(path_pair_list).getList()
	# for c in component_list:
	# 	print(c.id.getName())

	ta = TreeAnalyzer(component_list, ComponentIdentifier('srs007', 'main_asm'))

	print("#### quantity ####")
	cl = ta.getQuantityList()
	for c in cl:
		print(c.id.getName(), cl[c])

	print("#### depend order ####")
	dl = ta.getDependOrderList()
	for c in dl:
		print(c.id.getName())

