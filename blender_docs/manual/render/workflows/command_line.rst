
************
Command Line
************

In some situations we want to increase the render speed,
access Blender remotely to render something or build scripts that use the command line.

One advantage of using the command line is that we do not need a graphical display
(no need for X server on Linux for example)
and consequently we can render via a remote shell (typically SSH).

See :doc:`Command Line Arguments </advanced/command_line/arguments>`
for a full list of arguments
(for example to specify which scene to render, the end frame number, etc.), or simply run:

.. code-block:: sh

   blender --help

.. note::

   Arguments are executed in the order they are given!

   The following command will not work, since the output and extension are set after Blender is told to render:

   .. code-block:: sh

      blender -b file.blend -a -x 1 -o //render

   The following command will behave as expected:

   .. code-block:: sh

      blender -b file.blend -x 1 -o //render -a

   **Always** position ``-f`` or ``-a`` as the last arguments.


Platforms
=========

How to actually execute Blender from the command line depends on the platform and where you
have installed Blender. Here are basic instructions for the different platforms.


Linux
-----

Open a terminal, then go to the directory where Blender is installed,
and run Blender like this:

.. code-block:: sh

   cd <blender installation directory>
   ./blender

If you have Blender installed in your ``PATH``
(usually when Blender is installed through a distribution package), you can simply run:

.. code-block:: sh

   blender


macOS
-----

Open the terminal application, go to the directory where Blender is installed,
and run the executable within the app bundle, with commands like this:

.. code-block:: sh

   cd /Applications/Blender
   ./blender.app/Contents/MacOS/blender

If you need to do this often,
you can make an alias so that typing just ``blender`` in the terminal works.
For that you can run a command like this in the terminal (with the appropriate path).

.. code-block:: sh

   echo "alias blender=/Applications/Blender/blender.app/Contents/MacOS/blender" >> ~/.bash_profile

If you then open a new terminal, the following command will work:

.. code-block:: sh

   blender


MS-Windows
----------

Open the Command Prompt, go to the directory where Blender is installed,
and then run Blender:

.. code-block:: bat

   cd c:\<blender installation directory>
   blender

You can also add the Blender folder to your system ``PATH`` so that do you do not have to ``cd`` to it each time.


Examples
========

Single Image
------------

.. code-block:: sh

   blender -b file.blend -f 10

``-b``
   Render in the background (without UI).
``file.blend``
   Path to the blend-file to render.
``-f 10``
   Render only the 10th frame.

.. code-block:: sh

   blender -b file.blend -o /project/renders/frame_##### -F EXR -f -2

``-o /project/renders/frame_#####``
   Path of where to save the rendered image, using five padded zeros for the frame number.
``-F EXR``
   Override the image format specified in the blend-file and save to an OpenEXR image.
``-f -2``
   Render only the second last frame.

.. warning::

   Arguments are case sensitive! ``-F`` and ``-f`` are not the same.


Animation
---------

.. code-block:: sh

   blender -b file.blend -a

``-a``
   Render the whole animation using all the settings saved in the blend-file.

.. code-block:: sh

   blender -b file.blend -E BLENDER_RENDER -s 10 -e 500 -t 2 -a

``-E BLENDER_RENDER``
   Use the "Blender Render" engine.
   For a list of available render engines, run ``blender -E help``.
``-s 10 -e 500``
   Set the start frame to ``10`` and the end frame to ``500``.
``-t 2``
   Use only two threads.
