
******************
Grease Pencil Menu
******************

Transform
=========

Strokes can be edited by transforming the locations of points.


Translation, Rotation, Scale
----------------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Toolbar --> Tools --> Transform`
   :Menu:      :menuselection:`Stroke --> Transform --> Move, Rotate, Scale, ...`
   :Hotkey:    :kbd:`G`, :kbd:`R`, :kbd:`S`

Like other elements in Blender, points and strokes can be
moved :kbd:`G`, rotated :kbd:`R` or scaled :kbd:`S` as described in
the :doc:`Basic Transformations </scene_layout/object/editing/transform/introduction>` section.
When in *Edit Mode*,
:doc:`Proportional Editing </scene_layout/object/editing/transform/control/proportional_edit>`
is also available for the transformation actions.


Transform Snapping
------------------

Basic move, rotate and scale transformations for selected points/strokes.
See :doc:`Move, Rotate, Scale Basics </modeling/meshes/editing/basics/move_rotate_scale>` for more information.


Tools
-----

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Strokes --> Transform`
   :Panel:     :menuselection:`Toolbar --> Tools --> Stroke Tools`

The *Bend*, *Shear*, *To Sphere*, *Extrude* and *Shrink fatten* transform tools are described
in the :doc:`Editing tool </grease_pencil/modes/edit/tools>` section.


Mirror
======

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Hotkey:    :kbd:`Ctrl-M`

The *Mirror* tool is also available, behaving exactly the same as with
:doc:`mesh vertices </modeling/meshes/editing/transform/mirror>`.


Snap
====

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Strokes --> Snap`
   :Hotkey:    :kbd:`Shift-S`

:doc:`Mesh snapping </scene_layout/object/editing/transform/control/snap>`
also works with *Grease Pencil* components.


Animation
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode, Draw Mode
   :Menu:      :menuselection:`Strokes --> Animation`

The stroke animation tools are described
in the :doc:`Animation </grease_pencil/animation/tools>` section.


Interpolation
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode, Draw Mode
   :Menu:      :menuselection:`Strokes --> Interpolation`

The stroke animation tools are described
in the :ref:`Animation <grease-pencil-animation-tools-interpolation>` section.


Duplicate
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Duplicate`
   :Hotkey:    :kbd:`Shift-D`

Duplicates the selected elements, without creating any connections
with the rest of the strokes (unlike *Extrude*, for example),
and places the duplicate at the location of the original elements.


Split
=====

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Split`
   :Hotkey:    :kbd:`V`

Splits (disconnects) the selected points from the rest of the stroke.
The separated points are left exactly at the same position as the original points but they belong to a new stroke.


Copy
====

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Copy`
   :Hotkey:    :kbd:`Ctrl-C`

Copy the selected points/strokes to the clipboard.


Paste / Paste & Merge
=====================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Paste`, :menuselection:`Stroke --> Paste & Merge`
   :Hotkey:    :kbd:`Ctrl-V`

Type
   Copy
      Paste the points/strokes copied from the clipboard.

   Merge
      Paste the points/strokes copied from the clipboard into the active layer.


Separate Strokes
================

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Separate`
   :Hotkey:    :kbd:`P`

Separate the selected elements into a new *Grease Pencil* object.

Selected Points
   Separate the selected points into a new *Grease Pencil* object.

Selected Strokes
   Separate the selected strokes into a new *Grease Pencil* object.
   If one point of a stroke is selected, the entire stroke will be separated.

Active Layer
   Separate all the strokes in the active layer into a new *Grease Pencil* object.
   See :doc:`2D Layers </grease_pencil/properties/layers>` for more information.


Clean Up
========

These tools help to cleanup degenerate geometry on the strokes.


Delete Loose Points
-------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Clean Up --> Delete Loose Points`

Removes unconnected points.


.. _bpy.ops.gpencil.stroke_merge_by_distance:

Merge by Distance
-----------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Clean Up --> Merge by Distance`

*Merge by Distance* is a useful tool to simplify a stroke by merging
the selected points that are closer than a specified distance to each other.

Merge Distance
   Sets the distance threshold for merging points.
Unselected
   Allows points in selection to be merged with unselected points.
   When disabled, selected points will only be merged with other selected ones.


Boundary Strokes
----------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Clean Up --> Boundary Strokes, Boundary Strokes All Frames`

Removes boundary strokes used by the *Fill* tool.
See :doc:`Fill tool </grease_pencil/modes/draw/tool_settings/fill>` for more information.

Mode
   Active Frame Only
      Removes boundary strokes from the current frame.
   All frames
      Removes boundary strokes from all frames.


Reproject Strokes
-----------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Clean Up --> Reproject Strokes`

Sometimes you may have drawn strokes unintentionally in different locations in the 3D space
but they look right from a certain plane or from the camera view.
You can use Reproject Strokes to flatten all the selected strokes from a certain viewpoint.

Front
   Reproject selected strokes onto the front plane (XZ).
Side
   Reproject selected strokes onto the side plane (YZ).
Top
   Reproject selected strokes onto the top plane (XY).
View
   Reproject selected strokes onto the current view.
Surface
   Reproject selected strokes onto the mesh surfaces.
Cursor
   Reproject selected strokes onto 3D cursor rotation.

.. list-table::

   * - .. figure:: /images/grease-pencil_modes_edit_stroke_menu_reproject-strokes-1.png
          :width: 200px

          Original drawing from the front view.

     - .. figure:: /images/grease-pencil_modes_edit_stroke_menu_reproject-strokes-2.png
          :width: 200px

          Original drawing in the 3D view.

     - .. figure:: /images/grease-pencil_modes_edit_stroke_menu_reproject-strokes-3.png
          :width: 200px

          Strokes reprojected onto the front plane to fix strokes misalignment.

     - .. figure:: /images/grease-pencil_modes_edit_stroke_menu_reproject-strokes-1.png
          :width: 200px

          Drawing after reprojection operation from the front view.


Delete
======

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Delete`
   :Hotkey:    :kbd:`X`, :kbd:`Delete`, :kbd:`Ctrl-X`

Options for the Erase pop-up menu:

Points
   Deletes the selected points.
   When only one point remains, there is no more visible stroke,
   and when all points are deleted, the stroke itself is deleted.

Strokes
   Deletes all the strokes that selected points belongs to.

Frames
   Deletes all the strokes at the current frame and in the current layer/channel.

Dissolve :kbd:`Ctrl-X`
   Deletes the selected points without splitting the stroke.
   The remaining points in the strokes stay connected.

Dissolve between :kbd:`Ctrl-X`
   Deletes all the points between the selected points without splitting the stroke.
   The remaining points in the strokes stay connected.

Dissolve Unselect :kbd:`Ctrl-X`
   Deletes all the points that are not selected in the stroke without splitting the stroke.
   The remaining points in the strokes stay connected.

Delete All Active Frames
   Deletes all the strokes at the current frame in all layers/channels.
