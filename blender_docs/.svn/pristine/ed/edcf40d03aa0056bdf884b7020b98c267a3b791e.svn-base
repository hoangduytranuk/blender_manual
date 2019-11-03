
***********
Stroke Menu
***********

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Strokes`

This page covers many of the tools in the *Strokes* menu.
These are tools that work primarily on strokes, however,
some also work with point selections.


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
   :Menu:      :menuselection:`Strokes --> Animation`, :menuselection:`Strokes --> Interpolation`

The animations and stroke interpolation tools are described
in the :doc:`Animation </grease_pencil/animation/introduction>` section.


Extrude Points
==============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Toolbar --> Tools --> Stroke Tools --> Extrude`
   :Hotkey:    :kbd:`E`

Extrudes points by duplicating the selected points, which then can be moved.
The new points stay connected with the original points of the edit line.

.. note::

   Since *Grease Pencil* strokes can only have one start an end point,
   a new stroke will be created when extrude intermediate points in the strokes.


Duplicating
===========

Duplicate
---------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Duplicate`
   :Hotkey:    :kbd:`Shift-D`

Duplicates the selected elements, without creating any connections
with the rest of the strokes (unlike *Extrude*, for example),
and places the duplicate at the location of the original elements.


Copy
----

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Copy`
   :Hotkey:    :kbd:`Ctrl-C`

Copy the selected points/strokes to the clipboard.


Paste
-----

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


Subdividing and Smoothing
=========================

Smooth
------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Smooth`

Softens strokes by reducing the differences in the locations of the points along the line,
while trying to maintain similar values that make the line fluid and smoother.

Repeat
   The number of times to repeat the procedure.

Factor
   The amount of the smoothness to apply.

Selected points
   When enabled, limits the effect to only the selected points within the stroke.

Position
   When enabled, the operator affect the points location.

Thickness
   When enabled, the operator affect the points thickness.

Strength
   When enabled, the operator affect the points strength (alpha).

UVs
   When enabled, the operator affect the UV rotation on the points.


Subdivide
---------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Subdivide`

Subdivides the strokes by inserting points between the selected points.

Number of Cuts
   The number of subdivisions to perform.

Smooth
   The amount of the smoothness on subdivided points.

Repeat
   Number of times to repeat the procedure.

Selected points
   When enabled, limits the effect to only the selected points within the stroke.

Position
   When enabled, the operator affect the points location.

Thickness
   When enabled, the operator affect the points thickness.

Strength
   When enabled, the operator affect the points strength (alpha).

UVs
   When enabled, the operator affect the UV rotation on the points.


Simplify
--------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Simplify`

Reduce the amount of points in the strokes.

Fixed
   Deletes alternated points in the strokes, except the start and end points.

   Steps
      The number of times to repeat the procedure.

Adaptive
   Uses the RDP algorithm (Ramer-Douglas-Peucker algorithm) for points deletion.
   The algorithm tries to obtain a similar line shape with fewer points.

   Factor
      Controls the amount of recursively simplifications applied by the algorithm.


Separating
==========

Trim
----

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Trim`

Trims selected stroke to first loop or intersection.

.. list-table::

   * - .. figure:: /images/grease-pencil_modes_edit_stroke_menu_trim-1.png
          :width: 320px

          Original stroke.

     - .. figure:: /images/grease-pencil_modes_edit_stroke_menu_trim-2.png
          :width: 320px

          Result of trim operation.


Separate
--------

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


Split
-----

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Split`
   :Hotkey:    :kbd:`V`

Splits (disconnects) the selected points from the rest of the stroke.
The separated points are left exactly at the same position as the original points but they belong to a new stroke.


Merging
=======

Merge
-----

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Merge`

Combine all selected points into a unique stroke.
All the selected points will be connected by new edit lines when needed to create the new stroke.


Join
----

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Join --> Join, Join and copy`
   :Hotkey:    :kbd:`Ctrl-J`, :kbd:`Shift-Ctrl-J`

Join two or more strokes into a single one.

Type
   Join :kbd:`Ctrl-J`
      Join selected strokes by connecting points.

   Join and copy :kbd:`Shift-Ctrl-J`
      Join selected strokes by connecting points in a new stroke.

Leave Gaps
   When enabled, do not use geometry to connect the strokes.


Close
-----

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Close`
   :Hotkey:    :kbd:`F`

Close or open strokes by connecting the last and first point.

Type
   Close all
      Close all open selected strokes.

   Open all
      Open all closed selected strokes.

   Toggle
      Close or Open selected strokes as required.

Create geometry
   When enabled, points are added for closing the strokes.
   If disabled,  the operator act the same as *Toggle Cyclic*.


Flip Direction
==============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Flip Direction`

Reverse the direction of the points in the selected strokes
(i.e. the start point will become the end one, and vice versa).


Layer and Materials
===================

Move to Layer
-------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Move to Layer`
   :Hotkey:    :kbd:`M`


A pop-up menu to move the stroke to a different layer.
You can choose the layer to move the selected strokes to
from a list of layers of the current *Grease Pencil* Object.
You can also add a new layer to move the selected stroke to.


Assign Material
---------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Assign Material`

Changes the material linked to the selected stroke.
You can choose the name of the material to be used by the selected stroke
from a list of material of the current *Grease Pencil* Object.


Arrange Strokes
===============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Arrange Strokes`

Change the drawing order of the strokes in the 2D layer.

Bring Forward
   Moves the selected points/strokes upper the next one in the drawing order.

Send Backward
   Moves the selected points/strokes below the previous one in the drawing order.

Bring to Front
   Moves to the top the selected points/strokes.

Send to Back
   Moves to the bottom the selected points/strokes.


Toggle Cyclic
=============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Toggle Cyclic`

Toggles between an open stroke and closed stroke (cyclic).

Type
   Close all
      Close all open selected strokes.

   Open all
      Open all closed selected strokes.

   Toggle
      Close or Open selected strokes as required.

   Create geometry
      When enabled, points are added for closing the strokes like when using the *Close* tool.
      If disabled, the stroke is close without any actual geometry.


Toggle Caps
===========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Toggle Caps`

Toggle ending cap styles of the stroke.

Default
   Sets stroke start and end points to rounded (default).

Both
   Toggle stroke start and end points caps to flat or rounded.

Start
   Toggle stroke start point cap to flat or rounded.

End
   Toggle stroke end point cap to flat or rounded.

.. list-table::

   * - .. figure:: /images/grease-pencil_modes_edit_stroke_menu_cap-1.png
          :width: 200px

          Stroke ending with rounded caps.

     - .. figure:: /images/grease-pencil_modes_edit_stroke_menu_cap-2.png
          :width: 200px

          Stroke ending with flat caps.

     - .. figure:: /images/grease-pencil_modes_edit_stroke_menu_cap-3.png
          :width: 200px

          Stroke ending with combined caps.


Cleaning Up
===========

These tools help to cleanup degenerate geometry on the strokes.


Loose Points
------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Stroke --> Clean Up --> Loose Points`

Removes disconnected points.


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


Deleting
========

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
