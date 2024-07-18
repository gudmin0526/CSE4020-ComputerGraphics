import glfw
from OpenGL.GL import *
import numpy as np

gComposedM = np.identity(3)

# C, D
def key_callback(window, key, scancode, action, mods):
    global gComposedM
    if key == glfw.KEY_Q and action == glfw.PRESS:
        gComposedM = np.array(
            [[1.,0.,-.1],[0.,1.,0.],[0.,0.,1.]]
        ) @ gComposedM
    if key == glfw.KEY_E and action == glfw.PRESS:
        gComposedM = np.array(
            [[1.,0.,.1],[0.,1.,0.],[0.,0.,1.]]
        ) @ gComposedM
    if key == glfw.KEY_A and action == glfw.PRESS:
        degree10 = np.radians(10)
        gComposedM = gComposedM @ np.array(
            [[np.cos(degree10),-np.sin(degree10),0.],
            [np.sin(degree10),np.cos(degree10),0.],
            [0.,0.,1.]]
        ) 
    if key == glfw.KEY_D and action == glfw.PRESS:
        degree10 = np.radians(10)
        gComposedM = gComposedM @ np.array(
            [[np.cos(degree10),np.sin(degree10),0.],
            [-np.sin(degree10),np.cos(degree10),0.],
            [0.,0.,1.]]
        )
    if key == glfw.KEY_1 and action == glfw.PRESS:
        gComposedM = np.identity(3)

# B
def render(T): 
    glClear(GL_COLOR_BUFFER_BIT) 
    glLoadIdentity() 
    # draw cooridnate 
    glBegin(GL_LINES) 
    glColor3ub(255, 0, 0) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([1.,0.])) 
    glColor3ub(0, 255, 0) 
    glVertex2fv(np.array([0.,0.])) 
    glVertex2fv(np.array([0.,1.])) 
    glEnd() 
    # draw triangle 
    glBegin(GL_TRIANGLES) 
    glColor3ub(255, 255, 255) 
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] ) 
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] ) 
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] ) 
    glEnd() 

def main():
    global gComposedM
    if not glfw.init():
        return

    # A 
    window = glfw.create_window(480, 480, "2020089007-3-1", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gComposedM)
        glfw.swap_buffers(window)

    glfw.terminate()


global _primitive_type
_primitive_type = GL_LINE_LOOP

if __name__ == "__main__":
    main()