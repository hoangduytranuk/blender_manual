
****************
Images as Planes
****************

.. admonition:: Reference
   :class: refbox

   :Category:  Import-Export
   :Menu:      :menuselection:`File --> Import/Export --> FBX (.fbx)`

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
   Todo.
Force Reload
   Todo.
Animate Image Sequences
   Todo.


Compositing Nodes
-----------------

Setup Corner Pin
   Todo.


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
      :term:`Straight Alpha`, :term:`Premultiplied Alpha`, Channel Packed, None
Auto Refresh
   Todo.


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
      Todo.
