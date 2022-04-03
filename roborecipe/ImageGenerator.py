from OpenGL.GL   import *
from OpenGL.GLU  import *
from OpenGL.GLUT import *
from PIL import Image
from PIL import ImageOps

class PartSource:
    def __init__(self):
        self.triangles = None
        self.position = [0,0,0]
        self.rotation = [0,0,0,0]
        self.move = [0,0,0,0]
        self.color = "gray"

class ViewSource:
    def __init__(self):
        self.output_filepath = ""
        self.part_list = []
        self.look_from = [200,0,0]
        self.look_at = [0,0,0]
        self.step = 0

class ImageGenerator:
    def __init__(self, argv):
        self.InitWindow(argv)
        self.target_view_list = []

    def renderViewList(self, view_list):
        self.target_view_list = view_list
        glutTimerFunc(100, self.timerProcess, 0)
        glutMainLoop()

    def InitWindow(self, argv):
        glutInit(argv)
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(640, 640)
        glutInitWindowPosition(100, 100)
        glutCreateWindow("test")             # modify
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        # lighting
        whiteColor = [ 0.0, 0.8, 0.0, 1.0 ]
        grayColor = [ 0.2, 0.2, 0.2, 1.0 ]
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, whiteColor)
        glLightfv(GL_LIGHT0, GL_SPECULAR, whiteColor)
        glLightfv(GL_LIGHT0, GL_AMBIENT, grayColor)

        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        # glutTimerFunc(100, self.timerProcess, 0)

    def display(self):
        None

    def display_view(self, view, step):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        light_pos = [ -0.0, 0.0, 200.0, 1.0 ]
        lf = view.look_from
        la = view.look_at
        self.initScene(light_pos, lf, la)
        rate=0
        if 0<view.step:
            rate=1.0*step/view.step
        self.putParts(view.part_list,rate)
        glFlush()
        glutSwapBuffers()
        glFinish()

    def initScene(self, light_pos, look_from, look_to):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        gluLookAt(look_from[0], look_from[1], look_from[2], look_to[0], look_to[1], look_to[2], 0.0, 0.0, 1.0)

    def putParts(self, part_list,rate):
        for part in part_list:
            glScalef(1.0, 1.0, 1.0)
            glColor3f(0.5, 0.5, 0.5)
            glPushMatrix()
            pos=[0,0,0]
            pos[0]=part.position[0]+part.move[0]*rate
            pos[1]=part.position[1]+part.move[1]*rate
            pos[2]=part.position[2]+part.move[2]*rate
            glTranslated(pos[0], pos[1], pos[2])

            glBegin(GL_TRIANGLES)
            for tri in part.triangles:
                length=tri.normal.length()
                glNormal3f(-tri.normal.x/length,-tri.normal.y/length,-tri.normal.z/length)
                glVertex([tri.points[0].x,tri.points[0].y,tri.points[0].z])
                glVertex([tri.points[1].x,tri.points[1].y,tri.points[1].z])
                glVertex([tri.points[2].x,tri.points[2].y,tri.points[2].z])
            glEnd()
            glPopMatrix()

    def capture(self):#name example: "output.png"
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


    def reshape(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(80, 1, 1.5, 2000)
        glMatrixMode(GL_MODELVIEW)

    # main process
    def timerProcess(self, arg):
        for view in self.target_view_list:
            if view.step == 0: # static image
                self.display_view(view, 0)
                img = self.capture()
                img.save(view.output_filepath, save_all=True)
                print("write image to ", view.output_filepath)
            else: # gif
                image_list=[]
                for i in range(view.step+1):
                    r = view.step - i
                    self.display_view(view, r)
                    img = self.capture()
                    image_list.append(img)
                image_list[0].save(view.output_filepath, save_all=True, append_images=image_list[1:], duration=100, loop=0)
                print("write git to ", view.output_filepath)
        print("finish render")
        glutLeaveMainLoop()


if __name__ == '__main__':
    from sys import argv
    from stl_load import *

    p1 = PartSource()
    stl1 = stl_load()
    stl1.load_stl("/home/ubuntu/roborecipe/old_resources/Laser1.stl")
    p1.triangles = stl1.get_triangles()

    p2 = PartSource()
    stl2 = stl_load()
    stl2.load_stl("/home/ubuntu/roborecipe/old_resources/Laser2.stl")
    p2.triangles = stl2.get_triangles()
    p2.position = [0,0,0]
    p2.move = [0,0,50]

    view1 = ViewSource()
    view1.output_filepath = "/home/ubuntu/roborecipe/out.png"
    view1.part_list.append(p1)
    view1.part_list.append(p2)
    view1.look_from = [200,0,100]
    view1.look_at = [0,0,0]
    view1.step=0

    view2 = ViewSource()
    view2.output_filepath = "/home/ubuntu/roborecipe/out.gif"
    view2.part_list.append(p1)
    view2.part_list.append(p2)
    view2.look_from = [200,0,100]
    view2.look_at = [0,0,0]
    view2.step=10

    ig = ImageGenerator(sys.argv)
    ig.renderViewList([view1, view2])
