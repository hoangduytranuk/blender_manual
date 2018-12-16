
****************
Stroke Edit Mode
****************

Enter Stroke Edit Mode with the *Mode* select menu in the 3D Views header or
toggle the *Enable Editing* in the Grease Pencil panel
*(only available in 2D editors such as UV/Image editor, Node editor, etc.)*, or use :kbd:`D-Tab`.
In this mode, many common editing tools will operate on Grease Pencil stroke points instead.

These tools let you move and reshape Grease pencil strokes after they have been drawn.

Open the Grease Pencil tab on the Tool Shelf.
Look for the tools in the Edit Strokes panel shown here:

.. figure:: /images/interface_grease-pencil_stroke-edit_panel.png

   Edit panel with Grease pencil strokes.


Selecting
=========

Grease pencil strokes are formed from a series of connected vertex points.
To make changes, first select points on the strokes that you want to edit.
You can only select points on the active layer.
The selected points are highlighted as in the image above.

.. hint::

   Set the layer's *Stroke Thickness* to 1 to make the points more visible.

Use the mouse to select the points, or one of the selection buttons in the panel as detailed in
:doc:`Basic Selection </modeling/meshes/selecting/introduction>`.

Various selection functions similar to those available when editing meshes can be used:

.. list-table::
   :stub-columns: 1

   * - Select All
     - :kbd:`A`
   * - Border Select
     - :kbd:`B`
   * - Circle Select
     - :kbd:`C`
   * - Lasso Select
     - :kbd:`Ctrl-LMB`
   * - Select Linked
     - :kbd:`L`, :kbd:`Ctrl-L`
   * - Select More
     - :kbd:`Ctrl-NumpadPlus`
   * - Select Less
     - :kbd:`Ctrl-NumpadMinus`
   * - Select Stroke
     - :kbd:`Alt-LMB`


Editing
=======

Header
------

Some tools can be accessed through the 3D View header. e.g. Copy/Paste.

Onion Skinning
   Toggles :ref:`grease-pencil-onion`.
Selection Mask, Alpha
   See `Further Options`_.


.. (todo <2.8 move) to a better place

Menu
----

Shrink/Flatten :kbd:`Alt-S`
   Adjust the pressure values of selected stroke points.
   This provides a way to modify the thickness of strokes by moving the mouse or the :kbd:`Wheel`.
Delete All Active Frame :kbd:`D-X`
   Deletes all strokes in the active frame. It can be accessed using :kbd:`D-X` (anywhere),
   as well as :kbd:`Shift-X` (Edit Strokes Mode only) or the :menuselection:`GPencil --> Delete` menu.
   This makes it easier to quickly get rid of throwaway scribbles.
Move to Layer :kbd:`M`
   Can be used to move strokes between layers (including to a new layer).


Edit Strokes Panel
------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Stroke Mode
   :Panel:     :menuselection:`Tool Shelf --> Grease Pencil --> Edit Strokes`
   :Menu:      :menuselection:`GPencil`

Copy :kbd:`Ctrl-C`
   Copies the selected Grease Pencil strokes (or actually, points and segments).
Paste :kbd:`Ctrl-V`
   Pastes the previously copied strokes.
Paste & Merge
   Pastes the previously copied strokes and merge in active layer.

Delete :kbd:`X`
   Points
      Delete the selected points, leaving a gap in the stroke.
   Dissolve
      Reconnect the ends so there is no gap in the stroke.
   Strokes
      Delete the entire stroke containing any selected points.
   Frame
      Delete a frame when doing :doc:`Animating Sketches </editors/3dview/grease_pencil/drawing/layers>`.
Duplicate :kbd:`Shift-D`
   Make a copy of the selected points at the same location. Use the mouse to *Translate* them into position.
   :kbd:`LMB` places them at their new position. :kbd:`RMB` cancels and removes the duplicates.
Toggle Cyclic
   Close or open the selected stroke by adding an edge from the last to first point.

Bend :kbd:`Shift-W`
   Bends selected item between the 3D cursor and the mouse.
Mirror :kbd:`Ctrl-M`
   Mirrors selected strokes along one or more axes.
Shear :kbd:`Shift-Ctrl-Alt-S`
   Shears selected items along the horizontal screen axis.
To Sphere :kbd:`Shift-Alt-S`
   Move selected vertices outward in a spherical shape around the midpoint.

Arrange Strokes
   Arranges the selection of strokes up/down in the drawing order of the active layer.

   Bring Forward, Send Backward, Bring to Front, Send to Back
Move to Color
   Sets the active color as the new color to all selected strokes.

Subdivide
   Adds a number of new points evenly between two or more points,
   to set the number of points to add use *Number of Cuts*.
Join Strokes
   Type
      Join :kbd:`Ctrl-J`
         Joins selected strokes.
      Join & Copy :kbd:`Shift-Ctrl-J`
         Joins selected strokes as a new stroke.
   Leave Gaps
      Leaves gaps between joined strokes instead of linking them.
Flip Direction
   Flips the start and end of a stroke.
Show Directions
   Displays stroke drawing direction with a bigger green dot of the start point
   and a smaller red dot for the end point.

Reproject Strokes
   Plane
      Reprojects the selected strokes from the current viewpoint to get all points on the same plane again.
      This can be useful to fix problem from accidental 3D cursor movement, or viewport changes.
   Surface
      Project strokes onto geometry, instead of only doing this in a planar (i.e. parallel to viewplane) way
      (experimental).


Interpolate Panel
-----------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Stroke Mode
   :Panel:     :menuselection:`Tool Shelf --> Grease Pencil --> Interpolate`
   :Menu:      :menuselection:`GPencil --> Interpolate`

