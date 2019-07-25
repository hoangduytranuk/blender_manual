.. _bpy.ops.view3d.ruler:
.. _tool-measure:

*******
Measure
*******

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Menu:      :menuselection:`Toolbar --> Measure`

The ruler is an interactive tool where you can drag lines in the scene to measure distances or angles.
Optionally snapping to geometry could be activated for better accuracy or to measure wall thickness.
The ruler can be accessed from the Toolbar.

.. figure:: /images/editors_3dview_toolbar_measure_ruler-example.png

   Example of the ruler and protractor.


Usage
=====

Here are common steps for using the ruler:

#. Activate the Ruler from the Toolbar.
#. Click and drag in the viewport to define the initial start/end point for the ruler.
#. Orbit the view and click on either end of the ruler to re-position it.
   Holding :kbd:`Ctrl` enables snap to elements.
#. Click on the middle to measure angles.
#. Press :kbd:`Return` to store the ruler for later use or :kbd:`Esc` to cancel.

.. note::

   Editing operations can be used while the ruler is running,
   however, tools like the knife cannot be used at the same time.

.. note::

   Unit settings and scale from the scene are used for displaying dimensions.


Shortcuts
=========

- :kbd:`Ctrl-LMB` Adds new ruler.
- :kbd:`LMB` Drag end points to place them, hold :kbd:`Ctrl` to snap, hold :kbd:`Shift` to measure thickness.
- :kbd:`LMB` Drag the center point to measure angles, drag out of the view to convert back to a ruler.
- :kbd:`Delete` Deletes the ruler.
- :kbd:`Ctrl-C` Copies the rulers value to the clipboard.
- :kbd:`Esc` Exit tool.
- :kbd:`Return` Saves the rulers for the next time the tool is activated.
