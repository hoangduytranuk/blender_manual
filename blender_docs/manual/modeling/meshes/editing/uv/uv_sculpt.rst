.. _bpy.types.ToolSettings.use_uv_sculpt:

************
UV Sculpting
************

.. admonition:: Reference
   :class: refbox

   :Mode:      Paint Mode and Mask Mode
   :Panel:     :menuselection:`Tools Shelf --> Options --> UV Sculpt`,
               :menuselection:`Tools Shelf --> Tools`
   :Menu:      :menuselection:`UVs --> UV Sculpt`
   :Hotkey:    :kbd:`Q`

The UV Sculpting "mode" allow you to grab, pinch and smooth UVs, just like Sculpt Mode.
It can be activated with :kbd:`Q` or by checking UV Sculpt in the *UVs* menu.


UV Sculpt
=========

When UV sculpting is activated, the Toolbar shows the brush tool selection and options.

Lock Borders
   Locks the boundary of UV islands from being affected by the brush.
   This is very useful to preserve the shape of UV islands.
Sculpt All Islands
   To edit all islands and not only the island nearest to the brush center
   when the sculpt stroke was started.
UV Sculpt Tools
   Brushes that operate on UVs.
   All brushes use the Airbrush Stroke Method: they continue to act as long as you keep :kbd:`LMB` pressed.

   Grab :kbd:`G`
      The Grab brush moves UVs around.
   Relax :kbd:`S`, :kbd:`Shift-LMB`
      The Relax brush makes UVs more evenly distributed.
      The algorithm relies on space, not stretch minimization,
      so most probably a minimize stretch will have to be run for optimal results.
      However it is great to use after stitching islands,
      or when unwrap produces cluttered results to smooth the distribution of UVs.

      Relaxation Method
         There are two relax algorithms:

         Laplacian, HC
   Pinch :kbd:`P`
      The Pinch brush moves UVs toward brush center.
      The pinch brush can be inverted by pressing :kbd:`Ctrl-LMB`.
Show Brush
   Hides the sculpt cursor.
