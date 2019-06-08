.. _splash:

*************
Splash Screen
*************

When starting Blender, the splash screen appears in the center of the window.
It contains options create new projects or open recently opened blend-files.
A more detailed description can be found below.

.. figure:: /images/interface_splash_current.png
   :align: center

   Blender Splash Screen.

To close the splash screen and start a new project,
click anywhere outside the splash screen (but inside the Blender Window) or press :kbd:`Esc`.
The splash screen will disappear revealing the default screen.

To reopen the splash click on the Blender icon in the Top bar and select :guilabel:`Splash Screen`.

Information Region
   The upper part of the splash screen contains the splash image with a lot of key information overlaid.

   Title
      Besides the Blender icon and text, it shows the Blender version. e.g. the current version is |BLENDER_VERSION|.
   Date
      At the top-right corner, you can see the date on that Blender version was compiled.
   Hash
      The Git Hash. This can be useful to give to support personnel, when diagnosing a problem.
   Branch
      Optional branch ID.
Interactive Region
   The interactive region is the bottom half of the splash screen and provides how to get a project started.

   New File
      Options for starting a new project, based on predefined application templates.
   Recent Files
      Your most recently opened blend-files. This gives quick and easy access to your recent projects.
   Open
      Allows opening an existing blend-file.
   Recover Last Session
      Blender will try to recover the last session based on temporary files. See :doc:`/troubleshooting/recover`.
   Links
      Links official web pages, the same could be found in the *Help* Menu of the Info Editor.
      See :ref:`help-menu`.


Quick Set Up
============

When you open Blender for the first time the interactive region of the splash screen
is replaced with a couple initial preferences to configure how you interact inside Blender.

.. note::

   These options can always be changed later in the :doc:`Preferences </editors/preferences/index>`

Shortcuts
   Presets for the default :doc:`keymap </editors/preferences/keymap>` for Blender.
   Note that this manual assumes that you use the "Blender" keymap.

   Blender
      This is the default keymap.
      Read more about this keymap :doc:`here </interface/keymap/blender_default>`
   Blender 2.7x
      This keymap is intended to match the last major series of Blender versions
      and is designed for people upgrading who do not want to relearn the keymap.
   Industry Compatible
      This keymap is indented to match of common creation software
      and is intended for people who use many different creation software.
      Read more about this keymap :doc:`here </interface/keymap/industry_compatible>`

Select With
   Controls which mouse button, either right or left, is used to select items in Blender.
Spacebar
   Controls the action of :kbd:`Spacebar`.
   These and other shortcuts can be modified in the :doc:`keymap preferences </editors/preferences/keymap>`.

   Play
      Starts playing through the :doc:`Timeline </editors/timeline>`,
      this option is good for animation or video editing.
   Tools
      Opens the toolbar underneath the cursor to quickly change the active tool.
      This option is good for if doing a lot of modeling or rigging.
   Search
      Opens up the :doc:`operator search </interface/controls/templates/operator_search>`.
      This option is good for someone who is new to Blender and is unfamiliar with its menus and shortcuts.
Theme
   Choose between a light or dark theme for Blender.
   Themes can be customized more in the :doc:`Preferences </editors/preferences/themes>`
