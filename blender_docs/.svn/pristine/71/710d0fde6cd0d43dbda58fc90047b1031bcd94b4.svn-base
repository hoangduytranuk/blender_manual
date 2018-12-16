
************
Introduction
************

Modifiers are automatic operations that affect an object in a non-destructive way. With modifiers,
you can perform many effects automatically that would otherwise be too tedious to do manually
(such as subdivision surfaces) and without affecting the base geometry of your object.

They work by changing how an object is displayed and rendered, but not the geometry which you can edit directly.
You can add several modifiers to a single object to form `The Modifier Stack`_
and *Apply* a modifier if you wish to make its changes permanent.

.. figure:: /images/modeling_modifiers_introduction_menu.png

   Modifiers menu.

There are four types of modifiers:

Modify
   The *Modify* group of modifiers includes tools similar to the *Deform Modifiers* (see below),
   but which do not directly affect the shape of the object;
   rather they affect some other data, such as vertex groups.
Generate
   The *Generate* group of modifiers includes constructive tools that either change
   the general appearance of or automatically add new geometry to an object.
Deform
   The *Deform* group of modifiers only changes the shape of an object without adding new geometry,
   and are available for meshes, and often texts, curves, surfaces and/or lattices.
Simulate
   The *Simulate* group of modifiers activates simulations. In most cases, these
   modifiers are automatically added to the modifiers stack whenever a *Particle System*
   or *Physics* simulation is enabled. Their only role is to define
   the place in the modifier stack used as base data by the tool they represent.
   Generally, the attributes of these modifiers are accessible in separate panels.


.. _bpy.types.Modifier.show:

Interface
=========

.. _fig-modifiers-panel-layout:

.. figure:: /images/modeling_modifiers_introduction_panel-layout.png

   Panel layout (Subdivision Surface as an example).

Each modifier has been brought in from a different part of Blender,
so each has its own unique settings and special considerations. However,
each modifier's interface has the same basic components, see Fig. :ref:`fig-modifiers-panel-layout`.

At the top is the *panel header*.
The icons each represent different settings for the modifier (left to right):

Expand (down/right arrow icon)
   Collapse modifier to show only the header and not its options.
Type
   An icon as a quick visual reference of the modifier's type.
Name
   Every modifier has a unique name per object. Two modifiers on one object must have unique names,
   but two modifiers on different objects can have the same name. The default name is based off the modifier type.
Render (camera icon)
   Toggles visibility of the modifier's effect in the render.
Show in viewport (eye icon)
   Toggles visibility of the modifier's effect in the 3D View.
Show in Edit Mode (box icon)
   Displays the modified geometry in Edit Mode, as well as the original geometry which you can edit.
Show on cage (triangle icon)
   When enabled, the final modified geometry will be shown in Edit Mode and can be edited directly.
Move (up/down arrow icon)
   Moves modifier up/down in the stack.
Delete ``X``
   Deletes the modifier.

.. note::

   The *Box* and *Triangle* icons may not be available depending on the type of modifier.

Below the header are two buttons:

Apply
   Makes the modifier "real" -- converts the object's geometry to match the applied modifier,
   and deletes the modifier.
Copy
   Creates a duplicate of the modifier at the bottom of the stack.

.. warning::

   Applying a modifier that is not first in the stack will ignore the stack order and
   could produce undesired results.

Below this header, all of the options unique to each modifier will be displayed.


.. _modifier-stack:

The Modifier Stack
------------------

Modifiers are a series of non-destructive operations which can be applied on top of an object's geometry.
They can be applied in just about any order the users chooses.

This kind of functionality is often referred to as a "modifier stack"
and is also found in several other 3D applications.

In a modifier stack the order in which modifiers are applied has an effect on the result.
Fortunately modifiers can be rearranged easily by clicking the convenient up and down arrow icons.
For example, the image below shows :doc:`Subdivision Surface </modeling/modifiers/generate/subsurf>`
and :doc:`Mirror </modeling/modifiers/generate/mirror>` modifiers that have switched places.

.. list-table:: Modifier Stack example.

   * - .. figure:: /images/modeling_modifiers_generate_mirror_subsurf2.png
          :width: 320px

          The Mirror modifier is the last item in the stack and
          the result looks like two surfaces.

     - .. figure:: /images/modeling_modifiers_generate_mirror_subsurf1.png
          :width: 320px

          The Subdivision surface modifier is the last
          item in the stack and the result is a single merged surface.

Modifiers are calculated from top to bottom in the stack.
In this example, the desired result (on right) is achieved by first mirroring the object,
and then calculating the subdivision surface.


Example
^^^^^^^

.. figure:: /images/modeling_modifiers_introduction_stack-example-3.png

   In this example a simple subdivided cube has been transformed into a rather complex object using
   a stack of modifiers.

`Download example file <https://wiki.blender.org/wiki/File:25-Manual-Modifiers-example.blend>`__.
