
*********
Structure
*********

.. _curve-bezier:

Bézier Curves
=============

The main elements used in editing Bézier curves are the control points and handles.
A segment (the actual curve) is found between two control points.
The handles define the curvature of the segment.

In the image below,
the control points can be found in the middle of the pink line,
while the handles comprise the extensions from the control point.
The arrows visualize the normals of the curve, which indicate i.e.
the direction and the tilt.

.. figure:: /images/modeling_curves_structure_control-points-handles.png

   Bézier Curve in Edit Mode.


.. _curve-bezier-handle-type:

Handle Types
------------

There are four Bézier curve handle types.
They can be accessed by pressing :kbd:`V` and selecting from the list that appears,
or by pressing the appropriate hotkey combination.

.. figure:: /images/modeling_curves_structure_bezier-handle-types.png
   :align: right

   Bézier Curve Handle Types.


.. _curve-handle-type-auto:

Automatic :kbd:`V A`
   This handle has a completely automatic length and direction
   which is set by Blender to ensure the smoothest result.
   These handles convert to *Aligned* handles when moved. (Yellow handles).
Vector :kbd:`V V`
   Both parts of a handle always point to the previous handle or the next handle which allows
   you to create curves or sections thereof made of straight lines or with sharp corners.
   Vector handles convert to *Free* handles when moved. (Green handles).
Aligned :kbd:`V L`
   These handles always lie in a straight line,
   and give a continuous curve without sharp angles. (Purple handles).
Free :kbd:`V F`
   The handles are independent of each other. (Black handles).


.. _curve-nurbs:

NURBS
=====

N.U.R.B.S. is the abbreviation of Non-Uniform Rational B-Splines.
One of the major differences between Bézier objects and NURBS objects is that Bézier curves
are approximations. For example, a Bézier circle is an *approximation* of a circle,
whereas a NURBS circle is an *exact* circle.
NURBS theory can be a *very* complicated topic. For an introduction,
please consult the `Wikipedia page <https://en.wikipedia.org/wiki/NURBS>`__.