The following two operators can be used for interpolating between a pair of Grease Pencil frames.
To use these operators, there need to be Grease Pencil frames on both sides of the current frame.
(Also, note that the current frame cannot be on one of the frames that the interpolation is occurring between).

Interpolate :kbd:`Ctrl-Alt-E`
   It allows you to interactively pick a new sketch interpolate from the neighboring sketches.
   This is equivalent to the *Breakdown* tool for armatures.
Sequence :kbd:`Shift-Ctrl-E`
   This fills the space between a pair of Grease Pencil frames with interpolated frames.
   It is equivalent to the *Sample* tool in the Dope Sheet Editor.
Remove Breakdowns
   Can be used to delete generated "breakdown" keyframes (i.e. the small blue points).


Options
^^^^^^^

Interpolate All Layers
   Checkbox to interpolate all layers, not only active.
Interpolate Selected Strokes
   Checkbox to interpolate only the selected strokes in the original frame.


Sequence Options
^^^^^^^^^^^^^^^^

It is possible to control how the *Interpolate Sequence* tool blends between the two frames.

Linear
   The tool will interpolate between the two frames at a constant rate.
Custom Curve
   It is also possible to define a custom curve to get more fine-grained control over the interpolation
   using a :ref:`curve widget <ui-curve-widget>`.
Easing Equations
   The Robert Penner easing equations (and associated controls) can also be used to
   control the interpolation speed/shape, just like for F-Curves or Keyframes
   (:ref:`see also for more information <editors-graph-fcurves-settings-interpolation>`).


.. _bpy.types.GPencilSculptSettings:

Sculpt Strokes Panel
--------------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Stroke Mode
   :Panel:     :menuselection:`Tool Shelf --> Grease Pencil --> Sculpt Strokes`
   :Menu:      :menuselection:`GPencil --> Sculpt Strokes/Brushes`
   :Hotkey:    :kbd:`E-LMB`

Several tools for editing Grease Pencil strokes are provided in the form of brushes which
you can use to "paint" or "sculpt" the appearance of the strokes without having to keep doing
a tedious select-tweak-select-tweak pattern of edits.

Hold :kbd:`E-LMB` and drag to sculpt.


Brushes
^^^^^^^

The brushes currently implemented are:

Smooth
   Allows you to selectively relax jitter/shake and bumpiness, to tidy up messy parts of your sketches.

   Affect Pressure
      Use this option to perform smoothing on stroke thickness values.

Thickness
   The Thickness Brush can be used to increase (Add) or decrease (Subtract) the thickness of
   the parts of the stroke under the cursor.
Strength
   Increase/decrease (:kbd:`Ctrl`) the alpha value of the stroke. E.g. for creating fading effects.
Grab
   Takes the stroke points which fall within the brush circle when the sculpting action begins,
   and allows you to translate this set of points.
Push
   The Push Brush is very similar to the Grab brush, in that it also allows the user to translate stroke points.
   However, unlike the Grab Brush, the Push Brush is not restricted to operating only on the first set of points
   which were under the brush when the sculpt action was initiated. Instead, on each brush movement,
   the points currently under the brush get moved based on the amount
   the brush has moved since the last time it was evaluated.
Twist
   Used to twist/rotate points around the cursor, creating a "swirling" effect.
   It is useful for applying low levels of distortion to stroke points.
   The *Direction* controls whether the points are rotated in a clockwise (CW) or anti-clockwise (CCW) direction.
Pinch/Inflate
   Used to draw points away from the cursor, or towards it.

   Pinch
      Draw points towards the cursor.
   Inflate
      Push points away from the cursor.
Randomize
   Randomizes the stroke attributes.
   e.g. with *Position* enabled it displaces the points randomly in screen space to create jittered/jagged lines.
Clone Brush
   Used to paste the previously copied points (in the copy-paste buffer on the active layer),
   located at the point where you clicked.

   Hold :kbd:`LMB` and drag to position and adjust the pasted strokes.
   The strokes center follows the movements of the brush/cursor ("Stamp Mode").

   Use Falloff
      When the *Use Falloff* option is enabled, instead of moving all the newly pasted strokes by the same amount,
      only the points that are currently under the cursor get affected. Thus, in this mode of operation,
      the brush is closer to a Paste and Push operation instead ("Stamp and Smudge").

   .. Ed: not available any more? 2.78
      Continuous: As the brush moves, repeatedly just paste new copies for where the brush is now.
      In effect, this treats the contents of the copy buffer as the "brush template/kernel"
      used for "dabbing" samples all over the canvas.


Common Options
^^^^^^^^^^^^^^

Radius :kbd:`Shift-F`/:kbd:`Wheel`
   The size of the brush. Increase/decrease brush size with :kbd:`Shift-F` when not sculpting or
   with :kbd:`Wheel` while sculpting (i.e. with the pen tip down, or mouse button held).
Strength :kbd:`Ctrl-F`/:kbd:`Shift-Wheel`
   The Strength of the brush, can be changed by the pressure of the stylus.
   (In/decrease see *Radius*).
Use Falloff
   Enables a linear falloff to calculate the influence of the brush on a point.
   That is, a point closer to the midpoint of the brush (i.e. the point under the cursor)
   will get affected more than the ones at the edges.
Direction :kbd:`Ctrl-E-LMB`
   Radio button to invert the brush effect.
Affect
   Enable sculpt for position, strength (alpha value) and thickness in Smooth and Randomize brush.


Further Options
^^^^^^^^^^^^^^^

Selection Mask
   Used to restrict the brush to only operating on the selected points.
Alpha :kbd:`Ctrl-H`
   Alpha value of the visualization for selected vertices.
   The visibility can be toggled (hide/unhide) using :kbd:`Ctrl-H`.
