import sys
import pyglet
from pyglet.gl import *
from noise import pnoise1
from random import random
import time
window = pyglet.window.Window(visible=False, resizable=True)


def on_resize(width, height):
    """Setup 3D viewport"""
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, 1.0 * width / height, 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


window.on_resize = on_resize
window.set_visible()

points = 100
span = 5.0
speed = 1.0

if len(sys.argv) > 1:
    octaves = int(sys.argv[1])
else:
    octaves = 2

base = 0
min = max = 0

timeREF = 1479030185  #time.time()

y = 0.005


@window.event
def on_draw():
    global min, max

    global timeREF, y
    window.clear()
    glLoadIdentity()
    glTranslatef(0, 0, -1)
    r = range(256)
    glBegin(GL_LINE_STRIP)
    for i in r:
        x = float(i) * span / points - 0.5 * span
        y = pnoise1(float(i) / 20.0 + base, octaves)
        print(float(i) / 20.0 + base)
        # y = pnoise1(x + base, octaves)
        # time.sleep(0.005)
        # print(time.time() - timeREF)
        # y = (random() * 2 - 1)
        glVertex3f(x * 2.0 / span, y, 0)

    glEnd()

# @window.event
# def on_draw():
#     global min, max
#
#     global timeREF
#     window.clear()
#     glLoadIdentity()
#     glTranslatef(0, 0, -1)
#     r = range(256)
#     y = 0.005
#     glBegin(GL_LINE_STRIP)
#     for i in r:
#         x = float(i) * span / points - 0.5 * span
#         y = (random() - 0.5)
#         glVertex3f(x * 2.0 / span, y, 0)
#
#     timeREF = time.time()
#     glEnd()


def update(dt):
    global base
    base += dt * speed


pyglet.clock.schedule_interval(update, 1.0 / 3.0)

pyglet.app.run()
