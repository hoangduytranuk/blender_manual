
************
Introduction
************

The rigid body simulation can be used to simulate the motion of solid objects.
It affects the position and orientation of objects and does not deform them.

Unlike the other simulations in Blender, the rigid body simulation works closer with the animation system.
This means that rigid bodies can be used like regular objects and be part of parent-child relationships,
animation constraints and drivers.


Creating a Rigid Body
=====================

Right now only mesh objects can participate in the rigid body simulation.
To create rigid bodies, either click on *Rigid Body* button in the *Physics* tab of
the Properties editor or use the *Add Active*/*Add Passive* buttons in the *Physics* tab of the *Toolbar*.

There are two types of rigid body: active and passive. *Active* bodies are dynamically simulated, while *passive*
bodies remain static. Both types can be driven by the animation system when using the *Animated* option.

During the simulation,
the rigid body system will override the position and orientation of dynamic rigid body objects.
Note however, that the location and rotation of the objects are not changed,
so the rigid body simulation acts similar to a constraint.
To apply the rigid body transformations you can use
the *Apply Object Transform* operator.

The scale of the rigid body object also influences the simulation, but is always controlled by the animation system.

Rigid body physics on the object can be *removed* with the *Rigid Body* button
in the *Physics* tab in the Properties editor or in the :menuselection:`Object --> Rigid Body` menu.
