.. (TODO) out of date, need update
   https://developer.blender.org/rB6554207841a4

.. _bpy.types.SimpleDeformModifier:

**********************
Simple Deform Modifier
**********************

The Simple Deform Modifier allows easy application of a simple deformation to
an object (meshes, lattices, curves, surfaces and texts are supported).

Using another object, it is possible to define the axis and origin of the deformation,
allowing application of very different effects.


Options
=======

.. figure:: /images/modeling_modifiers_deform_simple-deform_panel.png

   Simple Deform.

Mode
   This radio button defines the kind of deformation which will be applied.

   Twist
      Rotates around the Z axis.
   Bend
      Bends the mesh over the Z axis.
   Taper
      Linearly scales along Z axis.
   Stretch
      Stretches the object along the Z axis (negative *Factor* leads to squash),
      preserving volume by scaling inversely on the X and Y axes.

Vertex Group
   The name of the vertex group that indicates whether and how much each vertex is influenced by the deformation.

Origin
   The name of an object that defines the origin of deformation (usually an empty). This object can be:

   - Rotated to control the axis (its local Z axis is now used as the deformation axis).
   - Translated to control the origin of deformation.
   - Scaled to change the deform factor.

   .. note::

      When the object controlling the origin (the one in the *Origin* field)
      is a child of the deformed object, this creates a cyclic dependency in Blender's data system.
      The workaround is to create a new empty and parent both objects to it.

Angle/Factor
   The amount of deformation. Can be negative to reverse the deformation.

Limits
   These settings allow you to set the lower and upper limits of the deformation.
   The upper limit cannot be lower than lower limit.

Lock X Axis / Lock Y Axis (Taper and Stretch modes only)
   These controls whether the X and/or Y coordinates are allowed to change or not.
   Thus it is possible to squash the X coordinates of an object and keep the Y coordinates intact.
