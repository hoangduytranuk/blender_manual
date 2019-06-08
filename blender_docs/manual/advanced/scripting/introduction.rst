
************
Introduction
************

Python is an interpreted, interactive,
object-oriented programming language. It incorporates modules, exceptions, dynamic typing,
very high-level dynamic data types, and classes.
Python combines remarkable power with very clear syntax.

Python scripts are a powerful and versatile way to extend Blender functionality.
Most areas of Blender can be scripted, including animation, rendering, import and export,
object creation and the scripting of repetitive tasks.

To interact with Blender, scripts can make use of
the tightly integrated :abbr:`API (Application Programming Interface)`.


General Information
===================

Links that are useful while writing scripts:

- `Python.org <https://www.python.org/>`__
  -- General information about Python.
- `Blender Python API <https://www.blender.org/api/current/>`__
  -- Official API documentation. Use this for referencing while writing scripts.
- `API Introduction <https://www.blender.org/api/current/info_quickstart.html>`__
  -- A short introduction to get you started with the API. Contains examples.


Links that deal with distributing your scripts:

- `Sharing scripts <https://wiki.blender.org/wiki/Process/Addons>`__
  -- Information on how to share your scripts and get them included in the official Blender distribution.
- `Creating Add-ons <https://wiki.blender.org/wiki/Process/Addons/Guidelines>`__
  -- Add-ons are used to encapsulate and distribute scripts.
- `Add-ons project <https://developer.blender.org/project/profile/3/>`__
  -- Project to maintain a central repository of extensions to Blender.


Getting Started
===============

.. rubric:: Manual links

The following links take you from the basics to the more advanced
concepts of Python scripting for Blender.

- :doc:`Text Editor </editors/text_editor>`
- :doc:`Python Console </editors/python_console>`
- Info Editor's :ref:`info-report-console`


.. rubric:: External links

Here are external links containing a lot of good information to start learning how to write scripts for Blender:

- `Introductory tutorial by Satish Goda
  <https://sites.google.com/site/satishgoda/blender/learningblender25/introduction-to-blender-python-api>`__
  Takes you from the beginning and teaches how to do basic API manipulations.
- `Ira Krakow's video tutorials <https://www.youtube.com/watch?v=vmhU_whC6zw>`__
  First video in a series of video tutorials.
- `Quickstart guide <https://en.wikibooks.org/wiki/Blender_3D:_Blending_Into_Python/2.5_quickstart>`__
  A quickstart guide for people who already have some familiarity with Python and Blender.
- `Examples thread <https://blenderartists.org/t/scripting-examples-for-2-5-update-mar-26th-2010/456132>`__
  A forum thread containing many short working script examples.
- `Introduction to Python
  <https://cgcookie.com/archive/introduction-to-scripting-with-python-in-blender/>`__
  A one-hour video tutorial introducing Python and the Blender API.


Extending Blender
=================

Add-ons
-------

Add-ons are scripts you can enable to gain extra functionality within Blender,
they can be enabled from the Preferences.

Outside of the Blender executable,
there are literally hundreds of add-ons written by many people:

- Officially supported add-ons are bundled with Blender.
- Other **Testing** add-ons are included in development builds but not official releases.
  Many of them work reliably and are very useful but are not ensured to be stable for release.

For an overview of all add-ons available, see
the `Scripts Catalog <https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts>`__.


Scripts
-------

Apart from add-ons, there are also scripts you can use to extend Blender's functionality:

- Modules: Utility libraries for import into other scripts.
- Presets: Settings for Blender's tools and key configurations.
- Startup: These files are imported when starting Blender.
  They define most of Blender's UI, as well as some additional core operators.
- Custom scripts: In contrast to add-ons they are typically intended for one-time execution via
  the :doc:`Text Editor </editors/text_editor>`.


Saving your own Scripts
-----------------------

File Location
^^^^^^^^^^^^^

All scripts are loaded from the ``scripts`` folder of
the :doc:`local, system and user paths </getting_started/installing/configuration/directories>`.

You can setup an additional search path for scripts in
:ref:`prefs-file-paths` :menuselection:`Preferences --> File Paths`.


Installation
^^^^^^^^^^^^

Add-ons are conveniently installed through Blender in the :doc:`Preferences </editors/preferences/addons>`.
Click the :menuselection:`Install from File...` button and select the ``.py`` or ``.zip`` file.

To manually install scripts or add-ons, place them in the ``add-ons``, ``modules``, ``presets``,
or ``startup`` directory according to their type. See the description above.

You can also run scripts by loading them in the :doc:`Text Editor </editors/text_editor>`.
