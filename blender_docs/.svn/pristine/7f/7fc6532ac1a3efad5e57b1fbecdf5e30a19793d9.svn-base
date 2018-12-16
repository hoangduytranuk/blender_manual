
*****************
BAM Asset Manager
*****************

Refactoring linked blend-files is a common practice in a production environment.
While some basic operations can be accomplished within Blender,
sometimes it is more practical to perform them on the command line or via a script.
During the production of Cosmos Laundromat (Gooseberry Open Movie Project)
the *BAM Asset Manager* (BAM) was developed. The original scope of BAM included
client-server asset management tools going beyond Blender,
but it was later refocused on core utilities to perform two operations:

#. Blend-file packing
#. Automatic dependencies remapping

The following section of the manual focuses on how to use BAM.

.. figure:: /images/pipeline_bam_chart.png
   :align: center

   Asset manager.


Installing BAM
==============

BAM is a standalone Python package, that can be run on any system without any particular configuration.
The only requirement is Python 3 (and pip, the Python package manager, to easily install BAM).

Windows, Linux and macOS provide different ways to install Python 3 and pip.
Check out the online docs to learn more about a specific platform.

Once Python 3 and pip3 are available, BAM can be installed via command line by typing:

.. code-block:: bash

   pip3 install blender-bam

After a successful installation, the ``bam`` command will be available.
By typing it and pressing :kbd:`Enter`, all the available subcommands will be displayed.


bam pack
========

This command is used for packing a ``.blend`` file and *all*
its dependencies into a ``.zip`` file for redistribution. ::

   usage: bam pack [-h] [-o FILE] [-m MODE] [-e PATTERNS] [-a] [-q] [-c LEVEL]
                paths [paths ...]

You can simply pack a blend-file like this to create a zip-file of the same name.

.. code-block:: sh

   bam pack /path/to/scene.blend

You may also want to give an explicit output directory.
The example shows how to pack a blend with maximum compression for online downloads.

.. code-block:: sh

   bam pack /path/to/scene.blend --output my_scene.zip --compress=best

The command provides several options to adapt to different workflows
(final distribution, partial extraction, rendering).

``-o``, ``--output`` ``<FILE>``
   Output file or a directory when multiple inputs are passed.
``-m``, ``--mode`` ``<MODE>``
   Output file or a directory when multiple inputs are passed. Possible choices: ``ZIP``, ``FILE``.
``-e``, ``--exclude`` ``<PATTERN(S)>``
   Optionally exclude files from the pack.

   ``--exclude="*.png"``
      Using Unix shell-style wild-cards *(case insensitive)*.
   ``--exclude="*.txt;*.avi;*.wav"``
      Multiple patterns can be passed using the ``;`` separator.
``-a``, ``--all-deps``
   Follow all dependencies (unused indirect dependencies too).
``-q``, ``--quiet``
   Suppress status output.
``-c``, ``--compress`` ``<LEVEL>``
   Compression level for resulting archive.
   Possible choices: ``default``, ``fast``, ``best``, ``store``.
``--repo`` ``<DIR PATH>``
   Specify a "root" path from where to pack the selected file.
   This allows for the creation of a sparse copy of the production tree, without any remapping.
``--warn-external``
   Report external libraries errors (missing paths).


Examples
--------

Consider the following directory layout,
and in particular the file *01_01_A.lighting.blend* with its linked libraries.

.. code-block:: none

   ~/agent327/
   └─ lib/
      ├─ chars/
      |  ├─ agent.blend  ------------->|
      |  ├─ boris.blend  ------------->|
      |  └─ barber.blend               |
      └─ scenes/                       |
         ├─ 01-opening                 |
         ├─ 01_01_A.lighting.blend  <--|  < BAM pack this file
         └─ 01_01_A.anim.blend  ------>|

Once we run ``bam pack /scenes/01-opening/01_01_A.lighting.blend``
we obtain a *01_01_A.lighting.zip* inside of which we find the following structure.

.. code-block:: none

   ~/01_01_A.lighting
      ├─ 01_01_A.lighting.blend
      └─ __/
         ├─ 01_01_A.anim.blend
         └─ __/
            └─ lib/
               └─ chars/
                  ├─ agent.blend
                  └─ boris.blend

Note how all paths have been remapped relative to the placement
of *01_01_A.lighting.blend* in the root of the output.
If we run ``bam pack /scenes/01-opening/01_01_A.lighting.blend --repo ~/agent327``,
the output will be different.

.. code-block:: none

   ~/01_01_A.lighting
      ├─ lib/
      |  └─ chars/
      |     ├─ agent.blend
      |     └─ boris.blend
      └─ scenes
         └─ 01-opening/
            ├─ 01_01_A.lighting.blend  < The BAM packed file
            └─ 01_01_A.anim.blend

In this case no path is remapped, and we simply strip out any file
that is not referenced as a direct or indirect dependency of *01_01_A.lighting.blend*.
This is effectively a sparse copy of the original production tree.


bam remap
=========

Remap blend-file paths::

   usage: bam remap [-h] {start,finish,reset} ...

This command is a three step process:

#. First run ``bam remap start .`` which stores the current state of your project (recursively).
#. Then re-arrange the files on the file system (rename, relocate).
#. Finally run ``bam remap finish`` to apply the changes, updating the ``.blend`` files internal paths.

.. code-block:: sh

   cd /my/project

   bam remap start .
   mv photos textures
   mv barbershop_v14_library.blend barberhop_libraray.blend
   bam remap finish

.. note::

   Remapping creates a file called ``bam_remap.data`` in the current directory.
   You can relocate the entire project to a new location but on executing ``finish``,
   this file must be accessible from the current directory.

.. note::

   This command depends on files unique contents,
   take care not to modify the files once remap is started.


Subcommands
-----------

remap start
^^^^^^^^^^^

Start remapping the blend-files::

   usage: bam remap start [-h] [-j] [paths [paths ...]]

``-j``, ``--json``
   Generate JSON output.


remap finish
^^^^^^^^^^^^

Finish remapping the blend-files::

   usage: bam remap finish [-h] [-r] [-d] [-j] [paths [paths ...]]

``-r``, ``--force-relative``
   Make all remapped paths relative (even if they were originally absolute).
``-d``, ``--dry-run``
   Just print output as if the paths are being run.
``-j``, ``--json``
   Generate JSON output.


remap reset
^^^^^^^^^^^

Cancel path remapping::

   usage: bam remap reset [-h] [-j]

``-j``, ``--json``
   Generate JSON output.
