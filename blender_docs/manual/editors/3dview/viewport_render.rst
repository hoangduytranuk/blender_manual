
***************
Viewport Render
***************

Viewport rendering uses the 3D View's drawing for quick *preview* renders.

This allows you to inspect your animatic
(for object movements, alternate angles, etc.).

This can also be used to preview your animations --
in the event your scene is too complex for your system to play back in real-time in the 3D View.

You can use *Viewport Render* to render both images and animations.

Below is a comparison between the Viewport render and a final render using
the Cycles Renderer.

.. list-table:: Model by © 2016 pokedstudio.com

   * - .. figure:: /images/render_opengl_example-opengl-render.jpg
          :width: 320px

          Viewport render.

     - .. figure:: /images/render_opengl_example-cycles-render.jpg
          :width: 320px

          Full render.

.. TODO2.8 Replace this text with overlays.

.. tip:: Showing Only Rendered Objects

   To access this option, enable the *Only Render* in the :doc:`Display Panel </editors/3dview/properties/panels>`.

   While this option is not specific to Viewport rendering, it's often useful to enable,
   since it removes data such as rigs and empties that can be a distraction.


.. TODO2.8

Settings
========

.. admonition:: Reference
   :class: refbox

   :Editor:    Info Editor
   :Menu:      :menuselection:`Render --> Viewport Render Options`

For the most part, *Viewport Render* uses the viewport settings,
Sampling and Alpha Transparency Mode options can be set by
the :menuselection:`Render --> Viewport Render Options` from the Info Editor header.
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
