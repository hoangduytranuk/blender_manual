.. _bpy.types.MovieTrackingCamera:

***********
Camera Data
***********

This panel contains all settings of the camera used for filming the movie
which is currently being edited in the Clip editor.


Camera
======

Camera Presets
   Predefined settings can be used here.
   But such settings as distortion coefficients and principal point are not included in the presets and
   should be filled in even if camera presets are used.
Sensor
   Width
      Is the width of the CCD sensor in the camera. This value can be found in camera specifications.
   Pixel Aspect Ratio
      Is the pixel aspect of the CCD sensor. This value can be found in camera specifications,
      but can also be guessed. For example, you know that the footage should be 1920×1080,
      but the images themselves are 1280×1080. In this case, the pixel aspect is: 1920 / 1280 = 1.5.
Optical Center
   Is the optical center of the lens used in the camera. In most cases it is equal to the image center,
   but it can be different in some special cases. Check camera/lens specifications in such cases.
   To set the optical center to the center of image, there is a :kbd:`Return` button below the sliders.


Lens
====

Focal Length
   Is self-explanatory; it is the focal length with which the movie was shot.
   It can be set in millimeters or pixels.


Lens Distortion
---------------

Distortion Model
   Polynomial
      Polynomial radial distortion.
   Division
      It defines high distortions, which makes this model suitable much better for cameras with fisheye lenses.

Coefficients
   Coefficients are used to compensate for lens distortion when the movie was shot.
   Currently these values can be tweaked by hand only (there are no calibration tools yet)
   using tools available in Distortion mode.
   Basically, just tweak K1 until solving is most accurate for the known focal length
   (but also take grid and Grease Pencil into account to prevent "impossible" distortion).

   The coefficients of the division model work independent from each other and
   positive values will give a barrel distortion.

   K1, K2 and K3
