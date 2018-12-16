.. _bpy.ops.curve.primitive*add:

**********
Primitives
**********

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode and Edit Mode
   :Panel:     :menuselection:`Tool Shelf --> Create --> Add Primitive/Curve`
   :Menu:      :menuselection:`Add --> Curve`
   :Hotkey:    :kbd:`Shift-A`

.. figure:: /images/modeling_curves_primitives_add-curve-menu.png
   :align: right

   Add Curve menu.

In Object Mode, the *Add Curve* menu, provides five different curve primitives:


Bézier Curve
============

Adds an open 2D Bézier curve with two control points.


Bézier Circle
=============

Adds a closed, circle-shaped 2D Bézier curve (made of four control points).


NURBS Curve
===========

Adds an open 2D :term:`NURBS` curve, with four control points, with *Uniform* knots.


NURBS Circle
============

Adds a closed, circle-shaped 2D :term:`NURBS` curve (made of eight control points).


Path
====

Adds a :term:`NURBS` open 3D curve made of five aligned control points,
with *Endpoint* knots and the *Curve Path* setting enabled.


Draw Curve
==========

A free-hand :doc:`draw tool </modeling/curves/editing/draw>` for curve creation by dragging the mouse.


Common Options
==============

Radius, Align to View, Location, Rotation
   See :ref:`Common Object Options <object-common-options>`.
