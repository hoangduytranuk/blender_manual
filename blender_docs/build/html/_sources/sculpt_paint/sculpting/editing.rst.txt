
*******
Editing
*******

Sculpt
======

.. _bpy.ops.sculpt.set_pivot_position:

Set Pivot
   Like Object and Edit Mode, Sculpt Mode also has a :term:`pivot point`.
   This is because the basic move, scale, rotate transforms are also possible in Sculpt Mode.

   Origin
      Sets the pivot to the origin of the sculpt.
   Unmasked
      Sets the pivot position to the average position of the unmasked vertices.
   Mask Border
      Sets the pivot position to the center of the mask's border.
   Active Vertex
      Sets the pivot position to the active vertex position.
   Surface
      Sets the pivot position to the surface under the cursor.

      .. seealso::

         :doc:`Object and Edit Mode Pivot </editors/3dview/controls/pivot_point/index>`

Rebuild BVH
   Recalculates the :term:`BVH` used by :doc:`/sculpt_paint/sculpting/tool_settings/dyntopo`
   which can improve performance which might degrade over time while using Dyntopo.


Mask
====

See :doc:`/sculpt_paint/sculpting/hide_mask`.


.. _sculpting-editing-facesets:

Face Sets
=========

Todo.
