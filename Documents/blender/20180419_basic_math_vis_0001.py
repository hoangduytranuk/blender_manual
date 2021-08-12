import bpy
from math import sin, cos, pi

def circle_coord(angle):
    rad = angle * pi / 180
    x = cos(rad)
    y = sin(rad)
    return (x,y)

for i in range(0, 8):
    x,y = circle_coord(i * 45)
    bpy.ops.mesh.primitive_cube_add(location=(x*3, y*3, 0))