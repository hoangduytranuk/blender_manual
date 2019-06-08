.. _bpy.types.ColorManaged:
.. TODO/Review: {{review|partial=X|im=needs images}}.

****************
Color Management
****************

Color management is one of the most important tools that an artist can use.
It allows an artist to make sure that an image stays the same from rendering, to saving, to post-processing.
Color management also allows an artist to tweak things like exposure, gamma, or the overall color grade.

.. figure:: /images/render_post-process_color-management_different-exposures.jpg
   :width: 300px
   :align: right

   Different views and exposures of the same render.

To achieve color management in Blender, the `OpenColorIO <http://opencolorio.org/>`__
(OCIO) library has been integrated into Blender.
This library offers fine control over different :abbr:`LUT (Look Up Table)`
along with integrating your own set of color profiles to keep your work linearized with other software.


Scene Linear Color Space
========================

For correct results, different :term:`color spaces <color space>`
are needed for rendering display and storage of images.
Rendering and compositing is best done in scene *linear* color space,
which corresponds more closely to nature, and makes computations more physically accurate.

.. figure:: /images/render_post-process_color-management_linear-workflow.svg

   An example of a linear workflow.

If the colors are linear, it means that if in reality, we double the number of photons,
the color values are also doubled. Put another way,
if we have two photos/renders each with one of two lights on, and add those images together,
the result would be the same as a render/photo with both lights on. It follows that such
a radiometrically linear space is best for photorealistic rendering and compositing.

However, these values do not directly correspond to human perception or the way display devices
work and image files are often stored in different color spaces,
so we have to take care to do the right conversion into and out of this linear color space.


.. _render-post-color-management:

