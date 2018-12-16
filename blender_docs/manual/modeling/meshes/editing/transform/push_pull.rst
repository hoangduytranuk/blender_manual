.. _bpy.ops.transform.push_pull:

*********
Push/Pull
*********

.. admonition:: Reference
   :class: refbox

   :Mode:      Object and Edit Modes
   :Panel:     :menuselection:`Tool Shelf --> Tools --> Transform --> Push/Pull`
   :Menu:      :menuselection:`Object/Mesh --> Transform --> Push Pull`

.. figure:: /images/modeling_meshes_editing_transform_push-pull_operator-panel.png
   :align: right

   Push/Pull distance.

*Push/Pull* will move the selected elements (objects, vertices, edges or faces)
closer together (Push) or further apart (Pull).
Specifically, each element is moved towards or away from the center by the same distance.
This distance is controlled by moving the mouse up (Push) or down (Pull), numeric input or through slider control.


Usage
=====

Select the elements you want to operate on and activate the Push/Pull transform tool.
The Push/Pull tool can be invoked from the :menuselection:`Object/Mesh --> Transform --> Push/Pull` menu
or by pressing :kbd:`Spacebar` and using the operator search menu to search for *Push* or
*Pull*. The amount of movement given to the selection can be determined
interactively by moving the mouse or by typing a number.
Pressing :kbd:`Return` will confirm the transformation. The confirmed transformation can
be further edited by pressing :kbd:`F6` or by going into the Tool Shelf :kbd:`T` and
altering the Distance slider provided that no other actions take place between
the *Push/Pull* transform confirmation and accessing the slider.

Note that the result of the *Push/Pull* transform is also dependent on the number
and type of selected elements (objects, vertices, faces, etc.).
See below for the result of using *Push/Pull* on a number of different elements.

.. figure:: /images/modeling_meshes_editing_transform_push-pull_objects-equidistant.png

   Equidistant Objects being pushed together.

.. figure:: /images/modeling_meshes_editing_transform_push-pull_objects-random.png

   Random Objects being pushed together.

.. figure:: /images/modeling_meshes_editing_transform_push-pull_vertices-push-pull.png

   Push (middle) vertices around the 3D cursor compared to Scale (right).
