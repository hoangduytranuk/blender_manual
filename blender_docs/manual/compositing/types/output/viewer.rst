.. _bpy.types.CompositorNodeViewer:

***********
Viewer Node
***********

.. figure:: /images/compositing_types_output_viewer_node.png
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
   the viewer node (*Properties* panel in Properties region, with the viewer node selected):

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
   (last selected, indicated with a slightly darker header) will be shown on the backdrop or in the UV/Image editor.


Using the UV/Image Editor
=========================

The viewer node allows results to be displayed in the UV/Image Editor.
The image is facilitated in the header by selecting *Viewer Node* in the linked *Image* data-block menu.
The UV/Image Editor will display the image from the currently selected viewer node.

To save the image being viewed,
use :menuselection:`Image --> Save As Image`, :kbd:`F3` to save the image in a file.

The UV/Image Editor also has three additional options in its header to view Images with or
without Alpha, or to view the Alpha or Z itself.
Holding :kbd:`LMB` in the Image display allows you to sample the values.
