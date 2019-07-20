
*******
Startup
*******

Blender
=======

There are some common causes for problems when using Blender. If you cannot find a solution to your problem here,
try asking the :doc:`community </getting_started/about/community>` for help.

If Blender crashes on startup, there are a few things to check for:

- See if your computer meets the `minimum requirements <https://www.blender.org/download/requirements/>`__.
- Confirm that your graphics card is supported and that the drivers are up to date.
- Make sure you are using the correct Blender version (32 or 64 bit) for your architecture.

Known causes listed below.


Python
======

If you get an error on startup like:

.. code-block:: python

   Fatal Python error: Py_Initialize: unable to load the file system codec

you may have set your system's ``PYTHONPATH`` environment variable.

In this case, Blender's bundled Python will attempt to use the ``PYTHONPATH``.
If the Python version is different from the version used by Blender, this will crash Blender on startup.

To solve the problem, either clear the ``PYTHONPATH`` before starting Blender
(can also be done with a launcher script),
or set it to a compatible Python version.


Common Startup Messages
=======================

The *Blender Console Window* can display many different types of status and error messages.
Some messages simply inform the user what Blender is doing, but have no real impact on Blender's ability to function.
Other messages can indicate serious errors that will most likely prevent Blender carrying out a particular task and
may even make Blender non-responsive or shut down completely. The *Blender Console Window* messages can
also originate internally from within the Blender code or from external sources such as
:doc:`Python scripts </editors/preferences/addons>`.

``found bundled python: {DIR}``
   This message indicates that Blender was able to find the :ref:`Python <scripting-index>`
   library for the Python interpreter embedded within Blender.
   If this folder is missing or unable to be found,
   it is likely that an error will occur, and this message will not appear.

``Read prefs: {DIR}/userpref.blend``
   The user preferences use this path.
