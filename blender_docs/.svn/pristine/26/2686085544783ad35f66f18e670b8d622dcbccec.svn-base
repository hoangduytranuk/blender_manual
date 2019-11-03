.. _bpy.types.TransformOrientation:
.. _bpy.types.SpaceView3D.transform_orientation:
.. TODO/Review: {{review|Need to change and explain the behavior of the transform orientation.
   It is toggled between the chosen orientation and
   the global orientation when transformations are made by shortcuts}}.

**********************
Transform Orientations
**********************

.. admonition:: Reference
   :class: refbox

   :Mode:      Object and Edit Modes
   :Panel:     :menuselection:`Sidebar region --> Transform Orientations`
   :Hotkey:    :kbd:`Alt-Spacebar`

*Transform Orientations* affect the behavior of
:doc:`Transformations </scene_layout/object/editing/transform/basics>`: *Location*, *Rotation*, and *Scale*.
You will see an effect on
the :doc:`Object Gizmo </scene_layout/object/editing/transform/control/gizmos>`
(the widget in the center of the selection), as well as on transformation constraints,
:doc:`Axis Locking </scene_layout/object/editing/transform/control/axis_locking>`.

For example, when you press :kbd:`X`, during the execution of the operation,
it will constrain the transformation to the *Global* X axis.
But if you press :kbd:`X` a second time it will constrain to your *Transform Orientation*\ 's X axis.

.. figure:: /images/scene-layout_object_editing_transform_control_orientations_menu.png

   Transform Orientations selector.

The Orientations options can be set through the *Transform Orientation* selector in a 3D View header.

In addition to the five preset options,
you can define your own custom orientation (see `Custom Orientations`_ below).


Orientations
============

Global
   The gizmo matches the *Global* (or *World*) axis.

   The :doc:`Axis </editors/3dview/startup_scene>` in the top right corner of the viewport,
   and the *Grid Floor*, shows the axes of world coordinate system.

Local
   The gizmo matches the *Object* axis.

   When an object is rotated, the direction of the *Local* gizmo
   matches to the object's rotation relative to the global axes.
   While the *Global* gizmo always correspond to world coordinates.

Normal
   The Z axis of the gizmo will match
   the :doc:`Normal </modeling/meshes/editing/normals>` of the selected element.
   If multiple elements are selected, it will orient towards the average of those normals.

   In *Object Mode*, this is equivalent to *Local* orientation.

Gimbal
   Uses a :term:`Gimbal` behavior that can be changed
   depending on the current :ref:`Rotation Mode <rotation-modes>`.

View
   The gizmo will match the 3D View (viewport):

   - Y: Up/Down
   - X: Left/Right
   - Z: Towards/Away from the screen

.. TODO2.8

   Examples
   --------

   .. list-table:: Cube with the rotation gizmo active in multiple transform orientations.

      * - .. figure:: /images/scene-layout_object_editing_transform_control_orientations_manipulator-global-1.png

            Default cube with Global transform orientation selected.

      - .. figure:: /images/scene-layout_object_editing_transform_control_orientations_manipulator-global-2.png

            Rotated cube with Global orientation, gizmo has not changed.

      - .. figure:: /images/scene-layout_object_editing_transform_control_orientations_manipulator-local.png

            Local orientation, gizmo matches to the object's rotation.

      * - .. figure:: /images/scene-layout_object_editing_transform_control_orientations_manipulator-normal.png

            Normal orientation, in Edit Mode.

      - .. figure:: /images/scene-layout_object_editing_transform_control_orientations_manipulator-gimbal.png

            Gimbal transform orientation.

      - .. figure:: /images/scene-layout_object_editing_transform_control_orientations_manipulator-view.png

            View transform orientation.


Custom Orientations
-------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Object and Edit Modes
   :Panel:     :menuselection:`Sidebar region --> Transform Orientations`
   :Hotkey:    :kbd:`Ctrl-Alt-Spacebar`

You can define custom transform orientations, using object or mesh elements. Custom transform
orientations defined from objects use the *Local* orientation of the object whereas those
defined from selected mesh elements (vertices, edges, faces)
use the *Normal* orientation of the selection.

.. figure:: /images/scene-layout_object_editing_transform_control_orientations_custom.png

   Transform Orientations panel.

The *Transform Orientations* panel, found in the header of the 3D View,
can be used to manage transform orientations: selecting the active orientation,
adding ("+" icon), deleting ("X" icon) and rename custom orientations.

The default name for these orientations comes from whatever you have selected.
If an edge, it will be titled, "Edge", if an object,
it will take that object's name, etc.


Create Orientation
^^^^^^^^^^^^^^^^^^

To create a custom orientation, select the object or mesh element(s) and
click the "+" button on the *Transform Orientations* panel.

.. figure:: /images/scene-layout_object_editing_transform_control_orientations_custom-name.png

   Create Orientation :ref:`ui-undo-redo-adjust-last-operation` panel.

Just after creating the orientation,
the *Create Orientation* :ref:`ui-undo-redo-adjust-last-operation` panel gives a few options:

Name
   Text field for naming the new orientation.
Use View
   The new orientation will be aligned to the view space.
Use after creation
   If checked it leaves the newly created orientation active.
Overwrite previous
   If the new orientation is given an existing name, a suffix will be added to it to avoid overwriting the old one,
   unless *Overwrite previous* is checked, in which case it will be overwritten.


.. _bpy.ops.transform.transform:

Align to Transform Orientation
==============================

.. admonition:: Reference
   :class: refbox

   :Mode:      Object and Edit Modes
   :Menu:      :menuselection:`Object --> Transform --> Align to Transform Orientation`

Aligns (rotates) the selected objects so that their local orientation matches the active transform orientation
in the Transform orientation panel or the *Orientation* selection
in the Transform :ref:`ui-undo-redo-adjust-last-operation` panels.
