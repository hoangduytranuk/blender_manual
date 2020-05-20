.. _bpy.types.Brush.smooth_deform_type:
.. _bpy.types.Brush.surface_smooth_shape_preservation:
.. _bpy.types.Brush.surface_smooth_current_vertex:
.. _bpy.types.Brush.surface_smooth_iterations:

******
Smooth
******

.. admonition:: Reference
   :class: refbox

   :Mode:      Sculpt Mode
   :Tool:      :menuselection:`Toolbar --> Smooth`
   :Hotkey:    :kbd:`S`

Eliminates irregularities in the area of the mesh within the brush's
influence by smoothing the positions of the vertices.

Deformation
   Deformation type that is used in the brush.

   Laplacian
      Smooths the surface and the volume.
   Surface
      Smooths the surface of the mesh, while preserving the volume.

      Shape Preservation
         How much of the original shape is preserved when smoothing.
      Per-Vertex Displacement
         How much the position of each individual vertex influences the final result.
      Iterations
         Number of smoothing iterations per brush step.
