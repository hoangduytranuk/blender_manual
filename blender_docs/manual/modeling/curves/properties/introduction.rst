.. (todo add) generalize from extrude

************
Introduction
************

Attributes
==========

Weight
------

This sets the "goal weight" of selected control points,
which is used when a curve has :doc:`Soft Body </physics/soft_body/index>` physics,
forcing the curve to "stick" to their original positions, based on the weight.


Radius
------

The Radius allows you to directly control the width of the extrusion along the "spinal" curve.
The *Radius* of the points is set using the *Shrink/Fatten Radius* transform tool :kbd:`Alt-S`,
the :menuselection:`Curve --> Transform --> Shrink/Fatten Radius`,
or the :menuselection:`Properties region --> Transform --> Radius`.

.. figure:: /images/modeling_curves_properties_introduction_extrude-radius.png
   :width: 320px

   One control point radius set to zero.

.. tip::

   Remember, these curves can be converted into meshes with :kbd:`Alt-C` in Object Mode.


Tilt
----

This setting controls how the normals (visualization: arrows)
twist around each control point -- so it is only relevant with 3D curves!
You set it using the *Tilt* transform tool in the Tool Shelf,
the :menuselection:`Properties region --> Transform --> Tilt`,
:menuselection:`Curve --> Transform --> Tilt`.

You can also reset it to its default value (i.e. perpendicular to the original curve plane)
with :kbd:`Alt-T`, :menuselection:`Curve --> Control Points --> Clear Tilt`.
With NURBS, the tilt is always smoothly interpolated.
However, with Bézier, you can choose the interpolation algorithm
between Linear, Ease, B-Spline, and Cardinal,
in the :menuselection:`Properties Editor --> Object Data --> Active Spline --> Tilt`.

.. figure:: /images/modeling_curves_properties_introduction_extrude-mean-tilt.png
   :width: 320px

   30 degree Mean Tilt of all control points.
