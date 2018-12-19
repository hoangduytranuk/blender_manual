.. _bpy.ops.export:
.. _bpy.ops.import:

***************************
Importing & Exporting Files
***************************

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Info Editor --> File --> Import/Export`

Sometimes you may want to utilize files that either came from other 2D or 3D software,
or you may want to use the things you have made in Blender and edit them in other software.
Luckily, Blender offers a wide range of file formats (e.g. OBJ, FBX, 3DS, PLY, STL, etc.)
that can be used to import and export.

Popular formats are enabled by default, other formats are also supported and distributed with Blender,
these can be enabled in the User Preferences through the use of :doc:`Add-ons </preferences/addons>`.

.. hint::

   If you are not interested in technical details,
   a good rule of thumb for selecting import/export formats for your project is:

   Use :abbr:`STL (STereoLithography)`
      if you intend to import/export the files for CAD software.
      This format is also commonly used for loading into 3D printing software.
   Use :abbr:`FBX (Filmbox)`
      if you intend to export objects with rigs and/or animation
      to be used in other 3D creation suites or game development.
   Use :abbr:`DAE (Collada)`
      if you intend to export objects with rigs and/or animation
      to be used in other 3D creation suites or game development (provided they support Collada).
      See also the :doc:`Blender Collada module </pipeline/collada>`
   Use :abbr:`ABC (Alembic)`
      if you want to import/export a large amount of scene data.
      This :doc:`Alembic </pipeline/alembic>` format is also useful to export an animated mesh
      (rather than a static mesh + the armature + the animation of the armature).
      That animated mesh from an Alembic file can then be used for shading and lighting.

.. seealso::

   More information on the add-ons to import/export these file types can be found :ref:`here <addons-io>`.
