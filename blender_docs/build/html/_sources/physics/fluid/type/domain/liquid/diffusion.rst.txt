.. |m2.s-1| replace:: m\ :sup:`2`.s\ :sup:`-1`
.. |kg.m-3| replace:: kg.m\ :sup:`-3`

.. _bpy.ops.fluid.preset:

*********
Diffusion
*********

.. admonition:: Reference
   :class: refbox

   :Type:      Domain
   :Panel:     :menuselection:`Physics --> Fluid --> Viscosity`

Viscosity (todo).

Viscosity Presets
   The viscosity refers to the "thickness" of the fluid and actually the force needed to
   move an object of a certain surface area through it at a certain speed.

   For manual entry, please note that the normal real-world viscosity
   (the so-called dynamic viscosity) is measured in Pascal-seconds (Pa.s),
   or in Poise units (P, equal to 0.1 Pa.s), and commonly centiPoise units (cP, equal to 0.001 Pa.s).

   Blender, on the other hand, uses the kinematic viscosity which is dynamic viscosity in Pa.s,
   divided by the density in |kg.m-3|, unit |m2.s-1|.

   The table below gives some examples of fluids together with their dynamic and kinematic viscosities.

   .. list-table::
      Blender viscosity unit conversion.
      :header-rows: 1

      * - Fluid
        - Dynamic viscosity (in cP)
        - Kinematic viscosity (Blender, in |m2.s-1|)
      * - Water (20 °C)
        - 1.002×10\ :sup:`0` (1.002)
        - 1.002×10\ :sup:`-6` (0.000001002)
      * - Oil SAE 50
        - 5.0×10\ :sup:`2` (500)
        - 5.0×10\ :sup:`-5` (0.00005)
      * - Honey (20 °C)
        - 1.0×10\ :sup:`4` (10,000)
        - 2.0×10\ :sup:`-3` (0.002)
      * - Chocolate Syrup
        - 3.0×10\ :sup:`4` (30,000)
        - 3.0×10\ :sup:`-3` (0.003)
      * - Ketchup
        - 1.0×10\ :sup:`5` (100,000)
        - 1.0×10\ :sup:`-1` (0.1)
      * - Melting Glass
        - 1.0×10\ :sup:`15`
        - 1.0×10\ :sup:`0` (1.0)

   Manual entries are specified by a floating point number and an exponent. These floating point and
   exponent entry fields (scientific notation) simplify entering very small or large numbers.

   The viscosity of water at room temperature is 1.002 cP, or 0.001002 Pa.s; the density of water is
   about 1000 |kg.m-3|, which gives a kinematic viscosity of 0.000001002 |m2.s-1| --
   so the entry would be 1.002 times 10 to the minus six (1.002×10\ :sup:`-6` in scientific notation).

   Hot glass and melting iron are fluids, but very thick; you should enter something like
   1.0×10\ :sup:`0` (= 1.0) as its kinematic viscosity (indicating a value of 1.0×10\ :sup:`6`\ cP).

   Note that the simulator is not suitable for non-fluids, such as materials that do not "flow".
   Simply setting the viscosity to very large values will not result in rigid body behavior,
   but might cause instabilities.

   .. note:: Viscosity Varies

      The default values in Blender are considered typical for those types of fluids and "look right" when animated.
      However, actual viscosity of some fluids,
      especially sugar-laden fluids like chocolate syrup and honey, depend highly on temperature and concentration.
      Oil viscosity varies by :abbr:`SAE (Society of Automobile Engineers)` rating.
      Glass at room temperature is basically a solid, but glass at 1500 °C flows (nearly) like water.

.. _bpy.types.FluidDomainSettings.viscosity_base:

Base
   The base of the viscosity value (e.g. 1.002 in the case of water (20 °C)).

.. _bpy.types.FluidDomainSettings.viscosity_exponent:

Exponent
   The exponent of the viscosity value that will be multiplied by 10\ :sup:`-6`
   (e.g. 6 in the case of water (20 °C)).

.. _bpy.types.FluidDomainSettings.domain_size:

Real World Size
   Size of the domain object in the real world in meters. If you want to create a mug of coffee,
   this might be 10 cm (0.1 meters), while a swimming pool might be 10 m. The size set here defines
   the longest side of the domain bounding box.

.. _bpy.types.FluidDomainSettings.surface_tension:

Surface Tension
   Surface tension in grid units. Higher value will produce liquids with greater surface tension.
