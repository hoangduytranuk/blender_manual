
*********
Selecting
*********

By default Blender uses the :kbd:`LMB` to select items in the Blender window.
Alternatively, the :kbd:`RMB` can be used instead by changing
the :doc:`Preferences </editors/preferences/keymap>`.
Blender has several selecting tools that can be used across the different editors.


Selection Tools
===============

.. _tool-select-tweak:

Select Regular
--------------

.. admonition:: Reference
   :class: refbox

   :Hotkey:    :kbd:`LMB`

Clicking on an item selects it,
using modifier keys you can perform other operations.


.. _tool-select-box:
.. _bpy.ops.*.select_box:

Select Box
----------

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Select --> Box Select`
   :Hotkey:    :kbd:`B`

To activate the tool, press :kbd:`B` or click and drag :kbd:`LMB`.
With *Select Box* you draw a rectangle while holding down :kbd:`LMB`.
Any item that lies even partially within this rectangle becomes selected.
If any item that was last active appears in the selection it will become active.

For deselecting items, use :kbd:`MMB`.

.. list-table:: Box Select example.

   * - .. _fig-mesh-select-basics-start:

       .. figure:: /images/editors_3dview_toolbar_select-box_border-select1.png
          :width: 200px

          Start.

     - .. _fig-mesh-select-basics-selecting:

       .. figure:: /images/editors_3dview_toolbar_select-box_border-select2.png
          :width: 200px

          Selecting.

     - .. _fig-mesh-select-basics-complete:

       .. figure:: /images/editors_3dview_toolbar_select-box_border-select3.png
          :width: 200px

          Complete.


.. _bpy.ops.*.select_circle:
.. _tool-select-circle:

Select Circle
-------------

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Select --> Circle Select`
   :Hotkey:    :kbd:`C`

*Select Circle* :kbd:`C` is used by moving with dotted circle through item with :kbd:`LMB`.
You can select any item by touching of the circle area.
It is possible to dynamically change the diameter of circle by scrolling :kbd:`Wheel`
or with :kbd:`NumpadPlus` and :kbd:`NumpadMinus` as seen in pictures below.
Deselection is under the same principle -- :kbd:`MMB`.

.. list-table:: Circle Select example.

   * - .. figure:: /images/editors_3dview_toolbar_select-circle_circle-select1.png
          :width: 320px

          Start.

     - .. figure:: /images/editors_3dview_toolbar_select-circle_circle-select2.png
          :width: 320px

          Selecting.

     - .. figure:: /images/editors_3dview_toolbar_select-circle_circle-select3.png
          :width: 320px

          Dragging.


.. _bpy.ops.*.select_lasso:
.. _tool-select-lasso:

Select Lasso
------------

.. admonition:: Reference
   :class: refbox

   :Hotkey:    :kbd:`Ctrl-RMB`

Lasso select is used by drawing a dotted line around item to be selected.
To use this hold :kbd:`Ctrl-RMB` and simply draw around the items you want to select.

Lasso select adds to the previous selection. For deselection, use :kbd:`Shift-Ctrl-LMB`.

.. list-table:: An example of using the *Lasso Select tool* in *Vertex Select Mode*.

   * - .. figure:: /images/editors_3dview_toolbar_select-lasso_lasso-select1.png
          :width: 200px

          Start.

     - .. figure:: /images/editors_3dview_toolbar_select-lasso_lasso-select2.png
          :width: 200px

          Selecting.

     - .. figure:: /images/editors_3dview_toolbar_select-lasso_lasso-select3.png
          :width: 200px

          Complete.


Selecting Modes
===============

.. admonition:: Reference
   :class: refbox

   :Tool:      Select Tools
   :Panel:     :menuselection:`Tool Settings --> Mode`

Each tool has some sort of mode to configure how to tool interacts with existing selections.
Note that not every selection tool supports each of these modes.

Set
   Sets a new selection ignoring any existing selections.
Extend
   Adds newly selected items to the existing selection.
   The selection can also be extended by :kbd:`Shift-LMB`.
Subtract
   Removes newly selected items from the existing selection.
   Items can be removed from the selection by :kbd:`Shift-LMB` already selected items.
Invert
   Selects non-selected items and deselects existing selection.
   The selection can also be inverted by :kbd:`Ctrl-I`.
Intersect
   Selects items that intersect with existing selection.
