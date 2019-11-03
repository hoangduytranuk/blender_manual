.. _bpy.types.SmokeCollSettings:

*********
Collision
*********

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Physics --> Smoke`
   :Type:      Collision

*Smoke Collision* objects are used to deflect smoke and influence airflow.

To define any mesh object as a *Smoke Collision* object,
add smoke physics by clicking *Smoke* in :menuselection:`Properties --> Physics`.
Then select *Collision* as the *Smoke Type*.

.. TODO2.8:
   .. figure:: /images/physics_smoke_types_collision_settings.png
      :align: right

      Smoke Collision options.


Options
=======

.. TODO, cannot figure out what the differences between the collision types are :/
.. Wild speculation on SE: https://blender.stackexchange.com/q/1723/599

.. Lukas Toenne investigated this (https://developer.blender.org/T45842#329325) and
   it appears that rigid and static are the same.

Collision type
   Static
      Simple collision model which can be calculated quickly, but may be inaccurate for moving objects.
   Animated
      More complex collision model which takes into account impulse imparted to smoke when the collider is moving.
      Calculations are slower, but more accurate for moving objects.
   Rigid
      Identical to *Static* (unfinished code).


Forces
======

:doc:`Force Fields </physics/forces/force_fields/index>`
(such as wind or vortex) are supported, like most physics systems.
The influence individual force types have can be :ref:`controlled <smoke-field-weights>` per domain object.
