
***********************
Configuring Peripherals
***********************

Displays
========

A full HD display or higher is recommended.
Multi-monitor setups are supported, and workspaces can be configured to span multiple monitors.

.. figure:: /images/getting-started_configuration_hardware_multi-monitor.jpg

   Example of Blender's multi-monitor support.


Input Devices
=============

Blender supports various types of input devices:

- Keyboard (recommended: keyboard with numeric keypad, English layout works best)
- Mouse (recommended: three button mouse with scroll wheel)
- NDOF Device (also known as *3D Mouse*)
- Graphic Tablet

.. note::

   If you are missing an input device such as a mouse or numpad Blender
   can change its :doc:`keymap </interface/keymap/blender_default>` to emulate these devices.
   Settings to enable this can be found in the :doc:`Input Preferences </editors/preferences/input>`.


Mouse
-----

Mouse Button Emulation
^^^^^^^^^^^^^^^^^^^^^^

If you do not have a 3 button mouse,
you will need to emulate it by checking the option in the :doc:`Preferences </editors/preferences/input>`.

The following table shows the combinations used:

.. list-table::
   :stub-columns: 1

   * - 3-button Mouse
     - :kbd:`LMB`
     - :kbd:`MMB`
     - :kbd:`RMB`
   * - 2-button Mouse
     - :kbd:`LMB`
     - :kbd:`Alt-LMB`
     - :kbd:`RMB`


Keyboard
--------

Numpad Emulation
^^^^^^^^^^^^^^^^

If you do not have a numeric Numpad on the side of your keyboard,
you may want to emulate one (uses the numbers at the top of the keyboard instead,
however, removes quick access to layer visibility).

.. seealso::

   Read more about *Numpad Emulation* in the :doc:`Preferences </editors/preferences/input>`.


Non-English Keyboards
^^^^^^^^^^^^^^^^^^^^^

If you use a keyboard with a non-English keyboard layout, you still may benefit from switching
your computer to the UK or US layout as long as you work with Blender.

.. note::

   You can also change the default keymap and
   default hotkeys from the :doc:`Preferences </editors/preferences/input>`,
   however, this manual assumes you are using the default keymap.


.. _hardware-tablet:

Graphic Tablet
--------------

Graphics tablets can be used to provide a more traditional method of controlling the mouse cursor using a pen.
This can help to provide a more familiar experience for artists
who are used to painting and drawing with similar tools,
as well as provide additional controls such as pressure sensitivity.

.. note::

   If you are using a graphic tablet instead of a mouse and pressure sensitivity does not work properly,
   try to place the mouse pointer in the Blender window and then unplug/replug your graphic tablet. This might help.


.. _hardware-ndof:

NDOF (3D Mouse)
---------------

3D mice or :abbr:`NDOF (N-Degrees of Freedom)` devices are hardware that you can use to navigate a scene in Blender.
Currently only devices made by 3Dconnexion are supported.
These devices allow you to explore a scene, as well as :ref:`Fly/Walk modes <3dview-fly-walk>`.

.. seealso::

   See :doc:`Input Preference </editors/preferences/input>` for more information on configuring peripherals.
