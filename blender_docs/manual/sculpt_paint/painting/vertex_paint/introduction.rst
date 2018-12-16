
************
Introduction
************

Vertex Painting is a simple way of painting color onto an object,
by directly manipulating the color of vertices, rather than textures,
and is fairly straightforward.

When a vertex is painted,
the color of the vertex is modified according to the settings of the brush. The color of all
visible planes and edges attached to the vertex are then modified with a gradient to the color
of the other connected vertices. Note that the color of occluded faces is not modified.

Vertex colors can be painted by switching to *Vertex Paint Mode*;
however, it will not show up in the render unless you check *Vertex Color Paint*
in the :doc:`Materials Options </render/blender_render/materials/properties/options>` panel (for Blender Renderer).
You can also the use :doc:`/render/blender_render/materials/nodes/types/input/geometry`
to access vertex color information in the material node tree.

For Cycles materials, can be used :doc:`/render/cycles/nodes/types/input/attribute`.

.. list-table::

   * - .. figure:: /images/sculpt-paint_painting_vertex-paint_introduction_mode-menu.png

          Vertex Painting Mode.

     - .. figure:: /images/sculpt-paint_painting_vertex-paint_introduction_material-options.png

          Blender Renderer material options.
