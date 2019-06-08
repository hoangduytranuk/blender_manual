
*************
Object Origin
*************

Each object has an origin point. The location of this point determines where the object is located in 3D space.
When an object is selected, a small circle appears, denoting the origin point.
The location of the origin point is important when translating, rotating or scaling an object.
See :doc:`Pivot Points </scene_layout/object/editing/transform/control/pivot_point/index>` for more.

The color of the origin is set by the :ref:`animation-state-colors` and
in light blue to denote library linkage on both the source and the linked object.
The size can be changed in the :doc:`Interface tab </editors/preferences/interface>` of the Preferences.


.. _bpy.ops.object.origin_set:

Set Origin
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      Object and Edit Modes
   :Panel:     :menuselection:`Tool Shelf --> Tools --> Edit --> Set Origin`
   :Menu:      :menuselection:`Object --> Transform`
   :Hotkey:    :kbd:`Shift-Ctrl-Alt-C`

The Object Origin and Geometry can be moved relative to each other and to the 3D Cursor.

Type
   Geometry to Origin
      Moves the model to the origin and
      this way the origin of the object will also be at the center of the object.
   Origin to Geometry
      Moves the origin to the center of the object and
      this way origin of the object will also be at the center of the object.
   Origin to 3D Cursor
      Moves the origin of the model to the position of the 3D cursor.
   Origin to Center of Mass
      Moves the origin to the calculated center of mass of model (assuming the mesh has a uniform density).
Center
   Median Point Center, Bounding Box Center
