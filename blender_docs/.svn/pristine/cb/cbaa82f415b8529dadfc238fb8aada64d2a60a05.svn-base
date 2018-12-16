.. |specials-button| image:: /images/interface_controls_buttons_menus_specials.png

.. _bpy.types.Menu:

*****
Menus
*****

Blender uses a variety of different menus for accessing options and tools.


.. _ui-header-menu:

Header Menus
============

.. figure:: /images/interface_controls_buttons_menus_menu-button.png
   :align: right

   The Info Editor menu buttons.

Most :ref:`headers <ui-region-header>` exhibit a set of menus, located immediately next
to the first *Editor Type* selector.
Header menus are used to configure the editor and access tools.
All Menu entries show the relevant shortcut keys, if any.


Collapsing Menus
----------------

Sometimes it's helpful to gain some extra horizontal space in the header by collapsing menus,
this can be accessed from the header context menu,
simply :kbd:`RMB` click on the header and enable it to collapse.

.. list-table::

   * - .. figure:: /images/interface_controls_buttons_menus_header-menu-expand.png
          :width: 310px

          Right-click on any of the header menus.

     - .. figure:: /images/interface_controls_buttons_menus_header-menu-collapsed.png
          :width: 310px

          Access the menu from the collapsed icon.


Select Menus
============

.. figure:: /images/interface_controls_buttons_menus_select-menu.png
   :align: right

   The 3D View mode select menu.

The Select menu or short selector lets you choose between a set of options. They can show a text and/or an icon.
The options are shown in a pop-up. The selected option is then shown as active.


.. _bpy.types.UIPopupMenu:

Pop-Up Menus
============

.. figure:: /images/interface_controls_buttons_menus_popup-menu.png
   :align: right

   The Viewport Shading pop-up menu.

Pop-up menus are overlays.
They are spawned by menus showing up and down triangles on the right or
after a key input at the mouse position.

If the content is too large to fit on the screen, small indicator triangles appear.
When moving the mouse over them scrolls the pop-up.

For example, the *Viewport Shading* button will produce a pop-up menu
with the available shading options.

Mouse selection
   :kbd:`LMB` on the desired item.
Numerical selection
   You can use the number keys or numpad to input an item in the list to select.
   For example, :kbd:`Numpad1` will select the first item and so on.

Pop-ups can be moved by dragging their title.

.. todo <2.8 duplicate: selection


Shortcuts
---------

- Use :kbd:`Wheel` while hovering with the mouse.
- Arrow keys can be used to navigate.
- Each menu item has an underlined character which can be pressed to activate it.
- Number keys or numpad can be used to access menu items.
  (Where :kbd:`1` is the first menu item, :kbd:`2` the second, etc.
  For larger menus :kbd:`Alt-1` the 11th... up to :kbd:`Alt-0` the 20th).
- Press :kbd:`Return` to activate the selected menu item.
- Press :kbd:`Esc` to cancel the menu, or move the mouse cursor far from the pop-up,
  or by :kbd:`LMB` clicking anywhere out of it.


Context Menu
============

Context menus are pop-ups opened with the :kbd:`RMB`.
Only the common options are listed below:

.. for the property associated with the control.

*Single* sets or gets the value of the button under the mouse pointer.
*All* on the other hand includes all combined buttons.

Reset All/Single to Default Value(s)
   Replaces the current value by the default :kbd:`Backspace`.
Unset
   ToDo.
Copy Data Path
   For scripting -- Copies the path of the Python property, relative to the data-block.
Copy To Selected
   Copies the property value to the selected object's corresponding property.
   A use case is if the Properties editor context is pinned.
Add Shortcut
   Lets you define a keyword or mouse shortcut and associates it with the control.
   To define the shortcut you must first move the mouse cursor over the button that pops up,
   and when "Press a key" appears you must press and/or click the desired shortcut.
Change Shortcut
   Lets you redefine the shortcut.
Remove Shortcut
   Unlinks the existing shortcut.
Online Manual
   See :ref:`help-manual-access`.
Online Python Reference
   Context-sensitive access to
   the `Python API Reference <https://www.blender.org/api/blender_python_api_current/>`__.
Edit Source
   For UI development -- Creates a text data-block with the source code associated with the control,
   in case the control is based on a Python script.
   In the Text Editor it points at the code line where the element is defined.
Edit Translation
   For UI development -- Points at the translation code line.

.. seealso::

   :doc:`/interface/common_shortcuts`.

   .. move paragraph there?


.. _ui-specials-menu:

Specials Menu
=============

The Specials pop-up menu contains a context-sensitive list of operators.
It is opened by a button with a down arrow on dark background |specials-button| or
with :kbd:`W` in most editors giving quick access to tools sensitive to the editor's mode.


.. _bpy.types.UIPieMenu:

Pie Menus
=========

A pie menu is a menu whose items are spread radially around the mouse.
Pie menus have to be activated in the User Preferences through
:menuselection:`Add-ons --> UI --> Pie Menus Official`.

.. figure:: /images/interface_controls_buttons_menus_pie-menu.png

   The shade pie menu.


Interaction
-----------

The pie menu is spawned by a key press,
which are listed in the :ref:`Add-on Preferences <user-prefs-addons-prefs>`.

Releasing the key without moving the mouse will keep the menu open and
the user can then move the mouse pointer towards the direction of a pie menu item and select it by clicking.
Releasing the key, after moving the mouse towards a pie menu item, will cause the menu to close and
the selected menu item to activate.

An open disc widget at the center of the pie menu shows
the current direction of the pie menu. The selected item is also highlighted.
A pie menu will only have a valid direction for item selection,
if the mouse is touching or extending beyond the disc widget at the center of the menu.

Pie menu items support key accelerators, which are the letters underlined on each menu item.
Also number keys can be used to select the items.

If there are sub-pies available, it is indicated by a plus icon.

See :ref:`Pie menu settings <prefs-pie-menu>`.
