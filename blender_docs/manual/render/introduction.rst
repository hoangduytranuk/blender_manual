
************
Introduction
************

Rendering is the process of creating a 2D image (or video) from your 3D scene.
What that image looks like is based on four factors which the user can control:

- A :doc:`Camera </render/cycles/camera>`
- The :doc:`Lighting </render/lighting/introduction>` in your scene
- The :doc:`Material </render/cycles/materials/introduction>` of each object
- Various render settings (quality, image size, layers, etc.)

Your computer will perform various complex calculations
based on those factors in order to give you your rendered image.
This process may take some time depending on the complexity of the scene and your hardware.

Once the render is complete, it is possible to do additional manipulation of the image,
called :doc:`Post Processing </render/post_process/index>`.

Finally, the output can be saved to an image or video file
using one of the :doc:`Output Formats </render/output/output>`.


Workflow
========

In general, the process for rendering is:

#. Position the camera.
#. Light the scene.
#. Setup materials.
#. Render a test image using lower quality settings.
#. Change or fix anything you noticed in the render.
#. Repeat the above two steps until you are satisfied.
#. Render a high-quality image, change or fix any issues and repeat until satisfied.
#. Save your image to a file, or render the animation to a video or image sequence.


.. _bpy.types.RenderSettings.engine:

Render Engines
==============

Renderers are programs that turn meshes, materials and lights into images.

Some renderers may be better at certain things than others due
to the math they use or core principles around which they were written.

Blender includes two renderers by default:

- :doc:`Eevee </render/eevee/index>`
- :doc:`Cycles </render/cycles/index>`

More renderers from third-party developers can also be added using
:doc:`Add-ons </preferences/addons>`.
