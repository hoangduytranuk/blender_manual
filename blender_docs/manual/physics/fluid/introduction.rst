
************
Introduction
************

Fluid physics are used to simulate physical properties of liquids especially water.
While creating a scene in Blender, certain objects can be marked to participate in the fluid simulation.
These can include but not limited to, being a fluid or as an obstacle.
For a fluid simulation you have to have a domain to define the space that the simulation takes up.
In the domain settings you will be able to define the global simulation parameters (such as viscosity and gravity).

.. figure:: /images/physics_fluid_introduction_example.jpg

   Example of a fluid simulation.


Workflow
========

In general, you follow these steps:

#. First you want to set
   the :doc:`simulation domain </physics/fluid/types/domain>`,
#. Next set
   the :doc:`fluid source(s) </physics/fluid/types/fluid_object>`, and specify there physical properties.
#. In some cases you may want to set other objects to
   :doc:`Control the Flow </physics/fluid/types/flow>` of the fluid.
#. You can also depending on your scene add other objects related to the fluid, like:
   :doc:`Obstacles </physics/fluid/types/obstacle>`,
   :doc:`Particles </physics/fluid/types/particle>` floating on the fluid.
#. And lastly you must
   :doc:`Bake the Simulation </physics/fluid/types/domain>`.

.. tip:: Baking is done on the Domain object!

   When you calculate the fluid simulation, you bake the simulation on the domain object.

   For this reason:

   - All the baking options are visible only when selecting the Domain Object,
   - Baking options are explained in the :ref:`the baking section <fluid-baking>` of the Domain manual page.

.. seealso::

   To know more about simulating fluids in Blender you can read
   the :doc:`fluids appendix </physics/fluid/appendix>`.
   There you can find the limitations and workarounds, and some additional links.
