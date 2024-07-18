import glfw
from OpenGL.GL import *
import numpy as np


def key_callback(window, key, scancode, action, mods):
    global _primitive_type
    if key == glfw.KEY_1 and action == glfw.PRESS:
        _primitive_type = GL_POINTS
    if key == glfw.KEY_2 and action == glfw.PRESS:
        _primitive_type = GL_LINES
    if key == glfw.KEY_3 and action == glfw.PRESS:
        _primitive_type = GL_LINE_STRIP
    if key == glfw.KEY_4 and action == glfw.PRESS:
        _primitive_type = GL_LINE_LOOP
    if key == glfw.KEY_5 and action == glfw.PRESS:
        _primitive_type = GL_TRIANGLES
    if key == glfw.KEY_6 and action == glfw.PRESS:
        _primitive_type = GL_TRIANGLE_STRIP
    if key == glfw.KEY_7 and action == glfw.PRESS:
        _primitive_type = GL_TRIANGLE_FAN
    if key == glfw.KEY_8 and action == glfw.PRESS:
        _primitive_type = GL_QUADS
    if key == glfw.KEY_9 and action == glfw.PRESS:
        _primitive_type = GL_QUAD_STRIP
    if key == glfw.KEY_0 and action == glfw.PRESS:
        _primitive_type = GL_POLYGON


def render():
    global _primitive_type

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(_primitive_type)
    for th in np.linspace(0, np.radians(330), 12):
        glVertex2fv(np.array([np.cos(th), np.sin(th)]))
    glEnd()


def main():
    if not glfw.init():
        return

    window = glfw.create_window(480, 480, "2020089007-2-1", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()
        glfw.swap_buffers(window)

    glfw.terminate()


global _primitive_type
_primitive_type = GL_LINE_LOOP

if __name__ == "__main__":
    main()
