
************
Introduction
************

Rigging is a general term used for adding controls to objects,
typically for the purpose of animation.

Rigging often involves using one or more of the following features:

:ref:`Armatures <armatures-index>`
   This allows mesh objects to have flexible joints and is often used for skeletal animation.
:ref:`Constraints <constraints-index>`
   To control the kinds of motions that make sense and add functionality to the rig.
:ref:`Object Modifiers <modifiers-index>`
   Mesh deformation can be quite involved, there are multiple modifiers that help control this.
:ref:`Shape Keys <animation-shape_keys-index>`
   To support different target shapes *(such as facial expressions)* to be controlled.
:ref:`Drivers <animation-drivers-index>`
   So your rig can control many different values at once,
   as well as making some properties automatically update based on changes elsewhere.

Rigging can be as advanced as your project requires,
rigs are effectively defining own user interface for the animator to use,
without having to be concerned the underlying mechanisms.

.. TODO nice images of rigged objects.


Examples
========

- An armature is often used with a modifier to deform a mesh for character animation.
- A camera rig can be used instead of animating the camera object directly to simulate real-world camera rigs
  *(with a boom arm, mounted on a rotating pedestal for example, effects such as camera jitter can be added too).*

.. TODO more examples?

.. seealso::

   The content of this chapter is simply a reference to how rigging is accomplished in Blender.
   It should be paired with additional resources such as Nathan Vegdahl's excellent (and free!)
   introduction to the fundamental concepts of character rigging,
   `Humane Rigging <https://www.youtube.com/playlist?list=PL3wFcRXImVPOQpi-wi7uriXBkykXVUntv>`__.
