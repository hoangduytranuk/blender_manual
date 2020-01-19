
*****
Basic
*****

.. admonition:: Reference
   :class: refbox

   :Mode:      Sculpt Mode
   :Panel:     :menuselection:`Toolbar --> Tools --> Brushes`

Brush Type
   TODO.


Brush Settings
==============

Radius
   This option controls the radius of the brush, measured in pixels.
   :kbd:`F` allows you to change the brush size interactively by
   dragging the mouse and then :kbd:`LMB` (the texture of the brush should be visible inside the circle).
   Typing a number then enter while using :kbd:`F` allows you to enter the size numerically.

   Size Pressure
      Brush size can be affected by enabling the pressure sensitivity icon,
      if you are using a :ref:`Graphics Tablet <hardware-tablet>`.
   Use Unified Radius
      Use the same brush *Radius* across all brushes.

Radius Unit
   TODO.

Strength
   Controls how much each application of the brush affects the model.
   For example, higher values cause the *Draw* brush to add depth to the model more quickly,
   and cause the *Smooth* brush to smooth the model more quickly.
   This setting is not available for *Grab*, *Snake Hook*, or *Rotate*.

   You can change the brush strength interactively by pressing :kbd:`Shift-F`
   in the 3D View and then moving the brush and then :kbd:`LMB`.
   You can enter the size numerically also while in :kbd:`Shift-F` sizing.

   Strength Pressure
      Brush strength can be affected by enabling the pressure sensitivity icon,
      if a supported tablet is being used.
   Use Unified Strength
      Use the same brush *Strength* across all brushes.

   .. tip::

      If the range of strengths does not seem to fit the model
      (for example, if even the lowest strength setting still makes too large of a change on the model)
      then you can scale the model (in Edit Mode, not Object Mode).
      Larger sizes will make the brush's effect smaller, and vice versa.

Direction :kbd:`Ctrl`
   Brush direction toggle, *Add* raises geometry towards the brush,
   *Subtract* lowers geometry away from the brush. This setting can be toggled with :kbd:`Ctrl` while sculpting.
Normal Radius
   Todo.
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
