.. |pivot-icon| image:: /images/scene-layout_object_editing_transform_control_pivot-point_menu.png

*******************
Bounding Box Center
*******************

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode and Edit Mode
   :Header:    |pivot-icon| :menuselection:`Pivot Point --> Bounding Box Center`
   :Hotkey:    :kbd:`Comma`

The bounding box is a rectangular box that is wrapped as tightly as possible around the selection.
It is oriented parallel to the world axes. In this mode the pivot point lies at the center of the bounding box.
You can set the pivot point to *Bounding Box* with :kbd:`Comma` or via the menu in the editor's header.
The image below shows how the object's bounding box size is determined by the size of the object.

.. figure:: /images/scene-layout_object_editing_transform_control_pivot-point_bounding-box-center_demo.png

   Relationship between an Object and its Bounding Box.


In Object Mode
==============

In *Object Mode*, transformation
takes place relative to the location of the objects origin (indicated by the yellow circle),
and the size of objects is not taken into account.
The image below shows the results of using the *Bounding Box* as
the pivot point in a number of situations.

.. figure:: /images/scene-layout_object_editing_transform_control_pivot-point_individual-origins_rotation-around-center.png

   Single object rotation.

In this example, the orange rectangle has its origin located on the far left of the mesh,
while the blue rectangle has its origin located in the center of the mesh.

When a single object is selected, the rotation takes place around its origin.

.. figure:: /images/scene-layout_object_editing_transform_control_pivot-point_bounding-box-center_object-mode.png

   Shows the location of the Bounding Box (left) pivot point compared to the Median Point (right).

The image above (left) shows that when multiple objects are selected,
the pivot point is calculated based on the bounding box of all the selected objects.
More precisely, the centers of objects are taken into account.


In Edit Mode
============

This time it is the Object Data that is enclosed in the bounding box.
The bounding box in *Edit Mode* takes no account of the Object(s) origins,
only the center of the selected vertices.

.. figure:: /images/scene-layout_object_editing_transform_control_pivot-point_bounding-box-center_edit-mode-rotation.png

   The effects of rotation in different mesh selection modes when the bounding box is set as the pivot point.
   The pivot point is shown by a yellow circle.

.. figure:: /images/scene-layout_object_editing_transform_control_pivot-point_bounding-box-center_median-point.png

   The Bounding Box center compared to the Median Point.
