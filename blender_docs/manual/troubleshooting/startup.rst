
*******
Startup
*******

Blender
=======

There are some common causes for problems when using Blender. If you cannot find a solution to your problem here,
try asking the :doc:`community </getting_started/about/community>` for help.

If Blender crashes on startup, there are a few things to check for:

- See if your computer meets the `minimum requirements <https://www.blender.org/download/requirements/>`__.
- Confirm that your graphics card is supported and that the drivers support at least OpenGL 2.1.
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
