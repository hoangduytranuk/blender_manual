
********
Metadata
********

.. figure:: /images/render_output_metadata_panel.png

   Metadata panel.

The *Metadata* panel includes options for writing metadata into render output.

.. note::

   Only some image formats support metadata:
   See :doc:`image formats </data_system/files/media/image_formats>`.

Stamp Output
   Add metadata as text to the render.

   Stamp Text Color
      Set the color and alpha of the stamp text.
   Stamp Background
      Set the color and alpha of the color behind the text.
   Font Size
      Set the size of the text.
   Draw Labels
      Draws the labels before the metadata text. For example,
      "Camera" in front of the camera name, etc.


.. rubric:: Enabled Metadata

Stamping can include the following data:

Time
   Includes the current scene time and render frame at ``HH:MM:SS.FF``.
Date
   Includes the current date and time.
Render Time
   Includes the render time.
Frame
   Includes the frame number.
Scene
   Includes the name of the active scene.
Memory
   Includes the peak memory usage.
Note
   Includes a custom note.

   .. hint::

      It can be useful to use the *Note* field if you are setting up a render farm.

      Since you can script any information you like into it,
      such as an identifier for the render-node or the job-number.

      For details on stamping arbitrary values,
      see: `this page <https://blender.stackexchange.com/questions/26643>`__.

Camera
   Includes the name of the active camera.
Lens
   Includes the name of the active camera's lens value.
Filename
   Includes the filename of the blend-file.
Marker
   Includes the name of the last marker.
Sequence Strip
   Includes the name of the foreground sequence strip.


.. rubric:: Sequencer

Strip Metadata
   Use metadata from the strips in the Sequencer.
