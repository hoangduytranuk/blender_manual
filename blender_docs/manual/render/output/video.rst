
************
Video Output
************

Preparing your Work for Video
=============================

Once you master the art of 3D animation, you will probably want to share your work with others;
either on the Internet (YouTube, Vimeo, etc.) or with family and friends (DVD/Blu-ray)
or even possibly for television broadcast.

To spare you some disappointment, here are some tips specifically targeted at video preparation.


Safe Areas and Overscan
-----------------------

For anyone creating motion graphics or simple text overlays, overscan is an important consideration.
Although its origins are rooted in historic analog TV systems, unfortunately even in 2017,
for various reasons it can still be an issue with modern digital flat screen TVs.

.. note::

   Due to various limitations in analog TV equipment, the displayed image could sometimes
   end up shifted horizontally or vary in size, which could lead to the area beyond
   the intended visible picture being shown. This hidden area sometimes contained junk noise,
   timing signals or closed-caption/subtitle data. To avoid this being visible to the viewer,
   the standard approach for TV manufacturers was to 'overscan' (zoom in) the displayed picture
   by a small amount (between 5-10% edge crop) to ensure that at no time would the hidden areas be visible.

   Although modern digital electronics have eliminated the issue of shifting image position,
   unfortunately, some TV manufacturers have included overscan on their flat screen TVs.
   Why? Because for many years it was given that the edge of the visible image would rarely be seen,
   so broadcasters would sometimes overlay 'hidden' data to the very edge of the image
   (e.g. some types of closed captions). Also, legacy analog recordings might still
   contain unwanted noise around the edge. To avoid consumer complaints,
   overscan is quite often enabled by default. For some flat screen TVs, it is not possible to disable it.


Enabling Safe Areas
-------------------

Blender has configurable safe-area markings which can be made visible by selecting the scene camera,
then in the camera settings by enabling :ref:`Safe Areas <camera-safe-areas>`. Several presets are available.
If you are producing work for a television network or indeed any client,
they may have their own rules and requirements on safe area dimensions -- so consult with them.


Color Reproduction
------------------

When exporting to many of the common video formats, the rendered RGB(A) images go through a conversion process
whereby they are translated to the YCbCr color model. Y corresponds to a gray-scale representation of the image,
Cb and Cr contain data for the blue and red channels respectively.
Green is encoded into the Y and Cb, Cr channels with some clever math.

Importantly, the color components are often stored at a lower resolution to the Y (grayscale) channel.
This can cause blurring/smearing which can be a problem with small text and some saturated color combinations --
so it is well worth doing test encodes to make sure that text remains legible. As with safe areas,
a TV network or client might have their own rules on minimum text size and positioning,
so always seek clarification when unsure.


.. _render-output-video-encoding-panel:
.. _bpy.types.FFmpegSettings:

Encoding Panel
==============

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Render --> Encoding`

.. figure:: /images/render_output_video_encoding-panel.png

   Encoding panel.

Here you choose which video container, codec, and compression settings you want to use.
With all of these compression choices, there is a trade-off between file size,
compatibility across platforms, and playback quality.

.. tip::

   When you view the :doc:`System Console </advanced/command_line/introduction>`,
   you can see some of the output of the encoding process.
   You will see even more output if you execute Blender as ``blender -d``.

Presets
   You can use the presets, which choose optimum settings for you for that type of output.
Container
   Video container or file type. For a list of all available options, see
   :doc:`video formats </files/files/media/video_formats>`.
Autosplit Output
   If your video is huge and exceeds 2GiB, enable Autosplit Output.
   This will automatically split the output into multiple files after the first file is 2Gig.
Codec
   Chooses the method of compression and encoding.
   For a list of all available options see :doc:`video formats </files/files/media/video_formats>`.

.. note:: Standards

   Some containers and codecs are not compatible with each other,
   so if you are getting errors check that your container and codec are compatible.
   Like containers and codecs are sometimes not compatible with each other, some codecs
   do not work with arbitrary dimensions. So, try to stick with common dimensions
   or research the limitations of the codec you are trying to use.

Output Quality
   These are preset `Rates <Rate>`_.
Encoding Speed
   Presets to change between a fast encode (bigger file size) and more compression (smaller file size).

Keyframe Interval
   The number of pictures per `Group of Pictures <https://en.wikipedia.org/wiki/Group_of_pictures>`__.
   Set to 0 for "intra_only", which disables `inter-frame <https://en.wikipedia.org/wiki/Inter-frame>`__ video.
   A higher number generally leads to a smaller file but needs a higher-powered device to replay it.
Max B-frames
   Enables the use of :term:`B‑frames <Frame Types>`.

   Interval
      The maximum number of :term:`B‑frames <Frame Types>` between non-B-frames.


Rate
----

Bitrate
   Sets the average `bit rate <https://en.wikipedia.org/wiki/Bit_rate>`__ (quality),
   which is the count of binary digits per frame.
   See also: `FFmpeg -b:v <https://ffmpeg.org/ffmpeg.html#Description>`__.
Rate
   Video files can use what is called variable bit rate (VBR).
   This is used to give some segments of the video less compressing to frames that need more data
   and less to frames with less data. This can be controlled by the *Minimum* and *Maximum* values.
Buffer
   The `decoder bitstream buffer <https://en.wikipedia.org/wiki/Video_buffering_verifier>`__ size.


Mux
---

`Multiplexing <http://www.afterdawn.com/glossary/term.cfm/multiplexing>`__
is the process of combining separate video and audio streams into a single file,
similar to packing a video file and .mp3 audio file in a zip-file.

Rate
   Maximum bit rate of the multiplexed stream.
Packet Size
   Reduces data fragmentation or muxer overhead depending on the source.


.. _render-output-video-encoding-audio:
.. _bpy.types.FFmpegSettings.audio:

Audio
-----

Audio Codec
   Audio format to use. For a list of all available options, see
   :doc:`video formats </files/files/media/video_formats>`.
Bitrate
   For each codec, you can control the bit rate (quality) of the sound in the movie.
   Higher bit rates are bigger files that stream worse but sound better.
   Use powers of 2 for compatibility.
Volume
   Sets the output volume of the audio.


Tips
----

.. tip:: The choice of video format depends on what you are planning to do.

It's not recommended to render directly to a video format in the first instance.
If a problem occurs while rendering, the file might become unplayable and you will
have to re-render all frames from the beginning. If you first render out a set
of static images such as the default PNG format or the higher-quality OpenEXR
(which can retain HDR pixel data), you can combine them as
an :doc:`Image Strip </editors/vse/sequencer/strips/movie_image>`
in the Video Sequence Editor (VSE). This way, you can easily:

- Restart the rendering from the place (the frame) where any problem occurred.
- Try out different video encoding options in seconds,
  rather than minutes or hours as encoding is usually much faster than rendering the 3d scene.
- Enjoy the rest of the features of the VSE, such as adding
  :doc:`Image Strips </editors/vse/sequencer/strips/movie_image>`
  from previous renders, audio, video clips, etc.

.. tip::

   You shouldn't post-process a lossy-compressed file as the compression artifacts may become visible.
   Lossy compression should be reserved as a final 'delivery format'.

If you are planning on doing significant post-processing and color correction,
it is best to output a frameset rendered in OpenEXR format.
If you plan to do only minimal changes after rendering and would prefer a single file,
choose lossless H.264 for high quality, or regular H.264 for lower quality.
