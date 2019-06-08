
************
Introduction
************

This chapter explains how to change Blender's default configuration with the *Preferences* editor.

The Blender *Preferences* editor contains settings to control how Blender behaves.
At the left of the editor, the available options are grouped into tabs.

.. figure:: /images/preferences_interface_tab.png

   Blender Preferences window.


Opening Preferences
===================

While the *Preferences* is its own editor type the best and easiest way to open it is
in a new window. To open the *Preferences* editor go to :menuselection:`Edit --> Preferences...`


Save User Settings
==================

Once you have set your preferences, you can either manually save them,
or just close the window and they will be saved automatically.

To manually save the preferences, from the preferences window open the small menu
in the bottom left and select *Save Current State*. There are two other options
related to saving the preferences:

Revert to Saved
   Undoes any unsaved modifications to preferences back to the previous saved state.
Auto-Save Preferences
   Toggle whether or not the preferences are saved when exiting the *Preferences* window.

.. tip::

   It can be valuable to make a backup of your preferences in the event that you lose your configuration.

   See the :doc:`directory layout </getting_started/installing/configuration/directories>`
   section to see where your preferences are stored.


.. _factory-settings:

Load Factory Settings
=====================

If you want to completely undo all the modifications made to the preferences
and revert them to the factory settings. Open the menu at the bottom left and select *Load Factory Settings*.
Note that no permanent changes are made until you save the preferences or close the preferences window.

.. note::

   Using this only resets the preferences and will not affect settings stored in the startup file.
   This includes app templates, area locations, and any Blender properties not part of the preferences.

   These must be reverted though :menuselection:`File --> Defaults`.
