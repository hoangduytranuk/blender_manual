.. _bpy.types.UserPreferencesEdit:

*******
Editing
*******

These preferences control how several tools will interact with your input.

.. figure:: /images/preferences_editing_tab.png


Link Materials To
=================

.. figure:: /images/preferences_editing_data-blocks-hierarchy.png

   Example for a mesh.

To understand this option properly, you need to understand how Blender works with Objects.
Almost everything in Blender is organized in a hierarchy of data-blocks.
A data-block can be thought of as containers for certain pieces of information. For example,
the Object data-block contains information about the Object's location while the Object Data
"ObData" data-block contains information about the mesh.

A material may be linked in two different ways:

.. figure:: /images/preferences_editing_data-blocks-link.png

   A material linked to Object Data (left) and Object (right).

Object Data
   Any created material will be created as part of the Object Data data-block.
Object
   Any created material will be created as part of the Object data-block.

:doc:`Read more about Blender's Data System </data_system/index>`.


New Objects
===========

Enter Edit Mode
   If selected, Edit Mode is automatically activated when you create a new object.
Align To
   World
      New objects align with world coordinates.
   View
      New object align with view coordinates.


Undo
====

Global Undo
   This enables Blender to save actions done when you are **not** in *Edit Mode*.
   For example, duplicating Objects, changing panel settings or switching between modes.

   .. warning::

      While disabling this option does save memory, it stops the :ref:`Redo Panel <ui-redo-last>`
      from functioning, also preventing tool options from being changed in some cases.

      For typical usage, its best to keep this enabled.
Steps
   Number of Undo steps available.
Memory Limit
   Maximum memory usage in Mb (0 is unlimited).

:doc:`Read more about Undo and Redo options </interface/undo_redo>`.


Grease Pencil
=============

Eraser Radius
   The size of the eraser used with the Grease pencil.

Manhattan Distance
   The minimum number of pixels the mouse should have moved either
   horizontally or vertically before the movement is recorded.
   Decreasing this should work better for curvy lines.
Euclidean Distance
   The minimum distance that mouse has to travel before movement is recorded.

Simplify Stroke
   This turns on the post-processing step of simplifying the stroke to remove about half of current points in it.
   It is only relevant when not drawing straight lines.

Default Color
   The default color for new Grease Pencil layers.

:doc:`Read more about Grease Pencil </editors/3dview/grease_pencil/index>`.


Playback
========

Allow Negative Frame
   Time Cursor can be set to negative frames with mouse or keyboard.
   When using *Use Preview Range*, this also allows playback.


Node Editor
===========

Auto-offset Margin
   Margin to use for :ref:`offsetting nodes <editors-nodes-usage-auto-offset>`.


Animation Editors
=================

F-Curve Visibility
   Opacity that unselected :doc:`F-Curves </editors/graph_editor/fcurves/index>`
   stand out from the *Graph Editor*.


Keyframing
==========

In many situations, animation is controlled by keyframes. The state of a value (e.g. location)
is recorded in a keyframe and the animation between two keyframes is interpolated by Blender.

Visual Keying
   When an object is using constraints, the object property value does not actually change.
   *Visual Keying* will add keyframes to the object property,
   with a value based on the visual transformation from the constraint.
Only Insert Needed
   This will only insert keyframes if the value of the property is different.
Auto Keyframing
   Enables *Auto Keyframe* by default for new scenes.
Show Auto Keying Warning
   Displays a warning at the top right of the *3D View*, when moving objects, if *Auto Keyframe* is on.
Only Insert Available
   This will only add keyframes to channel F-Curves that already exist.


New F-Curve Defaults
====================

Interpolation
   Controls the default :ref:`Interpolation <editors-graph-fcurves-settings-interpolation>`
   for newly created keyframes.
Handles
   Controls the default :ref:`Handle <editors-graph-fcurves-settings-handles>` for newly created F-Curves.
XYZ to RGB
   Color for X, Y or Z animation curves (location, scale or rotation)
   is the same as the color for the X, Y and Z axis.


Transform
=========

Release confirms
   Dragging :kbd:`LMB` on an object will move it.
   To confirm this (and other) transform, an :kbd:`LMB` is necessary by default.
   When this option is activated, the release of :kbd:`LMB` acts as confirmation of the transform.


Sculpt Overlay Color
====================

This color button allows the user to define a color to be used in the inner part of
the brushes circle when in sculpt mode, and it is placed as an overlay to the brush,
representing the focal point of the brush influence.
The overlay color is visible only when the overlay visibility is selected
(clicking at the *eye* to set its visibility), and the transparency of the overlay is
controlled by the alpha slider located at the :menuselection:`Option tab --> Overlay panel`
in the Tool Shelf.


.. _prefs-editing-duplicate-data:

Duplicate Data
==============

The *Duplicate Data* checkboxes define what data is copied with a duplicated Object and
what data remains linked. Any boxes that are checked will have their data copied along with
the duplication of the Object. Any boxes that are not checked will instead have their data linked
from the source Object that was duplicated.

For example, if you have Mesh checked,
then a full copy of the mesh data is created with the new Object,
and each mesh will behave independently of the duplicate.
If you leave the mesh box unchecked then when you change the mesh of one object,
the change will be mirrored in the duplicate Object.

The same rules apply to each of the checkboxes in the 'Duplicate Data' list.
