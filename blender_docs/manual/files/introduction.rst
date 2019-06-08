
************
Introduction
************

Each blend-file contains a database.
This database contains all scenes, objects, meshes, textures, etc. that are in the file.

A file can contain multiple scenes and each scene can contain multiple objects.
Objects can contain multiple materials which can contain many textures.
It is also possible to create links between different objects.


Outliner
========

You can easily inspect the contents of your file by using the *Outliner* editor,
which displays all of the data in your blend-file.

The *Outliner* allows you to do simple operations on objects,
such as selecting, renaming, deleting, linking and parenting.

:doc:`Read more about the Outliner </editors/outliner>`.


.. _pack-unpack-data:

Pack and Unpack Data
====================

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Info Editor --> File --> External Data --> Pack Into blend-file`

Blender has the ability to encapsulate (incorporate)
various kinds of data within the blend-file that is normally saved outside of the blend-file.
For example, an image texture that is an external image file can be
put "inside" the blend-file via *Pack Into blend-file*.
When the blend-file is saved, a copy of that image file is put inside the blend-file.
The blend-file can then be copied or emailed anywhere, and the image texture moves with it.

You know that an image texture is packed, because you will see
a little gift box icon displayed in the header.


Unpack Data
-----------

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Info Editor --> File --> External Data --> Unpack Into Files...`

When you have received a packed file, you can *Unpack Into Files...*.
If files are packed, there is also track of their original path,
which can be relative or absolute (this is needed in case of unpacking to original location).


Options
^^^^^^^

Use files in current directory (create when necessary)
   Unpacks all files in the same directory ``//`` as the blend-file,
   grouping them in proper folders (like ''textures'' for instance).
   However, if the final file exists already, it will use that file, instead of unpacking it.
Write files to current directory (overwrite existing files)
   Unpacks all files in the same directory as the blend-file,
   grouping them in proper folders (like ''textures'' for instance).
   If the final file exists already, it will overwrite it.
Use files in original location (create when necessary)
   Unpacks all files in their original location.
   However, if the final file exists already, it will use that file, instead of unpacking it.
Write files to original location (overwrite existing files)
   Unpacks all files in their original location. If the final file exists already, it will overwrite it.
Disable AutoPack, keep all packed files
   Cancels the operation and deactivates the *Automatically Pack Into .blend* option.
