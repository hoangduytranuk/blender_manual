.. _tool-grease-pencil-draw-erase:

**********
Erase Tool
**********

.. admonition:: Reference
   :class: refbox

   :Mode:      Draw Mode
   :Panel:     :menuselection:`Tool Shelf --> Tools --> Draw Tools --> Erase`

The Erase tool erase already drawn strokes.


Usage
=====

Selecting a Brush
-----------------

In the Topbar select the brush to use with the tool.

Brush
   The :ref:`ui-data-block` to select a preset brush type or a custom brush.
   Erase tool uses *Erase Brushes* types (soft, point and stroke).

For more information about erase brushes see:
:doc:`Erase Brush </grease_pencil/modes/draw/tool_settings/brushes/erase_brush>`


Soft Erasing
------------

- Select an erase brush of type Soft/Hard.

- Adjust brush settings.

Radius
   The radius of the brush in pixels.

   :kbd:`F` allows you to change the brush size interactively by dragging the mouse/pen.
   Typing a number then enter while using :kbd:`F` allows you to enter the size numerically.

      Use Pressure (pressure sensitivity icon)
         Uses stylus pressure to control how strong the effect is.
      Occlude Eraser (overlapping squares icon)
         Erase only strokes visible and not occluded by geometry.

Strength
   Control how much will affect the eraser the stroke transparency (alpha).

   You can change the brush strength interactively by pressing :kbd:`Shift-F`
   in the 3D View and then moving the mouse/pen and then :kbd:`LMB`.
   You can enter the size numerically also while in :kbd:`Shift-F` sizing.

      Use Pressure (pressure sensitivity icon)
         Uses stylus pressure to control how strong the effect is.

Affect Stroke Strength
   Amount of deletion of stroke strength (alpha) while erasing.
Affect Stroke Thickness
   Amount of deletion of stroke thickness while erasing.

- Click and hold :kbd:`LMB` or use the :kbd:`Pen` tip to delete strokes on the viewport.

.. list-table::

   * - .. figure:: /images/grease-pencil_modes_draw_tools_erase_soft-01.png
          :width: 200px

          Original drawing.

     - .. figure:: /images/grease-pencil_modes_draw_tools_erase_soft-02.png
          :width: 200px

          The eraser affect the transparency of the strokes.

     - .. figure:: /images/grease-pencil_modes_draw_tools_erase_soft-03.png
          :width: 200px

          Final result.


Point Erasing
-------------

- Select an erase brush of type Point.

- Adjust brush settings.

Radius
   Radius of the brush in pixels.

   Use Pressure (pressure sensitivity icon)
      Uses stylus pressure to control how strong the effect is.
   Occlude Eraser (overlapping squares icon)
      Erase only strokes visible and not occluded by geometry.

- Click and hold :kbd:`LMB` or use the :kbd:`Pen` tip to delete strokes on the viewport.

.. list-table::

   * - .. figure:: /images/grease-pencil_modes_draw_tools_erase_point-01.png
          :width: 200px

          Original drawing.

     - .. figure:: /images/grease-pencil_modes_draw_tools_erase_point-02.png
          :width: 200px

          The eraser delete one point at a time.

     - .. figure:: /images/grease-pencil_modes_draw_tools_erase_point-03.png
          :width: 200px

          Final result.


Stroke Erasing
--------------

- Select an erase brush of type Stroke.

- Adjust brush settings.

Radius
   Radius of the brush in pixels.

   Use Pressure (pressure sensitivity icon)
      Uses stylus pressure to control how strong the effect is.
   Occlude Eraser (overlapping squares icon)
      Erase only strokes visible and not occluded by geometry.

- Click and hold :kbd:`LMB` or use the :kbd:`Pen` tip to delete strokes on the viewport.

.. list-table::

   * - .. figure:: /images/grease-pencil_modes_draw_tools_erase_stroke-01.png
          :width: 200px

          Original drawing.

     - .. figure:: /images/grease-pencil_modes_draw_tools_erase_stroke-02.png
          :width: 200px

          The eraser delete one stroke at a time.

     - .. figure:: /images/grease-pencil_modes_draw_tools_erase_stroke-03.png
          :width: 200px

          Final result.
