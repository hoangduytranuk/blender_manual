
************
Introduction
************

The different node editors are used to work with node-based workflows.
Each node editor type has there own specific purpose, so,
here we will only give an overview of what the generic node editor is.
In the list below it shows a list of different types of node trees and where each is documented.

.. figure:: /images/editors_node-editor_introduction_example.jpg

   Example of a node editor.

.. _tab-node-tree-types:

.. list-table::
   :header-rows: 1
   :class: valign
   :widths: 10 30 60

   * - Icon
     - Name
     - Documentation
   * - .. figure:: /images/editors_node-editor_introduction_icons-material.png
     - Material Nodes
     - :doc:`Cycles </render/shaders/nodes/index>` and
       :doc:`Eevee </render/engines/eevee/materials/nodes/index>`.
   * - .. figure:: /images/editors_node-editor_introduction_icons-render-layers.png
     - Composite Nodes
     - Documentation can be found in the :doc:`Compositing </compositing/index>` section.
   * - .. figure:: /images/editors_node-editor_introduction_icons-texture.png
     - Texture Nodes
     - Texture Nodes are covered
       in the :doc:`UV editor </editors/texture_node/introduction>` docs.

After choosing what node context you want to use, you have to enable nodes with the *Use Nodes* button.


Editor Interface
================

Header
------

The *Header* contains various menus, buttons and options, partially based on the current node tree type.

.. figure:: /images/editors_node-editor_introduction_header.png

   Common node editor header options.

View
   This menu changes your view of the editor.
Select
   This menu allows you to select a node or groups of nodes.
Add
   This menu allows you to add nodes.
Node
   This menu allows you to do things with selected nodes.
Use Nodes
   Tells the render engine to use the node map in computing the material color or rendering the final image,
   or not. If not, the map is ignored and the basic render of the material tabs or scene is accomplished.
Use Pinned
   When enabled, the editor will retain the material or texture, even when the user selects a different object.
   A node tree can then be edited independent of the object selection in the 3D View.
Go to Parent button
   This button allows you go to parent node tree e.g. leaving a group.


Toolbar
-------

The *Toolbar* is a context-sensitive region, natively containing tools for the Grease Pencil
and buttons for adding nodes. The Toolbar is organized using tabs.


Sidebar
-------

The *Sidebar* region contains properties for the current selected node as well as node editor specific settings.


Navigating
==========

Navigating the node editors is done with the use of both mouse movement and keyboard shortcuts.

Pan :kbd:`MMB`
   Move the view up, down, left and right.
Zoom :kbd:`Ctrl-MMB`, :kbd:`Wheel`
   Move the camera forwards and backwards.
View Selected
   :kbd:`NumpadPeriod`
View All
   :kbd:`Home`


Adding Nodes
============

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Tool Shelf`
   :Menu:      :menuselection:`Add`
   :Hotkey:    :kbd:`Shift-A`

Nodes are added in two ways to the node editors:

#. By using the Tool Shelf which has buttons for adding nodes, organized with tabs.
#. By using the :menuselection:`Add` menu :kbd:`Shift-A`.
