.. _bpy.types.ExplodeModifier:

****************
Explode Modifier
****************

The *Explode* modifier is used to alter the mesh geometry by moving/rotating its faces in a way
that roughly tracks particles emitted by that object, making it look as if the mesh is being exploded
(broken apart and pushed outward).

For this modifier to have any visible effect, there needs to be a particle system on its object.
That particle system will control how the mesh is exploded.

Both the number of emitted particles and number of faces determine how granular the *Explode* modifier is.
More faces and more particles will mean more individual pieces.

.. Broken link to the demo video...
   Here is
   a `demo video <https://wiki.blender.org/uploads/7/7b/Manual_-_Explode_Modifier_-_Exploding_Cube_-_2.5.ogg>`__
   showing a cube with a particle system and *Explode* modifier.
   (`blend-file <https://wiki.blender.org/wiki/File:Manual_-_Explode_Modifier_-_Exploding_Cube_-_2.5.blend>`__).

Here is
a `demo blend-file <https://wiki.blender.org/wiki/File:Manual_-_Explode_Modifier_-_Exploding_Cube_-_2.5.blend>`__
showing a cube with a particle system and *Explode* modifier.

.. note::

   The *Explode* modifier must come after the *Particle System* one in the :ref:`modifier stack <modifier-stack>`,
   in order for the former to get required data from the later.


Options
=======

.. figure:: /images/modeling_modifiers_simulate_explode_panel.png
   :align: right

   The Explode modifier, with a Particle System above it.

Vertex Group
   Vertices in this group may not be affected by the *Explode* modifier.
   Vertices with full weight are not affected at all,
   while vertices with less weight have a higher chance of being affected.

   Vertices with null weight will be treated like those which do not belong to the group at all, and explode normally.

   Protect
      Clean vertex group edges. Depending on the weights assigned to that vertex group,
      either completely protect those faces from being affected by the *Explode* modifier
      (which would happen if the faces had a weight value of 1),
      or completely remove protection from those faces
      (which would happen if the faces had a weight value of 0).

Particle UV
   If set, the U value of the coordinates in that :term:`UV map` will be overwritten
   with the age of the particle attached to the matching mesh face
   (in proportion, from 0 for not yet born particles, to 1 for dead ones).

   The V value is set to a constant 0.5 value.

   This allows e.g. to make the color of a fragment (face) vary during it 'explosion' phase,
   by using a texture with a gradient of colors along its *U* axis.

Cut Edges
   Split the mesh in pieces based on location of emitted particles, instead of using existing faces.
   This will typically give a splitting that appears more random.

Unborn
   Show faces when their attached particles are unborn.
Alive
   Show faces when their attached particles are alive.
Dead
   Show faces when their attached particles are dead.
Size
   Scale each face using the size of its attached particle, once that particle is alive.

Refresh
   Refresh data in the *Explode* modifier.
