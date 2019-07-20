.. _bpy.types.SimpleDeformModifier:

**********************
Simple Deform Modifier
**********************

The *Simple Deform* modifier allows easy application of a simple deformation to
an object (meshes, lattices, curves, surfaces and texts are supported).

Using another object, it is possible to define the axis and origin of the deformation,
allowing application of very different effects.


Options
=======

.. figure:: /images/modeling_modifiers_deform_simple-deform_panel.png
   :align: right

   The Simple Deform modifier.

Mode
   Defines the kind of deformation which will be applied.

   Twist
      Rotates the mesh around the specified *Axis*.
   Bend
      Bends the mesh over the specified *Axis*.
   Taper
      Linearly scales along the specified *Axis*.
   Stretch
      Stretches the object along the specified *Axis* (negative *Factor* leads to squash),
      preserving volume by scaling inversely on the two other axes.

Vertex Group
   The name of the vertex group that indicates whether and how much each vertex is influenced by the deformation.

Axis, Origin
   The name of an object that defines the origin and axis of deformation (usually an empty). This object can be:

   - Rotated to control the axis (its local *Axis* is now used as the deformation one).
   - Moved to control the origin of the deformation.
   - Scaled to change the deformation factor.

Angle/Factor
   The amount of deformation. Can be negative to reverse the deformation.

Limits
   These settings allow you to set the lower and upper limits of the deformation.
   The upper limit cannot be lower than the lower one.

Lock X/Y/Z (Twist, Taper and Stretch modes only)
   These controls whether the coordinates along the two other axes are allowed to change or not.
   E.g. if you *Stretch* your object along its Z axis,
   it is possible to squash along the X axis only, by locking the Y one.
