from OpenGL.GL   import *
from OpenGL.GLU  import *
from OpenGL.GLUT import *
from sys import argv
from roborecipe.StlLoader import *

class PartSource:
    def __init__(self):
        self.filename = ""
        self.stl_model = None
        self.position = [0,0,0]
        self.rotation = [0,0,0,0]

class ViewSource:
    def __init__(self):
        self.filename = ""
        self.part_list = []

class ImageGenerator:
    def __init__(self):
        None


def init(): 
   glClearColor(0.0, 0.0, 0.0, 0.0)
#    glShadeModel(GL_FLAT)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glLoadIdentity()                 # clear the matrix 
    # viewing transformation 
    gluLookAt(0.0, 0.0, 600.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glScalef(1.0, 1.0, 1.0)          # modeling transformation 
    glutWireCube(10.0)

    stl1 = stl_load()
    stl1.load_stl("/home/ubuntu/roborecipe/old_resources/Laser1.stl")
    # stl1.draw()

    glBegin(GL_TRIANGLES)
    for tri in stl1.get_triangles():
        length=tri.normal.length()
        glNormal3f(-tri.normal.x/length,-tri.normal.y/length,-tri.normal.z/length)
        print("try",tri.points[0].x,tri.points[0].y,tri.points[0].z)
        glVertex([tri.points[0].x,tri.points[0].y,tri.points[0].z])
        glVertex([tri.points[1].x,tri.points[1].y,tri.points[1].z])
        glVertex([tri.points[2].x,tri.points[2].y,tri.points[2].z])
    glEnd()


    glFlush()

def reshape(w, h):
   glViewport(0, 0, w, h)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
#    glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 2000.0)
   gluPerspective(80, 1, 1.5, 2000)
   glMatrixMode(GL_MODELVIEW)

## ----------------------------------------
if __name__ == '__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(640, 640)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("test")             # modify
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    # glutKeyboardFunc(keyboard)         # append
    glutMainLoop()