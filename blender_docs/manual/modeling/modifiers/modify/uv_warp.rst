.. _bpy.types.UVWarpModifier:

****************
UV Warp Modifier
****************

The *UV Warp* modifier uses two objects to define a transformation which is applied to the chosen UV map.

Its purpose is to give you direct control over the object's UVs in the 3D View,
allowing you to directly move, rotate and scale existing UV coordinates using controller objects or bones.


Options
=======

.. figure:: /images/modeling_modifiers_modify_uv-warp_panel.png
   :align: right

UV Center
   The center point of the UV map to use when applying scale or rotation.
   With (0, 0) at the bottom left and (1, 1) at the top right. Defaults to (0.5, 0.5).
UV Axis
   The axes to use when mapping the 3D coordinates into 2D.
From, To
   The two objects used to define the transformation. See `Usage`_ below.
Vertex Group
   The vertex group can be used to scale the influence of the transformation per vertex.
UV Map
   Which UV map to modify.
   Defaults to the active rendering layer.


Usage
=====

How the UVs are warped is determined by the difference between the transforms (location, rotation and scale)
of the *from* and *to* objects.

If the *to* object has the same transforms as the *from* object, the UVs will not be changed.

Assuming the *UV Axis* of the modifier is X/Y and the scale of the objects is (1, 1, 1), if the *to* object is
one unit away from the *from* object on the X axis, the UVs will be transformed on the U axis (horizontally)
by one full UV space (the entire width of the image).
