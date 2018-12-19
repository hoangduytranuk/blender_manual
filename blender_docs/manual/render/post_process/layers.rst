.. _bpy.types.RenderLayer:

*************
Render Layers
*************

Render layers allow you to render your scene in separate layers,
usually with the intension of compositing them back together afterwards.

This can be useful for several purposes, such as color correcting certain elements differently,
blurring the foreground as a fast manual method of creating DoF,
or reducing the render quality for unimportant objects.

Using Render Layers can also save you from having to re-render your entire image each time you change something,
allowing you to instead re-render only the layer(s) that you need.


Layer List
==========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Scene --> Scene`

.. figure:: /images/render_post-process_layers_list.png

   Layer list.

This is a list of all the Render Layers in the current scene.

Only layers which are enabled (checkbox on right is ticked) will be rendered.
If the pin icon at the bottom right of the list is enabled, only the active (highlighted) layer will be rendered.

Render Layers can be added and removed using the ``+`` and ``-`` buttons on the right,
and existing layers can be renamed by double-clicking on their name.


Layer Panel
===========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Scene --> Layer`

.. figure:: /images/render_post-process_layers_panel.png

   Layer panel.

The Layer Panel shows the settings of the active Render Layer from the list above.

You can select multiple layers using :kbd:`Shift-LMB`.

Scene
   The Scene Layers, showing which are currently visible and will be rendered.
Layer
   The Scene Layers which are associated with the active Render Layer.
   Objects in those Scene Layers will be rendered in that Render Layer.
   When an object is in the Scene Layers but not the Render Layer,
   it will still cast shadows and be visible in reflections, so it is still indirectly visible.
Mask Layer
   Objects on these will mask out other objects appearing behind them.
   This can be used for compositing objects into footage,
   to take into account objects in front of the virtual objects blocking the view from the camera.
Material Override
   Overrides all material settings to use the Material chosen here.

   Examples of where this might be used:

   - To check lighting by using a plain diffuse material on all objects.
   - Render a wireframe of the scene.
   - Create a custom render pass such as an anti-aliased matte or global coordinates.

.. seealso::

   Additional options shown in this panel are different for each render engine. See these options for:

   - :doc:`Cycles </render/cycles/settings/scene/render_layers/passes>`


Usage
=====

Each Render Layer has an associated set of :doc:`Scene Layers </editors/3dview/object/properties/relations/layers>`.
Objects which are on one of the associated Scene Layers are shown in that Render Layer,
as long as that Scene Layer is also visible.

.. warning::

   Only the objects in visible Scene Layers will be rendered.
   So, if only Scene Layer 1 is visible and your Render Layer set specifies to render only Layers 2 and 3,
   nothing will be rendered.
