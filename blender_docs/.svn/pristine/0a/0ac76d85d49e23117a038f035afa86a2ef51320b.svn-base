
*********************
GoB (GoZ) for Blender
*********************

:Name: GoB
:Location: :menuselection:`Top info panel --> two buttons Import/Export`
:Version: 3.0.6
:Blender: 2.80
:Category: Import-Export
:Author: Stunton, JoseConseco, kromar
:Link: https://github.com/JoseConseco/GoB/releases

ZBrush is a very powerful sculpting/painting program. With this ZBrush/Blender applink script you can easily move your objects and textures between these two programs.

Features
========

You can transfer:

- Objects (only meshes)
- Polypainting
- UVs
- Mask
- Polygroup
- Diffuse map
- Normal map
- Displacement map
- Polyfroups from Materials
- Polyfroups from Uv's


Installation
============

#. Install the GoB addon for blender (follow steps from 'Configure Blender') and activate.
#. Put the 'Blender' folder directly inside the GoZApps folder at this path. ``Windows: C:/Users/Public/Pixologic/GoZApps`` ``Macintosh: /Users/Shared/Pixologic/GoZApps``
#. Re-install GoZ_for_ZBrush_Installer_WIN for Zbrush from here: ``C:\Program Files\Pixologic\ZBrush 2019\Troubleshoot Help\GoZ_for_ZBrush_Installer_WIN.exe``
#. Launch ZBrush 2019.1 and run GoZ once and choose your blender install location.


Configure Blender
=================

.. note::

   If you have a previous version, remove it via the Addon panel
   (unroll the GoB entry and remove it) before continuing.

Github breaks (changes) name of zip file and the first (root) folder inside zip,
when you download addon. Both zip file and first folder inside should be named:
'GoB' The addon final location should look like this:
``-C:/Users/XXXXX/AppData/Roaming/Blender Foundation/Blender/2.80/scripts/addons/GoB``

#. In Blender, open the addon panel, then click the *Install From Files...* button at the bottom. Select the **GoB.zip** file, this will install the addon inside the correct folder.
#. Check the GoB box and save the User preferences to launch it at startup. Then click on the Import icon on the header (on top of Blender) to activate autoloading.


Configure Addon
===============

Open the addon panel, then found GOB.

It have few useful import-export options:

Shading Mode
   Flat or Smooth shading when import
Modifiers
   Export, Export and Apply and Ignore
Polygroups
   From Materials, Uv's, Ignore

Usage
=====

The addon adds two icons Import/Export to the top info panel:

- By clicking on the Export icon, you export the selected mesh objects into ZBrush.
- By clicking on the Import icon, you enable autoloading mode. Latest objects are imported from GoZ.


Known issues
------------

- Blender can not have two objects with the same name, but ZBrush can. So if you export several objects from ZBrush, check names or some objects will be missed.
- Polygroups inside ZBrush use faces for grouping. Blender uses vertices for grouping, so the script does some conversion. There are some bugs with polygroups, so you might lose them...
- Same for polypainting, in Blender a vertex can have one color per face, but not in ZBrush.
