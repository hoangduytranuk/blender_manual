.. _bpy.types.HookGpencilModifier:

*************
Hook Modifier
*************

The *Hook* Modifier is used to deform stroke points using another object
(usually an empty or a bone but it can be any object).

As the hook moves, it pulls points from the strokes with it.
You can think of it as animated
:doc:`Proportional Editing </scene_layout/object/editing/transform/control/proportional_edit>`.


Options
=======

.. figure:: /images/grease-pencil_modifiers_deform_hook_panel.png
   :align: right

   The Hook modifier.

Object
   The name of the object to hook points to.

Radius
   The size of the hooks influence.
Strength
   Adjust this hooks influence on the stroke points, were (0.0 to 1.0) (no change to fully follow the hook).


Falloff
-------

Falloff Type
   This can be used to adjust the kind of curve that the hook has on the stroke points.
   You can also define a custom curve to get a much higher level of control.

Uniform Falloff
   This setting is useful when using hooks on scaled objects,
   especially in cases where non-uniform scale would stretch the result of the hook.


Influence Filters
-----------------

See :ref:`grease-pencil-modifier-influence-filters`.

.. note::

   The Hook Modifier stores points indices from the original strokes to determine what to affect;
   this means that modifiers that generate geometry, like a Subdivision Surface Modifier,
   should always be applied **after** the Hook Modifier;
   otherwise the generated geometry will be left out of the hook's influence.


Example
-------

.. figure:: /images/grease-pencil_modifiers_deform_hook_sample.png

   Empty used as Hook to manipulate a vertex group (right eye of the monkey).
