.. _bpy.types.NormalEditModifier:

********************
Normal Edit Modifier
********************

The Normal Edit Modifier affects (or generates) custom normals. It uses a few simple parametric methods
to compute normals (quite useful in game development and architecture areas), and mixes back those generated normals
with existing ones.

.. (todo <2.8 add) nice image


Options
=======

.. figure:: /images/modeling_modifiers_modify_normal-edit_panel.png

   Normal Edit Modifier.

Mode
   Radial
      Radial aligns normals with the (origin, vertex coordinates) vector, in other words all normals seems to radiate
      from the given center point, as if they were emitted from an ellipsoid surface.
   Directional
      Directional makes all normals point (converge) towards a given target object.
Target Object
   Uses this object's center as reference point when generating normals.

   Optional in *Radial* mode, mandatory in *Directional* one.
Parallel Normals
   Makes all normals parallel to the line between both objects' centers,
   instead of converging towards target's center.

   Only relevant in *Directional* mode.

Offset
   Gives modified object's center an offset before using it to generate normals.

   Only relevant in *Radial* mode if no *Target Object* is set,
   and in *Directional* mode when *Parallel Normals* is set.


Mix Mode
--------

Mix Mode
   How to affect existing normals with newly generated ones.

   Note the *Multiply* option is **not** a cross product, but a mere component-by-component multiplication.
Mix Factor
   How much of the generated normals get mixed into existing ones.
Vertex Group
   Allows per-item fine control of the mix factor. Vertex group influence can be reverted using the small
   "arrow" button to the right.
Max Angle
   (Todo)

   .. https://developer.blender.org/rBac7feaed3d4d

Lock Polygon Normals (padlock icon)
   (Todo)

   .. https://developer.blender.org/rB0eb324671315


Usage
=====

This modifier can be used to quickly generate radial normals for low-poly tree foliage or
"fix" shading of toon-like rendering by partially bending default normals...

The only mandatory prerequisite to use it is to enable *Auto Smooth* option in Mesh properties, *Normals* panel.

.. tip::

   More complex normal manipulations can be achieved by copying normals from one mesh to another,
   see the :doc:`Data Transfer Modifier </modeling/modifiers/modify/data_transfer>`.


Example
=======

.. figure:: /images/modeling_modifiers_modify_normal-edit_example.jpg
   :width: 680px

   Examples of edit custom normals to point towards a given direction,
   see `example blend-file <http://download.blender.org/ftp/mont29/persistent_data/sapling_CN.blend>`__.

The left tree mesh has unmodified normals, while on the right one a *Normal Edit* modifier is used to bend them
towards the camera. This shading trick is often used in games to fake scattering in trees and other vegetation.
