.. _bpy.types.ClothSettings:

********
Settings
********

Cloth
=====

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Cloth`

Presets
   Contains a number of :ref:`preset <ui-presets>` cloth examples.
Quality
   Set the number of simulation steps per frame. Higher values result in better quality, but is slower.
Speed
   Adjust how fast time flows in the cloth simulation.


Material
--------

Mass
   The mass of the cloth material.
Structural
   Overall stiffness of the cloth.
Bending
   Wrinkle coefficient. Higher creates more large folds.


Damping
-------

Spring
   Damping of cloth velocity. Higher values give a more smooth result (less jiggling).
Air
   Air normally has some thickness which slows falling things down.
Velocity
   Damps the velocity to help the cloth reach the final resting position faster.


Pinning
-------

The first thing you need when pinning cloth is
a :doc:`Vertex Group </modeling/meshes/properties/vertex_groups/index>`.
There are several ways of doing this including using the Weight Paint tool to paint the areas you want to pin
(see the :doc:`/sculpt_paint/painting/weight_paint/index` section of the manual).
The weight of each vertex in the group controls how strongly it is pinned.

.. figure:: /images/physics_cloth_settings_cloth-settings_pinning.png

   Cloth pinning.

Once you have a vertex group set, things are pretty straightforward; all you have to do is
press the *Pinning* button in the *Cloth* panel and select which
vertex group you want to use, and the stiffness you want it at.

Stiffness
   Target position stiffness. You can leave the stiffness as it is; the default value of 1 is fine.


Pinning Clothing to an Armature
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Clothing can be simulated and pinned to an armature.
For example, a character could have a baggy tunic pinned to the character's waist with a belt.

The typical workflow for pinning:

#. Set the armature to its bind pose.
#. Model clothing that encloses but does not penetrate the character's mesh.
#. Parent the clothing objects to the armature. The armature will now have several child meshes bound to it.
#. Create a new vertex group on each cloth object for its pinned vertices.
#. Add vertices to be pinned to this vertex group and give these vertices non-zero weights
   (you probably want weight = 1).
   For example the belt area of the tunic would be in the vertex group and have weight one.
#. Designate the clothing objects as "cloth" in the Physics tab of the Properties editor.
   Make sure the Cloth Modifier is below the Armature Modifier in the modifier stack.
#. Press the *Pinning of Cloth* button in the *Cloth* panel and select the vertex group.
#. Designate the character's mesh as "collision" object in the Physics tab of the Properties editor.
#. The clothing is now ready. Non-pinned vertices will be under control of the Cloth modifier.
   Pinned vertices will be under control of the Armature modifier.

.. note::

   When animating or posing the character you must begin from the bind pose.
   Move the character to its initial pose over several frames so the physics engine can simulate the clothing moving.
   Very fast movements and teleport jumps can break the physics simulation.

.. Note that if you move the cloth object ''after'' you have already run some simulations,
   you must unprotect and clear the cache; otherwise, Blender will use the position of
   the current/cached mesh's vertices when trying to represent where they are.
   Editing the shape of the mesh, after simulation, is also discussed below.
   You may disable the cloth and edit the mesh as a normal mesh editing process.
   This is jumping ahead and not clear and not true at this point.
   --[[User:Roger|Roger]] 18:42, 27 April 2008 (UTC)

   Finally, use the Timeline editor Play button,
   or press :kbd:`Alt-A` in the 3D View to run the simulation.
   Your cloth will fall and interact with Deflection objects as it would in the real world.

.. This is jumping ahead and not clear and not true at this point.
   --[[User:Roger|Roger]] 18:42, 27 April 2008 (UTC)


Dynamic Mesh
------------

Dynamic Mesh allows animating the rest shape of cloth using shape keys or
modifiers (e.g. an Armature modifier or any deformation modifier) placed above the Cloth modifier.
When it is enabled, the rest shape is recalculated every frame, allowing unpinned
cloth to squash and stretch following the character with the help of shape keys or modifiers, but
otherwise move freely under control of the physics simulation.

Normally cloth uses the state of the object in the first frame to compute the natural rest
shape of the cloth, and keeps that constant throughout the simulation. This is reasonable
for fully realistic scenes, but does not quite work for clothing on cartoon style characters
that use a lot of squash and stretch.


Cloth Stiffness Scaling
=======================

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Cloth Stiffness Scaling`

Structural Stiffness
   Defines a vertex group to control over structural stiffness.
Maximum
   Maximum structural stiffness value.

Bending Stiffness
   Defines a vertex group to control over bending stiffness.
Maximum
   Maximum structural bending value.


Cloth Sewing Springs
====================

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Cloth Sewing Springs`

Another method of restraining cloth similar to pinning is sewing springs.
Sewing springs are virtual springs that pull vertices in one part of
a cloth mesh toward vertices in another part of the cloth mesh.
This is different from pinning which binds vertices of the cloth mesh in place or to another object.
A clasp on a cloak could be created with a sewing spring.
The spring could pull two corners of a cloak about a character's neck.
This could result in a more realistic simulation than pinning the cloak to
the character's neck since the cloak would be free to slide about the character's neck and shoulders.

Sewing springs are created by adding extra edges to a cloth mesh that are not included in any faces.
They should connect vertices in the mesh that should be pulled together.
For example the corners of a cloak.

To activate the springs, enable the *Cloth Sewing Springs* panel.


Options
-------

Sewing Force
   Maximum force that can be applied by sewing springs. Zero means unbounded, but it is not
   recommended to leave the field at zero in most cases, as it can cause instability due to
   extreme forces in the initial frames where the ends of the sewing springs are far apart.


Shrinking
^^^^^^^^^

The *Cloth Sewing Springs* panel also contains controls for shrinking the actual cloth faces.

Shrinking Group
   Vertex group that is used to vary the intensity of the shrinking effect over the cloth.

Min
   Fraction of the size to shrink the cloth by around vertices with weight 0 (or those not in vertex group).
   The value 0.01 means shrink by 1% etc.
Max
   Fraction of the size to shrink the cloth by around vertices with weight 1.

Like unbounded sewing forces, immediately applying a large amount of shrink can cause
instability, so it is advisable to keyframe these fields and ease in from 0 during draping.


Cloth Field Weights
===================

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Cloth Field Weights`

As other physics dynamics systems, Cloth simulation is also influenced by external force effectors.
