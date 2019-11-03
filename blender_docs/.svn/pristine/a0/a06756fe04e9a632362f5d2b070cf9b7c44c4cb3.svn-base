
************
Introduction
************

:term:`Constraints <Constraint>` (also known as joints) for rigid bodies connect two rigid bodies.

The physics constraints are meant to be attached to an :term:`Empty` object.
The constraint then has fields which can be pointed at the two physics-enabled object
which will be bound by the constraint.
The *Empty* object provides a location and axis for the constraint distinct from the two constrained objects.
The location of the entity hosting the physics constraint marks a location and
set of axes on each of the two constrained objects.
These two anchor points are calculated at the beginning of the animation and their position and
orientation remain fixed in the *local* coordinate system of the object for the duration of the animation.
The objects can move far from the constraint object, but the constraint anchor moves with the object.
If this feature seems limiting, consider using multiple objects with a non-physics *Child of* constraint and
animate the relative location of the child.


Connect
=======

The quickest way to constrain two objects is to select both and
click the *Connect* button in :menuselection:`Object --> Rigid Body`.
This creates a new *Empty* object (named "Constraint") with a physics constraint
already attached and pointing at the two selected objects.


Physics Menu
============

Also you can create *Rigid Body Constraint* on one of the two constrained objects with
*Rigid Body Constraint* button of the *Physics* tab in the Properties editor.
This constraint is dependent on the object location and rotation on which it was created.
This way, there are no *Empty* object created for the constraint.
The role of the *Empty* object is put on this object.
The constrained object can be then set as *Passive* type for better driving the constrain.

Additional parameters appear in the *Rigid Body Constraint* panel of the *Physics* tab in the Properties editor
for the selected *Empty* object or the one of the two constrained objects with the created constraint.


Common Options
==============

Rigid Body Constraint panel.

Enabled
   Specifies whether the constraint is active during the simulation.
Disable Collisions
   Allows constrained objects to pass through one another.
Object 1
   First object to be constrained.
Object 2
   Second object to be constrained.
Breakable
   Allows constraint to break during simulation. Disabled for the *Motor* constraint.
   This can be used to simulate destruction.

   Threshold
      Impulse strength that needs to be reached before constraint breaks.

Override Iterations
   Allows to make constraints stronger (more iterations) or weaker (less iterations)
   than specified in the rigid body world.

   Iterations
      Number of constraint solver iterations made per simulation step for this constraint.

Limits
   By using limits you can constrain objects even more by specifying a translation/rotation range on/around
   respectively one axis (see below for each one individually). To lock one axis, set both limits to 0.
