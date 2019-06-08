.. _bpy.types.UserPreferencesView:

*********
Interface
*********

Interface configuration lets you change how UI elements are displayed and how they react.

.. figure:: /images/preferences_interface_tab.png


Display
=======

Resolution Scale
   Adjusts the size of fonts and buttons relative to the automatically detected DPI.
   During typical usage, you may prefer to use zoom which is available in many parts of Blender interface.
Line Width
   Scale of lines and points in the interface e.g. button outlines, edges and vertex points in the 3D View.

   Thin, Auto, Thick
Splash Screen
   Display the :ref:`splash` when starting Blender.
Tooltips
   When enabled, a tooltip will appear when your mouse pointer is over a control.
   This tip explains the function of what is under the pointer,
   gives the associated hotkey (if any) and the Python function that refers to it.
Python Tooltips
   Displays a property's Python information below the tooltip.
Developer Extras
   TODO 2.8.
Large Cursors
   Use large mouse cursors when available.


Editors
=======

Region Overlap
   This checkbox will enable Blender to draw regions overlapping the 3D View.
   It means that the *Tool Shelf* and *Sidebar regions*,
   will be drawn overlapping the 3D View editor.

   If you have a capable graphics card and drivers with *Triple Buffer* support,
   clicking the checkbox will enable the overlapping regions to be drawn using the *Triple Buffer* method,
   which will also enable them to be drawn using Alpha, showing the 3D View contents through the regions.
Corner Splitting
   TODO 2.8.
Color Picker Type
   Choose which type of :term:`color space` you prefer. It will show when clicking :kbd:`LMB` on any color button.

   See the different color picker types at the :doc:`Color picker </interface/controls/templates/color_picker>` page.
Header Position
   TODO 2.8.
Factor Display Type
   How factor value types are displayed in the user interface.

   Factor
      Values are displayed as float numbers.
   Percentage
      Values are displayed as percentages.


2D Viewports
============

.. _prefs-interface-manipulator:

Manipulator
   Turns manipulator on and off.
Size
   Diameter of the manipulator.
Handle Size
   Size of manipulator handles, as a percentage of the manipulator radius (*size*/ 2).
Hotspot
   Hotspot size (in pixels) for clicking the manipulator handles.


.. _prefs-system-international:

Translation
===========

Blender supports a wide range of languages, enabling this checkbox will enable Blender to
support International Fonts. International fonts can be loaded for the User Interface and
used instead of the font bundled with Blender by default.

This will also enable options for translating the User Interface
through a list of languages and tips for Blender tools which appear
whenever the mouse pointer hovers over a tool button.

Blender supports I18N for internationalization.
For more Information on how to load International fonts,
see: :doc:`Editing Texts </modeling/texts/selecting_editing>` page.


Text Rendering
==============

Anti-aliasing
   Enable interface text anti-aliasing.
   When disabled, texts are drawn using straight text rendering (filling only absolute pixels).
Hinting
   TODO 2.8.
Interface Font
   Replacement for the default user interface font.
Mono-space Font
   Same as above but for the mono-space font.


Menus
=====

Open on Mouse Over
------------------

Select this to have the menu open by placing the mouse pointer over the entry instead of clicking on it.

   Top Level
      Time delay in 1/10 second before a menu opens (*Open on Mouse Over* needs to be enabled).
   Sub Level
      Same as above for sub menus (for example: :menuselection:`File --> Open Recent`).


.. _prefs-pie-menu:

Pie Menus
---------

Animation Timeout
   Length of animation when opening Pie Menus.
Tab Key Timeout
   Keystrokes held longer than this will dismiss the menu on release (in 1/100ths of a second).
Recenter Timeout
   The window system tries to keep the pie menu within the window borders.
   Pie menus will use the initial mouse position as center for this amount of time, measured in 1/100ths of a second.
   This allows for fast dragged selections.
Radius
   The size of the Pie Menu set with the distance (in pixels) of the menu items from the center of the pie menu.
Threshold
   Distance from center before a selection can be made.
Confirm Threshold
   Distance threshold after which selection is made (zero disables).
