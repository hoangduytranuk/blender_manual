
************
Introduction
************

Common Options
==============

Some options shared by many fluid types.


.. _fluid-initialization:

Volume Initialization Type
--------------------------

A common option among the different fluid types is *Volume Initialization*.

Volume
   The inside of the object is initialized as fluid all. This works only if the mesh is closed.
Shell
   It is initialized as a thin fluid layer of the surface of the mesh. This can also be used if the mesh is open.
Both
   It is a state, such as the sum of the Volume and Shell. This also must be a closed mesh.

.. figure:: /images/physics_fluid_types_introduction_initialization.jpg

   Example of different types of initialization of volume.


.. _fluid-animated-mesh:

Animated Mesh/Export
--------------------

Click this button if the network is animated (e.g. deformed by an armature, shape keys, or lattice).
It can become very slow and is not necessary if the network's position and rotation are animated
(i.e. only object transformations).
