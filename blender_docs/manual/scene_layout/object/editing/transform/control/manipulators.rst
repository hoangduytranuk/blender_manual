.. |manip-menu| image:: /images/editors_3dview_object_editing_transform_control_manipulators_header.png

***************************
Transformation Manipulators
***************************

.. admonition:: Reference
   :class: refbox

   :Mode:      Object and Edit Modes
   :Menu:      |manip-menu|
   :Hotkey:    :kbd:`Ctrl-Spacebar`

The Transformation manipulator widgets allow mouse controlled translation, rotation and scaling in the 3D View.
There is a separate manipulator for each operation.
Each manipulator can be used separately or in combination with the others.

.. list-table:: The different Manipulators.

   * - .. figure:: /images/editors_3dview_object_editing_transform_control_manipulators_options-translate.png
          :width: 320px

          Translate.

     - .. figure:: /images/editors_3dview_object_editing_transform_control_manipulators_options-rotate.png
          :width: 320px

          Rotate.

     - .. figure:: /images/editors_3dview_object_editing_transform_control_manipulators_options-scale.png
          :width: 320px

          Scale.

     - .. figure:: /images/editors_3dview_object_editing_transform_control_manipulators_options-all.png
          :width: 320px

          Combination.


Header Controls
===============

Manipulators can be accessed through the header of the *3D View*.

Axis
   Enable/disable the manipulators :kbd:`Ctrl-Spacebar`.
Manipulators
   Toggles each of the manipulators. Clicking with :kbd:`Shift-LMB` on multiple manipulator icons
   will combine the manipulators.

   Arrow
      Translation.
   Arc
      Rotation.
   Box
      Scale.
Transform Orientation
   A select menu of
   the :doc:`Transform Orientations </scene_layout/object/editing/transform/control/orientations>`.


Manipulator Controls
====================

Basic
-----

You can use the widget by dragging one of the three colored axes with :kbd:`LMB`.
The transformation will be locked to the clicked axis.

Dragging the small white circle allows free transformation.
In case of the rotation manipulator this starts a :ref:`trackball rotation <view3d-transform-trackball>`.
The rotation manipulator contains another big outer white circle to activate free transformation.

Releasing the mouse confirms the operation (*confirm on release*).


Extended
--------

The operations work in same way as described in
:doc:`precision control </scene_layout/object/editing/transform/control/precision/index>` except:

Holding down :kbd:`Shift` *after* you :kbd:`LMB`
the manipulator handle will constrain the action to smaller increments.
Holding down :kbd:`Shift` *before* you :kbd:`LMB` click on one of the handles will cause the manipulator action
to be performed relative to the other two axes. See :ref:`view3d-transform-plane-lock`.

.. seealso::

   The :ref:`Manipulator Preferences <prefs-interface-manipulator>`.
