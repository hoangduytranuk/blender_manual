
************
Introduction
************

The Graph editor is the main animation editor.
It allows you to modify the animation for any properties using
:doc:`F-Curves </editors/graph_editor/fcurves/introduction>`.

The Graph editor has two modes, *F-Curve* for :doc:`Actions </animation/actions>`,
and *Drivers* for :doc:`Drivers </animation/drivers/index>`. Both are very similar in function.

.. figure:: /images/editors_graph-editor_introduction_example.png

   The Graph Editor.


Curve View
==========

The curve view allows you to view and edit F-Curves.
An F-Curve has several key parts:

Curve
   The curve defines the value (Y axis) of the property over time (X axis).

   See :doc:`F-Curves </editors/graph_editor/fcurves/index>`.
Keyframes
   Keyframes are user-defined values on certain frames and are represented by little black squares.
   These become orange if selected.

   See :doc:`Keyframes </animation/keyframes/index>` for more information.
Handles
   Each keyframe has a handle that helps determine the values of the curve between keyframes.
   These handles are represented by extruding lines with circular ends
   and can be selected and modified to change the shape of the curve.

   See :ref:`editors-graph-fcurves-settings-handles` for more information.

.. figure:: /images/editors_graph-editor_fcurves_introduction.png

   A simple curve.

.. seealso::

   See :doc:`F-Curves </editors/graph_editor/fcurves/introduction>` for more info.


Navigation
----------

As with most editors, you can:

Pan
   Pan the view vertically (values) or horizontally (time) with click and drag (:kbd:`MMB`).
Zoom
   Zoom in and out with the mouse wheel (:kbd:`Wheel`).
Scale View
   Scale the view vertically or horizontally (:kbd:`Ctrl-MMB`).


.. _graph_editor-2d-cursor:
.. _bpy.types.SpaceGraphEditor.cursor:

2D Cursor
---------

.. figure:: /images/editors_graph-editor_introduction_2dcursor.png
   :align: right

   Graph Editor 2D Cursor.

The current frame is represented by a green vertical line called the *Time Cursor*.

As in the :doc:`Timeline </editors/timeline>`,
you can change the current frame by pressing or holding :kbd:`LMB`.

The green horizontal line is called the *Cursor*.
This can be disabled via the *View Menu* or the *View Properties* panel.

The *Time Cursor* and the *Cursor* make the *2D Cursor*.
The *2D Cursor* is mostly used for editing tools.

.. seealso:: See Graph Editor's :ref:`graph_editor-view-properties`.


View Axes
---------

For *Actions* the X axis represents time,
the Y axis represents the value to set the property.

For *Drivers* the X axis represents the *Driver Value*,
the Y axis represents the value to set the property.

Depending on the selected curves, the values have different meaning:
For example rotation properties are shown in degrees,
location properties are shown in Blender Units.
Note that *Drivers* use radians for rotation properties.


Header
======

.. _graph-view-menu:

View Menu
---------

Realtime Updates
   When transforming keyframes, changes to the animation data are propagated to other views.
Show Cursor
   Toggles the visibility of the `2D Cursor`_.
Show Sliders
   A toggle option that shows the value sliders for the channels.
   See the Fig. :ref:`fig-dope-sheet-action`.
Show Group Colors
   Draw groups and channels with colors matching their corresponding groups.
AutoMerge Keyframes
   Automatically merge nearby keyframes.
Use High Quality Drawing
   Draws F-Curves using anti-aliasing and other fancy effects (disable for better performance).
Show Handles :kbd:`Ctrl-H`
   Toggles the display of a curve's handles in the curve view.
Only Selected Curve Keyframes
   Only shows the keyframes markers on the selected curves.
Only Selected Keyframes Handles
   Only shows the handles for the currently selected curves.
View All :kbd:`Home`
   Reset viewable area to show all keyframes.
View Selected :kbd:`NumpadPeriod`
   Reset viewable area to show selected keyframes.
View Frame :kbd:`Numpad0`
   Centers the area to the Time cursor.

.. seealso::

   - See Graph Editor's :ref:`graph_editor-view-properties`.
   - See Timeline's :ref:`timeline-view-menu`.


.. _graph-preview-range:

Preview Range
^^^^^^^^^^^^^

