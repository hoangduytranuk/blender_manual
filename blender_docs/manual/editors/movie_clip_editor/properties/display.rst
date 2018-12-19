
*************
Display Panel
*************

This panel contains display settings related on editor itself.

Channels
   The R, G, B toggles control the color channels used for frame preview.
   It is needed because the tracking algorithm works with grayscale images and it is not
   always obvious to see which channels disabled will increase contrast of feature points and reduce noise.
Grayscale Preview (B/W)
   Shows the whole frame gray-scale.
Mute (eye icon) :kbd:`M`
   Changes displaying on movie frame itself with black square,
   It helps to find tracks which are tracked inaccurately or which were not tracked at all.
Render Undistorted
   Applies the *Lens Distortion* settings to the viewport image in order to display the footage undistorted.
   It is only a preview option, which does not actually change the footage itself.
Lock to Selection :kbd:`L`
   Makes the editor display selected tracks at the same screen position
   along the whole footage during playback or tracking.
   This option helps to control the tracking process and
   stop it when the track is starting to slide off or when it jumped.
Display Stabilization
   This option makes the displayed frame be affected by the 2D stabilization settings
   (available in reconstruction mode only).
   It is only a preview option, which does not actually change the footage itself.
Grid
   Displays a grid which is originally orthographic,
   but is affected by the distortion model (available in distortion mode only).
   This grid can be used for manual calibration --
   distorted lines of grids are equal to straight lines in the footage.
Calibration
   Applies the distortion model for Grease pencil strokes (available in distortion mode only).
   This option also helps to perform manual calibration.
   A more detailed description of this process will be added later.
Display Aspect Ratio
   Changes the aspect ratio for displaying only. It does not affect the tracking or solving process.
