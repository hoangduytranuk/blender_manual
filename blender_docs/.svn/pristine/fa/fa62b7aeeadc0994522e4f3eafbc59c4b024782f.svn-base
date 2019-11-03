
*************
GPU Rendering
*************

:abbr:`GPU (Graphics Processing Unit)` rendering makes it possible to use your
graphics card for rendering, instead of the CPU. This can speed up rendering
because modern GPUs are designed to do quite a lot of number crunching.
On the other hand, they also have some limitations in rendering complex scenes, due to more limited memory,
and issues with interactivity when using the same graphics card for display and rendering.

To enable GPU rendering, go into the :menuselection:`Preferences --> System --> Cycles Render Devices`,
and select either *CUDA* or *OpenCL*. Next, you must configure each scene to use GPU rendering in
:menuselection:`Properties --> Render --> Device`.


Supported Hardware
==================

Blender supports two different technologies to render on the GPU depending on the particular GPU manufacture.


NVIDIA CUDA
-----------

NVIDIA :abbr:`CUDA (Compute Unified Device Architecture)`
is supported for GPU rendering with *NVIDIA* graphics cards.
Blender supports graphics cards with compute capability 3.0 and higher.
To make sure your GPU is supported,
see the `list of NVIDIA graphics cards <https://developer.nvidia.com/cuda-gpus>`__
with the compute capabilities and supported graphics cards.

NVIDIA CUDA GPU rendering is supported on Windows, macOS, and Linux.


AMD OpenCL
----------

:abbr:`OpenCL (Open Computing Language)`
is supported for GPU rendering with *AMD* graphics cards.
Blender Supports graphics cards with :abbr:`GCN (Graphics Core Next)` generation 2 and above.
To make sure your GPU is supported,
see the `list of GCN generations <https://en.wikipedia.org/wiki/Graphics_Core_Next#Iterations>`__
with the GCN generation and supported graphics cards.

AMD OpenCL GPU rendering is supported on Windows and Linux, but not on macOS.


Supported Features and Limitations
==================================

GPU rendering supports all the same features as CPU rendering, except two:

- Open Shading Language.
- Advanced volume light sampling to reduce noise.


Frequently Asked Questions
==========================

Why is Blender unresponsive during rendering?
---------------------------------------------

While a graphics card is rendering, it cannot redraw the user interface, which makes Blender unresponsive.
We attempt to avoid this problem by giving back control over the GPU as often as possible,
but a completely smooth interaction cannot be guaranteed, especially on heavy scenes.
This is a limitation of graphics cards for which no true solution exists,
though we might be able to improve this somewhat in the future.

If possible, it is best to install more than one GPU,
using one for display and the other(s) for rendering.


Why does a scene that renders on the CPU not render on the GPU?
---------------------------------------------------------------

There maybe be multiple causes,
but the most common is that there is not enough memory on your graphics card.
We can currently only render scenes that fit in graphics card memory,
and this is usually smaller than that of the CPU. Note that, for example, 8k, 4k,
2k and 1k image textures take up respectively 256MB, 64MB, 16MB and 4MB of memory.

We do intend to add a system to support scenes bigger than GPU memory,
but this will not be added soon.


Can multiple GPUs be used for rendering?
----------------------------------------

Yes, go to :menuselection:`Preferences --> System --> Compute Device Panel`, and configure it as you desire.


Would multiple GPUs increase available memory?
----------------------------------------------

No, each GPU can only access its own memory.


What renders faster, NVIDIA or AMD, CUDA or OpenCL?
---------------------------------------------------

Currently NVIDIA with CUDA is rendering fastest, but this really depends on the hardware you buy.
Currently, CUDA and OpenCL are about the same in the newest mid-range GPUs.
However, CUDA is fastest in the respect of high-end GPUs.


Error Messages
==============

In case of problems, be sure to install the official graphics drivers from the NVIDIA or AMD website,
or through the package manager on Linux.


Unsupported GNU version! gcc 4.7 and up are not supported!
----------------------------------------------------------

On Linux, depending on your GCC version you might get this error. There are two possible solutions:

Use an alternate compiler
   If you have an older GCC installed that is compatible with the installed CUDA toolkit version,
   then you can use it instead of the default compiler.
   This is done by setting the ``CYCLES_CUDA_EXTRA_CFLAGS`` environment variable when starting Blender.

   Launch Blender from the command line as follows:

   .. code-block:: sh

      CYCLES_CUDA_EXTRA_CFLAGS="-ccbin gcc-x.x" blender

   (Substitute the name or path of the compatible GCC compiler).

Remove compatibility checks
   If the above is unsuccessful, delete the following line in
   ``/usr/local/cuda/include/host_config.h``

   ::

      #error -- unsupported GNU version! gcc 4.7 and up are not supported!

This will allow Cycles to successfully compile the CUDA rendering kernel the first time it
attempts to use your GPU for rendering. Once the kernel is built successfully, you can
launch Blender as you normally would and the CUDA kernel will still be used for rendering.


CUDA Error: Invalid kernel image
--------------------------------

If you get this error on Windows 64-bit, be sure to use the 64-bit build of Blender,
not the 32-bit version.


CUDA Error: Kernel compilation failed
-------------------------------------

This error may happen if you have a new NVIDIA graphics card that is not yet supported by
the Blender version and CUDA toolkit you have installed.
In this case Blender may try to dynamically build a kernel for your graphics card and fail.

In this case you can:

#. Check if the latest Blender version
   (official or `experimental builds <https://builder.blender.org/download/experimental/>`__)
   supports your graphics card.
#. If you build Blender yourself, try to download and install a newer CUDA developer toolkit.

Normally users do not need to install the CUDA toolkit as Blender comes with precompiled kernels.


CUDA Error: Out of memory
-------------------------

This usually means there is not enough memory to store the scene on the GPU.
We can currently only render scenes that fit in graphics card memory,
and this is usually smaller than that of the CPU. See above for more details.


The NVIDIA OpenGL driver lost connection with the display driver
----------------------------------------------------------------

If a GPU is used for both display and rendering,
Windows has a limit on the time the GPU can do render computations.
If you have a particularly heavy scene, Cycles can take up too much GPU time.
Reducing Tile Size in the Performance panel may alleviate the issue,
but the only real solution is to use separate graphics cards for display and rendering.

Another solution can be to increase the time-out,
although this will make the user interface less responsive when rendering heavy scenes.
`Learn More Here <https://msdn.microsoft.com/en-us/Library/Windows/Hardware/ff570087%28v=vs.85%29.aspx>`__.


CUDA error: Unknown error in cuCtxSynchronize()
-----------------------------------------------

An unknown error can have many causes, but one possibility is that it is a time-out.
See the above answer for solutions.
