
*******************************
Import & Export of Node Shaders
*******************************

While Blender now only supports the advance node-based shading model for its materials,
most IO formats only support a basic shading model, similar to the legacy fixed pipeline of old GPUs.

Blender features a way to convert between those, which any add-on can use, but it is currently pretty basic still.
Especially for exporting from Blender materials, the node system must follow some strict requirements.

.. note::

   Currently, only the :doc:`OBJ </addons/io_scene_obj>` and :doc:`FBX </addons/io_scene_fbx>`
   IO addons uses that method.

.. note::

   The wrapper is designed to be as symetrical as possible
   (i.e. it is expected to give reproducible results acrross several import/export cycles)

.. figure:: /images/addons_io_node_shaders_info-example.png
   :align: center

   A typical setup of shader nodes that is can be exported.


Supported Node Setup
====================

This is especially important for exporting, importing will simply re-generate a similar set-up.

Note that the features listed below are those supported by the wrapper.
Each add-on may have its own way to adapt them to its material system, some may not be handled by it, etc.

Principled BSDF
   The main shader must be of :doc:`that type </render/shader_nodes/shader/principled>`.
   Only parameters defined there, and textures linked to it, will be exported.

   Currently handled parameters:
    * Base color *(supports texture)*
    * Specular intensity *(supports texture)*
    * Specular tint
    * Roughness *(supports texture)*
    * Metallic *(supports texture)*
    * IOR *(supports texture)*
    * Transmission *(supports texture)*
    * Alpha *(supports texture)*

Normal Map
   If linked to the `Normal` input of the `Principled BSDF` node,
   :doc:`this node </render/shader_nodes/vector/normal_map>` is also supported (including its texture obviously).

Textures
   Only :doc:`Image </render/shader_nodes/textures/image>` textures using an UV mapping are supported.
   You may also use a :doc:`Mapping </render/shader_nodes/vector/mapping>` node to move/rotate/scale it.
   
