
****
Hair
****

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Render --> Hair`

These are global settings that apply to all instances of hair systems.
The resolution of the strands is controlled by the step values in particle settings.
Each hair system uses the material identified in the particle settings in the same way as Blender Internal.

Use Hair
   Enables rendering of hair particle systems.

Primitive
   Triangles
      Uses a triangle mesh.

      Resolution
         Number of times to subdivide the hair.
         Higher values gives better quality results at the cost of increased memory usage.
   Line Segments
      Uses a straight curve primitive.
   Curve Segments
      Uses a smooth Cardinal curve primitive. These interpolate a path through the curve keys.
      However, it renders slower than line segments.

      Curve Subdivisions
         The interpolated path is subdivided to give points to connect.
         The parameter subdivisions sets the number of divisions used.

Shape
   Thick
      Cylindrical segments between two points.

      Cull back-faces
         Excludes strands emitted from the mesh backfacing the camera.

   Ribbons
      Are flat planes following the strand direction facing the camera.
