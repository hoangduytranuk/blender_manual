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

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Tool:      :menuselection:`Tool Shelf --> Radius`
   :Panel:     :menuselection:`Sidebar --> Transform --> Radius`
   :Menu:      :menuselection:`Curve --> Transform --> Radius`
   :Hotkey:    :kbd:`Alt-S`

The Radius allows you to directly control the width of the extrusion along the "spinal" curve.
The *Radius* of the points is set using the *Radius* transform tool. Or in the Siderbar *Transform* panel.

.. figure:: /images/modeling_curves_properties_introduction_extrude-radius.png
   :width: 320px

   One control point radius set to zero.


Tilt
----

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Tool:      :menuselection:`Tool Shelf --> Tilt`
   :Panel:     :menuselection:`Sidebar --> Transform --> Tilt`
   :Menu:      :menuselection:`Control Points --> Tilt`
   :Hotkey:    :kbd:`Ctrl-T`

This setting controls how the normals (visualized as arrows)
twist around each control point -- so it is only relevant with 3D curves!

.. figure:: /images/modeling_curves_properties_introduction_extrude-mean-tilt.png
   :width: 320px

   30 degree Mean Tilt of all control points.


Clear Tilt
^^^^^^^^^^

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Menu:      :menuselection:`Control Points --> Clear Tilt`
   :Hotkey:    :kbd:`Alt-T`

You can also reset the tilt to its default value (i.e. perpendicular to the original curve plane).
With NURBS, the tilt is always smoothly interpolated. However, with Bézier,
you can choose the :ref:`interpolation algorithm <bpy.types.Spline.tilt_interpolation>`.
