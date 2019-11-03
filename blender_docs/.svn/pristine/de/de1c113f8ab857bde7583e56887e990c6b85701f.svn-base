.. _bpy.types.UserPreferencesView:

*********
Interface
*********

Interface configuration lets you change how UI elements are displayed and how they react.

.. figure:: /images/editors_preferences_section_interface.png


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
   gives the associated hotkey (if any).
Python Tooltips
   Displays a property's Python information below the tooltip.
Developer Extras
   .. _prefs-interface-dev-extras:

   Show settings and menu items which are intended to help developers, this includes:

   Button Context Menu
      Online Python Reference
         To open the Python reference manual.
      Copy Python Command
         To copy the expression used when pressing the button.
      Edit Source
         To edit Python source code that defines the button.
      Edit Translation
         The option to edit-translations
         (Only when the *Manage UI translations* add-on is also enabled).
   3D View
      Show Indices
         The option to show mesh vertex/edge/face indices in the overlay popover.

Large Cursors
   Use large mouse cursors when available.


Editors
=======

Region Overlap
   This makes regions overlap the viewport.
   It means that the *Toolbar* and *Sidebar* regions,
   will be displayed overlapping the 3D Viewport.
Corner Splitting
   Split & join by dragging from the corners.

   When disabled, you can use the context menu for area separators to perform these operations.
Navigation Controls
   Show navigation controls at top right of the window.

   This impacts the 3D Viewport as well as image spaces.

   .. note::

      If you're familiar with navigation key shortcuts, this can be disabled.

Color Picker Type
   Choose which type of :term:`color space` you prefer. It will show when clicking :kbd:`LMB` on any color field.

   See the different color picker types at the :doc:`Color picker </interface/controls/templates/color_picker>` page.
Header Position
   The default header position.

   Using default uses top for most window types and the positions saved in the file.
   Otherwise you can choose to force top/bottom header alignment.
Factor Display Type
   How factor value types are displayed in the user interface.

   Factor
      Values are displayed as float numbers between 0.0 and 1.0.
   Percentage
      Values are expressed as a percentage between 0 and 100.


.. _prefs-interface-translation:

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
   When disabled, texts are rendered using straight text rendering (filling only absolute pixels).
Hinting
   Adjust `font hinting <https://en.wikipedia.org/wiki/Font_hinting>`__,
   controls the spacing and crispness of text display.
Interface Font
   Replacement for the default user interface font.
Mono-space Font
   Replacement for the default mono-space interface font
   *(use in the Text editor and Python Console)*.


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
Tap Key Timeout
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
