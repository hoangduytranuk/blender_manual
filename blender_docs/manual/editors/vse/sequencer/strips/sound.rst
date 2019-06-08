.. _bpy.types.SoundSequence:

************
Sound Strips
************

As well as images and movies the VSE can also edit audio tracks.
You can add Waveform Audio format ``WAV``, ``mp3`` and other audio formats files from your drive,
or from sound encoded within a movie, and mix them using an F-Curve as a volume control.

.. figure:: /images/editors_vse_sequencer_strips_sound_editing.png

   Example of sound editing.


Options
=======

Pack
   This allows you to save the audio file into the blend-file.
Caching
   Caching loads a file into RAM and plays it from there, instead of reading it for the hard drive.

.. _sequencer-sound-waveform:

Draw Waveform
   Draws either the waveform or the strip name, file name, duration.
   This can be useful for syncing two or more sound strips.
Volume
   Controls the volume of the strip. Typically values should be between 0 and 1.
   If you use higher values it's possible that clipping happens, which drastically influences sound quality.
Pitch
   Transposes the frequency of the audio.
   This basically changes the playback speed of the sound which also results in a pitch change.
   Unfortunately this leads to possible seeking errors and the length of the strip isn't updated as well.
Pan
   Used to pan the audio from left and right channels. Only works for mono sources.
   Values can be between -2 and 2, where 0 means front/center, -1 means to the left and 1 to the right.
   In case of multichannel audio (rear speakers) you can pan to those with the higher values: -2, 2 is back.
   So this value basically represents the angle at which it's played.

Trim Duration
   Offset the start and end of a sound strip.


Working with Audio Tracks
=========================

A sound strip is just like any other strip in the VSE. You can grab and move it,
adjust its starting offset using :kbd:`RMB` over the arrow end handles,
and :kbd:`K` cut it into pieces.
A useful example is cutting out the "um's" and dead voice time.

You can have as many sound strips as you wish and the result will be the mixing of all of them.
You can give each strip its own name and volume via the Sidebar region.

Overlapping strips are automatically mixed down during the rendering process.
For example, you can have the announcer on channel 5, background music on channel 6,
and Foley sound effects on channel 7.

.. seealso::

   In the :ref:`timeline-playback` menu of the Timeline you will find some options
   concerning audio playback behavior.


Animating Audio Track Properties
================================

To animate sound strips simply hit :kbd:`I` over any of its values.
Examples of animating an audio strip are to fade in/out background music or to adjust volume levels.
Layered/crossed sound strips are added together;
the lower channel does not override and cut out higher channels (unlike image and video strips).
This makes Blender an audio mixer.
By adding audio tracks and using the curves to adjust each tracks' sound level,
you have an automated dynamic multi-track audio mixer!


Output
======

There are two ways to render out your audio. You can either have it encoded with a video file
or in its own audio file. To render your audio in a video file make sure to use a video format
as the output with an audio codec and hit the render *Animation* button in the Properties editor.
Read more on how to do this :doc:`here </render/output/video>`. To render as an audio file simple
use the *Audio* button. Read more on how to do this :doc:`here </render/output/video>`.


Known Limitations
=================

Hiss, Crackle and Pop
---------------------

.. EDITORS NOTE:
   This is a common problem and unavoidable see T37432#351492

In some cases when *Caching* is disabled, playback noise/hiss is introduced.

If you hear pops and crackles, usually that is a sign that your hardware cannot keep up in real-time playback.
They will not be present in your final rendered animation output.

Also, static hiss can occur whenever two or more sound strips are overlapping in the timeline.
