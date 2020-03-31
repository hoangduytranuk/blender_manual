
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
This can help provide a more familiar experience for artists
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


.. _hardware-head-mounted-displays:

Head-Mounted Displays (Virtual Reality)
=======================================

:abbr:`HMDs (Head-Mounted Displays)` make it possible to place users in an interactive, virtual environment.
Attached to the head, they track head movements to project a seemingly surrounding world onto small
screens in front of the user's eyes. If the system works well, they experience the virtual environment as
if they were really inside of it.


Supported Platforms
-------------------

Virtual reality support in Blender is implemented through the multi-platform OpenXR standard.
This standard is new and therefore support for it is still limited.

.. list-table:: OpenXR compatible platforms.
   :header-rows: 1

   * - Platform
     - Operating System
     - Notes
   * - `Windows Mixed Reality <https://www.microsoft.com/windows/windows-mixed-reality>`__
     - Windows
     - Requires the Windows 10 May 2019 Update (1903)
   * - `Oculus Rift <https://www.oculus.com/>`__
     - Windows
     - `Prototype Release <https://developer.oculus.com/blog/prototype-openxr-for-oculus/>`__
   * - `Monado <https://monado.dev/>`__
     - GNU/Linux
     - *Not* recommended for general use yet


Getting Started
---------------

The following subsections describe how an HMD can be set up for usage with the `supported platforms`_.
If this is not done, Blender will report an error when trying to start a virtual reality session.


Windows Mixed Reality
^^^^^^^^^^^^^^^^^^^^^

To check if a PC meets the requirements to run Windows Mixed Reality, Microsoft offers
the `Windows Mixed Reality PC Check <https://www.microsoft.com/en-us/p/windows-mixed-reality-pc-check/9nzvl19n7cnc>`__
application.

- Make sure the Windows 10 May 2019 Update (1903) is installed.
- If the system meets all requirements, the Mixed Reality Portal should already be installed.
  It is also available in
  the `Microsoft Store <https://www.microsoft.com/en-us/p/mixed-reality-portal/9ng1h8b3zc7m>`__.
  On first use it will guide through some setup steps.
- Launch the Mixed Reality Portal. Click the menu button ``...`` in the lower left corner.
  In the menu it opens, select the *Set up OpenXR*. Windows Mixed Reality is now ready to be used with OpenXR.

For more information, refer to Windows'
`Getting Started Guide for Windows Mixed Reality and OpenXR
<https://docs.microsoft.com/windows/mixed-reality/openxr#getting-started-with-openxr-for-windows-mixed-reality-headsets>`__.


Oculus Rift
^^^^^^^^^^^

Oculus only provides prototype OpenXR support. To use it, Blender has to be started in
a special way, as described below.

- Download and install the `Oculus Rift software <https://www.oculus.com/setup/>`__.
- Start Blender by double clicking the ``blender_oculus`` script inside the installation directory.
  It will open a command-line window with further information.


Monado
^^^^^^
Monado is a :doc:`free and open source </getting_started/about/license>` XR platform for Linux. It is not yet ready for
production usage and should only be used for testing purposes.

`There are packages available <https://launchpad.net/~monado-xr/+archive/ubuntu/monado>`__ for Debian based
distributions. For others it has to be compiled from source, which in this case is not recommended for people with
little experience in compiling software. Follow the `Getting Started Guides
<https://gitlab.freedesktop.org/monado/monado/-/blob/master/README.md>`__ from Monado to do so nevertheless.


Completing the Setup
--------------------

Inside Blender, the :doc:`VR Scene Inspection add-on </addons/3d_view/vr_scene_inspection>`
needs to be enabled to access virtual reality features.