Settings
========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Scene --> Color Management`

.. figure:: /images/render_post-process_color-management_panel.png

   Scene settings for color management.


Display
-------

Correct display of renders requires a conversion to the display device color space, which can be configured here.
A computer monitor works differently from a digital cinema projector HDTV. The scene properties have these settings:

Display Device
   The device that the image is being viewed on.

   Most computer monitors are configured for the sRGB color space,
   and so when working on a computer usually this option should just be left to the default.
   It would typically be changed when viewing the image on another display device connected to the computer,
   or when writing out image files intended to be displayed on another device.

   Rec709 is commonly used for HDTVs, while XYZ and DCI-P3 are common for digital projectors.

   Color management can be disabled by setting the device to None.

.. figure:: /images/render_post-process_color-management_linear-display-space.svg

   Conversion from linear to display device space.


Render
------

There is also an artistic choice to be made for renders. Partially that is
because display devices cannot display the full spectrum of colors and only have limited
brightness, so we can squeeze the colors to fit in the gamut of the device.
Besides that, it can also be useful to give the renders a particular look, e.g.
as if they have been printed on real film.

Another common use case is when you want to inspect renders,
to see details in dark shadows or bright highlights, or identify render errors.
Such settings would be only used temporarily and not get used for final renders.

View
   These are different ways to view the image on the same display device.

   Default
      Does no extra conversion besides the conversion for the display device.
   Filmic
      For more photorealistic results and better handling of high dynamic range.
      The contrast can be adjusted by changing the *Look* option for the Filmic view transform.
   RRT
      Uses the ACES Reference Rendering Transform, to simulate a film-like look.
   Film
      Uses a technique known as film emulation to give renders a look
      similar to what might be expected from a film-based camera.
      This is usually done by crushing the blacks and decreasing the contrast of the image.
   Raw
      Intended for inspecting the image but not for final export.
      Raw gives the image without any color space conversion.
   Log
      Intended for inspecting the image but not for final export.
      Log works similar to Raw but gives a more "flat" view of the image without very dark or light areas.
   False Color
      Shows a heat map of image intensities, to visualize the dynamic range.
Exposure
   Used to control the image brightness (in stops) applied before color space conversion.
   It is calculated as follows: :math:`output\_value = render\_value × 2^{(exposure)}`
Gamma
   Extra gamma correction applied after color space conversion. Note that the default sRGB or Rec709 color space
   conversions already include a gamma correction of approximately 2.2 (except the *Raw* and *Log* views),
   so this would be applied in addition to that.
Look
   Choose an artistic effect from a set of measured film response data which
   roughly emulates the look of certain film types. Applied before color space conversion.
Use Curves
   Adjust RGB Curves to control image colors before color space conversion.
   Read more about using the :ref:`ui-curve-widget`.


Sequencer
---------

Color Space
   The color space that the Sequencer operates in. By default, the Sequencer operates in sRGB space,
   but it can also be set to work in Linear space like the Compositing nodes, or another color space.
   Different color spaces will give different results for color correction, crossfades, and other operations.


Image Files
===========

When loading and saving media formats it is important to have color management in mind.
File formats such as PNG or JPEG will typically store colors in a color space ready for
display, not in a linear space. When they are, for example, used as textures in renders,
they need to be converted to linear first, and when saving renders for display on the web,
they also need to be converted to a display space. Other file formats like OpenEXR store
linear color spaces and as such are useful as intermediate files in production.

When working with image files, the default color space is usually the right one.
If this is not the case,
the color space of the image file can be configured in the image settings. A common situation
where manual changes are needed is when working with or baking normal maps or displacement maps,
for example. Such maps do not actually store colors, just data encoded as colors.
In such cases, they should be marked as *Non-Color Data*.

Image data-blocks will always store float buffers in memory in the scene linear color space,
while a byte buffer in memory and files in a drive are stored in the color space specified with this setting:

Color Space
   The color space of the image file on a drive. This depends on the file format,
   for example, PNG or JPEG images are often stored in sRGB, while OpenEXR images are stored in a linear color space.
   Some images such as normal, bump or stencil maps do not strictly contain 'colors',
   and on such values, no color space conversion should ever be applied.
   For such images, the color space should be set to *None*.

.. figure:: /images/render_post-process_color-management_image-settings.png

   Image settings for color management.

By default only renders are displayed and saved with the render view transformations applied.
These are the Render Result and Viewer image data-blocks,
and the files saved directly to a drive with the Render Animation operator.
However, when loading a render saved to an intermediate OpenEXR file,
Blender cannot detect automatically that this is a render
(it could be e.g. an image texture or displacement map).
We need to specify that this is a render and that we want the transformations applied,
with these two settings:

View as Render
   Display the image data-block (not only renders) with view transform, exposure, gamma, RGB curves applied.
   Useful for viewing rendered frames in linear OpenEXR files the same as when rendering them directly.
Save as Render
   Option in the image save operator to apply the view transform, exposure, gamma, RGB curves.
   This is useful for saving linear OpenEXR to e.g. PNG or JPEG files in display space.


OpenColorIO Configuration
=========================

Blender comes with a standard OpenColorIO configuration that
contains a number of useful display devices and view transforms.
The reference linear :term:`color space` used is the linear color space
with Rec. 709 chromaticities and D65 white point.

However, OpenColorIO was also designed to give a consistent user experience across
`multiple applications <http://opencolorio.org/CompatibleSoftware.html>`__,
and for this, a single shared configuration file can be used.
Blender will use the standard OCIO environment variable to read an OpenColorIO configuration
other than the default Blender one. More information about how to set up such a workflow
can be found on the `OpenColorIO website <http://opencolorio.org/>`__.

We currently use the following color space rules:

scene_linear
   Color space used for rendering, compositing, and storing all float precision images in memory.
default_sequencer
   Default color space for the Sequencer, *scene_linear* if not specified.
default_byte
   Default color space for byte precision images and files, *texture_paint* if not specified.
default_float
   Default color space for float precision images and files, *scene_linear* if not specified.

The standard Blender configuration also includes some support for
`ACES <https://www.oscars.org/science-technology/sci-tech-projects/aces>`__
(`code and documentation <https://github.com/ampas/aces-dev>`__),
even though we have a different linear color space.
It is possible to load and save EXR files with the Linear ACES color space,
and the RRT view transform can be used to view images with their standard display transform.
However, the ACES gamut is larger than the Rec. 709 gamut,
so for best results, an ACES specific configuration file should be used.
OpenColorIO provides an `ACES configuration <http://opencolorio.org/configurations/index.html>`__ file,
though it may need a few more tweaks to be usable in production.
