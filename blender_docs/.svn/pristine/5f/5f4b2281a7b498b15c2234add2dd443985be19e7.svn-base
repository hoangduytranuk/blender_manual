.. _tool-grease-pencil-draw-fill:

*********
Fill Tool
*********

.. admonition:: Reference
   :class: refbox

   :Mode:      Draw Mode
   :Panel:     :menuselection:`Tool Shelf --> Tools --> Draw Tools --> Fill`

The Fill tool is used to automatically fill closed strokes areas.


Usage
=====

Selecting Brush and Material
----------------------------

On the Topbar select the brush and material to use with the tool.

Brush
   The :ref:`ui-data-block` to select a preset brush type or a custom brush.
   Fill tool uses *Fill Brushes* types.   

Material
   Data-Block selector for the material.

   Pin Material (pin icon)
      Pin the material to the brush.

      The final appearance of the strokes is a combination of a brush and a material used,
      stick the material to the brush gives more control and avoid lack of coordination between the two.


For more information about brushes and materials see: :doc:`Fill Brush </grease_pencil/modes/draw/brushes/fill_brush>`
and :doc:`Material </grease_pencil/materials/introduction>`


Common Brush Options
---------------------

You can also configure the brush main settings exposed on the topbar for convenience.
For complete fill brushes configuration and settings see: :doc:`Fill Brush </grease_pencil/modes/draw/brushes/fill_brush>`.

Leak Size
   Size in pixel to consider the leak closed.

Thickness
   The thickness radius of the boundary stroke in pixels.
   
Simplify
   Number of simplify steps to apply to the boundary line.
   Higher values reduce the final filled area accuracy.

Boundary
   Sets the type of fill boundary limits calculation to perform.

   Default
      Use the thickness of the strokes and the editing lines together.
   Stroke
      Use only the thickness of the strokes (ignore edit lines).
   Line
      Use only the edit lines (ignore strokes).
   Show lines (grid icon)
      Toggle show help lines to see the fill boundary.


Filling Areas
-------------

Click :kbd:`LMB` in a closed stroke area. The tool will automatically calculate
the boundary and create a new closed stroke filled with the material selected.

.. list-table::

   * - .. figure:: /images/grease-pencil_modes_draw_tools_fill_fill-01.png
          :width: 200px

          Original Drawing.

     - .. figure:: /images/grease-pencil_modes_draw_tools_fill_fill-02.png
          :width: 200px

          Use the fill tool to leak materials on closed areas.

     - .. figure:: /images/grease-pencil_modes_draw_tools_fill_fill-03.png
          :width: 200px

          Final filled drawing.


Boundary Strokes
----------------

If you have a large gap in an area that you want fill,
you can use *Boundary Strokes*, a temporary help lines for closing open shapes.
To create a Boundary Strokes use :kbd:`Alt-LMB` and draw a line to close the desired area.

.. list-table::

   * - .. figure:: /images/grease-pencil_modes_draw_tools_fill_boundary-strokes-01.png
          :width: 200px

          Original Drawing.

     - .. figure:: /images/grease-pencil_modes_draw_tools_fill_boundary-strokes-02.png
          :width: 200px

          Add Boundary Strokes to close open areas (red lines).

     - .. figure:: /images/grease-pencil_modes_draw_tools_fill_boundary-strokes-03.png
          :width: 200px

          Use Fill Tool to leak material on the new closed area.

When you are satisfied with the fill result you can delete the Boundary strokes using
the *Clean Up* tool in the :doc:`Stroke Menu </grease_pencil/modes/edit/stroke_menu>` in Edit Mode.


Switch to Draw Tool
--------------------

Use :kbd:`Ctrl-LMB` to change temporary to the active draw tool.
For example to manually cover small areas difficult to reach for the fill tool.
see :doc:`Draw Tool </grease_pencil/modes/draw/tools/draw>` for more information.


Fill Options
============

Resolution
   Multiplier for fill resolution.
   Higher values gives better fill boundary accuracy but slower time for calculations.

Ignore Transparent strokes
   When enabled, strokes with transparency does not take into account on fill boundary calculations.

   Threshold
      Threshold value to consider a material transparent.
