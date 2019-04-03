
*************
Tabs & Panels
*************

Tabs
====

.. figure:: /images/interface_window-system_tabs-panels_tabs_tabs-horizontal.png

   Horizontal tab header.

.. figure:: /images/interface_window-system_tabs-panels_tabs-vertical.png
   :align: right

   Tools tab (selected), Create, etc.

Tabs are overlapping sections in the user interface.
The Tabs header can be vertical (Tool Shelf) or
horizontal (Properties Editor, User Preferences).


Switching/Cycling
-----------------

Vertical tabs can be switched with the :kbd:`Wheel` within the tab header and
:kbd:`Ctrl-Wheel` changes tabs from anywhere in the region.

You can also cycling through tabs with :kbd:`Ctrl-Tab` and :kbd:`Shift-Ctrl-Tab`.

.. container:: lead

   .. clear


.. _ui-panels:
.. _bpy.types.Panel:

Panels
======

.. figure:: /images/interface_window-system_tabs-panels_panels.png
   :align: right

   Tool Shelf panels.

   Orange: Panel Headers.

The smallest organizational unit in the user interface is a panel.
Panels can be collapsed to hide its contents.
They are used in the *Properties Editor*, but also
for example in the *Tool Shelf* and the *Properties region*.

In the image on the right there are three panels: *Transform*, *Edit* and *History*.
The *Edit* panel is expanded and the other two panels are collapsed.


Collapsing and Expanding
------------------------

A triangle on the left of the title shows the expanded (▼) and collapsed (►) state of the panel.

- A click with the :kbd:`LMB` on the panel header expands or collapses it.
- Pressing :kbd:`A` expand/collapses the panel under the mouse pointer.
- A :kbd:`Ctrl-LMB` click on the header of a specific panel will collapse
  all other panels and make this the only expanded one.
- Dragging with :kbd:`LMB` over the headers will expand or collapse many at once.


Position
--------

You can change the position of a panel within its region by clicking and
dragging it with the :kbd:`LMB` on the grip widget (\:\:\:\:) in the upper right corner.


Pinning
-------

Often it is desirable to view panels from different tabs at the same time.
This has been solved by making panels pinnable.

A pinned panel remains visible regardless of which tab has been selected.
You can pin a panel by :kbd:`Shift` clicking its header,
or by :kbd:`RMB` clicking on the header and choosing *Pin* in the context menu.

In the image shown to the right,
is an example of the *Mesh Options* pinned in the tools tab.


Zoom
----

The zoom factor of a whole region with panels can be changed by
:kbd:`Ctrl-MMB` clicking and moving the mouse anywhere within that region
or use the :kbd:`NumpadPlus` and :kbd:`NumpadMinus` to zoom in and out the contents.
Pressing :kbd:`Home` (Show All) will reset the zooming at the screen/panel focused by the mouse pointer.


Alignment
---------

The alignment of the panels in the *Properties Editor* can be changed
between vertical and horizontal. To do this click with :kbd:`RMB` somewhere
within the main region of the *Properties Editor* and choose either
*Horizontal* or *Vertical* from the appearing menu. Keep in mind though that
the panels are optimized for vertical alignment.
