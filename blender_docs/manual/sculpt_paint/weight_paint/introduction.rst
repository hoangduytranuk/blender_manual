
************
Introduction
************

Vertex Groups can potentially have a very large number of associated vertices
and thus a large number of weights (one weight per assigned vertex).
*Weight Painting* is a method to maintain large amounts of weight information
in a very intuitive way.

It is primarily used for rigging meshes, where the vertex groups are used to
define the relative bone influences on the mesh. But we use it also for
controlling particle emission, hair density, many modifiers, shape keys, etc.

.. figure:: /images/sculpt-paint_weight-paint_introduction_example.jpg

   Vertex Group in Weight Paint Mode.

You enter *Weight Paint Mode* from the Mode Menu :kbd:`Ctrl-Tab`.
The selected Mesh Object is displayed slightly shaded with a rainbow color spectrum.
The color visualizes the weights associated to each vertex in the active Vertex Group.
By default *blue* means unweighted and *red* means fully weighted.

You assign weights to the vertices of the Object by painting on it with weight brushes.
Starting to paint on a mesh automatically adds weights to the active Vertex Group
(a new Vertex Group is created if needed).


The Weighting Color Code
========================

Weights are visualized by a gradient using a cold/hot color system,
such that areas of low value (with weights close to 0.0) are displayed as blue (cold)
and areas of high value (with weights close to 1.0) are displayed as red (hot).
And all in-between values are displayed as rainbow colors (blue, green, yellow, orange, red).

.. figure:: /images/sculpt-paint_weight-paint_introduction_color-code.png

   The color spectrum and their respective weights.

In addition to the above described color code, Blender has a special visual notation
(as an option) for unreferenced vertices: They are displayed as black.
Thus you can see the referenced areas (displayed as cold/hot colors) and
the unreferenced areas (in black) at the same time.
This is most practicable when you look for weighting errors.
See :doc:`/sculpt_paint/weight_paint/tool_settings/options`.

.. figure:: /images/sculpt-paint_weight-paint_introduction_color-code-black.png

   Unreferenced vertices example.

.. note::

   You can customize the colors in the weight gradient by enabling
   :ref:`Custom Weight Paint Range <prefs-system-weight>` in the *System* tab
   of the *Preferences*.
