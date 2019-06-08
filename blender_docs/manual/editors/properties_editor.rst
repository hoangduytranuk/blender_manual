.. _bpy.types.SpaceProperties:

*****************
Properties Editor
*****************

.. figure:: /images/editors_properties-editor_top.png
   :align: right

   Properties editor top part.

The *Properties Editor* is used to edit data and properties for the *Active Scene* and the *Active Object*.


Tabs
====

The Properties editor shows several tabs,
which can be chosen via the icon row in the header.
The tabs are documented in their own manual sections,
the links are listed below.


Scene/Render
------------

These tabs are used to add features, and to change properties for the Active Scene.

.. figure:: /images/editors_properties-editor_render.png
   :align: right

   Scene/Render tabs.

.. _properties-render-tab:

- :doc:`Render </render/output/index>` and Settings:
  :doc:`Eevee </render/engines/eevee/index>`, :doc:`Cycles </render/engines/cycles/settings/index>`
- :doc:`/render/layers/index`
- :doc:`Scene </scene_layout/scene/properties>`
- World: :doc:`Eevee </render/engines/eevee/world>`, :doc:`Cycles </render/engines/cycles/world>`


.. _properties-data-tabs:

Object & Object Data
--------------------

These tabs are used to add features, and to change properties for the Active Object
(and other active elements, material, curve, etc.).

.. figure:: /images/editors_properties-editor_object.png
   :align: right

   Object Data tabs.

The Object Data tabs shown depend on what type of object was selected last (the Active Object).

- :doc:`Object </scene_layout/object/properties/index>`
- :doc:`/animation/constraints/index`
- :doc:`/modeling/modifiers/index`

..

- :doc:`Mesh </modeling/meshes/properties/object_data>`
- :doc:`Curve </modeling/curves/properties/index>`
- :doc:`Surface </modeling/surfaces/properties>`
- :doc:`Metaball </modeling/metas/properties>`
- :doc:`Text </modeling/texts/properties>`
- :doc:`Empty </modeling/empties>`

..

- :doc:`Armature </animation/armatures/properties/index>`
- :doc:`Bones </animation/armatures/bones/properties/index>`
- :doc:`Bone Constraints </animation/armatures/posing/bone_constraints/introduction>`
- :doc:`Lattice </animation/lattice>`

..

- :doc:`Speaker </render/output/audio/speaker>`
- Camera: :doc:`Cycles </render/camera>`
- Lamp: :doc:`General settings </render/lighting/lamp_panel>`,
  :doc:`Cycles </render/engines/cycles/lighting>`

..

- Material: :doc:`Eevee </render/engines/eevee/materials/settings>`,
  :doc:`Cycles </render/engines/cycles/materials/index>`
- Texture: :doc:`Texture Nodes </editors/uv/textures/index>`,
  :doc:`Cycles </render/engines/cycles/materials/texture_editing>`
- :doc:`Particles </physics/particles/index>`
- :doc:`Physics </physics/index>`


.. (todo add) Generic Object Data page?


Main View
=========

.. figure:: /images/editors_properties-editor_interface.png

   The Properties Editor with the Mesh tab selected.

At the top of the each tab a list of icons explains the context in which the properties are being edited.
In the example above, the mesh *Cube* is linked to the object *Cube* which is linked to the scene *Scene*.

.. This is a branch of the scene graph?

By toggling the pin symbol on the left side on and off,
Blender can be told to display only the selected property or to follow context.
