.. _prefs-save-load:

***********
Save & Load
***********

Blend Files
===========

Relative Paths
   By default, external files use a :doc:`relative path </files/files/relative_paths>`.
Compress File
   Compress blend-file when saving.

   This option will compact your files whenever Blender is saving them.
   Dense meshes, large packed textures or lots of elements in your scene
   will result in a large blend being created.

   This option may slow down Blender when you quit,
   or under normal operation when Blender is saving your backup files.
   Using this option trades processor time for file size.
Load UI
   Default setting is to load the Window layout
   (the :doc:`Workspaces </interface/window_system/workspaces>`) of the saved file.
   This can be changed individually when loading a file from
   the *Open blend-file* panel of the :doc:`File Browser </editors/file_browser/index>`.

Save Preview Images
   Previews of images and materials in the :doc:`File Browser </editors/file_browser/index>`
   are created on demand. To save these previews into your blend-file,
   enable this option (at the cost of increasing the size of your blend-file).
Tabs as Spaces
   When hitting :kbd:`Tab` the tabs get written as keyboard spaces.
Save Prompt
   Asks for confirmation before closing or opening a new
   blend-file if the current file has unsaved changes

Save Versions
   Number of versions created for the same file (for backup).

   This option tells Blender to keep the indicated number of saved versions of
   your file in your current working directory when you manually save a file.
   These files will have the extension: ``.blend1``, ``.blend2``, etc.,
   with the number increasing to the number of versions you specify. Older files will be named with a higher number.
   e.g. With the default setting of 2, you will have three versions of your file: ``*.blend`` (your last save),
   ``*.blend1`` (your second last save) and ``*.blend2`` (your third last save).
Recent Files
   Number of files displayed in :menuselection:`File --> Open Recent`.


.. _prefs-auto-save:

Auto Save
---------

Auto Save Temporary Files
   Enables :doc:`Auto Save </troubleshooting/recover>`.
   Tells Blender to *automatically* save a backup copy of your work-in-progress files to the :ref:`temp-dir`.
Timer
   This specifies the number of minutes to wait between each :doc:`Auto Save </troubleshooting/recover>`.
   The default value of the Blender installation is 2 minutes.
   The minimum is 1, and the Maximum is 60 (save every hour).


.. _prefs-auto-execution:

Auto Execution
--------------

Python scripts (including driver expressions) are not executed by default for security reasons.

Auto Run Python Scripts
   You may choose to ignore these security issues and allow scripts to be executed automatically.
Excluded Paths
   Blend-files in these folders will *not* automatically run Python scripts.
   This can be used to define where blend-files from untrusted sources are kept.

.. seealso::

   :doc:`Python Security </advanced/scripting/security>`.


File Browser
============

Filter File Extensions
   By activating this, the file region in the File Browser will only show appropriate files
   (i.e. blend-files when loading a complete Blender setting).
   The selection of file types may be changed in the file region.

   .. figure:: /images/preferences_file_filter.png

      File extension filter.

Hide Dot File/Data-blocks
   Hide file which start with ``.`` on file browsers (in Linux and Apple systems, ``.`` files are hidden).
Hide Recent Locations
   Hide the *Recent* panel of the :doc:`File Browser </editors/file_browser/index>`
   which displays recently accessed folders.
Hide System Bookmarks
   Hide System Bookmarks in the *File Browser*.
Show Thumbnails
   Display a thumbnail of images and movies when using the :doc:`File Browser </editors/file_browser/index>`.
