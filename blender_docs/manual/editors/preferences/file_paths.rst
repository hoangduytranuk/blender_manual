.. _bpy.types.UserPreferencesFilePaths:
.. _prefs-file-paths:

**********
File Paths
**********

The *File* tab in *Preferences* allows you to configure auto-save preferences
and set default file paths for blend-files, rendered images, and more.

Locations for various external files can be set for the following options:

.. figure:: /images/preferences_file_tab.png

   Preferences File Paths tab.


Data
====

Fonts
   Default location when searching for font files.
Textures
   Default location when searching for image textures.
Scripts
   An additional location to search for Python scripts. See `Scripts Path`_ below.
Sounds
   Default location when searching for sound files.
Temporary Files
   The location where temporary files are stored.


Scripts Path
------------

By default Blender looks in several directories (OS dependent) for scripts.
By setting a user script path in the preferences an additional directory is looked in.
This can be used to store certain scripts/templates/presets independently of
the currently used Blender Version.

Inside the specified folder, specific subfolders have to be created to tell Blender what to
look for and where. This folder structure has to mirror the structure of the scripts folder found in
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


Render
======

Render Output
   Where rendered images/videos are saved.
Render Cache
   The location where cached render images are stored.


Applications
============

Image Editor
   The path to an external program to use for image editing.
Animation Player
   The path to an external program to use for playback of rendered animations.

.. note:: If these folders do not exist, they will *not* be created automatically.


Development
===========

Only Visible when *Developer Extras* is enabled.

I18n Branches
   The path to the ``/branches`` directory of your local svn-translation copy, to allow translating from the UI.
