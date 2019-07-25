.. _bpy.ops.mesh.noise:

*****
Noise
*****

.. admonition:: Reference
   :class: refbox

   :Mode:      Edit Mode
   :Panel:     :menuselection:`Toolbar --> Tools --> Mesh Tools --> Deform: Noise`

.. note::

   *Noise* is an old feature. The :doc:`Displace Modifier </modeling/modifiers/deform/displace>`
   is a non-destructive alternative to the Noise tool and is a more flexible way to realize these sorts of effects.
   The key advantages of the modifier are that it can be canceled at any moment,
   you can precisely control how much and in which direction the displacement is applied, and much more...

The *Noise* function allows you to displace vertices in a mesh based on the gray
values of the first texture slot of the material applied to the mesh.

The mesh must have a material and a texture assigned to it for this tool to work.
To avoid having the texture affect the material's properties,
it can be disabled in the texture menu.

The *Noise* function displaces vertices along the object's ±Z axis only.

*Noise* permanently modifies your mesh according to the material texture.
Each click adds onto the current mesh.
For a temporal effect, map the texture to Displacement for a render-time effect.
In *Object Mode* or *Edit Mode*, your object will appear normal, but will render deformed.

The deformation can be controlled by modifying the *Mapping* panel and/or
the texture's own panel (e.g. *Clouds*, *Marble*, etc.).

.. list-table::

   * - .. figure:: /images/modeling_meshes_editing_transform_noise_example-before.png
          :width: 320px

          Mesh before noise is added.

     - .. figure:: /images/modeling_meshes_editing_transform_noise_example-after.png
          :width: 320px

          Mesh after noise is added, using basic cloud texture.
