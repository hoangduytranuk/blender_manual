
************
Introduction
************

.. figure:: /images/modeling_meshes_properties_vertex-groups_introduction_panel.png
   :align: right

   The Vertex Group panel.

Vertex Groups are mainly used to tag the vertices belonging
to parts of a Mesh Object or :term:`Lattice`. Think of the legs of a chair or
the hinges of a door, or hands, arms, limbs, head, feet, etc. of a character.
In addition you can assign different *weight values*
(in the range [ 0.0, 1.0 ] ) to the vertices within a Vertex Group.
Hence Vertex Groups are sometimes also named *Weight Groups*.


Usage
=====

Vertex Groups are most commonly used for Armatures.
But they are also used in many other areas of Blender, like for example:

- Armature Deformation *(also called Skinning)*
- Shape keys
- Modifiers
- Particle Generators
- Physics Simulations

.. seealso::

   :doc:`Skinning Mesh Objects </animation/armatures/skinning/introduction>`.

Many more usage scenarios are possible.
Actually you can use *Vertex Groups* for whatever makes sense to you.
In some contexts Vertex Groups can also be automatically generated
(e.g. for rigged objects). However, in this section we will focus
on manually created (user-defined) Vertex Groups.

.. note::

   Vertex groups only apply to Mesh and Lattice Objects.
