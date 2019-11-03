.. (todo add) links
.. _bpy.types.NodeSocket:
.. _bpy.types.NodeTree:

**********
Node Parts
**********

All nodes in Blender are based off of a similar construction.
This applies to :ref:`any type of node <tab-node-tree-types>`.
These parts include the Title, Sockets, Preview and more.

.. figure:: /images/interface_controls_nodes_parts_overview.png


Title
=====

The *Title* shows the name/type of the node.
It can be overridden by changing the value of Label in the *Node* section of the *Sidebar region* :kbd:`N`.
On the left side of the title is the *collapse toggle*
which can be used to collapse the node this can also be done with :kbd:`H`.

.. figure:: /images/interface_controls_nodes_parts_collapsed.png

   How a node appears when collapsed.


.. _bpy.types.NodeLink:

Sockets
=======

The *Sockets* input and output values from the node.
They appear as little colored circles on either side of the node.
Unused sockets can be hidden with :kbd:`Ctrl-H`.
There are two kinds of sockets: `inputs`_ and `outputs`_.

Each socket is color-coded depending on what type of data it handles.

Color (yellow)
   Indicates that color information needs to be input or will be output from the node.
   Depending on the node tree type, the color has an alpha channel or not.
Numeric (gray)
   Indicates numeric value's information.
   It can either be a single numerical value or a so-called "value map".
   (You can think of a value map as a gray-scale map where the different amount of
   bright/dark reflects the value for each point.)
   If a single value is used as an input for a "value map" socket, all points of the map are set to this same value.
   Common use: Alpha maps and value options for a node.
Vector (blue)
   Indicates vector, coordinate and normal information.
Shader (green)
   Used for shaders in :doc:`Cycles </render/cycles/index>` and :doc:`Eevee </render/eevee/index>`.


Inputs
------

The *Inputs* are located on bottom left side of the node,
and provide the data the node needs to perform its function.
Each input socket, except for the green shader input, when disconnected,
has a default value which can be edited via a color, numeric, or vector interface input.
In the screenshot of the node above, the second color option is set by a color interface input.


Outputs
-------

The *Outputs* are located on the top right side of the node,
and can be connected to the input of nodes further down the node tree.


.. _bpy.types.NodeSetting:

Properties
==========

Many nodes have settings which can affect the way they interact with inputs and outputs.
Node settings are located below the outputs and above any inputs.

.. figure:: /images/interface_controls_nodes_parts_controls.png

   An example of the controls on the chroma key node.


Preview
-------

On some nodes this shows a preview image of how the output data for a certain channel will appear.
Usually it shows color data.

The preview can be toggled using the icon on the very top right-hand corner of the node, next to the title.

.. figure:: /images/interface_controls_nodes_parts_previewless.png

   How a node appears without the preview.
