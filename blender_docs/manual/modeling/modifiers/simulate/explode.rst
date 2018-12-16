.. _bpy.types.ExplodeModifier:

****************
Explode Modifier
****************

The Explode Modifier is used to alter the mesh geometry by moving/rotating its faces in a way that roughly
tracks particles emitted by that object, making it look as if the mesh is being exploded
(broken apart and pushed outward).

For the Explode Modifier to have a visible effect, there needs to be particle system on it.
The particle system on the mesh is what controls how the mesh will be exploded,
and therefore without the particle system the mesh will not appear to alter.

Both the number of emitted particles and number of faces determine how granular the Explode Modifier will be.
More faces and more particles will mean more individual pieces.

Here is
a `demo video <https://wiki.blender.org/uploads/7/7b/Manual_-_Explode_Modifier_-_Exploding_Cube_-_2.5.ogg>`__
showing a cube with a particle system and Explode Modifier.
(`Blend-file <https://wiki.blender.org/wiki/File:Manual_-_Explode_Modifier_-_Exploding_Cube_-_2.5.blend>`__).

.. note::

   The Explode Modifier must come after the Particle System Modifier
   because the Particle System Modifier has the information needed to drive the Explode Modifier.


Options
=======

.. figure:: /images/modeling_modifiers_simulate_explode_panel.png

   Explode Modifier panel with Particle System Modifier above it.

Vertex group
   Vertices in this group may not be affected by the Explode Modifier.
   Vertices with full weight are not affected at all,
   while vertices with less weight have a higher chance of being affected.

   Vertices with no weight will be treated like those which do not belong to the group at all and explode normally.

Protect
   Clean vertex group edges. Depending on the weights assigned to that vertex group;
   either completely protect those faces from being affected by the Explode Modifier
   (which would happen if the faces had a weight value of 1) or completely remove protection from those faces
   (which would happen if the faces had a weight value 0).

Particle UV
   UV map to change with particle age.

Cut Edges
   Cut face edges for nicer shrapnel.

Unborn
   Show mesh when particles are unborn.
Alive
   Show mesh when particles are alive.
Dead
   Show mesh when particles are dead.
Size
   Use particle size for shrapnel.

Refresh
   Refresh data in the Explode Modifier.
