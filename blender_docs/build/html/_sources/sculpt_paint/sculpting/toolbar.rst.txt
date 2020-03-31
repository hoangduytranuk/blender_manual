
*******
Toolbar
*******

.. figure:: /images/sculpt-paint_sculpting_tools_brushes.png
   :align: right

Draw :kbd:`X`
   Moves vertices inward or outward,
   based the average normal of the vertices contained within the drawn brush stroke.

Draw Sharp
   Similar to the *Draw* brush however, it deforms the mesh from the original coordinates
   and uses the *Sharper* :doc:`Falloff </sculpt_paint/brush/falloff>`.
   This is useful for creating cloth wrinkles, stylized hair or hard surface edges.

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

Inflate :kbd:`I`
   Similar to *Draw*,
   except that vertices in *Inflate* mode are displaced in the direction of their own normals.

Blob
   Pushes mesh outward or inward into a spherical shape with settings to
   control the amount of magnification at the edge of the sphere.

Crease :kbd:`Shift-C`
   Creates sharp indents or ridges by pushing or pulling the mesh, while pinching the vertices together.

Smooth :kbd:`S`
   Eliminates irregularities in the area of the mesh within the brush's
   influence by smoothing the positions of the vertices.

Flatten :kbd:`Shift-T`
   The *Flatten* brush determines an "area plane"
   located by default at the average height above/below the vertices within the brush area.
   The vertices are then pulled towards this plane.
   The inverse of the *Flatten* brush is the *Contrast* brush
   which pushes vertices up or down away from the brush plane.

Fill
   Works like the Flatten brush, but only brings vertices below the brush plane upwards.

Scrape
   The *Scrape* brush works like the *Flatten* brush, but only brings vertices above the plane downwards.

Multiplane Scrape
   Scrapes the mesh with two angled planes at the same time, producing a sharp edge between them.
   This is useful for creating edges when sculpting hard surface objects.

Pinch :kbd:`P`
   Pulls vertices towards the center of the brush.
   The inverse setting is *Magnify*, in which vertices are pushed away from the center of the brush.

Grab :kbd:`G`
   Used to drag a group of vertices around. *Grab* selects a group of vertices on mouse-down,
   and pulls them to follow the mouse. And unlike other brushes,
   *Grab* does not move different vertices as the brush is dragged across the model.
   The effect is like moving a group of vertices in Edit Mode with Proportional Editing enabled,
   except that *Grab* can make use of other Sculpt Mode options (like textures and symmetry).

Elastic Deform
   Used to simulate realistic deformations such as grabbing or twisting of :term:`elastic` objects.
   For example, this tool works great for modeling the shape of flesh like objects such as humans or animals.
   When pressing :kbd:`Ctrl`, the brush deforms vertices along the normal of the active vertex.

Snake Hook :kbd:`K`
   Pulls vertices along with the movement of the brush to create long, snake-like forms.

Thumb
   Similar to the *Nudge* brush, this one flattens the mesh in the brush area,
   while moving it in the direction of the brush stroke.

Pose
   This brush is used to pose a model simulating an armature-like deformation.
   The pivot point for rotation is calculated automatically based
   on the radius of the brush and the topology of the model.
   When pressing :kbd:`Ctrl`, the pose brush applies a twist rotation
   to the posing segments instead of using the rotation or an IK deformation.
   The falloff of the rotation across multiple segments is controlled by the brush falloff curve.

Nudge
   Moves vertices in the direction of the brush stroke.

Rotate
   Rotates vertices within the brush in the direction the cursor is moved. The initial drag direction
   is the zero angle and by rotating around the center you can create a vortex effect.

Slide Relax
   This brush slides the topology of the mesh in the direction of the stroke
   without changing the geometrical shape of the mesh.
   When pressing :kbd:`Shift`, the brush enters *Relax* mode
   which tries to create an even distribution of quads without deforming the volume of the mesh.

Simplify
   This brush collapses short edges (as defined by the detail size) whether or
   not the *Collapse Short Edges* option is enabled.
   This brush has no effect if dynamic topology is not enabled.

Mask :kbd:`M`
   Lets you select mesh parts to be unaffected by other brushes by painting vertex colors.
   The mask values are shown as gray-scale.
   I.e. the darker a masked area is, the less effect sculpting on it will have.
   See also the options of the :ref:`sculpt-mask-menu` menu.

Mesh Filter
   Applies a deformation to all vertices in the mesh at the same time.
   To use this tool, simply click and drag away from the object to have a positive effect
   and click and drag towards the mesh to have a negative effect.

Move
   Translation tool.

Rotate
   Rotation tool.

Scale
   Scale tool.

Transform
   Tool to adjust the objects translation, rotations and scale.

:ref:`Annotate <tool-annotate>`
   Draw free-hand annotation.

   Annotate Line
      Draw straight line annotation.
   Annotate Polygon
      Draw a polygon annotation.
   Annotate Eraser
      Erase previous drawn annotations.
