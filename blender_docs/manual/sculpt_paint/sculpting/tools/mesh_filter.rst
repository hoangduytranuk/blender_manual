
***********
Mesh Filter
***********

.. admonition:: Reference
   :class: refbox

   :Mode:      Sculpt Mode
   :Tool:      :menuselection:`Toolbar --> Mesh Filter`

Applies a deformation to all vertices in the mesh at the same time.
To use this tool, click and drag away from the object to have a positive effect
and click and drag towards the mesh to have a negative effect.

Filter Type
   Smooth
      Eliminates irregularities of the mesh by making the positions of the vertices more uniform.
      This filter works similar to the *Smooth Brush*.
   Scale
      Increases the size of the mesh.
      This filter works similar to the :ref:`Scale Transform <bpy.ops.transform.resize>`.
   Inflate
      Displaces vertices uniformly along their normal.
      This filter works similar to the *Inflate Brush*.
   Sphere
      Morphs the mesh progressively into a sphere.
      This filter works similar to the :ref:`To Sphere Transform <bpy.ops.transform.tosphere>`.
   Random
      Randomly moves vertices along the vertex normal.
      This filter works similar to the :ref:`Randomize Transform <bpy.ops.object.randomize_transform>`.
   Relax
      Tries to create an even distribution of quads without deforming the volume of the mesh.
      This filter works the same as the *Relax* mode of the *Slide Relax* brush.
Strength
   The amount of effect the filter has on the mesh.
Deformation Axis
   Apply the deformation only on the selected axis.
