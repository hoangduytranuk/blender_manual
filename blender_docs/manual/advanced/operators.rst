
*********
Operators
*********

.. _bpy.ops.wm.debug_menu:

Debug Menu
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Menu:      None
   :Hotkey:    :kbd:`Ctrl-Alt-D`

This operator brings up a menu to set Blender into a certain debug mode.

There are several possible values, for example the most useful, a value of ``256``
enables a debug panel in Cycles render settings that can be used to enable/disable
special kernels and other special debugging features.

.. tip::

   Developers can search the code for ``G.debug_value`` to find other possible uses for this operator.

.. note::

   Additional debug options are available by launching Blender in debug mode or setting ``bpy.app.debug = True``.


.. _bpy.ops.wm.redraw_timer:

Redraw Timer
============

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Menu:      None
   :Hotkey:    :kbd:`Ctrl-Alt-T`

This operator brings up a menu with a list of tests to benchmark UI drawing along with undo/redo functions.


.. _bpy.ops.wm.memory_statistics:

Memory Statistics
=================

.. admonition:: Reference
   :class: refbox

   :Mode:      ``--debug-memory``
   :Menu:      None
   :Hotkey:    None

This operator which can be found by searching "Memory Statistics" from
the :doc:`Operator Search </interface/controls/templates/operator_search>`
will print useful information about memory objects, their size and user count.

.. important::

   To fully use this operator run Blender from the console with ``--debug-memory``.


.. _bpy.ops.wm.dependency_relations:

Dependency Relations
====================

.. admonition:: Reference
   :class: refbox

   :Mode:      ``--debug-depsgraph``
   :Menu:      None
   :Hotkey:    None

This operator which can be found by searching "Dependency Relations" from
the :doc:`Operator Search </interface/controls/templates/operator_search>`
will print the relations for every scene and object in the blend-file.

.. important::

   This operator will only work if Blender is started from the console with ``--debug-depsgraph``.

