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
  :doc:`Blender Internal </render/blender_render/settings/index>`, :doc:`Cycles </render/cycles/settings/index>`
- :doc:`/render/post_process/layers`
- :doc:`Scene </data_system/scenes/properties>`
- World: :doc:`Blender Internal </render/blender_render/world/index>`, :doc:`Cycles </render/cycles/world>`


.. _properties-data-tabs:

Object & Object Data
--------------------

These tabs are used to add features, and to change properties for the Active Object
(and other active elements, material, curve, etc.).

.. figure:: /images/editors_properties-editor_object.png
   :align: right

   Object Data tabs.

The Object Data tabs shown depend on what type of object was selected last (the Active Object).

- :doc:`Object </editors/3dview/object/properties/index>`
- :doc:`/rigging/constraints/index`
- :doc:`/modeling/modifiers/index`

..

- :doc:`Mesh </modeling/meshes/properties/object_data>`
- :doc:`Curve </modeling/curves/properties/index>`
- :doc:`Surface </modeling/surfaces/properties>`
- :doc:`Metaball </modeling/metas/properties>`
- :doc:`Text </modeling/texts/properties>`
- :doc:`Empty </modeling/empties>`

..

- :doc:`Armature </rigging/armatures/properties/index>`
- :doc:`Bones </rigging/armatures/bones/properties/index>`
- :doc:`Bone Constraints </rigging/armatures/posing/bone_constraints/introduction>`
- :doc:`Lattice </rigging/lattice>`

..

- :doc:`Speaker </render/audio/speaker>`
- Camera: :doc:`Blender Internal </render/blender_render/camera/object_data>`,
  :doc:`Cycles </render/cycles/camera>`
- Lamp: :doc:`Blender Internal </render/lighting/lights/lamp_panel>`,
  :doc:`Cycles </render/cycles/lamps>`

..

- Material: :doc:`Blender Internal </render/blender_render/materials/index>`,
  :doc:`Cycles </render/cycles/materials/index>`
- Texture: :doc:`Blender Internal </editors/uv_image/uv/textures/index>`,
  :doc:`Cycles </render/cycles/materials/texture_editing>`
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
