.. _bpy.types.CompositorNodeViewer:

***********
Viewer Node
***********

.. figure:: /images/compositing_node-types_CompositorNodeViewer.png
   :align: right

   Viewer Node.

The *Viewer* node is a temporary, in-process viewer.
It could be plug in anywhere to inspect an image or value map in your node tree.

Select a view node with :kbd:`LMB` to switch between multiple view nodes.
It is possible to automatically plug a Viewer node to any other node
by pressing :kbd:`Shift-Ctrl-LMB` on it.


Inputs
======

See :doc:`Composite Node </compositing/types/output/composite>`.


Properties
==========

Tile order
   The tile order can be defined for the backdrop image, using the *Tile order* field in the properties of
   the viewer node (*Properties* panel in Sidebar region, with the viewer node selected):

   Rule of thirds
      Calculates tiles around each of the nine zones defined by the *rule of thirds*.
   Bottom up
      Tiles are calculated from the bottom up.
   Random
      Calculates tiles in a non-specific order.
   Center
      Calculates the tiles around a specific center, defined by X and Y fields.

      X, Y


Outputs
=======

This node has no output sockets.

.. note::

   It is possible to add multiple Viewer nodes, though only the active one
   (last selected, indicated with a slightly darker header) will be shown on the backdrop or in the Image editor.


Using the Image Editor
======================

The viewer node allows results to be displayed in the Image Editor.
The image is facilitated in the header by selecting *Viewer Node* in the linked *Image* data-block menu.
The Image Editor will display the image from the currently selected viewer node.

To save the image being viewed,
use :menuselection:`Image --> Save As...`, :kbd:`Shift-S` to save the image in a file.

The Image Editor also has three additional options in its header to view Images with or
without Alpha, or to view the Alpha or Z itself.
Click and holding the mouse in the Image display allows you to sample the values.
