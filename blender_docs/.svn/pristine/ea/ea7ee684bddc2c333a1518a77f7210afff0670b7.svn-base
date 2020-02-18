
******
Remesh
******

.. admonition:: Reference
   :class: refbox

   :Mode:      All Paint Modes
   :Header:    :menuselection:`Tool Settings --> Remesh`
   :Panel:     :menuselection:`Sidebar --> Tool --> Remesh`
   :Hotkey:    :kbd:`Ctrl-R` (Voxel), :kbd:`Ctrl-Alt-R` (Quadriflow)

Remeshing is a technique that automatically rebuilds the geometry with a more uniform topology.
Remeshing can either add or remove the amount of topology depending on a defined resolution.
This technique is especially useful for :doc:`sculpting </sculpt_paint/sculpting/index>`,
to generate better topology after blocking out the initial shape.

The Voxel Remesher uses an OpenVDB to generate a new manifold mesh from the current geometry.
It produces a mesh with perfectly even distributed topology and
it does not have any performance penalty once the new mesh is calculated.
This makes the voxel remesher great for sculpting has it is possible to
sculpt at a much higher level of detail than using other features
like dyntopo which often adds more performance overhead.

Voxel Size
   The resolution or the amount of detail the remeshed mesh will have.
   The value is used to define the size, in object space, of the :term:`Voxel`.
   These voxels are assembled around the mesh and are used to determine the new geometry.
   For example a value of 0.5m will create topological patches that are about 0.5m
   (assuming *Preserve Volume* is enabled).
   Lower values preserve finer details but will result in a mesh with a much more dense topology.

   Sample Voxel Size
      Used to adjust the *Voxel Size* by picking and an area of the mesh
      to match the denseness of polygons after the remesh operation.

Adaptivity
   Todo 2.81.
Fix Poles
   Todo 2.81.
Smooth Normals
   Applies the :ref:`Smooth Normals <bpy.ops.object.shade_smooth>` operator to the resulting mesh.

Preserve Volume
   Todo 2.81.
Preserve Paint Mask
   Todo 2.81.
Voxel Remesh
   Todo 2.81.

.. note::

   Remeshing only works on the original mesh data and
   ignores generated geometry from modifiers, shape keys, rigging, etc.

.. seealso::

   :doc:`Remesh modifier </modeling/modifiers/generate/remesh>`
