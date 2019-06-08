.. _bpy.types.Material.preview_render_type:

*******
Preview
*******

The Preview panel gives a quick visualization of the active material applied on to one of several basic objects.
Including its *Shaders*, *Ramps*, *Mirror*, *Transparency* properties and *Textures*.
It provides several shapes that are very useful for designing new shaders:
For some shaders (like those based on *Ramp* colors, or a Diffuse shader like *Minnaert*),
one needs fairly complex or specific previewing shapes to decide if the shader being designed achieves its goal.


Options
=======

Flat XY plane
   Useful for previewing textures and materials of flat objects, like walls, paper and such.
Sphere
   Useful for previewing textures and materials of sphere-like objects,
   but also to design metals and other reflective/transparent materials, thanks to the checkered background.
Cube
   Useful for previewing textures and materials of cube-like objects, but also to design procedural textures.
   Features a checkered background.
Monkey
   Useful for previewing textures and materials of organic or complex non-primitive shapes.
   Features a checkered background.
Hair strands
   Useful for previewing textures and materials of strand-like objects, like grass, fur, feathers and hair.
   Features a checkered background.
Large Sphere with Sky
   Useful for previewing textures and materials of sphere-like objects,
   but also to design metals and other reflective materials, thanks to the gradient Sky background.


Examples
========

.. list-table::

   * - .. figure:: /images/render_blender-render_materials_properties_preview_flat.png

          Plane preview.

     - .. figure:: /images/render_blender-render_materials_properties_preview_sphere.png

          Sphere preview.

     - .. figure:: /images/render_blender-render_materials_properties_preview_cube.png

          Cube preview.

   * - .. figure:: /images/render_blender-render_materials_properties_preview_monkey.png

          Monkey preview.

     - .. figure:: /images/render_blender-render_materials_properties_preview_hair.png

          Hair Strands preview.

     - .. figure:: /images/render_blender-render_materials_properties_preview_sky.png

          Sky Sphere preview.
