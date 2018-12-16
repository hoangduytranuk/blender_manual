
*************
OpenGL Render
*************

OpenGL rendering uses the 3D View's drawing for quick *preview* renders.

This allows you to inspect your animatic
(for object movements, alternate angles, etc.).

This can also be used to preview your animations --
in the event your scene is too complex for your system to play back in real-time in the 3D View.

You can use OpenGL to render both images and animations.

Below is a comparison between the OpenGL render and a final render using
the Cycles Renderer.

.. list-table:: Model by © 2016 pokedstudio.com

   * - .. figure:: /images/render_opengl_example-opengl-render.jpg
          :width: 320px

          OpenGL render.

     - .. figure:: /images/render_opengl_example-cycles-render.jpg
          :width: 320px

          Full render.

.. tip:: Showing Only Rendered Objects

   To access this option, enable the *Only Render* in the :doc:`Display Panel </editors/3dview/properties/panels>`.

   While this option is not specific to OpenGL rendering, it's often useful to enable,
   since it removes data such as rigs and empties that can be a distraction.


Settings
========

.. admonition:: Reference
   :class: refbox

   :Editor:    Info Editor
   :Menu:      :menuselection:`Render --> OpenGL Render Options`

For the most part, *OpenGL Render* uses the viewport settings,
Sampling and Alpha Transparency Mode options can be set by
the :menuselection:`Render --> OpenGL Render Options` from the Info Editor header.
Additionally, some render settings are used too:

- Render Dimensions
- Render Aspect
- File Format & Output (file path, format, compression settings, etc.)


Rendering
=========

Activating OpenGL render from the menu will render from the active camera.

You can also render any viewport, from the header of the *3D View*,
using the small button showing a *Camera*.

.. figure:: /images/render_opengl_view-port-render-buttons.png

   OpenGL Render buttons.

As with a normal render, you can abort it with :kbd:`Esc`.

Render a Still Image
   Click on the small button showing a *camera* in the header of the 3D View.

   Or from the menu: :menuselection:`Render --> OpenGL Render Image`
   from the header of the *Info Editor*
Render an Animation
   Click on the small button showing a *slate* in the header of the 3D View.

   Or from the menu: :menuselection:`Render --> OpenGL Render Animation`
   from the header of the *Info Editor*
Render from the Sequencer
   Click on the small button showing a *slate* in the header of *Sequencer* preview region.

   Using scene strips in the Sequencer you can edit together scenes to quickly render an entire sequence of shots.

   This can be activated using the render icons in the Sequencer's playback header.


Known Limitations
=================

OpenGL Anti-Aliasing Support
----------------------------

Some graphics cards do not support this feature
(known as the frame-buffer multi-sample OpenGL extensions).

In this case rendering works but no anti-aliasing is performed.

Enabling *Full Sample*, can be used to workaround this limit,
because it does not rely on hardware multi-sample support.

.. hint::

   Exact extensions needed, as listed in output from :ref:`help-system-info` (OpenGL section):

   - ``GL_ARB_texture_multisample``
   - ``GL_EXT_framebuffer_blit``
   - ``GL_EXT_framebuffer_multisample_blit_scaled``
   - ``GL_EXT_framebuffer_multisample``
