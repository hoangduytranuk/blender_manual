
*************
Active Spline
*************

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Properties --> Curve --> Active Spline`

.. figure:: /images/modeling_curves_properties_data_active-spline-panel-curves.png

   Curves Active Spline panel.

Cyclic U
   Closes the curve.
Resolution U
   Alters the smoothness of each segment by changing the number of subdivisions.

.. _bpy.types.Spline.tilt_interpolation:

Tilt Interpolation
   Alters how the tilt of a segment is calculated.
Radius
   Alters how the radius of a beveled curve is calculated.
   The effects are easier to see after :ref:`increasing the radius <modeling-curve-radius>`.
Smooth
   Smooths the normals of the curve.


NURBS Curves
============

One of the characteristics of a NURBS object is the *knot vector*.
This is a sequence of numbers used to determine the influence of the control points on the curve.
While you cannot edit the knot vectors directly,
you can influence them through the *Endpoint* and *Bézier* options in the Active Spline panel.
Note that, the *Endpoint* and *Bézier* settings only apply to open NURBS curves.

.. figure:: /images/modeling_curves_properties_data_active-spline-panel-nurbs.png
   :align: center

   NURBS Active Spline panel.

.. _modeling-curve-knot:

Cyclic
   Makes the NURBS curve cyclic.

   .. list-table::

      * - .. figure:: /images/modeling_curves_properties_data_nurbs-default.png

             Default NURBS curve.

        - .. figure:: /images/modeling_curves_properties_data_nurbs-cyclic.png

             A NURBS curve with Cyclic applied.

Bézier
   Makes the NURBS curve act like a Bézier curve.
   The NURBS control points act like *Free* handles of Bézier curve.
   Depending on the *Order*, 3 or 4 control points form one curve segment.
   Cyclic and Endpoint must be disabled for this option to work.
Endpoint
   Makes the curve contact the end control points. Cyclic must be disabled for this option to work.

   .. list-table::

      * - .. figure:: /images/modeling_curves_properties_data_nurbs-default.png

             Default NURBS curve.

        - .. figure:: /images/modeling_curves_properties_data_nurbs-endpoint.png

             A NURBS curve with Endpoint enabled.

.. _modeling-curve-order:

Order
   The order of the NURBS curve determines the area of influence of the control points over the curve.
   Higher order values means that a single control point has a greater
   influence over a greater relative proportion of the curve.
   The valid range of *Order* values is 2-6 depending on the number of control points present in the curve.

   .. list-table::

      * - .. figure:: /images/modeling_curves_properties_data_nurbs-default.png

             NURBS curves with orders of 4.

        - .. figure:: /images/modeling_curves_properties_data_nurbs-order.png

             NURBS curves with orders of 2.
