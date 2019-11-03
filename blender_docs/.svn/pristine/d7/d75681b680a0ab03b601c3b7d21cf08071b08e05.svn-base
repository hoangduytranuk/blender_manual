
***************
Viewport Render
***************

Viewport rendering uses the 3D Viewport rendering for quick *preview* renders.

This allows you to inspect your animatic
(for object movements, alternate angles, etc.).

This can also be used to preview your animations --
in the event your scene is too complex for your system to play back in real-time in the 3D View.

You can use *Viewport Render* to render both images and animations.

Below is a comparison between the Viewport render and a final render using
the Cycles Renderer.

.. list-table:: Model by © 2016 pokedstudio.com

   * - .. figure:: /images/editors_3dview_viewport-render_example-workbench-render.jpg
          :width: 320px

          Viewport render using Solid Mode.

     - .. figure:: /images/editors_3dview_viewport-render_example-eevee-render.jpg
          :width: 320px

          Viewport render using Look Dev Mode.

     - .. figure:: /images/editors_3dview_viewport-render_example-cycles-render.jpg
          :width: 320px

          Full render.

.. tip::

   Disable overlays to render the viewport without any additional overlays.

   While this option is not specific to Viewport rendering, it's often useful to
   enable, since it removes data such as rigs and empties that can be a distraction.


Settings
========

.. admonition:: Reference
   :class: refbox

   :Editor:    Topbar
   :Menu:      :menuselection:`Render --> Viewport Render Options`

For the most part, *Viewport Render* uses the current viewport settings.
Some settings are located in the render panel of the render engine
that is used to render the view.

Solid mode uses the render settings of Workbench;
LookDev mode uses the render settings of Eevee.

Sampling and Alpha Transparency Mode options can be set in :menuselection:`Properties --> Render --> Sampling`.
Make sure the Workbench or Eevee render engine is selected to see the appropriate values.

Additionally, some render settings are used too:

- Render Dimensions
- Render Aspect
- File Format & Output (file path, format, compression settings, etc.)


Rendering
=========

Activating *Viewport Render* will render from the current active view.
This means that if you are not in an active camera view then
a virtual camera is used to match the current perspective.
To get an image from the camera point of view,
enter the active camera view with :kbd:`Numpad0`.

As with a normal render, you can abort it with :kbd:`Esc`.

Render a Still Image
   To render a still image use :menuselection:`3D Viewport --> View --> Viewport Render Image`.
Render an Animation
   to render an animation use :menuselection:`3D Viewport --> View --> Viewport Render Animation`.

.. tip::

   You can limit the viewport render to a particular region with
   :ref:`Render Regions <editors-3dview-navigate-render-region>`.
