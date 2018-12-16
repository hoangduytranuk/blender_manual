
******************
Bump & Normal Maps
******************

*Normal Maps* and *Bump Maps* both serve the same purpose:
they simulate the impression of a detailed 3D surface,
by modifying the shading as if the surface had lots of small angles, rather than being completely flat.
Because it is just modifying the shading of each pixel,
this will not cast any shadows and will not obstruct other objects. If the camera angle is too flat to the surface,
you will notice that the surface is not really shaped.

Both *Bump Maps* and *Normal Maps* work by modifying the normal angle
(the direction pointing perpendicular from a face), which influences how a pixel is shaded.
Although the terms *Normal Map* and *Bump Map* are often used
synonymously, there are certain differences.

Bump maps
   These are textures that store an *intensity*, the relative height of pixels from the viewpoint of the camera.
   The pixels seem to be moved by the required distance in the direction of the face normals.
   (The "bump" consists only of a displacement, which takes place along the existing,
   and unchanged, normal vector of the face).
   You may either use grayscale pictures or the intensity values of an RGB texture (including images).

Normal maps
   These are images that store a *direction*, the direction of normals directly in the RGB values of an image.
   They are much more accurate, as rather than only simulating the pixel being away from the face along a line,
   they can simulate that pixel being moved at any direction, in an arbitrary way.
   The drawbacks to normal maps are that unlike bump maps, which can easily be painted by hand,
   normal maps usually have to be generated in some way,
   often from higher resolution geometry than the geometry you are applying the map to.

   Normal maps in Blender store a normal as follows:

   - Red maps from (0 - 255) to X (-1.0 - 1.0)
   - Green maps from (0 - 255) to Y (-1.0 - 1.0)
   - Blue maps from (0 - 255) to Z (0.0 - 1.0)

   Since normals all point towards a viewer, negative Z values are not stored (they would be invisible anyway).
   In Blender we store a full blue range, although some other implementations also map blue colors (128 - 255) to
   (0.0 - 1.0). The latter convention is used in "Doom 3" for example.


Workflow
========

The steps involved in making and using Bump and Normal Maps is:

#. Model a highly detailed ("hi-poly") model.
#. Bake the Bump and/or Normal maps.
#. Make a low-poly, less detailed model.
#. Map the map to the low-poly model using a common coordinate system.

Consult the Modeling section for how to model a highly detailed model using the Mesh tools.
How much detail you put in is totally up to you.
The more ridges and details (knobs, creases, protrusions) you put in, the more detailed your map will be.

Baking a map, simply put, is to take the detail of a high polygon mesh, and apply it to a similar object.
The similar object is identical to the high-poly mesh except with less vertices.
Use the :doc:`Render Bake </render/blender_render/bake>` feature in Blender to accomplish this.

Modeling a low-poly using Blender's Mesh editing tools. In general,
the same or similar faces should exist that reflect the model. For example,
a highly detailed ear may have 1000 faces in the high-poly model. In the low-poly model,
this may be replaced with a single plane, oriented in the same direction as the detailed ear mesh.
(*Tip*: Blender's :doc:`multi-resolution mesh </modeling/modifiers/generate/multiresolution>`
modeling feature can be used to good effect here).

Mapping is the process of applying a texture to the low-poly mesh.
Consult the :doc:`Textures Mapping section </editors/uv_image/uv/textures/properties/mapping>`
for more information on applying a texture to a mesh's material. Special considerations for Bump and Normal Maps is:

- When using a Bump map, map the texture to *Normal* and enable *No RGB*.
- When using a Normal map, map the texture to *Normal*.

The coordinate systems of the two objects must match. For example, if you bake using a UV map of the high-poly model,
you must UV map the low-poly model and line up its UV coordinates to match the outline of the high-poly image.
(see :ref:`UV unwrapping <editors-uv-image-index>` to line up with the high-poly map edges).
