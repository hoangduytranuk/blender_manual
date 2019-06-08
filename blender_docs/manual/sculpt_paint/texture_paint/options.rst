
*******
Options
*******

See the :ref:`Overlay & Appearance <sculpt-paint-brush-appearance>` options.


Project Paint
=============

Occlude
   With Geometry occlusion active only exposed (not hidden by other mesh parts) pixels are affected.
   This also allows for 3D stencils to be used to mask out areas of the surface too.
Cull
   With backface culling enabled you can only paint on the front side of faces.
Normal
   Activates a view normal falloff which means that as faces point away from the view
   the brush strokes fade away to prevent harsh edges.

   Angle
      The normal angle at which the falloff begins.
Cavity Mask
   Cavity masking means that the brush will be masked if there is a cavity or a hill
   on the mesh surface depending on the mesh options. The cavity algorithm is vertex-based.
Bleed
   Seam Bleed extends the paint beyond UV island bounds to avoid visual artifacts (like bleed for baking).
Dither
   Amount of dithering when painting on 8 bit images.
Unified Settings
   Brush options shared between the brush types.

   Size, Color, Strength
