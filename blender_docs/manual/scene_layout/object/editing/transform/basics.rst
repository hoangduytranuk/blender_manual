
*********************
Basic Transformations
*********************

.. _bpy.ops.transform.translate:

Grab/Move
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode, Edit Mode, and Pose Mode
   :Panel:     :menuselection:`Tool Shelf --> Tools --> Transform --> Translate`
   :Menu:      :menuselection:`Object type --> Transform --> Grab/Move`
   :Hotkey:    :kbd:`G`

In Object Mode, the grab/move option lets you translate (move) objects.
Translation means changing location of objects.
It also lets you translate any elements that make up the object within the 3D space of the active 3D View.

Pressing :kbd:`G` activates "Grab/Move" transformation mode.
The selected object or element then moves freely according to the mouse pointer's location and camera.

You can also move an object by clicking and holding :kbd:`RMB` on the object to move it.
To confirm the action, press :kbd:`LMB`.

While Grab/Move is active, the amount of change in the X, Y,
and Z coordinates is displayed at the bottom left corner of the 3D View editor.

.. figure:: /images/editors_3dview_object_editing_transform_basics_grab-display-values.png

   Translation Display.

.. tip::

   Moving an object in Object Mode changes the object's origin.
   Moving the object's vertices/edges/faces in Edit Mode does not change the object's origin.


.. _bpy.ops.transform.rotate:

Rotate
======

.. admonition:: Reference
   :class: refbox

   :Mode:      Object and Edit Modes
   :Panel:     :menuselection:`Tool Shelf --> Tools --> Transform --> Rotate`
   :Menu:      :menuselection:`Object/Mesh/Curve/Surface --> Transform --> Rotate`
   :Hotkey:    :kbd:`R`

Rotation is also known as a spin, twist, orbit, pivot, revolve,
or roll and involves changing the orientation of elements (vertices, edge, face, object, etc.)
around one or more axes or
the :doc:`Pivot Point </scene_layout/object/editing/transform/control/pivot_point/index>`.

The angle of rotation will be displayed in the footer of the 3D View editor.

.. figure:: /images/editors_3dview_object_editing_transform_basics_rotate-display-values.png

   Rotation values.


.. _view3d-transform-trackball:
.. _bpy.ops.transform.trackball:

Trackball Rotation
------------------

A free rotation mode. Press :kbd:`R R` to enable Trackball rotation.


.. _bpy.ops.transform.resize:

Scale
=====

.. admonition:: Reference
   :class: refbox

   :Mode:      Object and Edit Modes
   :Panel:     :menuselection:`Tool Shelf --> Tools --> Transform --> Scale`
   :Menu:      :menuselection:`Object/Mesh/Curve/Surface --> Transform --> Scale`
   :Hotkey:    :kbd:`S`

Scaling means changing proportions of objects.
Pressing :kbd:`S` will enter the *Scale* transformation mode where
the selected element is scaled inward or outward according to the mouse pointer's location.
The element's scale will increase as the mouse pointer is moved away from the Pivot Point and
decrease as the pointer is moved towards it. If the mouse pointer crosses from the original side of
the :doc:`Pivot Point </scene_layout/object/editing/transform/control/pivot_point/index>` to the opposite side,
the scale will continue in the negative direction and flip the element.

.. figure:: /images/editors_3dview_object_editing_transform_basics_scale-basic-usage.png

   Basic scale usage. From left to right, the panels show: the original Object,
   a scaled down Object, a scaled up Object and a scale-flipped Object.

The amount of scaling will be displayed in the footer of the 3D View editor.

.. figure:: /images/editors_3dview_object_editing_transform_basics_scale-display-values.png

   Scale values.


Common Options
==============

There are multiple ways to transform an element which include:

- The keyboard shortcut.
- The menu in the header or the Transform panel in the Tool Shelf.
- The :doc:`3D Transform Manipulator </scene_layout/object/editing/transform/control/manipulators>`
  widget.
- The :doc:`Transform panel </scene_layout/object/properties/transforms>`
  in the Sidebar region or the Object tab.


Confirm and Cancel
------------------

:kbd:`LMB` click to accept changes.
This behavior can be changed globally by activating *Release Confirms*
in the :doc:`Preferences </editors/preferences/editing>`,
so that a single :kbd:`RMB` drag can be used to move and confirm.

To cancel the transformation press :kbd:`RMB` or :kbd:`Esc` instead.
This will reset the object or element to its original state.

.. seealso::

   Using combination of shortcuts gives you more control over your transformation.
   See :doc:`Transform Control </scene_layout/object/editing/transform/control/index>`.


Operator Panel
--------------

In the case of the 3D View, there is the possibility to tweak the operation once accepted,
using the specific Operator panel corresponding to the tool.

Value
   The amount of the transformation.

   Vector, Angle
Constrain Axis
   Used to constraint the transformation to one or more axes.

   X, Y, Z
Orientation
   Shows the :doc:`Orientations </scene_layout/object/editing/transform/control/orientations>`
   of the constraint axes.
Proportional Editing, Falloff, Size
   Activates/deactivates *Proportional Editing* and configures the type *Falloff* and
   *Size* of the :doc:`/scene_layout/object/editing/transform/control/proportional_edit` tool.
Edit Grease Pencil
   ToDo.

.. _modeling_transform_edit-texture-space:

Edit Texture Space :kbd:`Shift-T`:kbd:`Shift-Alt-T`
   This checkbox lets you apply the transformation on the :ref:`Texture Space <properties-texture-space>`,
   instead of the object or element itself. Only available in translation and scale.
   This option is also available via the shortcuts, :kbd:`Shift-T` (move) and :kbd:`Shift-Alt-T` (scale).
Confirm on Release
   Shows if either the operation was drag-and-release or move-and-confirm.


Workflow
--------

Using Keyboard Shortcuts
^^^^^^^^^^^^^^^^^^^^^^^^

#. Use :kbd:`RMB` to select the elements you want to transform.
#. Tap :kbd:`G`, or :kbd:`R`, or :kbd:`S` once to enter the transformation mode.
#. Transform the elements by moving the mouse.
#. :kbd:`LMB` click to accept changes.
