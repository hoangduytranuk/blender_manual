.. _bpy.types.SmoothModifier:

***************
Smooth Modifier
***************

The Smooth Modifier smooths a mesh by flattening the angles between adjacent faces in it,
just like :menuselection:`Specials --> Smooth` in Edit Mode.
It smooths without subdividing the mesh -- the number of vertices remains the same.

.. figure:: /images/modeling_modifiers_deform_smooth_panel.png

   Smooth Modifier panel.

This modifier is not limited to smoothing, though.
Its control factor can be configured outside the (0.0 to 1.0) range
(including negative values), which can result in interesting deformations.


Options
=======

Axis
   Toggle buttons to enable/disable the modifier in the X, Y and/or Z axes directions.

   X, Y, Z
Factor
   The factor to control the smoothing amount.
   Higher values will increase the effect.
   Values outside this range (above 1.0 or below 0.0) distort the mesh.
Repeat
   The number of smoothing iterations,
   equivalent to executing the Smooth tool multiple times.
Vertex Group
   A vertex group name, to restrict the effect to the vertices in it only.
   This allows for selective, real-time smoothing, by painting vertex weights.


Algorithm
=========

The calculation done by the Smooth Modifier is a simple and logical one,
and can be thought of as the geometric equivalent of blurring images.

Each new vertex position is simply the average position of surrounding vertices
(the vertices connected to the same edge as it).

.. (TODO) Add diagrams.


Example
=======

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_transform_smooth_mesh-before.png
          :width: 200px

          Mesh before smoothing.

     - .. figure:: /images/modeling_meshes_editing_transform_smooth_mesh-one-iteration.png
          :width: 200px

          Mesh after one smoothing iteration.

     - .. figure:: /images/modeling_meshes_editing_transform_smooth_mesh-ten-iterations.png
          :width: 200px

          Mesh after ten smoothing iterations.
