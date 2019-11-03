
*****
Brush
*****

.. admonition:: Reference
   :class: refbox

   :Mode:      Sculpt Mode
   :Panel:     :menuselection:`Toolbar --> Tools --> Brush`
   :Menu:      :menuselection:`Brush --> Sculpt Tool`

Brush Type
   TODO.
Radius
   This option controls the radius of the brush, measured in pixels.
   :kbd:`F` allows you to change the brush size interactively by
   dragging the mouse and then :kbd:`LMB` (the texture of the brush should be visible inside the circle).
   Typing a number then enter while using :kbd:`F` allows you to enter the size numerically.
   Brush size can be affected by enabling the pressure sensitivity icon,
   if you are using a :ref:`Graphics Tablet <hardware-tablet>`.
Strength
   Controls how much each application of the brush affects the model.
   For example, higher values cause the *Draw* brush to add depth to the model more quickly,
   and cause the *Smooth* brush to smooth the model more quickly.
   This setting is not available for *Grab*, *Snake Hook*, or *Rotate*.

   You can change the brush strength interactively by pressing :kbd:`Shift-F`
   in the 3D View and then moving the brush and then :kbd:`LMB`.
   You can enter the size numerically also while in :kbd:`Shift-F` sizing.
   Brush strength can be affected by enabling the pressure sensitivity icon,
   if a supported tablet is being used.

   .. tip::

      If the range of strengths does not seem to fit the model
      (for example, if even the lowest strength setting still makes too large of a change on the model)
      then you can scale the model (in Edit Mode, not Object Mode).
      Larger sizes will make the brush's effect smaller, and vice versa.

Direction :kbd:`Ctrl`
   Brush direction toggle, *Add* raises geometry towards the brush,
   *Subtract* lowers geometry away from the brush. This setting can be toggled with :kbd:`Ctrl` while sculpting.
Autosmooth
   Sets the amount of smoothing to be applied to each stroke.
Topology
   See :ref:`Dyntopo <bpy.types.Brush.topology_rake_factor>`.
Normal Weight :kbd:`Ctrl`
   Constrains brush movement along the surface normal.
   Especially useful with the *Grab* brush, can be temporarily enabled by holding :kbd:`Ctrl`.
   E.g. *Grab* brush can be used to push a depression (hole) into the mesh when *Normal Weight* is set.

   Applies to *Grab* and *Snake Hook* brushes.
Plane Offset
   Offset for planar brushes (Clay, Fill, Flatten, Scrape),
   shifts the plane that is found by averaging the faces above or below.
Plane Trim
   Ability to limit the distance that planar brushes act.
   If trim is enabled vertices that are further away from the offset plane than
   the trim distance are ignored during sculpting.


Options
=======

Accumulate
   Causes stroke dabs to accumulate on top of each other.
Radius Unit
   TODO.
Sculpt Plane
   Use this menu to set the plane in which the sculpting takes place.
   In other words, the primary direction that the vertices will move.

   Area Plane
      The movement takes place in the direction of average normal for all active vertices within the brush area.
      Essentially, this means that the direction is dependent on the surface beneath the brush.
   View Plane
      Sculpting in the plane of the current 3D View.
   X, Y, Z Plane
      The movement takes place in the positive direction of one of the global axes.

Original Normal
   When locked it keeps using the normal of the surface where stroke was initiated,
   instead of the surface normal currently under the cursor.
Front Faces Only
   When enabled, the brush only affects vertices that are facing the viewer.
2D Falloff
   This turns the brush influence into a cylinder (the depth along the view is ignored) instead of a sphere.
   It can be used along the outline of a mesh to adjust its silhouette.
