# cut and paste this into the python console
## (note this imports this file and several others)
'''
import bpy

#bpy.ops.console.clear(scrollback=True, history=True)

mypath = r"C:\\Users\\jeffw\\OneDrive\\Documents\\blender\\"
basicname = mypath+"constructor.py" 
exec(compile(open(basicname).read(), basicname, 'exec'))

'''

import bpy
import pickle
import numpy as np

def add_arrow(name, start,end,radius):
    #The general strategy here will be to build the vector at the origin, then translate it to the intended location during the parenting step
    relative_end = end - start

    bpy.ops.curve.primitive_bezier_curve_add()
    rod = bpy.context.object
    rod.data.dimensions = '3D'
    rod.data.fill_mode = 'FULL'
    rod.data.use_fill_caps = True
    rod.data.bevel_depth = radius/2 #radius of the cylinder
    rod.data.bevel_resolution = 4 #controls the smoothness
   
    rod.data.splines[0].bezier_points[0].co = (0,0,0)
    rod.data.splines[0].bezier_points[0].handle_left_type = 'VECTOR'

    rod.data.splines[0].bezier_points[1].co = relative_end*0.8
    rod.data.splines[0].bezier_points[1].handle_left_type = 'VECTOR'

    bpy.ops.curve.primitive_bezier_curve_add()
    cone = bpy.context.object
    cone.data.dimensions = '3D'
    cone.data.fill_mode = 'FULL'
    cone.data.use_fill_caps = True
    cone.data.bevel_depth = radius
    cone.data.bevel_resolution = 4

    cone.data.splines[0].bezier_points[0].co = relative_end*0.8
    cone.data.splines[0].bezier_points[0].handle_left_type = 'AUTO'
    cone.data.splines[0].bezier_points[0].handle_right_type = 'AUTO'

    cone.data.splines[0].bezier_points[1].co = relative_end
    cone.data.splines[0].bezier_points[1].handle_left_type = 'AUTO'
    cone.data.splines[0].bezier_points[1].handle_right_type = 'AUTO'

    bpy.ops.curve.primitive_bezier_curve_add()
    taper = bpy.context.object

    taper.data.splines[0].bezier_points[0].co = (0,1,0)
    taper.data.splines[0].bezier_points[0].handle_left_type = 'AUTO'
    taper.data.splines[0].bezier_points[0].handle_right_type = 'AUTO'

    taper.data.splines[0].bezier_points[1].co = (1,0,0)
    taper.data.splines[0].bezier_points[1].handle_left_type = 'AUTO'
    taper.data.splines[0].bezier_points[1].handle_right_type = 'AUTO'

    cone.data.taper_object = taper

    bpy.ops.object.empty_add(location=start)
    arrow = bpy.context.object
    arrow.name = name

    rod.parent = arrow
    cone.parent = arrow
    taper.parent = arrow

    return arrow



   



start = np.array([1,2,3])
end = np.array([6, 6, 6])

arrow = add_arrow('arrow', start,end, 1)

arrow.rotation_mode = 'AXIS_ANGLE'
arrow.rotation_axis_angle = (0,1,0,0)

for frame in range(100):
    arrow.rotation_axis_angle = (frame*2*np.pi/360,1,0,0)
    arrow.keyframe_insert(data_path="rotation_axis_angle", frame=frame)
