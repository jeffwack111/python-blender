# cut and paste this into the python console
## (note this imports this file and several others)
'''
import bpy

#bpy.ops.console.clear(scrollback=True, history=True)

mypath = r"C:\\Users\\jeffw\\OneDrive\\Documents\\python-blender\\"
basicname = mypath+"curve_anim.py" 
exec(compile(open(basicname).read(), basicname, 'exec'))

'''

#This script will animate a spline curve which lives on the x-axis using values from an array which will be unpickled at the start
#The position of the points of the curve will be given by a complex number, and interpreted with 1 pointing along the y axis
#and i pointing along the z axis


import bpy
import numpy as np
import pickle

bpy.ops.curve.primitive_bezier_curve_add(location=(0.0, 0.0, 0.0),enter_editmode=True)

for i in range(6):
    bpy.ops.curve.subdivide()


bpy.ops.object.editmode_toggle()

curve = bpy.context.object

curve.data.dimensions = '3D'
curve.data.fill_mode = 'FULL'

curve.data.use_fill_caps = True
curve.data.bevel_depth = 0.02 #radius of the cylinder
curve.data.bevel_resolution = 4 #controls the smoothness

points = curve.data.splines[0].bezier_points
N = len(points)

for frame in range(250):
    for n, point in enumerate(points):
        point.co = (n/N,np.sin(2*np.pi*(n/N+frame/250)),0)
        point.handle_right_type = 'AUTO'
        point.handle_left_type = 'AUTO'
        point.keyframe_insert(data_path="co", frame=frame)
        point.keyframe_insert(data_path='handle_right', frame=frame)
        point.keyframe_insert(data_path='handle_left', frame=frame)

