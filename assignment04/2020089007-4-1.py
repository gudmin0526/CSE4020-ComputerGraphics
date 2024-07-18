import glfw 
from OpenGL.GL import * 
import numpy as np 
from OpenGL.GLU import * 

def render(): 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
    glEnable(GL_DEPTH_TEST) 
 
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity() 
    glOrtho(-2,2, -2,2, -1,1) 
 
    glMatrixMode(GL_MODELVIEW) 
    glLoadIdentity() 
     
    drawFrame() 
    t = glfw.get_time() 
 
    # blue base transformation 
    glPushMatrix() # I I
    glTranslatef(np.sin(t), 0, 0) # T I
    drawFrame()
 
    # blue base drawing 
    glPushMatrix() # T T I
    glScalef(.2, .2, .2) # TS T I 
    glColor3ub(0, 0, 255) 
    drawBox() 
    glPopMatrix() # T I
 
    # red arm transformation 
    glPushMatrix() # T T I
    glRotatef(t*(180/np.pi), 0, 0, 1) # TR T I 
    glTranslatef(.5, 0, .01) # TRT T I

    # red arm drawing 
    glPushMatrix() # TRT TRT T I
    drawFrame()
    glScalef(.5, .1, .1) # TRTS TRT T I
    glColor3ub(255, 0, 0) 
    drawBox() 
    glPopMatrix() # TRT T I

    # green arm transformation
    glPushMatrix() # TRT TRT T I
    glTranslatef(.5, 0, .02) # TRTT TRT T I
    glRotatef(t*(180/np.pi), 0, 0, 1) # TRTTR TRT T I
    
    # green arm drawing
    glPushMatrix() # TRTTR TRTTR TRT T I
    drawFrame()
    glScale(.2, .2, .2) # TRTTRS TRTTR TRT T I
    glColor3ub(0, 255, 0)
    drawBox()
    glPopMatrix() # TRTTR TRT T I
 
    glPopMatrix() # TRT T I
    glPopMatrix() # T I
    glPopMatrix() # I
 
def drawBox(): 
    glBegin(GL_QUADS) 
    glVertex3fv(np.array([1,1,0.])) 
    glVertex3fv(np.array([-1,1,0.])) 
    glVertex3fv(np.array([-1,-1,0.])) 
    glVertex3fv(np.array([1,-1,0.])) 
    glEnd() 
 
def drawFrame(): 
    # draw coordinate: x in red, y in green, z in blue 
    glBegin(GL_LINES) 
    glColor3ub(255, 0, 0) 
    glVertex3fv(np.array([0.,0.,0.])) 
    glVertex3fv(np.array([1.,0.,0.])) 
    glColor3ub(0, 255, 0) 
    glVertex3fv(np.array([0.,0.,0.])) 
    glVertex3fv(np.array([0.,1.,0.])) 
    glColor3ub(0, 0, 255) 
    glVertex3fv(np.array([0.,0.,0])) 
    glVertex3fv(np.array([0.,0.,1.])) 
    glEnd() 
 
def main(): 
    if not glfw.init(): 
        return 
    window = glfw.create_window(480,480,'2020089007-4-1', None,None) 
    if not window: 
        glfw.terminate() 
        return 
    glfw.make_context_current(window) 
    glfw.swap_interval(1) 
 
    while not glfw.window_should_close(window): 
        glfw.poll_events() 
        render() 
        glfw.swap_buffers(window) 
 
    glfw.terminate() 
 
if __name__ == "__main__": 
    main() 