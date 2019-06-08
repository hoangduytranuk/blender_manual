.. _prefs-input-keymap-editor:

******
Keymap
******

Keymap Presets
   A list of predefined keymaps.
Import/Export
   See `Import/Export Key Configuration`_.

Preferences
===========

Select With
   Controls which mouse button, either right or left, is used to select items in Blender.
   If *Left* is selected the :kbd:`RMB` will be a context sensitive menu,
   if *Right* is selected the :kbd:`LMB` will place the 3D Cursor.

Select All Toggles
   TODO 2.8.
Spacebar Action
   Controls the action of :kbd:`Spacebar`.
   These and other shortcuts can be modified in the :doc:`keymap preferences </editors/preferences/keymap>`.

   Play
      Starts playing through the :doc:`Timeline </editors/timeline>`,
      this option is good for animation or video editing work.
   Tools
      Opens the Toolbar underneath the cursor to quickly change the active tool.
      This option is good for if doing a lot of modeling or rigging work.
   Search
      Opens up the :doc:`operator search </interface/controls/templates/operator_search>`.
      This option is good for someone who is new to Blender and is unfamiliar with the menus and shortcuts.


3D View
-------

Todo 2.8.


Editor
======

The Keymap editor lets you change the default Hotkeys. You can change keymaps for each of Blender's editors.

.. figure:: /images/preferences_input_keymap-editor.png

   Keymap editor.


.. rubric:: Usage

#. Select the keymap you want to change and click on the white arrows to open up the keymap tree.
#. Select which Input will control the function.
#. Change hotkeys as you want. Just click on the shortcut input and enter the new shortcut.

Active
   Todo.
ID Name
   Todo.
Event
   Type
      Todo.
   Value
      Todo.
   Modifier
      Todo.
Map Type
   Keyboard
      Only hotkey or combo hotkey :kbd:`E`, :kbd:`Shift-E`.
   Mouse
      Left/middle/right click. Can be combined with :kbd:`Alt`, :kbd:`Shift`, :kbd:`Ctrl`, :kbd:`Cmd`.
   NDOF
      Movement from a :ref:`3D Mouse <hardware_3d-mice>`.
   Tweak
      Click and drag. Can also be combined with the four previous keys.
   Text Input
      Use this function by entering a text.
   Timer
      Used to control actions based on a time period.
      e.g. By default, *Animation Step* uses "Timer 0", *Smooth View* uses "Timer 1".
RNA
   Todo.
Context Attributes
   Todo.


Restoring
---------

If you want to restore the default settings for a keymap,
just click on the *Restore* button at the top right of this keymap.

.. tip::

   Instead of deleting the default keymap to create your custom one,
   you can just add a new *Preset* for both the mouse and keyboard.


Filtering
---------

Filter Type
   Todo.
Search
   Todo


Import/Export Key Configuration
===============================

In some cases, you may need to save your configuration in an external file
(e.g. if you need to install a new system or share your keymap configuration with the community).
To do this, simply press the *Export Key Configuration* button found in the header.
After doing so, the File Browser will open to choose where to store the configuration.
The *Import Key Configuration* button installs a keymap configuration that is on
your computer but not in Blender.

The exported keymap will only contain keymaps and categories that have been modified by the user.
In addition, add-ons may register keymaps to their respective functions,
however, these keymaps are not exported unless changed by the user.
This exported file may be thought of as a *"keymap delta"* instead of a full keymap export.
