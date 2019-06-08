.. _bpy.types.FreestyleSettings:

*********
View Maps
*********

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Render Layer --> Freestyle`

.. figure:: /images/render_freestyle_view-map_freestyle-panel.png

   Freestyle panel.

There is only one view map per render layer. It controls the edge detection parameters.

Control Mode
   Which detected edges are actually rendered, and how, can be controlled either through:

   Parameter Editor Mode
      The user-friendly :doc:`parameter editor </render/engines/freestyle/parameter_editor/index>`.
   Python Scripting Mode
      Powerful but complex :doc:`Python scripting </render/engines/freestyle/python>`.

View Map Cache
   An option to reuse a previously computed view map for subsequent rendering.
   The cache is automatically updated when the mesh geometry of the input 3D scene has been changed.

   This functionality offers a major performance boost for Freestyle animation rendering
   when the camera-space mesh geometry is static, as well as for repeated still renders
   with updates of line stylization options.

   Although the ''View map cache'' checkbox is a render layer option,
   the cache memory is shared by all render layers and scenes.
   This means that if Freestyle is used for two or more render layers
   (possibly in different scenes through the compositor),
   then the cached view map for one render layer is replaced by a new view map
   for another render layer and hence no performance gain is expected.
Face Smoothness
   When enabled, *Smooth Shading* will be taken into account for edges calculation.
Crease Angle
   If two adjacent faces form an angle less than the defined *Crease Angle*,
   the edge between them will be rendered when using *Crease* edge type selection in a line set.
   The value also affects *Silhouette* edge type selection.
Culling
   Ignore the edges that are out of view.
   (Saves some processing time and memory, but may reduce the quality of the result in some cases).


Advanced Options
================

.. figure:: /images/render_freestyle_view-map_freestyle-panel-advanced.png

   Advanced Options enabled.


*Sphere Radius* affects the calculation of curvatures for *Ridge*,
*Valley* and *Suggestive Contour* edge type selection in a line set.
The curvature at each vertex is computed by averaging the shape of
the surface within the specified radius. Increasing the value reduces
noise and detail.

Kr Derivative Epsilon
   Controls the threshold on the minimum rate of change of curvature used to filter the output
   of the *Suggestive Contour* edge type selection. Increasing the value reduces the amount of
   rendered lines, starting from smoother areas of the object (further information in
   `this pdf <https://wiki.blender.org/wiki/File:Manual-2.6-Render-Freestyle-PrincetownLinestyle.pdf>`__).
