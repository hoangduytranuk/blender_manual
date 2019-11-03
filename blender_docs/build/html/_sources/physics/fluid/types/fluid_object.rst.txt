.. _bpy.types.FluidFluidSettings:

************
Fluid Object
************

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid`
   :Type:      Fluid

.. TODO2.8:
   .. figure:: /images/physics_fluid_types_fluid-object_fluid-panel.png

      Fluid object settings.

All regions of this object that are inside the domain bounding box will be used as
actual fluid in the simulation. If you place more than one fluid object inside the domain,
they should currently not intersect. Also make sure the surface normals are pointing outwards.
In contrast to domain objects, the actual mesh geometry is used for fluid objects.


Settings
========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid --> Settings`
   :Type:      Fluid

Volume Initialization Type
   See :ref:`Volume Initialization Type <fluid-initialization>`.

Animated Mesh/Export
   See :ref:`Animated Mesh/Export <fluid-animated-mesh>`.

Initial velocity
   Speed of the fluid at the beginning of the simulation, in meters per second.

.. tip:: The direction of Surface Normals makes a big difference!

   Blender uses the orientation of the Surface Normals to determine what is "inside of" the Fluid object and
   what is "outside". You want all of the normals to face *outside* (in *Edit Mode*, use :kbd:`Shift-N` or
   press :kbd:`F3` and choose :menuselection:`Mesh --> Normals --> Calculate Outside`).
   If the normals face the wrong way, you will be rewarded with a "gigantic flood of water",
   because Blender will think that the volume of the object is outside of its mesh!
   This applies regardless of the *Volume initialization* type setting.
