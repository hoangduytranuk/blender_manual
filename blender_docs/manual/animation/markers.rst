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
- :doc:`Video Sequence Editor </editors/vse/index>`
- :doc:`Timeline </editors/timeline>`

.. note::

   A marker created in one of these editors will also appear in all others that support them.


Types
=====

Next to the standard markers *pose markers* are another type of markers,
which are specific to armatures and shape keys.
They are used to denote poses in the Action Editor mode and Shape Keys Editor of Dope Sheet.


Visualization
=============

Standard
--------

.. figure:: /images/animation_markers_standard.png
   :align: right

   Markers: small but useful.

Most of the editors visualize markers the same way: as small triangles at their bottom,
white if unselected or yellow if selected.

If they have a name, this is shown to their right, in white when the marker is selected.

.. container:: lead

   .. clear


Sequencer
---------

.. figure:: /images/animation_markers_sequencer.png
   :align: right

   Markers in the Sequencer.

The *Video Sequence Editor* just adds a vertical dashed line to each marker
(gray if the marker is unselected, or white if it is selected).

.. container:: lead

   .. clear


3D View
-------

.. figure:: /images/animation_markers_3d-view.png
   :align: right

   Marker in a 3D View.

The 3D View does not allow you to create, edit, and remove markers,
it just show their name in the Object Info in the bottom left corner,
when on their frame (see Marker in a 3D View).

.. container:: lead

   .. clear


Pose Markers
------------

.. figure:: /images/animation_markers_pose.png
   :align: right

   Pose markers in the Action editor.

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
   :Hotkey:    :kbd:`M` or :kbd:`Ctrl-Alt-M` in the VSE editor

The simplest way to add a marker is to move to the frame where you would like it to appear,
and press :kbd:`M`.

.. hint::

   Markers can also be added while playback.


.. _marker-pose-add:

Pose Markers
------------

If *Show Pose Markers* is checked a pose marker and
a new pose in the :doc:`Pose Library </rigging/armatures/properties/pose_library>` are added.


Selecting
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Hotkey:    :kbd:`RMB`

Click :kbd:`RMB` on the marker's triangle to select it.
Use :kbd:`Shift-RMB` to select multiple markers.

In the Graph Editor, Dope Sheet, NLA Editor, and Video Sequence Editor,
you can also select all markers with :kbd:`Ctrl-A`, and apply selection tools on them like Border Select etc.
(as usual, :kbd:`LMB` to select, :kbd:`RMB` to deselect).
The corresponding options are found in the Select menu of these editors.

In the Timeline, you can select all markers with :kbd:`A`, and border select with :kbd:`B`.


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
the new ones are automatically placed in grab mode, so you can move them to the desired location.

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


Grab/Move Marker
----------------

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :menuselection:`Marker --> Grab/Move Marker`
   :Hotkey:    :kbd:`G`

Once you have one or more markers selected, press :kbd:`G`,
while hovering with the mouse over the marker bar,
to move them, and confirm the move with :kbd:`LMB` or :kbd:`Return`
(as usual, cancel the move with :kbd:`RMB`, or :kbd:`Esc`).
Or drag them with the :kbd:`RMB`.

By default, you grab the markers in one-frame steps, but if you hold :kbd:`Ctrl`,
the markers will move in steps corresponding to one second (according to the scene's *FPS*).


Show Pose Markers
-----------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Action Editor and Shape Keys Editor
   :Menu:      :menuselection:`Marker --> Show Pose Markers`

Only pose markers are shown and editable in Action editor or Shape Keys editor by enabling
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

Moves the time cursor to the next/previous marker relative to the current time cursor position.


.. _marker-bind-camera:

Bind Camera to Marker
=====================

.. admonition:: Reference
   :class: refbox

   :Editor:    Timeline Editor
   :Menu:      :menuselection:`View --> Bind Camera to Marker`
   :Hotkey:    :kbd:`Ctrl-B`

Switching cameras can be done with the *Timeline* operator *Bind Camera to Markers* by
having both the camera and marker selected.

The triangle above the camera will become shaded when active.


Workflow
--------

.. figure:: /images/animation_markers_camera-switch.png

First in the Timeline, add a set of markers used to switch cameras.
Press :kbd:`M` to add marker, then :kbd:`Ctrl-M` to rename,
duplicated markers should retain the same name.

#. In the 3D View, select the Camera the Markers will switch to.
#. In the Timeline, select the Marker(s) to switch to the Camera.
#. In the Timeline, press :kbd:`Ctrl-B` to Bind Cameras to Markers.
