
***************
Sculpting Tools
***************

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

   Persistent
      You can keep sculpting on the same layer between strokes when this is on.
   Set Persistent Base
      This button resets the base so that you can add another layer.

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

   Invert to Scrape
      When enabled, holding :kbd:`Ctrl` while sculpting
      changes the brush behavior to be the same as the *Scrape* brush.
      When disabled, holding :kbd:`Ctrl` while sculpting,
      will push vertices below the cursor downward.

Scrape
   The *Scrape* brush works like the *Flatten* brush, but only brings vertices above the plane downwards.

   Invert to Fill
      When enabled, holding :kbd:`Ctrl` while sculpting
      changes the brush behavior to be the same as the *Fill* brush.
      When disabled, holding :kbd:`Ctrl` while sculpting,
      will push vertices above the cursor up away from the cursor.

Multiplane Scrape
   Scrapes the mesh with two angled planes at the same time, producing a sharp edge between them.
   This is useful for creating edges when sculpting hard surface objects.

   Plane Angle
      The angle between the two planes of the brush, pressing :kbd:`Ctrl` inverts the angle.

   Dynamic Mode
      When enabled, the base angle is sampled from the mesh surface.
      The *Plane Angle* controls how much the angle will increase when applying pen pressure.
      When pressing :kbd:`Ctrl`, it locks the plane angle to 0 degrees.

   Show Cursor Preview
      Displays a preview of the two scrape planes
      and the angle they form instead of the cursor while performing the stroke.

Pinch :kbd:`P`
   Pulls vertices towards the center of the brush.
   The inverse setting is *Magnify*, in which vertices are pushed away from the center of the brush.

Grab :kbd:`G`
   Used to drag a group of points around. Unlike the other brushes,
   *Grab* does not modify different points as the brush is dragged across the model.
   Instead, *Grab* selects a group of vertices on mouse-down, and pulls them to follow the mouse.
   The effect is similar to moving a group of vertices in Edit Mode with Proportional Editing enabled,
   except that *Grab* can make use of other Sculpt Mode options (like textures and symmetry).

   Grab Active Vertex
      Snaps the maximum strength of the brush to the highlighted active vertex,
      making it easier to manipulate low poly models or meshes with subdivision surfaces.

      Enabling *Grab Active Vertex* also enables a dynamic mesh preview which
      generates a preview of vertices connected to om the active vertex.
      This helps to visualize the real geometry that is being manipulating while sculpting with active modifiers.

Snake Hook :kbd:`K`
   Pulls vertices along with the movement of the brush to create long, snake-like forms.

   Magnify
      The *Snake Hook* brush tends to loose volume along the stroke,
      with *Magnify* value greater than 0.5 it's possible to sculpt shapes without loosing volume.
   Rake
      A factor to support moving the mesh with rotation following the cursor's motion.

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

   Pose Origin Offset
      Offset of the pose origin in relation to the brush radius.
      This is useful to manipulate areas with a lot of complex shapes like fingers.
   Smooth Iterations
      Controls the smoothness of the falloff of the deformation.
   Pose IK Segments
      Controls how many :ref:`IK bones <bone-constraints-inverse-kinematics>`
      are going to be created for posing.

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

   Mask Tool
      The mask brush has two modes:

      Draw
         Mask drawing.
      Smooth :kbd:`Shift`
         Pressing :kbd:`Shift` with the mask brush active will toggle the mask smoothing mode.

Mesh Filter
   Applies a deformation to all vertices in the mesh at the same time.
   To use this tool, simply click and drag away from the object to have a positive effect
   and click and drag towards the mesh to have a negative effect.

   Filter Type
      Smooth
         Eliminates irregularities of the mesh by making the positions of the vertices more uniform.
         This filter works similar to the *Smooth Brush*.
      Scale
         Increases the size of the mesh.
         This filter works similar to the :ref:`Scale Transform <bpy.ops.transform.scale>`.
      Inflate
         Displaces vertices uniformly along their normal.
         This filter works similar to the *Inflate Brush*.
      Sphere
         Morphs the mesh to progressively look more like a sphere.
         This filter works similar to the :ref:`To Sphere Transform <bpy.ops.transform.tosphere>`.
      Random
         Randomly moves vertices along the vertex normal.
         This filter works similar to the :ref:`Randomize Transform <bpy.ops.object.randomize_transform>`.
      Relax
         Tries to create an even distribution of quads without deforming the volume of the mesh.
         This filter works the same as the *Relax* mode of the *Slide Relax* brush.
   Strength
      The amount of effect the filter has on the mesh.
   Deformation Axis
      Apply the deformation only on the selected axis.

:ref:`Annotate <tool-annotate>`
   Draw free-hand annotation.

   Annotate Line
      Draw straight line annotation.
   Annotate Polygon
      Draw a polygon annotation.
   Annotate Eraser
      Erase previous drawn annotations.
