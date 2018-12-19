
**********
Workspaces
**********

.. figure:: /images/interface_window-system_workspaces_screen.png
   :align: center

   Workspaces are located at the Top bar.

*Workspaces* are essentially predefined window layouts.
Blender's flexibility with :doc:`Areas </interface/window_system/areas>`
lets you create customized workspaces for different tasks such as
modeling, animating, and scripting. It is often useful to quickly switch between
different workspaces within the same file.


Controls
========

Tabs
   Click on the tabs titles to switch between the workspaces.
   To cycle between workspaces use :kbd:`Ctrl-PageUp` and :kbd:`Ctrl-PageDown`.
Add ``+``
   Click on the *Add* button to add a new workspace.
Context menu :kbd:`RMB`
   The context menu contains options to duplicate, delete and reorder workspaces.


Default Workspaces
==================

:Layout: A general workspace to preview your scene and objects.
:Modeling: For modification of geometry by modeling tools.
:Sculpting: For modification of meshes by sculpting tools.
:UV Editing: Mapping of image texture coordinates to 3D surfaces.
:Texture Paint: Tools for coloring image textures in the 3D View.
:Shading: Tools for specifying material properties for rendering.
:Animation: Tools for making properties of objects dependent on time.
:Rendering: For viewing and analyzing rendering results.
:Compositing: Combining and post-processing of images and rendering information.
:Scripting: Programming workspace for writing scripts.


Save and Override
=================

The workspaces are saved in the blend-file.
When you open a file, enabling the *Load UI* in the File Browser indicates that Blender should
use the file's screen layouts and overriding the current layout.
See :ref:`Load UI <file-load-ui>`.

A custom set of workspaces can be saved as a part of the :doc:`/data_system/files/startup_file`.
