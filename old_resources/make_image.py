#!/usr/bin/python

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import os
import sys
import math
from stl_load import *
from xml_load import *

from PIL import Image
from PIL import ImageOps
import time

xml1=xml_load("data.xml")
stl_dict=model_dict_load(xml1.model_dict)
#print(xml1.parts_list)
#print(xml1.model_dict)
#print(xml1.assembly_list)
#print(xml1.quantity_dict)
#print(xml1.views_list)

def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, 1.0*w/h, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)

g_rank=-1
g_shot=0
g_div=0
g_divmax=16
g_move=0
def draw():
    if g_rank==-1:
        draw_parts(g_shot)
    else:
        draw_graphyc(g_rank,g_shot,g_move)

def draw_graphyc(rank,shot,move):

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, light0p)

    view=[0,0,0,0,0,0,0]
    for i in xml1.views_list:
	if i[0]==rank and i[1]==shot:
            print("view",i)
            view[0:6]=i[2:8]

    gluLookAt(view[0], view[1], view[2], view[3], view[4], view[5], 0.0, 0.0, 1.0)
    
    
    for pt in xml1.assembly_list:
        if(pt[1]<=rank):
            if(pt[2]==0 and pt[1]==rank):
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT,  [0.1, 0.0, 0.0, 1.0])
                glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE,  [0.3, 0.0, 0.0, 1.0])
                glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.5, 0.0, 0.0, 1.0])
            elif(pt[2]==0):
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT,  [0.1*0.5, 0.1*0.5, 0.1*0.5, 1.0])
                glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE,  [0.3*0.5, 0.3*0.5, 0.3*0.5, 1.0])
                glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.5*0.5, 0.5*0.5, 0.5*0.5, 1.0])
            elif(pt[2]==1):
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT,  [0.0, 0.0, 0.1, 1.0])
                glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE,  [0.0, 0.0, 0.3, 1.0])
                glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.5, 1.0])

            temp=[0,0,0]
            if(pt[1]==rank):
                temp[0]=pt[3][0]+pt[5][0]*move
                temp[1]=pt[3][1]+pt[5][1]*move
                temp[2]=pt[3][2]+pt[5][2]*move
            else:
                temp[0]=pt[3][0]
                temp[1]=pt[3][1]
                temp[2]=pt[3][2]

            glPushMatrix();
            glTranslated(temp[0], temp[1], temp[2])
            glRotated(pt[4][0], pt[4][1], pt[4][2], pt[4][3])
            print(pt)
            stl_dict[pt[0]].draw()
            glPopMatrix();

    glFlush()
    glutSwapBuffers()

def draw_parts(pt_number):

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glLightfv(GL_LIGHT0, GL_POSITION, light0p)

    view=xml1.parts_list[pt_number][5]
    print("part",pt_number,view)
    gluLookAt(view[0], view[1], view[2], view[3], view[4], view[5], 0.0, 0.0, 1.0)
        
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT,  [0.1, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE,  [0.3, 0.0, 0.0, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.5, 0.0, 0.0, 1.0])
    
    glPushMatrix();
    glTranslated(0, 0, 0)
    glRotated(0, 1, 0, 0)
    stl_dict[xml1.parts_list[pt_number][0]].draw()
    glPopMatrix();

    glFlush()
    glutSwapBuffers()


def capture():#name example: "output.png"
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)
    # capure
    glReadBuffer(GL_FRONT)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
    # sace image
    image = Image.frombytes("RGBA", (width, height), data)
    image = ImageOps.flip(image) # upside down
    return image

#main loop
def timer_process(arg):
    global image_list,g_rank,g_shot,g_div,g_move

    g_rank=-1
    g_shot=0
    for i in range(xml1.parts_quantity):
        draw()
        glFlush()
        glFinish()
        capture().save("image/part_"+str(g_shot)+".gif", save_all=True)
        g_shot+=1

    g_rank=0
    g_shot=0
    while True:
        g_div+=1
        if g_div==g_divmax:
            g_shot+=1
            g_div=0
        if g_shot>=xml1.shot_list[g_rank]:
            g_rank+=1
            g_shot=0
        if g_rank>=xml1.maxrank+1:
            break

        g_move=(g_divmax-g_div%g_divmax-1)/(g_divmax-1.0)
        print(g_rank,g_shot,g_move)

        if g_move==1:
            image_list=[]
    
        draw()
        glFlush()
        glFinish()
        image_list.append(capture())

        if g_move==0:
            image_list[0].save("image/assemble_"+str(g_rank)+"_"+str(g_shot)+".gif", save_all=True, append_images=image_list[1:], duration=200, loop=0)

    sys.exit()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(640, 640)
glutCreateWindow("PyOpenGL 12")

glutDisplayFunc(draw)
glutReshapeFunc(resize)

glClearColor(0.0, 0.0, 1.0, 0.0)
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)

light0p = [ 0.0, 300.0, 200.0, 1.0 ]
whiteColor = [ 1.0, 1.0, 1.0, 1.0 ]
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_DIFFUSE, whiteColor)
glLightfv(GL_LIGHT0, GL_SPECULAR, whiteColor)

#main
step=0
image_last=None
image_list=[]
if not os.path.exists("image"):
    os.makedirs("image")

glutTimerFunc(100, timer_process, 0);

glutMainLoop()

