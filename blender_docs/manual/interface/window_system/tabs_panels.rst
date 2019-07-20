
*************
Tabs & Panels
*************

Tabs
====

.. figure:: /images/interface_window-system_tabs-panels_tabs.png
   :align: right
   :figwidth: 300px

   Top: Horizontal Tab header in the Topbar.
   Bottom: Vertical Tab header shows tab icons in the Properties Editor.

Tabs are used to control overlapping sections in the user interface.
Contents of only one Tab is visible at a time.
Tabs are listed in *Tab header*, which can be vertical or horizontal.


Switching/Cycling
-----------------

Vertical tabs can be switched with :kbd:`Ctrl-Wheel` from anywhere in
the region, and horizontal tabs with mouse cursor over tab headings.

You can also cycle through tabs with :kbd:`Ctrl-Tab` and
:kbd:`Shift-Ctrl-Tab`, or press down :kbd:`LMB` and move mouse over
tab header icons.

.. container:: lead

   .. clear


.. _ui-panels:
.. _bpy.types.Panel:

Panels
======

.. figure:: /images/interface_window-system_tabs-panels_panels.png
   :align: right
   :figwidth: 200px

   Panels in Properties editor.

   A panel is highlighted in yellow and a sub-panel in red.

The smallest organizational unit in the user interface is a panel.
*Panel header* is always visible, and it shows the title for the panel.
Panels may also include sub-panels.


Collapsing and Expanding
------------------------

Panels can be expanded to show, and collapsed to hide its contents,
shown by a triangle on the panel header. Collapsed panel is indicated
by down-arrow (▼) and expanded panel by right-arrow (►).

- A click with the :kbd:`LMB` on the panel header expands or collapses it.
- Pressing :kbd:`A` expand/collapses the panel under the mouse pointer.
- A :kbd:`Ctrl-LMB` click on the header of a specific panel will collapse
  all other panels and make this the only expanded one.
- Dragging with :kbd:`LMB` over the headers will expand or collapse many at once.


Position
--------

You can change the position of a panel within its region by clicking
and dragging it with the :kbd:`LMB` on the grip widget (\:\:\:\:)
located in Panel Header on the right side.


Pinning
-------

Sometimes it is desirable to view panels from different tabs at the same time.
This has been solved by making panels pinnable.

A pinned panel remains visible regardless of which tab has been selected.
You can pin a panel by clicking on the pin icon in its header.
Panels that do not have a pin icon can also be pined by :kbd:`RMB` and selecting *Pin*,
alternatively you use :kbd:`Shift-LMB` on the panel to also pin it.


Zoom
----

The zoom factor of a whole region with panels can be changed by
:kbd:`Ctrl-MMB` clicking and moving the mouse anywhere within that region
or use the :kbd:`NumpadPlus` and :kbd:`NumpadMinus` to zoom in and out the contents.
Pressing :kbd:`Home` (Show All) will reset the zooming at the screen/panel focused by the mouse pointer.
