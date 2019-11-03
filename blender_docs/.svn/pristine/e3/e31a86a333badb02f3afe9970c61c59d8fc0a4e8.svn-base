
**********
Properties
**********

Active F-Curve Panel
====================

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Sidebar region --> F-Curve --> Active F-Curve`

.. figure:: /images/editors_graph-editor_fcurves_properties_active-fcurve-panel.png

   Active F-Curve panel.

This panel displays properties for the active F-curve.

Channel Name
   ID Type + Channel name (X Location).
RNA Path
   RNA Path to property + Array index.
Color Mode
   Color Mode for the active F-curve.

   Auto Rainbow
      Increment the hue of the F-curve color based on the channel index.
   Auto XYZ to RGB
      For property sets like location XYZ, automatically set the set of colors to red, green, blue.
   User Defined
      Define a custom color for the active F-curve.
Auto Handle Smoothing
   Selects the method used to compute automatic Bézier handles (*Automatic*, *Auto Clamped*, *Vector*).

   None
      Only directly adjacent key values are considered when computing the handles.

      This legacy method is very simple and predictable, but it can only produce
      good smooth curves in the most trivial cases.

   Continuous Acceleration
      A system of equations is solved for each continuous stretch of curve without manual handles in order to
      avoid or minimize jumps in acceleration at every keyframe.


Active Keyframe Panel
=====================

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Sidebar region --> F-Curve --> Active Keyframe`

.. figure:: /images/editors_graph-editor_fcurves_properties_active-keyframe-panel.png

   Active Keyframe panel.

Interpolation
   Set the forward :ref:`editors-graph-fcurves-settings-interpolation` for the active keyframe.
Easing
   See :ref:`editors-graph-fcurves-settings-easing`.
Key
   Frame
      Set the frame for the active keyframe.
   Value
      Set the value for the active keyframe.
Left/Right Handle
   Set the position of the left/right interpolation handle for the active keyframe.

   Handle Type
      See :ref:`editors-graph-fcurves-settings-handles`.


.. _bpy.types.SpaceGraphEditor.show_cursor:
.. _bpy.ops.graph.frame_jump:
.. _graph_editor-view-properties:

View Properties
===============

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Sidebar region --> View --> View Properties`

.. figure:: /images/editors_graph-editor_fcurves_properties_view-panel.png
   :align: right

   View Properties.

Show Cursor
   Toggles the visibility of the :ref:`2D Cursor <graph_editor-2d-cursor>`.
Cursor from Selection
   Places the 2D Cursor at the midpoint of the selected keyframes.
Cursor Location
   Moves the cursor to the specified frame (X value) and value (Y value).
To Keys
   Applies the current location of the 2D cursor to the selected keyframes.

.. seealso:: Graph Editor's :ref:`graph-view-menu`.
