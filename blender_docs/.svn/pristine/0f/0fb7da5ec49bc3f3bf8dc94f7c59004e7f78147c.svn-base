.. _bpy.types.FluidDomainSettings.noise:

*****
Noise
*****

.. admonition:: Reference
   :class: refbox

   :Type:      Domain
   :Panel:     :menuselection:`Physics --> Smoke --> High Resolution`

Adding noise to the gas simulation creates a finer detailed looking simulation
while using a relatively low *Resolution Divisions*. This allows animators to quickly set up
a low resolution simulation and later add details without changing the overall fluid motion.

.. note::

   Fluid noise is an implementation of
   `Turbulence for Fluid Simulation
   <https://web.archive.org/web/20140911163550/https://graphics.ethz.ch/research/physics_animation_fabrication/simulation/turb.php>`__.


Upres Factor
   Factor by which to enhance the resolution of the noise.
Strength
   Strength of the noise.

   .. figure:: /images/physics_smoke_types_domain_high-resolution-strength.jpg
      :width: 400px

      From left to right, the domains' high resolution strengths are set to 0, 2, and 6.

Scale
   Todo.
Time
   Todo.


Smoke Noise vs. High Resolution Divisions
=========================================

*Upres Factor* and *Resolution Divisions* are not equivalent.
By using different combinations of these resolution settings, you can get a variety of different styles of smoke.

.. figure:: /images/physics_smoke_types_domain_high-resolution-comparison.jpg
   :align: center

   Comparison between a domain with 24 *Resolution Divisions* and 4 *Upres Factor* (left),
   and a domain with 100 *Resolution Divisions* and 1 *Upres Factor* division (right).

Low division simulations with lots of *Upres Factor* divisions generally appear
smaller in real-world scale, with many smaller details (larger flames, etc.).
They can be used to create pyroclastic plumes such as in the following image:

.. figure:: /images/physics_smoke_types_domain_note-on-resolution.jpg
   :align: center
