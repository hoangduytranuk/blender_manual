
***************
Sculpting Tools
***************

.. figure:: /images/sculpt-paint_sculpting_toolbar_index_brushes.png
   :align: right

Draw :kbd:`X`
   Moves vertices inward or outward,
   based the average normal of the vertices contained within the drawn brush stroke.

Clay :kbd:`C`
   Similar to the *Draw* brush, but includes settings to adjust the plane on which the brush acts.
   It behaves like a combination of the *Flatten* and *Draw* brushes.

Clay Strips
   Similar to the *Clay* brush, but it uses a cube to define the brush area of influence rather than a sphere.

Layer :kbd:`L`
   This brush is similar to *Draw*, except that the height of the displacement layer is capped.
   This creates the appearance of a solid layer being drawn.
   This brush does not draw on top of itself; a brush stroke intersects itself.
   Releasing the mouse button and starting a new stroke
   will reset the depth and paint on top of the previous stroke.

   Persistent
      You can keep sculpting on the same layer between strokes when this is on.
   Set Persistent Base
      This button resets the base so that you can add another layer.

Inflate/Deflate :kbd:`I`
   Similar to *Draw*,
   except that vertices in *Inflate* mode are displaced in the direction of their own normals.

Blob
   Pushes mesh outward or inward into a spherical shape with settings to
   control the amount of pinching at the edge of the sphere.

Crease :kbd:`Shift-C`
   Creates sharp indents or ridges by pushing or pulling the mesh, while pinching the vertices together.

Smooth :kbd:`S`
   As the name suggests, eliminates irregularities in the area of the mesh within the brush's
   influence by smoothing the positions of the vertices.

Flatten/Contrast :kbd:`Shift-T`
   The *Flatten* brush determines an "area plane"
   located by default at the average height above/below the vertices within the brush area.
   The vertices are then pulled towards this plane.
   The inverse of the *Flatten* brush is the *Contrast* brush
   which pushes vertices up or down away from the brush plane.

Fill/Deepen
   Works like the Flatten brush, but only brings vertices below the brush plane upwards.
   The inverse of the *Fill* brush is to *Deepen* by pushing vertices below the plane downward.

Scrape/Peaks
   The *Scrape* brush works like the *Flatten* brush, but only brings vertices above the plane downwards.
   The inverse of the *Scrape* brush is to *Peak* by pushing vertices above the plane up away from the plane.

Pinch/Magnify :kbd:`P`
   Pulls vertices towards the center of the brush.
   The inverse setting is *Magnify*, in which vertices are pushed away from the center of the brush.

Grab :kbd:`G`
   Used to drag a group of points around. Unlike the other brushes,
   *Grab* does not modify different points as the brush is dragged across the model.
   Instead, *Grab* selects a group of vertices on mouse-down, and pulls them to follow the mouse.
   The effect is similar to moving a group of vertices in Edit Mode with Proportional Editing enabled,
   except that *Grab* can make use of other Sculpt Mode options (like textures and symmetry).

Snake Hook :kbd:`K`
   Pulls vertices along with the movement of the brush to create long, snake-like forms.

   Pinch
      The *Snake Hook* brush tends to loose volume along the stroke,
      with pinch > 0.5 it's possible to sculpt shapes without loosing volume.
   Rake
      A factor to support moving the mesh with rotation following the cursor's motion.

Thumb
   Similar to the *Nudge* brush, this one flattens the mesh in the brush area,
   while moving it in the direction of the brush stroke.

Nudge
   Moves vertices in the direction of the brush stroke.

Rotate
   Rotates vertices within the brush in the direction the cursor is moved. The initial drag direction
   is the zero angle and by rotating around the center you can create a vortex effect.

Simplify
   This brush collapses short edges (as defined by the detail size) whether or
   not the *Collapse Short Edges* option is enabled.
   This brush has no effect if dynamic topology is not enabled.
   It can be found in the :menuselection:`Brush --> Sculpt Tool` menu.

Mask :kbd:`M`
   Lets you select mesh parts to be unaffected by other brushes by painting vertex colors.
   The mask values are shown as gray-scale.
   I.e. the darker a masked area is, the less effect sculpting on it will have.
   See also the options of the :ref:`sculpt-mask-menu` menu.

   Mask Tool
      The mask brush has two modes:

      Draw
         Mask drawing.
      Smooth :kbd:`Shift`
         Pressing :kbd:`Shift` with the mask brush active will toggle the mask smoothing mode.

:ref:`Annotate <tool-annotate>`
   Draw free-hand annotation.

   Annotate Line
      Draw straight line annotation.
   Annotate Polygon
      Draw a polygon annotation.
   Annotate Eraser
      Erase previous drawn annotations.
