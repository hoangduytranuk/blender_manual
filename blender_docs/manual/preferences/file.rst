.. _bpy.types.UserPreferencesFilePaths:

****
File
****

The *File* tab in *User Preferences* allows you to configure auto-save preferences and set default file paths for
blend-files, rendered images, and more.

.. figure:: /images/preferences_file_tab.png


.. _prefs-file-paths:

File Paths
==========

Locations for various external files can be set for the following options:

Fonts
   Default location when searching for font files.
Textures
   Default location when searching for image textures.
Render Output
   Where rendered images/videos are saved.
Scripts
   An additional location to search for Python scripts. See `Scripts Path`_ below.
Sounds
   Default location when searching for sound files.
Temp
   The location where temporary files are stored.
Render Cache
   The location where cached render images are stored.
I18n Branches
   The path to the ``/branches`` directory of your local svn-translation copy, to allow translating from the UI.
Image Editor
   The path to an external program to use for image editing.
Animation Player
   The path to an external program to use for playback of rendered animations.

.. note:: If these folders do not exist, they will *not* be created automatically.


Scripts Path
------------

By default Blender looks in several directories (OS dependent) for scripts.
By setting a user script path in the preferences an additional directory is looked in.
This can be used to store certain scripts/templates/presets independently of
the currently used Blender Version.

Inside the specified folder, specific subfolders have to be created to tell Blender what to look
for where. This folder structure has to mirror the structure of the scripts folder found in
the installation directory of Blender:

- scripts
- add-ons
- modules
- presets
- camera
- cloth
- interface_theme
- operator
- render
- ...
- startup
- templates
  Not all of the folders have to be present.

.. warning::

   Be sure that you have the right privileges for running the executable accessing the path defined.
   On MS-Windows for instance, if the option "Run this program as an administrator" is enabled for the executable,
   it will lead to a failure to open the editor due to a limitation within the OS User Account Control.
   Running a program with elevated privileges is potentially dangerous!


.. _prefs-auto-execution:

Auto Execution
==============

Python scripts (including driver expressions) are not executed by default for security reasons.

Auto Run Python Scripts
   You may choose to ignore these security issues and allow scripts to be executed automatically.
Excluded Paths
   Blend-files in these folders will *not* automatically run Python scripts.
   This can be used to define where blend-files from untrusted sources are kept.

.. seealso::

   :doc:`Python Security </advanced/scripting/security>`.


.. _prefs-save-load:

Save & Load
===========

Relative Paths
   By default, external files use a :doc:`relative path </data_system/files/relative_paths>`.
Compress File
   Compress blend-file when saving.

   This option will compact your files whenever Blender is saving them.
   Dense meshes, large packed textures or lots of elements in your scene
   will result in a large blend being created.

   This option may slow down Blender when you quit,
   or under normal operation when Blender is saving your backup files.
   Using this option traces processor time for file size.
Load UI
   Default setting is to load the Window layout
   (the :doc:`workspaces </interface/window_system/workspaces>`) of the saved file.
   This can be changed individually when loading a file from
   the *Open blend-file* panel of the :doc:`File Browser </editors/file_browser/index>`.
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

Save Versions
   Number of versions created for the same file (for backup).

   This option tells Blender to keep the indicated number of saved versions of your file in your current working
   directory when you manually save a file.
   These files will have the extension: ``.blend1``, ``.blend2``, etc.,
   with the number increasing to the number of versions you specify. Older files will be named with a higher number.
   e.g. With the default setting of 2, you will have three versions of your file: ``*.blend`` (your last save),
   ``*.blend1`` (your second last save) and ``*.blend2`` (your third last save).
Recent Files
   Number of files displayed in :menuselection:`File --> Open Recent`.
Save Preview Images
   Previews of images and materials in the :doc:`File Browser </editors/file_browser/index>`
   are created on demand. To save these previews into your blend-file,
   enable this option (at the cost of increasing the size of your blend-file).


.. _prefs-auto-save:

Auto Save
=========

Keep Session
   Automatically loads the ``quit.blend`` file after re-starting Blender.
   This file is always saved on quit, regardless of this option.
   See :ref:`Recover Last Session <troubleshooting-file-recovery>`.
Auto Save Temporary Files
   Enables :doc:`Auto Save </troubleshooting/recover>`.
   Tells Blender to *automatically* save a backup copy of your work-in-progress files to the :ref:`temp-dir`.
Timer
   This specifies the number of minutes to wait between each :doc:`Auto Save </troubleshooting/recover>`.
   The default value of the Blender installation is 2 minutes.
   The minimum is 1, and the Maximum is 60 (save every hour).


Text Editor
===========

Tabs as Spaces
   When hitting :kbd:`Tab` the tabs get written as keyboard spaces.
Author
   Name that will be used in exported files when the format supports such feature.
