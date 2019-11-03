.. _tool-grease-pencil-draw-fill:

*********
Fill Tool
*********

.. admonition:: Reference
   :class: refbox

   :Mode:      Draw Mode
   :Panel:     :menuselection:`Toolbar --> Tools --> Draw Tools --> Fill`

The Fill tool is used to automatically fill closed strokes areas.


Usage
=====

Selecting a Brush and Material
------------------------------

In the Tool Settings select the brush and material to use with the tool.
The Fill tool uses *Fill Brush* types.
See :ref:`grease-pencil-draw-common-options` for more information.


Common Brush Options
--------------------

You can also configure the brush main settings exposed on the Tool Settings for convenience.
For the fill brushes configuration and settings
see: :doc:`Fill Brush </grease_pencil/modes/draw/tool_settings/brushes/fill_brush>`.


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
-------------------

Use :kbd:`Ctrl-LMB` to change temporary to the active draw tool.
For example to manually cover small areas difficult to reach for the fill tool.
see :doc:`Draw Tool </grease_pencil/modes/draw/tool_settings/draw>` for more information.


Fill Options
============

Resolution
   Multiplier for fill resolution.
   Higher values gives better fill boundary accuracy but slower time for calculations.

Ignore Transparent strokes
   When enabled, strokes with transparency does not take into account on fill boundary calculations.

   Threshold
      Threshold value to consider a material transparent.
