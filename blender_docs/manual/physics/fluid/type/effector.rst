
********
Effector
********

Effector objects are used to deflect fluids and influence of the fluid flow.
To define any mesh object as an effector object,
add fluid physics by clicking *Fluid* in the :menuselection:`Properties --> Physics` tab.
Then select *Effector* as the fluid *Type*.

.. tip::

   :doc:`Force Fields </physics/forces/force_fields/index>`
   (such as wind or vortex) are supported, like in most physics systems.
   The influence individual force types have can be
   :doc:`controlled </physics/fluid/type/domain/field_weights>` per domain object.


.. _bpy.types.FluidEffectorSettings:

Settings
========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Fluid -- Settings`
   :Type:      Effector

Effector Type
   Todo.

   Collision
      Todo.
   Guide
      Todo.

      Velocity Factor
         Todo.
      Guide Mode
         Todo.

         Maximize
            Todo.
         Minimize
            Todo.
         Override
            Todo.
         Averaged
            Todo.

Is Planar
   Defines the effector as either a single dimension object i.e. a plane or the mesh is :term:`non-manifold`.
   This ensures that the fluid simulator will give the most accurate results for these types of meshes.
Surface Thickness
   Todo.
