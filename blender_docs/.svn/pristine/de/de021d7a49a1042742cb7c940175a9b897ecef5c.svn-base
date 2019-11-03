.. _tool-grease-pencil-draw-curve:

**********
Curve Tool
**********

.. admonition:: Reference
   :class: refbox

   :Mode:      Draw Mode
   :Panel:     :menuselection:`Tool Shelf --> Tools --> Draw Tools --> Curve`

The Curve tool create complex bezier style curves.


Usage
=====

Selecting Brush and Material
----------------------------

In the Topbar select the brush and material to use with the tool.

Brush
   The :ref:`ui-data-block` to select a preset brush type or a custom brush.
   Curve tool uses *Draw Brushes* types.   

Material
   Data-Block selector for the material.   

   Pin Material (pin icon)
      Pin the material to the brush.

      The final appearance of the strokes is a combination of the brush and material used,
      binding the material to the brush gives more control and avoids a lack of coordination between the two.

For more information about brushes and materials see: :doc:`Draw Brush </grease_pencil/modes/draw/brushes/draw_brush>`
and :doc:`Material </grease_pencil/materials/introduction>`.


Common Brush Options
---------------------

You can configure the brush main settings exposed on the topbar for convenience.
For complete draw brushes configuration and settings see:
:doc:`Draw Brush </grease_pencil/modes/draw/brushes/draw_brush>`.

Radius
   The radius of the brush in pixels.

   :kbd:`F` allows you to change the brush size interactively by dragging the mouse/pen or
   by typing a number then confirm.

      Use Pressure (pressure sensitivity icon)
         Uses stylus pressure to control how strong the effect is.

Strength
   Control the stroke transparency (alpha).
   From totally transparent (0.0) to fully opaque (1.0).

   You can change the brush strength interactively by pressing :kbd:`Shift-F`
   in the 3D View and then moving the mouse/pen and then :kbd:`LMB`.
   You can also enter the size numerically.

      Use Pressure (pressure sensitivity icon)
         Uses stylus pressure to control how strong the effect is.

Thickness Profile
   Use a :doc:`curve widget </interface/controls/templates/curve>`. to define the stroke thickness
   from the start (left) to end (right) of the stroke.

   Use Curve
      When enabled, the stroke use a curve profile to control the thickness along the curve.

.. list-table:: Different thickness profile samples.

   * - .. figure:: /images/grease-pencil_modes_draw_tools_curve-thickness-profile-01.png
          :width: 200px

     - .. figure:: /images/grease-pencil_modes_draw_tools_curve-thickness-profile-02.png
          :width: 200px

     - .. figure:: /images/grease-pencil_modes_draw_tools_curve-thickness-profile-03.png
          :width: 200px


Creating Curves
---------------

#. Click (:kbd:`LMB` or the :kbd:`Pen` tip) and drag the start point.
#. Release on the desired end point.
#. After releasing you can tweak the curve using two cyan bezier like manipulators.
#. Then confirm (:kbd:`Enter`/:kbd:`MMB`) or cancel (:kbd:`Esc`/:kbd:`RMB`).

While dragging you can use :kbd:`Shift` to use only one manipulator to tweak the curve (like Arc Tool), 
use :kbd:`Alt` to create the arc from a center point or :kbd:`M` to flip.

:kbd:`+` and :kbd:`-` or using the mouse :kbd:`Wheel` will increase or decrease the amount of points in the final curve.


.. list-table::

   * - .. figure:: /images/grease-pencil_modes_draw_tools_curve-01.png
          :width: 200px

          click and dragging the start point.

     - .. figure:: /images/grease-pencil_modes_draw_tools_curve-02.png
          :width: 200px

          Tweaking curve with the manipulators.

     - .. figure:: /images/grease-pencil_modes_draw_tools_curve-03.png
          :width: 200px

          The curve after confirming.


Extruding
----------

before confirming you can use :kbd:`E` to extrude the end point of the curve
to generate multiple connected curves.

.. list-table::

   * - .. figure:: /images/grease-pencil_modes_draw_tools_curve-extrude-01.png
          :width: 200px

          End point extruding.

     - .. figure:: /images/grease-pencil_modes_draw_tools_curve-extrude-02.png
          :width: 200px

          Tweaking the last curve with the manipulators.

     - .. figure:: /images/grease-pencil_modes_draw_tools_curve-extrude-03.png
          :width: 200px

          The connected curves after confirming.
