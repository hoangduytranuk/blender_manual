
**********************
Fluid Inflow / Outflow
**********************

To control the volume of the fluid simulation,
you can set objects in the scene to add or absorb fluid within the :doc:`Fluid Domain </physics/fluid/types/domain>`.


.. _bpy.types.InflowFluidSettings:

Inflow
======

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid`
   :Type:      Inflow

.. TODO2.8:
   .. figure:: /images/physics_fluid_types_flow_inflow.png

      Fluid Inflow settings.

This object will put fluid into the simulation, like a water tap.

Volume Initialization Type
   See :ref:`Volume Initialization Type <fluid-initialization>`.
Animated Mesh/Export
   See :ref:`Animated Mesh/Export <fluid-animated-mesh>`.
Local Coordinates/Enable
   Use local coordinates for the inflow.
   This is useful if the inflow object is moving or rotating, as the inflow stream will
   follow/copy that motion. If disabled, the inflow location and direction do not change.
Inflow Velocity
   Speed of the fluid that is created inside of the object.


.. _bpy.types.OutflowFluidSettings:

Outflow
=======

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid`
   :Type:      Outflow

.. TODO2.8:
   .. figure:: /images/physics_fluid_types_flow_outflow.png

      Fluid Outflow settings.

Any fluid that enters the region of this object will be deleted (think of a drain or a black hole).
This can be useful in combination with an inflow to prevent the whole domain from filling up.
When enabled, this is like a tornado (waterspout) or "wet vac" vacuum cleaner,
and the part where the fluid disappears will follow the object as it moves around.

Volume Initialization Type
   See :ref:`Volume Initialization Type <fluid-initialization>`.

Animated Mesh/Export
   See :ref:`Animated Mesh/Export <fluid-animated-mesh>`.
