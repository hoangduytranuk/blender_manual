
*****
Other
*****

This page describes other curve editing tools that are not accessible via the edit menus.


.. _bpy.ops.curve.draw:

Draw Curve
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Tool:      :menuselection:`Toolbar --> Draw`

The Curve draw tool allows you to free-hand draw curves.

Error
   Error distance in object units. This can be seen similar to a subdivision rate for the curve.
   Lower values give a result that is closer to the drawing stroke while higher values give more smoothed results.
Fit Method
   Refit
      Incrementally re-fits the curve (gives best results).
   Split
      Splits the curve until the tolerance is met (gives a better drawing performance).
Corner Angle
   Any angles above this are considered corners.
Cyclic
   Toggles whether or not the curve is :term:`Cyclic`.


.. _bpy.types.CurvePaintSettings:

Stroke Options
--------------

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Sidebar --> Tool --> Curve Stroke`
   :Menu:      :menuselection:`Tool Settings --> Curve Stroke`

.. figure:: /images/modeling_curves_editing_draw_curve-stroke-panel.png
   :align: right

   Curve Stroke panel.

Type
   Type of curve to use for drawing.

   Poly
      Bézier Curve with straight line segments (auto handles).
   Bézier
      Tolerance
         Lower values give a result that is closer to the drawing stroke,
         while higher values give more smoothed results.

      Method
         Refit
            Incrementally re-fits the curve (gives best results).
         Split
            Splits the curve until the tolerance is met (gives a better drawing performance).

      Detect Corners
         Detects corners and uses non-aligned handles for them.

         Corner Angle
            Any angles above this are considered corners.

Pressure Radius
   Min
      Minimum radius when the minimum pressure is applied (also the minimum when tapering).
   Max
      Radius to use when the maximum pressure is applied (or when a tablet is not used).

Projection Depth
   Options to control where/how the curves are drawn.

   Cursor
      Uses the depth under the cursor to draw curves.

   Surface
      Used to draw on top of other objects.

      Offset
         Distance to offset the curve from the surface.
      Absolute Offset
         Applies a fixed offset (does not scale by the curve radius).
      Only First
         Only uses the start of the stroke for the depth.

         Normal/View
            Draws perpendicular to the surface.
         Normal/Surface
            Draws aligned to the surface.
         View
            Draws aligned to the viewport.


.. _bpy.ops.curve.spline_weight_set:
.. _modeling-curve-weight:

Set Goal Weight
===============

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Specials --> Set Goal Weight`

Sets the curve's :ref:`Weight <curves-weight>` for the selected control point to the specified value.
If more than one control point is selected this will set the *Mean Weight*.


.. _bpy.ops.curve.vertex_add:

Add Vertex
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Hotkey:    :kbd:`Ctrl-RMB`

Interactively places new points with :kbd:`Ctrl-RMB` at the cursor position.
With the selection it deals in same manner as the *Extrude Curve and Move* tool.
