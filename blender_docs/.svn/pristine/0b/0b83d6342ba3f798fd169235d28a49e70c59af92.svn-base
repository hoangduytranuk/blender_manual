.. the title should be remeshing since retopology (feature based) is a subtype of remeshing.
   remeshing vs. retopology by dev Pablo Dobarro bcon19: https://www.youtube.com/watch?v=lxkyA4Xslzs&t=9m34s

**********
Retopology
**********

Retopology is the process of simplifying the topology of a mesh to make it cleaner and easier to work with.
Retopology is need for mangled topology resulting from sculpting or generated topology, for example from a 3D scan.
Meshes often need to be retopologized if the mesh is going to be deformed in some way.
Deformations can include rigging or physics simulations such as cloth or soft body.
Retopology can be done by hand by manipulating geometry in Edit Mode or through automated methods.


Using the Poly Build Tool
=========================

Todo 2.81.


.. _bpy.types.Mesh.remesh:
.. _bpy.ops.object.voxel_remesh:
.. _bpy.ops.object.quadriflow_remesh:

Remeshing
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      Object Mode, Sculpt Mode
   :Panel:     :menuselection:`Properties --> Object Data --> Remesh`

Remeshing is a technique that automatically rebuilds the geometry with a more uniform topology.
Remeshing can either add or remove the amount of topology depending on a defined resolution.
This technique is especially useful for :doc:`sculpting </sculpt_paint/sculpting/index>`,
to generate better topology after blocking out the initial shape.

.. note:: Limitations:

   - Remeshing only works on the original mesh data and
     ignores generated geometry from modifiers, shape keys, rigging, etc.
   - Remeshing will not work with the :doc:`/modeling/modifiers/generate/multiresolution>`

.. seealso::

   :doc:`Remesh modifier </modeling/modifiers/generate/remesh>`


Voxel
-----

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

Adaptivity
   Reduces the final face count by simplifying geometry where detail is not needed.
   This introduce triangulation to faces that do not require as much detail.
   Note, an *Adaptivity* value greater than zero disables *Fix Poles*.
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


Quad
----

Quadriflow Remesh
   Todo 2.81.
Use Paint Symmetry
   Todo 2.81.
Preserve Sharp
   Todo 2.81.
Preserve Mesh Boundary
   Todo 2.81.
Use Mesh Curvature
   Todo 2.81.
Preserve Paint Mask
   Todo 2.81.
Smooth Normals
   Applies the :ref:`Smooth Normals <bpy.ops.object.shade_smooth>` operator to the resulting mesh.

Modes
   Todo 2.81.
Number of Faces
   Todo 2.81.
