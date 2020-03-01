
************
Introduction
************

*Sculpt Mode* is similar to *Edit Mode* in that it is used to alter the shape of a model,
but Sculpt Mode uses a very different workflow:
instead of dealing with individual elements (vertices, edges, and faces),
an area of the model is altered using a brush.
In other words, instead of selecting a group of vertices,
Sculpt Mode manipulates geometry in the brush region of influence.

.. figure:: /images/sculpt-paint_sculpting_introduction_example.jpg

   Sculpting Mode Example.


Sculpt Mode
===========

Sculpt Mode is selected from the mode menu of the 3D View header.
Once Sculpt Mode is activated, the Toolbar of the 3D View will change to
Sculpt Mode specific panels. A red circle will appear and
follow the location of the cursor in the 3D View.

.. note::

   To have a predictable brush behavior, apply the scale of your mesh.


The Brush
=========

Sculpt Mode uses a similar brush to other the other :doc:`painting modes </sculpt_paint/brush/introduction>`,
but it is slightly more advanced. All the normal brush controls still apply,
and it functions exactly the same, however, the brush for sculpting is displayed in 3D.
This means that the brush will follow the contours of the mesh and the radius is displayed
by orienting the brush to match the meshes :term:`normal`.
How closely the cursor follows the curvature of the mesh can be changed in
the :doc:`Brush Settings </sculpt_paint/sculpting/tool_settings/brush_settings>`.

The brush can also change depending on the currently active :doc:`tool </sculpt_paint/sculpting/tools>`
to better display how that tool works.


Pivot Point
===========

Like Object and Edit mode Sculpt mode also has a :term:`Pivot Point`,
this is because the basic move, scale, rotate transforms are also possible in sculpt mode.

.. seealso::

   :doc:`Object and Edit Mode Pivot </scene_layout/object/editing/transform/control/pivot_point/index>`


.. _bpy.ops.sculpt.set_pivot_position:

Set Pivot
---------

.. admonition:: Reference
   :class: refbox

   :Mode:      Sculpt Mode
   :Menu:      :menuselection:`Sculpt --> Set Pivot`

Origin
   Sets the pivot to the origin of the sculpt
Unmasked
   Sets the pivot position to the average position of the unmasked vertices
Mask border
   Sets the pivot position to the center of the border of the mask
Active vertex
   Sets the pivot position to the active vertex position
Surface
   Sets the pivot position to the surface under the cursor
