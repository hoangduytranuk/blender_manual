.. |pivot-icon| image:: /images/scene-layout_object_editing_transform_control_pivot-point_menu.png

.. _pivot-point-index:

###############
  Pivot Point
###############

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode and Edit Mode
   :Header:    |pivot-icon| :menuselection:`Pivot Point`

When rotating or scaling an object or group of vertices/edges/faces,
you may want to shift the :term:`pivot point` to make it easier to manipulate an object.
Using this selector in the header of any 3D View, you can change the location of the pivot point.

.. figure:: /images/scene-layout_object_editing_transform_control_pivot-point_popover.png


Pivot Types
===========

.. toctree::
   :maxdepth: 2

   bounding_box_center.rst
   3d_cursor.rst
   individual_origins.rst
   median_point.rst
   active_element.rst


.. _bpy.types.ToolSettings.use_transform_data_origin:
.. _bpy.types.ToolSettings.use_transform_pivot_point_align:

Affect Only
===========

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode and Pose Mode
   :Header:    :menuselection:`Pivot Point --> Affect Only`

Origins
   Directly transforms the object's :doc:`origin </scene_layout/object/origin>`.
   This only works for objects with data which can be transformed;
   i.e. it will not work on Text objects.
Locations
   Changes the position of the object's origin relative to another point during transformation.
   In other words, the pivot point and the origin cannot share the same location.
   This will not affect the object local transforms, just it's position in world space.

   In the examples below, a comparison of the scaling and rotation of objects,
   when *Location* is enabled (middle) and disabled (right).

   .. figure:: /images/scene-layout_object_editing_transform_control_pivot-point_index_rotate.png

      Rotation example.

   .. figure:: /images/scene-layout_object_editing_transform_control_pivot-point_index_scale.png

      Scaling example.
