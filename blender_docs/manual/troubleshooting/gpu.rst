
*****************
Graphics Hardware
*****************

Blender makes use of OpenGL, which is typically hardware accelerated.

This means issues with the graphics card hardware and drivers can impact on Blender's behavior.
This page lists some known issues using Blender on different graphics hardware and how to troubleshoot them.


Performance
===========

When the entire interface is very slow and unresponsive (*even* with the default startup scene),
this is likely a problem with the OpenGL configuration.

Unfortunately, in this situation, you may have to do some of your own tests to find the cause.
Below are some common causes and possible solutions.

Upgrade your OpenGL Driver
   If you are experiencing any strange graphics problems with Blender,
   it is always good to double check if you are using the latest drivers.
Disable Anti-Aliasing :term:`FSAA, Multisampling <FSAA>`
   See :ref:`Invalid Selection, Disable Anti-Aliasing <troubleshooting-3dview-invalid-selection>`.
Change the *Window Draw Method*
   This is set in the :ref:`system preferences <prefs-system-window-draw>`.
   It is selected automatically, however, when experiencing problems it's worth
   checking if changing this resolves interface drawing problems.
