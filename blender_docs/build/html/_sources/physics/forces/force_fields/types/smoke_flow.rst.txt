
**********
Smoke Flow
**********

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Force Fields`
   :Type:      Smoke Flow

The *Smoke Flow* force field creates a force based on a :doc:`Smoke simulation </physics/smoke/index>` air flow.

It applies the smoke simulation air flow velocity as a force to other simulations that use force fields.
To use it you need to add a *Smoke Flow* force field and select a domain object for it.

For example fire sparkles could realistically flow along the air turbulence near the simulated fire.


Options
=======

.. TODO2.8:
   .. figure:: /images/physics_forces_force-fields_types_smoke-flow_panel.png

      UI for a Smoke Flow force field.

Domain Object
   An object that is used as a domain for the smoke simulation.
Apply Density
   Adjust the force strength based on the smoke density.
