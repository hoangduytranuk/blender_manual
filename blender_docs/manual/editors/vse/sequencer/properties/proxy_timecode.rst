
********************
Proxy/Timecode Panel
********************

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Sidebar region --> Strip --> Proxy/Timecode`

Once you have chosen the Proxy/Timecode parameters,
you need to use :menuselection:`Strip --> Rebuild Proxy and Timecode indices`
to generate the proxy clip and it will be available after Blender makes it.


.. _bpy.types.SequenceProxy:

Proxy
=====

.. figure:: /images/editors_vse_sequencer_properties_proxy-timecode_panel.png
   :align: right

A proxy is a lower resolution version (faster to load) that stands in for the main image or video.
When you Rebuild proxy Blender computes small images (like thumbnails)
for the big images and may take some time. After computing them, though, editing functions
like scrubbing and scrolling and compositing functions like cross using these proxies is much
faster but gives a low-res result. Disable proxies before final rendering.

In order to actually use the proxies, the proper Proxy Render Size selector value must
be selected in the Sidebar region of the Sequencer View (where the edit plays back).

Storage
   Defines whether the proxies are for individual strips or the entire sequence.

   Per Strip
      Proxies are stored in the directory of the input.

      Proxy Custom Directory
         By default, all generated proxy images are storing to the <path of original footage>
         /BL_proxy/<clip name> folder, but this location can be set by hand using this option.
      Proxy Custom File
         Allows you to use pre-existing proxies.

   Project
      All proxies are stored in one directory.

      Proxy Directory
         The location to store the proxies for the project.

Size
   Buttons to control how big the proxies are.
   The available options are 25%, 50%, 75%, 100 percent of original strip size.
Overwrite
   Saves over any existing proxies in the proxy storage directory.
Quality
   Defines the quality of the JPEG images used for proxies.
Timecode
   See `Timecode`_.
Set Selected Strip Proxies
   Same as choosing the *Proxy Size* and *Overwrite*.
Rebuild Proxy and Timecode Indices
   Generates Proxies and Timecodes, same as doing :menuselection:`Strip --> Rebuild Proxy and Timecode indices`.


Timecode
========

When you are working with footage directly copied from a camera without pre-processing it,
there might be bunch of artifacts, mostly due to seeking a given frame in sequence.
This happens because such footage usually does not have correct frame rate values in their headers. So,
for Blender to calculate the position of a needed frame in the stream works inaccurately and can give errant result.
There are two possible ways to avoid this:

#. Preprocess your video with e.g. MEncoder to repair the file header and insert the correct keyframes.
#. Use Proxy/Timecode option in Blender.


Options
-------

Timecode
   :term:`Timecode` to use on the selected movie strip.

The following timecodes are supported:

- No TC in use- do not use any timecode
- Record Run
- Free Run
- Free Run (rec date)
- Record Run No Gaps

.. note::

   Record Run is the timecode which usually is best to use, but if the clip's file is totally damaged,
   *Record Run No Gaps* will be the only chance of getting acceptable result.
