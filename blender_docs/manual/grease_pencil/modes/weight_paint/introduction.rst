
************
Introduction
************

Assigning weight to the points is primarily used for rigging strokes in cut-out animation,
where the vertex groups are used to define the relative bone influences on the strokes.
See :doc:`Using Vertex Group </sculpt_paint/weight_paint/usage>` for more information.

.. note::

   A vertex in *Grease Pencil* is called point.

Weight Painting is a method to maintain large amounts of weight information in a very intuitive way.
The selected *Grease Pencil* object is displayed slightly shaded with a rainbow color spectrum.
The color visualizes the weights associated to each point in the active vertex group.
By default blue means unweighted and red means fully weighted.

You assign weights to the points of the object by painting on it with weight brushes.
Starting to paint on a strokes automatically adds weights to the active vertex group
(a new vertex group is created if needed).


Weight Paint
============

.. figure:: /images/grease-pencil_modes_weight_paint_introduction_mode-selector.png

   3D View Mode selector: Weight Paint Mode.

Weight Paint Mode is selected from the *Mode* menu in the 3D View header.
Once Weight Paint Mode is activated, the Toolbar of the 3D View will change to Weight Paint Mode specific panels.
A red circle will appear and follow the location of the cursor in the 3D View.


Weight Options
==============

Multiframe
   Sometimes you may need to assign weight to several frames at the same time with the Weight Paint tools.

   You can activate multiframe edition with the Multiframe button next to the modes selector (faded lines icon).
   See :doc:`Multiframe </grease_pencil/multiframe>` for more information.
