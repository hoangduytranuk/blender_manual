
************
Introduction
************

Smoke simulation is a subset of the fluids system, and can be used for simulating collections
of airborne solids, liquid particulates and gases, such as those that make up smoke.
It simulates the fluid movement of air and generates animated :term:`voxel`
textures representing the density, heat, and velocity of other fluids or suspended particles
(e.g. smoke) which can be used for rendering.

.. figure:: /images/physics_smoke_types_domain_note-on-resolution.jpg

   Example of smoke simulation.

Smoke and fire are emitted into a :doc:`Domain </physics/smoke/types/domain>`
from a mesh object or particle system. Smoke movement is controlled by airflow inside the domain,
which can be influenced by :doc:`smoke collision objects </physics/smoke/types/collision>`.
Smoke will also be affected by the scene's gravity and :doc:`force fields </physics/forces/force_fields/index>`.
Airflow inside the domain can affect other physics simulations via the *Smoke Flow* force field.


Workflow
========

At least a :doc:`Domain </physics/smoke/types/domain>` object and
one :doc:`Flow object </physics/smoke/types/flow_object>` are required to create a smoke simulation.
A basic workflow looks like this:

#. Create a :doc:`Domain Object </physics/smoke/types/domain>`
   that defines the bounds of the simulation volume.
#. Define a :doc:`Flow object </physics/smoke/types/flow_object>`
   or objects which will emit smoke and fire.
#. Set :doc:`Collision objects </physics/smoke/types/collision>`
   to make the smoke interact with objects in the scene.
#. Assign a :doc:`Volumetric material </physics/smoke/material>`
   to the domain object.
#. Save the blend-file.
#. :doc:`Bake </physics/smoke/baking>`
   the simulation.

.. note::

   There is a *Quick Smoke* operator which will automatically create
   a domain object with a basic smoke/fire material.
   It can be found in :menuselection:`3D View --> Object --> Quick Effects --> Quick Smoke`,
   or with the operator search menu :kbd:`F3`.

.. note::

   Blender's smoke simulation is based on the paper
   `Wavelet Turbulence for Fluid Simulation <https://www.cs.cornell.edu/~tedkim/wturb/>`__
   and associated sample code.
