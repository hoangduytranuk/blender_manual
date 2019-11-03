.. _bpy.types.TimelineMarker:
.. _bpy.ops.marker:

*******
Markers
*******

Markers are used to denote frames with key points or significant events within an animation.
E.g. it could be that a character's animation starts, the camera changes position, or a door opens.
Markers can be given names to make them more meaningful at a quick glance.
They are available in many of Blender's editors.

.. note::

   Unlike keyframes, markers are always placed at a whole frame number, you cannot set a marker at frame 2.5.

Markers can be created and edited in the following editors:

- :doc:`Graph Editor </editors/graph_editor/introduction>`
- :doc:`Dope Sheet </editors/dope_sheet/introduction>`
- :doc:`NLA Editor </editors/nla/index>`
- :doc:`Video Sequence Editor </video_editing/index>`
- :doc:`Timeline </editors/timeline>`

.. note::

   A marker created in one of these editors will also appear in all others that support them.


Types
=====

Besides standard markers, *pose markers* are another type of markers,
which are specific to armatures and shape keys.
They are used to denote poses in the Action Editor mode and Shape Keys Editor of Dope Sheet.


Visualization
=============

Standard
--------

.. figure:: /images/animation_markers_standard.png
   :align: right

Most of the editors visualize markers as small white triangles in a separate
row at their bottom, empty if unselected or filled if selected.

If they have a name, this is shown to their right in white.

Vertical dashed lines can be enabled via the :menuselection:`View --> Show Marker Lines` menu option.


3D Viewport
-----------

.. figure:: /images/animation_markers_3d-view.png
   :align: right

The 3D Viewport does not allow you to create, edit or remove markers,
but it shows their name in the Object Info in the upper left corner,
when on their frame.


Pose Markers
------------

.. figure:: /images/animation_markers_pose.png
   :align: right

Pose markers show a diamond-shaped icon in the Dope Sheet.
In the NLA editor the pose markers are shown as a red dashed line.

.. container:: lead

   .. clear


Add Marker
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`Marker --> Add Marker`
   :Hotkey:    :kbd:`M`

The simplest way to add a marker is to move to the frame where you would like it to appear,
and press :kbd:`M`.

.. hint::

   Markers can also be added during playback.


.. _marker-pose-add:

Pose Markers
------------

If *Show Pose Markers* is checked, a pose marker and
a new pose in the :doc:`Pose Library </animation/armatures/properties/pose_library>` are added.


Selecting
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Hotkey:    :kbd:`LMB`

Click :kbd:`LMB` on the marker's triangle to select it.
Use :kbd:`Shift-LMB` to select multiple markers.

In the Graph Editor, Dope Sheet, NLA Editor, Timeline, and Video Sequence Editor,
you can also select all markers with :kbd:`A` while hovering the mouse over the marker row,
and apply selection tools on them like Box Select, etc.
(as usual, :kbd:`LMB` to select, :kbd:`RMB` to deselect).
The corresponding options are found in the Select menu of these editors.


.. _animation-markers-editing:

Editing
=======

Duplicate Marker
----------------

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`Marker --> Duplicate Marker`
   :Hotkey:    :kbd:`Shift-D`

You can duplicate the selected markers by pressing :kbd:`Shift-D`. Once duplicated,
the new ones are automatically placed in select mode, so you can move them to the desired location.

.. note::

   Note that unlike most other duplications in Blender,
   the names of the duplicated markers are not altered at all
   (no ``.001`` numeric counter append).


Duplicate Marker to Scene
-------------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`Marker --> Duplicate Marker to Scene...`

Duplicates the selected markers into another scene.


Deleting Markers
----------------

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`Marker --> Delete Marker`
   :Hotkey:    :kbd:`X`

To delete the selected markers simply press :kbd:`X`,
and confirm the pop-up message with :kbd:`LMB`.


Rename Marker
-------------

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`Marker --> Rename Marker`
   :Hotkey:    :kbd:`Ctrl-M`

Having dozens of markers scattered throughout your scene's time will not help you much unless you
know what they stand for. You can name a marker by selecting it, pressing :kbd:`Ctrl-M`,
typing the name, and pressing the OK button.


Move Marker
-----------

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`Marker --> Move Marker`
   :Hotkey:    :kbd:`G`

Once you have one or more markers selected, press :kbd:`G`,
while hovering with the mouse over the marker bar,
to move them, and confirm the move with :kbd:`LMB` or :kbd:`Return`
(as usual, cancel the move with :kbd:`RMB`, or :kbd:`Esc`).
Or drag them with the :kbd:`LMB`.

By default, you move the markers in one-frame steps, but if you hold :kbd:`Ctrl`,
the markers will move in steps corresponding to one second (according to the scene's *FPS*).


Show Pose Markers
-----------------

.. admonition:: Reference
   :class: refbox

   :Mode:      todo <2.8
   :Editor:    Action Editor and Shape Keys Editor
   :Menu:      :menuselection:`Marker --> Show Pose Markers`

Pose markers are only shown and editable in Action editor or Shape Keys editor by enabling
the :menuselection:`Marker --> Show Pose Markers` checkbox.


Make Markers Local
------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`Marker --> Make Markers Local`

It is possible to convert standard markers into pose markers with :menuselection:`Marker --> Make Markers Local`.
Note that the original marker will be gone. If you want to keep it, make a duplicate before you convert.


Jump to Next/Previous Marker
----------------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`Marker --> Jump to Next/Previous Marker`

Moves the playhead to the next/previous marker relative to the current playhead position.


.. _marker-bind-camera:

Bind Camera to Marker
=====================

.. admonition:: Reference
   :class: refbox

   :Editor:    Timeline
   :Menu:      :menuselection:`Marker --> Bind Camera to Markers`
   :Hotkey:    :kbd:`Ctrl-B`

*Bind Camera to Markers* is a special operator only available in the *Timeline*.
The operator allows markers to be used to set the active object as the active camera.

To use this operator, select the object to become the active camera
and select a marker to bind the active camera to.
If no marker is selected when the operator is preformed, a marker will be added.
When an object is bound to a marker, the marker will be renamed to the name of the active object.
These markers also have a camera icon next to the left of the name
to easily distinguish them from other informative markers

These markers can be moved to change the frame at which
the active camera is changed to the object the marker is bound to.
