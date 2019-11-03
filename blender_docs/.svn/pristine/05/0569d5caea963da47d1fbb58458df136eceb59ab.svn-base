
****
Tabs
****

Stroke
======

Strokes are the final rendered lines. Yet you can tweak them, for example,
by removing the ones longer/shorter than some threshold,
chaining lines into a single stroke or breaking a stroke into several ones based on angles,
dashed pattern, etc.


Chaining
--------

.. figure:: /images/render_freestyle_parameter-editor_line-style_tabs_stroke-chaining.png

   Chaining.

By default all retrieved lines from the line set are chained together.
There are two basic chaining methods:

Plain
   The default chaining method; it creates simple chains.

Sketchy
   This chaining option allows for generating chains of feature edges with sketchy multiple strokes.
   Basically, it generates *Round* strokes instead of a single one.
   It is only really useful if you use some random-driven modifiers in the line style!

Rounds
   It specifies the number of rounds in sketchy strokes.

Chaining can also be turned off to render each line separately,
which can be useful for line styles which depend on accurate representation of the line set.


Splitting
---------

.. figure:: /images/render_freestyle_parameter-editor_line-style_tabs_stroke-splitting.png

   Splitting.

You can split up chains of Freestyle lines by checking one of the following:

Min, Max 2D Angle
   Splits chains of feature edges when they make a 2D angle above (or below) a minimum (or maximum) threshold.
2D Length
   Splits chains when they are longer than the given value.
Material Boundary
   Splits chains of feature edges if they cross from one material to another.

Split Dash, Gap
   Splits the chains using the given dashed pattern
   ("D" stands for "dash", "G" stands for "gap"; see also `Dashed Line`_).

   D1, G1, D2, G2, D3, G3


Sorting
-------

.. figure:: /images/render_freestyle_parameter-editor_line-style_tabs_stroke-sorting.png

   Sorting.

You can sort the order of your strokes, allowing the lines to stack in the order given.

Sort key
   A sort key is used to determine the stacking order of lines.

   Distance from camera
      Lines closer to the camera lie on top of further lines.
   2D length
      Longer lines lie on top of shorter lines.
   Projected X, Y
      Sort by the projected X or Y value in the image coordinate system.
Integration Type
   Use in tandem with the Sort Key to determine the range for sorting.
   Since the distance of a line from the camera may vary over vertices,
   this option computes the sort key for a line from the values computed at
   individual vertices. The value computed for the line is:

   Mean
      The mean of the values obtained for the vertices.
   Min
      The minimum of the values obtained for the vertices.
   Max
      The maximum of the values obtained for the vertices.
   First
      The value obtained for the first vertex.
   Last
      The value obtained for the last vertex.
Sort Order
   With the given result you can choose to "Reverse" the sort order.


Selection
---------

.. figure:: /images/render_freestyle_parameter-editor_line-style_tabs_stroke-selection.png

   Selection.

You can also choose to only render selected chains.

Minimal, Maximal 2D Length
   Chains longer and/or shorter than *2D Length*.
Chain Count
   Allows the selection of first N chains.


Caps
^^^^

.. figure:: /images/render_freestyle_parameter-editor_line-style_tabs_stroke-caps.png

   Line tip caps.

You can choose between three types of line caps:

Butt
   Flat cap, exactly at the point the line ends.
Round
   A half circle centered on the end point of the line.
Square
   A square centered on the end point of the line
   (hence, like the circle, the drawn end of the line is slightly extended compared to its computed value).

.. figure:: /images/render_freestyle_parameter-editor_line-style_tabs_stroke-caps-example.png

   Line caps example.


Dashed Line
-----------

.. figure:: /images/render_freestyle_parameter-editor_line-style_tabs_stroke-dashed-line.png

   Dashes Line UI.

By enabling the *Dashed Line* checkbox,
you can specify three pairs of dash and gap lengths.
Dash values define the lengths of dash strokes,
while gap values specify intervals between two dashes.

If a zero gap is specified,
then the corresponding dash is ignored even if it has a non-zero value.

Dashes are treated as separate strokes, meaning that you can apply line caps,
as well as color, alpha and thickness modifiers.


Color
=====

.. figure:: /images/render_freestyle_parameter-editor_line-style_tabs_color.png

   Line Style Color UI.

In this tab you control the color of your strokes.

Base Color
   The base color for this line style.


Alpha
=====

.. figure:: /images/render_freestyle_parameter-editor_line-style_tabs_alpha.png

   Line Style Alpha UI.

In this tab you control the alpha (transparency) of your strokes.

Base Transparency
   The base alpha for this line style.


Thickness
=========

In this tab you control the thickness of your strokes.

.. figure:: /images/render_freestyle_parameter-editor_line-style_tabs_thickness.png

Base Thickness
   The base thickness for this line style.

Thickness Position
   Control the position of stroke thickness from the original (backbone) stroke geometry. There are four choices:

   Center
      The thickness is evenly split to the left and right side of the stroke geometry.
   Inside
      The strokes are drawn within object boundary.
   Outside
      The strokes are drawn outside the object boundary.
   Relative
      This allows you to specify the relative position by a number between 0.0 (inside) and 1.0 (outside),
      in the *Thickness Ratio* number button just below.

The thickness position options are applied only to strokes of edge types
*Silhouette* and *Border*,
since these are the only edge types defined in terms of the object boundary.
Strokes of other edge types are always drawn using the *Center* option.


Geometry
========

.. figure:: /images/render_freestyle_parameter-editor_line-style_tabs_geometry.png

   Line Style Geometry Overall UI.

In this tab you control the geometry of your strokes.
It contains only the option to add modifiers.


Texture
=======

.. figure:: /images/render_freestyle_parameter-editor_line-style_tabs_texture.png

   Line Style Texture.

Use Nodes/Textures
   In Cycles textures are defined by means of
   shader :doc:`nodes </render/freestyle/parameter_editor/line_style/nodes/index>`.
Spacing Along Stroke
   Allows to set the "pace" of textures mapped along the length of strokes.
Go to LineStyle Textures
   The "Go to LineStyle Textures" button is a shortcut to texture settings in the other tab.
