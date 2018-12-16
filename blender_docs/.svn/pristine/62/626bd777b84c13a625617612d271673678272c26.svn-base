.. _bpy.ops.transform.shear:

*****
Shear
*****

.. admonition:: Reference
   :class: refbox

   :Mode:      Object and Edit Modes
   :Menu:      :menuselection:`Object/Mesh/Curve/Surface --> Transform --> Shear`
   :Hotkey:    :kbd:`Shift-Ctrl-Alt-S`

Shearing is a form of movement where parallel surfaces move past one another. During this transform,
movement of the selected elements will occur along the horizontal axis of the current view.
The axis location will be defined by
the :doc:`Pivot Point </editors/3dview/object/editing/transform/control/pivot_point/index>`.
Everything that is "above" this axis will move (Shear)
in the same direction as your mouse pointer (but always parallel to the horizontal axis).
Everything that is "below" the horizontal axis will move in the opposite direction.

.. figure:: /images/modeling_meshes_editing_transform_shear_operator-panel.png

   Shear Offset Factor.


Usage
=====

Select the elements you want to operate on and activate the *Shear* transform tool.
The *Shear* tool can be invoked from
the :menuselection:`Object/Mesh/Curve/Surface --> Transform --> Shear` menu or by pressing
:kbd:`Shift-Ctrl-Alt-S`. The amount of movement given to the selection can be determined
interactively by moving the mouse or by typing a number.
Pressing :kbd:`Return` will confirm the transformation. The confirmed transformation can
be further edited by pressing :kbd:`F6` or by going into the Tool Shelf and
altering the Offset slider provided that no other actions take place between
the *Shear* transform confirmation and accessing the slider.

Note that the result of the *Shear* transform is also dependent on the number and
type of selected elements (objects, vertices, faces, etc.).
See below for the result of using *Shear* on a number of different elements.

.. figure:: /images/modeling_meshes_editing_transform_shear_mesh.png

   The effects of a Shear transform with different Pivot Points.

The three frames of the image above show the effects of shearing
on the selected vertices when the pivot point is altered.
In middle frame, the :doc:`Pivot Point </editors/3dview/object/editing/transform/control/pivot_point/index>`
is set to *Median Point*
and the mouse was moved to the left during the transform.
In right frame, the *Pivot Point* is set to the 3D cursor
which is located above the mesh.
When the mouse is moved to the left during a *Shear* transform,
the selected vertices are moved to the right as they are below the horizontal axis.

.. tip:: Shear Transform Magnitude

   The magnitude of the *Shear* transform applied to the selected elements is
   directly proportional to the distance from the horizontal axis.
   i.e. the further from the axis, the greater the movement.

.. figure:: /images/modeling_meshes_editing_transform_shear_objects.png

   The effects of a Shear transform on objects with different Pivot Points.

The three frames of the image above show the effects of shearing
on the selected Objects when the *Pivot Point* is altered.
In middle frame, the *Pivot Point* is set to *Median Point*
and the mouse was moved to the left during the transform.
In right frame, the *Pivot Point* is set to the 3D cursor
which is located above the Objects.
When the mouse is moved to the left during a *Shear* transform,
all of the selected Objects are moved to the right as they are below the horizontal axis.
Again, note that, the magnitude of the transform is proportional to the distance from the horizontal axis.
In this case, the lower Objects move further than the upper ones.
