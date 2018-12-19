
************
Introduction
************

The term *Image Texture* simply means that a graphic image,
which is a pixel grid composed of R, G, B, and sometimes Alpha values.
It is used as the input source to the texture.
As with other types of textures, this information can be used in a number of ways,
not only as a simple "decal".

*Video textures* are a some kind of Image textures and
based on movie file or sequence of successive numbered separate images.
They are added in the same way that image textures are.

When the Texture Type *Image or Movie* is selected, three new panels present
themselves allowing to control most aspects of how image textures are applied:
*Image*, *Image Sampling*, and *Image Mapping*.


About Image-Based Texturing
===========================

Texture images take up precious memory space,
often being loaded into a special video memory bank that is very fast and very expensive,
so it is often very small. So, keep the images as small as possible.
A 64×64 image takes up only one fourth the memory of a 128×128 image.

For photorealistic rendering of objects in animations, often larger image textures are used,
because the object might be zoomed in on in camera moves. In general, you want to use
a texture sized proportionally to the number of pixels that it will occupy in the final render.
Ultimately, you only have a certain amount of physical RAM to hold an image texture and
the model and to provide workspace when rendering your image.

For the most efficient memory usage, image textures should be square, with dimensions as powers of 2,
such as 32×32, 64×64, 128×128, 256×256, 1024×1024, 2048×2048, and 4096×4096.

If you can reuse images across different meshes, this greatly reduces memory requirements.
You can reuse images if you map those areas of the meshes that "look alike" to a layout that
uses the common image.

When using file textures, it is very important that you have
:doc:`Mapped the UVs </editors/uv_image/uv/editing/unwrapping/index>`
of the mesh, and they are laid out appropriately.

You do not have to UV map the *entire* mesh.
The sphere above on the left has some faces mapped,
but other faces use procedural materials and textures.
Only use UV textures for those portions of your mesh where you want very graphic,
precise detail. For example,
a model of a vase only needs UV texture for the rim where decorative artwork is incorporated.
A throw pillow does not need a different image for the back as the front;
in fact many throw pillows have a fabric (procedural material) back.

As another example, you should UV map both eyes of a head to the same image
(unless you want one bloodshot and the other clear).
Mapping both sides of a face to the same image might not be advisable,
because the location of freckles and skin defects are not symmetrical.
You could of course change the UV map for one side of the face to slightly offset,
but it might be noticeable.
Ears are another example where images or section of an image can be mapped to similar faces.


UV Textures vs. Procedural Textures
===================================

A Material Texture, that has a Map Input of UV,
and is an image texture that is mapped to Color, is equivalent to a UV texture.
It provides much more flexibility, because it can be sized and offset, and the degree to which
it affects the color of your object can be controlled in the Map To panel. In addition,
you can have different images for each texture channel; one for color, one for alpha,
one for normals, one for specularity, one for reflectivity, *etc.* Procedural textures,
like Clouds, are incredibly simple and useful for adding realism and details to an image.

.. list-table::
   :header-rows: 1
   :class: valign
   :widths: 40 60

   * - UV Texture
     - Procedural Texture
   * - Image maps to precise coordinates on the selected faces of the mesh.
     - Pattern is generated dynamically, and is mapped to the entire mesh (or portion covered by that material).
   * - The Image maps once to a range of mesh faces specifically selected.
     - Maps once to all the faces to which that material is assigned; either the whole mesh or a portion.
   * - Image is mapped once to faces.
     - Size XYZ in the Map Input allows tiling the texture many times across faces.
       Number of times depends on size of mesh.
   * - Affect the color and the alpha of the object.
     - Can also affect normals (bumpiness), reflectivity, emit, displacement,
       and a dozen other aspects of the mesh's appearance; can even warp or stencil subsequent textures.
   * - Can have many for a mesh.
     - Can be layered, up to 10 textures can be applied, layering on one another.
       Many mix methods for mixing multiple channels together.
   * - Any Image type (still, video, rendered). Generated test grid available.
     - Many different types: clouds, wood grain, marble, noise, and even magic.
   * - Provides the UV layout for animated textures.
     - Noise is the only animated procedural texture.
   * - Takes very limited graphics memory
     - Uses no or little memory; instead uses CPU compute power.

So, in a sense, a single UV texture for a mesh is simpler but more limited than using multiple textures
(mapped to UV coordinates), because they do one specific thing very well:
adding image details to a range of faces of a mesh.
They work together if the procedural texture maps to the UV coordinates specified in your layout.
As discussed earlier, you can map multiple UV textures to different images using
the UV Coordinate mapping system in the Map Input panel.
