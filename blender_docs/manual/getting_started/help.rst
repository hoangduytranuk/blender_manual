
***********
Help System
***********

Blender has a range of built-in and web-based help options.


Tooltips
========

.. figure:: /images/getting-started_help_tooltip.png

   Tooltip of the Renderer selector in the Info Editor.

When hovering the mouse cursor over a button or setting, after a few instants a tooltip appears.


Elements
--------

The context-sensitive Tooltip might contain some of these elements:

Short Description
   Related details depending on the control.
Shortcut
   A keyboard or mouse shortcut associated to the tool.
Value
   The value of the property.
Library
   Source file of the active object. See also :doc:`/data_system/linked_libraries`.
Disabled (red)
   The reason why the value is not editable.
Python
   For :ref:`scripting <scripting-index>` -- A Python command associated to
   the control (usually an operator or property).


.. _help-manual-access:

Context-Sensitive Manual Access
===============================

.. admonition:: Reference
   :class: refbox

   :Mode:      All modes
   :Menu:      :kbd:`RMB`, :menuselection:`Online Manual`
   :Hotkey:    :kbd:`Alt-F1`

You may want to access help for a tool or area from within Blender.

Use the key-shortcut, or context menu to visit pages from this reference manual within Blender.
This opens a webpage relating to the button under the cursor, supporting both tool and value buttons.

.. note::

   We do not currently have 100% coverage,
   you may see an alert in the info header if some tools do not have a link to the manual.

   Other times buttons may link to more general sections of the documentation.


.. _help-menu:

Help Menu
=========

The *Help* menu in the Info Editor header.

.. figure:: /images/getting-started_help_menu.png
   :align: right

   Help menu.


Web Links
---------

The first options of this menu provide direct links to Blender-related websites:
The same links can also be found in the :ref:`splash`.

Manual
   This is a link to the :doc:`Official Blender Manual </index>`
   which you are now reading.
Release Log
   The `release notes <https://www.blender.org/features/releases/>`__ on the Web
   for the changes made for the current Blender version.
Blender Website
   The `blender.org <https://www.blender.org/>`__ home page.
Blender Store
   The `Blender Store <https://store.blender.org/>`__, where you can buy
   Training DVD's, books, t-shirts and other products.
Developer Community
   The *blender.org* `Get Involved <https://www.blender.org/get-involved/>`__ page.
   This is the launch page for Blender software development, bug tracking, patches and scripts,
   education and training, documentation development and functionality research.
User Community
   Lists of many different `support venues <https://www.blender.org/support/user-community/>`__.
Report a Bug
   The `Blender Bug Tracker <https://developer.blender.org/maniphest/task/edit/form/1/>`__ (registration needed).

.. tip:: Browser and Internet Connection

   Some forms of Help start up your web browser and access the Blender Foundation's web servers.
   In order to do this, you must have configured a default web browser for your Operating System,
   and have a connection to the Internet.


Scripting Reference
-------------------

Python API Reference
   Python application programming interface (API)
   `Reference <https://www.blender.org/api/blender_python_api_current/>`__.
Operator Cheat Sheet
   Creates the ``OperatorList.txt`` text data-block, which you can access in the *Text Editor*.
   You can also use Blender Search to generate the file. It lists the available Python operators.


.. _help-system-info:

Save System Info
----------------

Access :menuselection:`Help --> Save System Info`.

This extracts system information which can be useful to include in bug reports,
inspecting the configuration or diagnosing problems.

You will be prompted to save a text file ``system-info.txt``.

The text file contains sections:

Blender
   This section shows you the Blender version, details about the build configuration,
   and the path in which Blender is running.
Python
   The Python version you are using, showing the paths of the Python programming language paths.
Directories
   Paths used for scripts, data files, presets and temporary files.

   Those directories are configured using the :doc:`User Preferences </preferences/file>` Editor.
OpenGL
   This section shows the OpenGL version, the name of the manufacturer,
   and lists the capabilities of your hardware and driver.


Splash Screen
-------------

Shows the :ref:`splash`.