Set Preview Range :kbd:`P`
   Interactively define frame range used for playback.
   Allows you to define a temporary preview range to use for the :kbd:`Alt-A` real-time playback
   (this is the same thing as the *Playback Range* option of
   the :ref:`Timeline editor header <animation-editors-timeline-headercontrols>`).
Clear Preview Range :kbd:`Alt-P`
   Clears the preview range.
Auto-Set Preview Range :kbd:`Ctrl-Alt-P`
   Automatically sets the preview range to playback the whole action or
   the selected NLA strips.


Markers Menu
------------

:doc:`Markers </animation/markers>` are used to denote frames with key points or significant events
within an animation. Like with most animation editors, markers are shown at the bottom of the editor.

.. figure:: /images/editors_graph-editor_introduction_markers.png

   Markers in animation editor.

For descriptions of the different marker tools see :ref:`Editing Markers <animation-markers-editing>`.


Mode
----

F-Curve for :doc:`Actions </animation/actions>`,
and Drivers for :doc:`Drivers </animation/drivers/index>`.

.. figure:: /images/editors_graph-editor_introduction_header-mode.png

   Graph Mode.


View Controls
-------------

.. figure:: /images/editors_graph-editor_introduction_header-view.png

   View controls.

Show Only Selected (mouse cursor icon)
   Only include curves related to the selected objects and data.
Show Hidden (ghost icon)
   Include curves from objects/bones that are not visible.
Show Only Errors (livesaver icon)
   Only include curves and drivers that are disabled or have errors.
   Useful for debugging.
Search Filter (magnifying glass icon) :kbd:`F`
   Only include curves with keywords contained in the search field.

   Multi-Word (az icon)
      Fuzzy/Multi-Word name filtering matches word snippets/partial words,
      instead of having to match everything. It breaks down the search string based on white-space placement.
      e.g. "lo ro" will filter all location and rotation, while "lc rt" will *not* work.
Type Filter
   Filter curves by property type.

   Data-block Sort (az icon)
      Objects data-blocks appear in alphabetical order, so that it is easier to find where they occur
      (as well as helping to keep the animation of related objects together in the NLA for instance).

      If you find that your playback speed suffers from this being enabled
      (it should only really be an issue when working with lots of objects in the scene),
      you can turn this off.

Normalize
   Normalize curves so the maximum or minimum point equals 1.0 or -1.0.

   Auto
      Automatically recalculate curve normalization on every curve edit.
      This is useful to prevent curves from jumping after tweaking it.


Curve Controls
--------------

.. figure:: /images/editors_graph-editor_introduction_header-edit.png

   Curve controls.

Proportional Editing :kbd:`O`
   See :doc:`Proportional editing </editors/3dview/object/editing/transform/control/proportional_edit>`.
Auto Snap
   Auto snap the keyframes for transformations.

   - No Auto-Snap
   - Frame Step
   - Second Step
   - Nearest Frame
   - Nearest Second
   - Nearest Marker

Pivot Point
   Pivot point for rotation.

   Bounding Box Center
      Center of the selected keyframes.
   2D Cursor
      Center of the *2D Cursor*. *Time Cursor* + *Cursor*.
   Individual Centers
      Rotate the selected keyframe *Bézier* handles.

Copy Keyframes :kbd:`Ctrl-C`
   Copy the selected keyframes to memory.
Paste Keyframes :kbd:`Ctrl-V`
   Paste keyframes from memory to the current frame for selected curves.
Create Snapshot (ghost icon)
   Creates a picture with the current shape of the curves.


Properties Region
=================

The panels in the *Properties Region*.


View Tab
--------

.. (Todo) duplicated here: \editors\graph_editor\fcurves\properties.rst

View Properties Panel
---------------------

.. figure:: /images/editors_graph-editor_fcurves_properties_view-panel.png

   View Properties panel.

Show Cursor
   Show the vertical *Cursor*.
Cursor from Selection
   Set the *2D cursor* to the center of the selected keyframes.
Cursor X
   *Time Cursor* X position.

   To Keys
      Snap selected keyframes to the *Time Cursor*.
Cursor Y
   Vertical *Cursor* Y position.

   To Keys
      Snap selected keyframes to the *Cursor*.


Further Tabs
------------

F-Curve Tab
   See :doc:`F-Curve </editors/graph_editor/fcurves/properties>`.
Drivers Tab
   See :doc:`/animation/drivers/drivers_panel`.
Modifiers Tab
   See :doc:`F-Modifiers </editors/graph_editor/fcurves/modifiers>`.
