#!/usr/bin/python3


import os
import math

from xml_load import *

from jinja2 import *

class HtmlGenerator:
    def __init__(self):
        None


f=None
def start_html(name):
	global f
	str="""
	<!DOCTYPE html>
	<html>
	<head>
	<title>RoboRecipe</title>
	</head>
	<body>
	"""
	f = open(name, 'w')
	f.write(str)


def end_html():
	str="""
	</body>
	</html>
	"""
	f.write(str)
	f.close()

def parts_list_html(xml1):
	f.write('<table border="1">')
	f.write("<tr>")
	f.write('<td>Image</td>')
	f.write('<td>Name</td>')
	f.write('<td>Type</td>')
	f.write('<td>Quantity</td>')
	f.write("</tr>")

	for i ,v in enumerate(xml1.parts_list):
		f.write("<tr>")
		f.write('<td><img src="image/part_'+str(i)+'.gif" width="200"></td>')
		f.write('<td>'+v[0]+'</td>')
		f.write('<td>'+v[2]+'</td>')
		f.write('<td>'+str(xml1.quantity_dict[v[0]])+'</td>')
		f.write("</tr>")

	f.write("</table>")

def assemble_list_html(xml1):
	for i in range(xml1.maxrank):
		f.write("<h2>Step"+str(i)+"</h2>")
	
		f.write('<table border="1">')	
		f.write("<tr>")
		f.write('<td>Image</td>')
		f.write('<td>Name</td>')
		f.write('<td>Quantity</td>')
		f.write("</tr>")
		print("")
		for j in range(len(xml1.apt_list[i])):
			jname=xml1.apt_list[i].keys()[j]
			jquantity=xml1.apt_list[i][xml1.apt_list[i].keys()[j]]
			print(jname,jquantity)
			for k in range(100):
				if xml1.parts_list[k][0]==jname:
					break
			print("No:",k)
					
			f.write("<tr>")
			f.write('<td><img src="image/part_'+str(k)+'.gif" width="200"></td>')
			f.write('<td>'+jname+'</td>')
			f.write('<td>'+str(jquantity)+'</td>')
			f.write("</tr>")

		f.write("</table>")

		for j in range(xml1.shot_list[i]):
			f.write('<img src="image/assemble_'+str(i)+'_'+str(j)+'.gif" width="500">')	

		f.write('<Hr Color="black">')

# def make_html(name):
# 	xml1=xml_load(name)
# 	#print(xml1.parts_list)
# 	#print(xml1.model_dict)
# 	#print(xml1.assembly_list)
# 	#print(xml1.quantity_dict)
# 	#print(xml1.views_list)
# 	start_html("index.html")
# 	f.write("<h1>Parts List</h1>")
# 	parts_list_html(xml1)
# 	f.write('<Hr Size="5" Color="black">')
# 	f.write("<h1>Assemble List</h1>")
# 	f.write('<Hr Color="black">')
# 	assemble_list_html(xml1)


# 	end_html()

# make_html("data.xml")






