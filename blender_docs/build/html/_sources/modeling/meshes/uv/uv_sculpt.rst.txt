.. _bpy.types.ToolSettings.use_uv_sculpt:

************
UV Sculpting
************

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Tool:      :menuselection:`Toolbar --> Grab`,
   :Tool:      :menuselection:`Toolbar --> Relax`,
   :Tool:      :menuselection:`Toolbar --> Pinch`
   :Panel:     :menuselection:`Sidebar --> Tool --> Brushes`

The sculpting tools allow you to grab, pinch and smooth UVs, just like for meshes in Sculpt Mode.
It can be activated with selecting either the *Grab*, *Relax*, or *Pinch* tool in the Toolbar.


Brushes
=======

Brushes
   The :ref:`ui-data-block` to select a preset brush type or a custom brush.

   Grab
      The Grab brush moves UVs around.
   Relax
      The Relax brush makes UVs more evenly distributed.
      The algorithm relies on space, not stretch minimization,
      so most probably a minimize stretch will have to be run for optimal results.
      However it is great to use after stitching islands,
      or when unwrap produces cluttered results to smooth the distribution of UVs.

      Relaxation Method
         There are two relax algorithms:

         Laplacian, HC
   Pinch
      The Pinch brush moves UVs toward the brush's center.
      The pinch brush can be inverted by pressing :kbd:`Ctrl-LMB`.


Brush Settings
==============

Radius
   This option controls the radius of the brush, measured in pixels.
   :kbd:`F` allows you to change the brush size interactively by dragging the mouse and then :kbd:`LMB`.
   Typing a number then enter while using :kbd:`F` allows you to enter the size numerically.

   Size Pressure
      Brush size can be affected by enabling the pressure sensitivity icon,
      if you are using a :ref:`Graphics Tablet <hardware-tablet>`.
   Use Unified Radius
      Use the same brush *Radius* across all brushes.

Strength
   Controls how much each application of the brush affects the UVs.
   You can change the brush strength interactively by pressing :kbd:`Shift-F`
   in the 3D Viewport and then moving the brush and then :kbd:`LMB`.
   You can enter the size numerically also while in :kbd:`Shift-F` sizing.

   Use Unified Strength
      Use the same brush *Strength* across all brushes.

.. note::

   All brushes use the :doc:`Airbrush Stroke Method </sculpt_paint/brush/stroke>`;
   they continue to act as long as you keep :kbd:`LMB` pressed.


Falloff
-------

The Falloff allows you to control the *Strength* falloff of the brush.
See :doc:`Painting Falloff </sculpt_paint/brush/falloff>` for more information.


Options
=======

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Sidebar --> Tool --> Options`

When UV sculpting is activated, the Sidebar shows the brush tool selection and options.

Lock Borders
   Locks the boundary of UV islands from being affected by the brush.
   This is very useful to preserve the shape of UV islands.
Sculpt All Islands
   To edit all islands and not only the island nearest to the brush center
   when the sculpt stroke was started.
Display Cursor
   Hides the sculpt cursor.
