
************
Render Panel
************

.. figure:: /images/render_output_render-panel_panel.png
   :align: right

   Render panel.

Render :kbd:`F12`
   Starts rendering a still image of the current frame.
Animation :kbd:`Ctrl-F12`
   Starts rendering an animation.
   See :doc:`Rendering Animations </render/output/animation>` for more detail.
Audio
   Mixes all the audio found in a scene and saves into one file.
   See :doc:`/render/output/audio/introduction`.

By default the biggest area is replaced with the Image Editor and the render appears.

To cancel the rendering process click the cancel button ``X`` besides the progress bar in the Info Editor,
or press :kbd:`Esc`.


.. _bpy.types.RenderSettings.display_mode:

Display
=======

Renders are displayed in the Image Editor. You can set the way this is displayed to
several different options in the Display menu:

Display
   Keep UI
      The image is rendered to the Image Editor, but the UI remains the same.
      You will need to open the Image Editor manually to see the render result.
   New Window
      A new floating window opens up, displaying the render.
   Image Editor
      One of the existing editors is replaced with the Image Editor, showing the render.
   Full Screen
      The Image Editor replaces the UI, showing the render.
Lock Interface
   Lock interface during rendering in favor of giving more memory to the renderer.
