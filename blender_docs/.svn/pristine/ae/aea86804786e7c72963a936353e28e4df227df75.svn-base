
****************
Images as Planes
****************

.. admonition:: Reference
   :class: refbox

   :Category:  Import-Export
   :Menu:      :menuselection:`File --> Import --> Images as Planes`,
               :menuselection:`3D Viewport --> Add --> Image --> Images as Planes`

This add-on imports images and creates planes with them as textures.
At the moment the naming for objects, materials, textures and meshes
is derived from the image name.

You can either import a single image, or all images in one directory.
When importing a directory you can either check the checkbox or leave the filename empty.

When importing images that are already referenced they are not re-imported
but the old ones reused as not to clutter the materials, textures and image lists.
Instead the plane gets linked against an existing material.

If you import the same image again but choose a different material/texture mapping, a new material is created.

The add-on has an option to translate pixel dimensions into units.


Properties
==========

Import Options
--------------

Relative Path
   Link to the image file using a :ref:`relative file path <files-blend-relative_paths>`.

Force Reload
   Reloads the image file into Blender if it is already added as an image data-block.

Animate Image Sequences
   Import sequentially numbers images as an animated image sequence instead of separate planes.


Compositing Nodes
-----------------

Setup Corner Pin
   Builds a compositing setup to reference this image using a Corner Pin node.


Material Settings
-----------------

Shader
   Principled
      Todo.
   Shadeless
      The material is set to shadeless.
   Emit
      Todo.

Override Material
   Todo.


Texture Settings
----------------

Use Alpha
   The alpha channel of the image is used for transparency.

   Alpha Mode
      Representation of alpha in the image file, to convert to and from when saving and loading the image.
      See :term:`Alpha Channel`.

      Straight
         Store RGB and alpha channels separately with alpha acting as a mask, also known as unassociated alpha.
         Commonly used by image editing applications and file formats like PNG.
         This preserves colors in parts of the image with zero alpha.
      Premultiplied
         Store RGB channels with alpha multiplied in, also known as associated alpha.
         The natural format for renders and used by file formats like OpenEXR.
         This can represent purely emissive effects like fire correctly, unlike straight alpha.
      Channel Packed
         Different images are packed in the RGB and alpha channels, and they should not affect each other.
         Channel packing is commonly used by game engines to save memory.
      None
         Ignore alpha channel from the file and make image fully opaque.

Auto Refresh
   Automatically refresh images on frame changes.


Position
--------

Offset Planes
   Local Axis
      Todo.
   Offset
      Todo.

Plane Dimensions
   Use the image's pixel count to determine the planes size in units.

   Absolute
      Todo.
   Camera Relative
      Todo.
   DPI
      Todo.
   Dots/BU
      Sets the mapping of dots to units.


Orientation
   Align
      Todo.
   Track Camera
      Uses a Locked Track Constraint to make the plane always align with the camera.
