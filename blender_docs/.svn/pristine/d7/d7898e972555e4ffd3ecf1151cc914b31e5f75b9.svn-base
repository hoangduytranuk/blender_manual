.. _prefs-input-keymap-editor:

******
Keymap
******

The key-map editor lets you adjust your key-map via:

:Presets: Predefined key-maps which come with Blender and can be added to.
:Preferences: Key-maps may define their own preferences to change the functionality or add additional key bindings.
:Key Map Items: You may add/remove/edit individual key-map entries.

.. figure:: /images/editors_preferences_section_keymap.png

   Blender Preferences Key-map section.


Preset Management
=================

Keymap Presets
   Select the key-map from a list of predefined key-maps.
Import
   Importing opens a File Browser to select a ``.py`` file to add to the list of key-map presets.
Export
   Saves the current key-map configuration as a preset others may use.

   All Keymaps
      When disabled, only the key-maps and categories that have been modified by the user will be exported.
      In addition, add-ons may register key-maps to their respective functions,
      however, these key-maps are not exported unless changed by the user.
      This exported file may be thought of as a *"key-map delta"* instead of a full key-map export.

      When enabled, the entire key-map is written.


Filtering
---------

Filter Type
   Name
      Search the key-map item by the operator name it runs.
   Key Binding
      Search the key-map item by the key used to activate it.

      .. hint::

         You could for example search with ``Ctrl Shift C`` for key-map items that use all these keys.
Search
   The text to search (leave blank to disable).


Preferences
===========

Key-maps may define their own preferences, these are predefined adjustments to the key-map you can make
without having to manually adjust individual key-map items which can cause problems with newer `Blender Versions`_.

See the :ref:`default key-map preferences <keymap-blender_default-prefs>`
for options available in the default key-map.


Editor
======

The Key-map editor lets you change the default Hotkeys. You can change key-maps for each of Blender's editors.

.. figure:: /images/editors_preferences_keymap_keymap-editor.png

   Key-map editor.


.. rubric:: Usage

#. Select the key-map you want to change and click on the white arrows to open up the key-map tree.
#. Select which Input will control the function.
#. Change hotkeys as you want. Just click on the shortcut input and enter the new shortcut.

Active
   Un-check to disable this key-map item.
Map Type
   Keyboard
      Single hotkey or key-combination.
   Mouse
      Actions from mouse buttons, tablet or track-pad input.
   NDOF
      Movement from a 3D mouse (:term:`NDOF`) device.
   Tweak
      Mouse click and drag *(optionally map drag direction to different actions)*.
   Text Input
      Use this function by entering a text.
   Timer
      Used to control actions based on a time period.
      e.g. By default, *Animation Step* uses "Timer 0", *Smooth View* uses "Timer 1".
Operator ID Name
   The identifier for the operator to call.

   .. hint::

      See :mod:`blender_api:bpy.ops` for a list of operators (remove the ``bpy.`` prefix for the identifier).
Event
   Type
      The key or button that activates this key-map item (depending on the map-type).
   Value
      The action (such as press, release, click, drag, etc.), (depending on the map-type).
   Modifier
      Additional keys to hold (such as :kbd:`Ctrl`, :kbd:`Shift`, :kbd:`Alt`).
Operator Properties
   Changes to the defaults properties this operator is activated with

.. seealso::

   :ref:`keymap-customize` for more information on key-map editing.


Restoring
---------

If you want to restore the default settings for a key-map,
just click on the *Restore* button at the top right of this key-map.

.. tip::

   Instead of deleting the default key-map to create your custom one,
   you can just add a new *Preset* for both the mouse and keyboard.


Known Limitations
=================

Blender Versions
----------------

A problem with modifying your own key-map is newer Blender versions key change the way tools are accessed,
breaking your customized key-map.

While the key-map can be manually updated, the more customizations you make, the higher the chance of conflicts
in newer Blender versions is.
