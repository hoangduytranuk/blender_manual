.. _bpy.types.CastModifier:

*************
Cast Modifier
*************

This modifier shifts the shape of a mesh, curve,
surface or lattice to any of a few predefined shapes (sphere, cylinder, cuboid).

It is equivalent to the *To Sphere* tool in *Edit Mode*
:menuselection:`Mesh --> Transform --> To Sphere`, :kbd:`Shift-Alt-S`
and what other programs call "Spherify" or "Spherize", but, as written above,
it is not limited to casting to a sphere.

.. tip::

   The :doc:`Smooth Modifier </modeling/modifiers/deform/smooth>` is a good companion to *Cast*,
   since the cast shape sometimes needs smoothing to look nicer or even to fix shading artifacts.

.. note::

   For performance reasons, this modifier only works with local coordinates.
   If the modified object looks wrong, you may need to apply its rotation :kbd:`Ctrl-A`,
   especially when casting to a cylinder.


Options
=======

.. figure:: /images/modeling_modifiers_deform_cast_panel.png

   Cast Modifier.

Cast Type
   Menu to choose target shape of the projection.

   Sphere, Cylinder, Cuboid
Axis
   Toggle buttons to enable/disable the modifier in the X, Y, Z axes directions
   (X and Y only for *Cylinder* cast type).

   X, Y, Z
Factor
   The factor to control blending between original and cast vertex positions.
   It is a linear interpolation: 0.0 gives original coordinates (i.e. modifier has no effect),
   1.0 casts to the target shape.
   Values below 0.0 or above 1.0 exaggerate the deformation, sometimes in interesting ways.
Radius
   If non-zero, this radius defines a sphere of influence.
   Vertices outside it are not affected by the modifier.
Size
   Alternative size for the projected shape. If zero,
   it is defined by the initial shape and the control object, if any.
From radius
   If activated, calculate *Size* from *Radius*, for smoother results.

Vertex Group
   A vertex group name, to restrict the effect to the vertices in it only.
   This allows for selective, real-time casting, by painting vertex weights.
Control Object
   The name of an object to control the effect.
   The location of this object's origin defines the center of the projection.
   Also, its size and rotation transform the projected vertices.

   .. hint::

      Animating (keyframing) this control object also animates the modified object.


Example
=======

.. figure:: /images/modeling_modifiers_deform_cast_example.jpg
   :width: 400px

   Top: Suzanne without modifiers. Middle: Suzanne with each type of Cast Modifier (Sphere, Cylinder and Cuboid).
   Bottom: Same as above, but now only X axis is enabled.
   `Sample blend-file <https://wiki.blender.org/wiki/File:263-Cast-Modifier.blend>`__.
