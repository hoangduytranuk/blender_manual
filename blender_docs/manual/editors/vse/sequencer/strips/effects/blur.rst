.. _bpy.types.GaussianBlurSequence:

*************
Gaussian Blur
*************

The Gaussian Blur strip is used to blur the input strip in a defined direction.
This can be used to blur a background or to blur a transition strip.


Options
=======

Size X
   Distance of the blur effect on the X axis.
Size Y
   Distance of the blur effect on the Y axis.


Example
=======

For example, in the image below it shows an example of this strip being used to blur a transition.
In this set up the *Gaussian Blur Strip* is modifying
an :doc:`Adjustment Layer Strip </editors/vse/sequencer/strips/effects/adjustment>`
where the curve defines the amount of blur over the length of the *Adjustment Layer Strip*.

.. figure:: /images/editors_vse_sequencer_strips_effects_blur_example.png

   Example of Blurring a Transition.
