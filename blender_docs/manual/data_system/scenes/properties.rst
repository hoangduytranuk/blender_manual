
****************
Scene Properties
****************

.. _bpy.types.Scene.camera:
.. _bpy.types.Scene.background_set:
.. _bpy.types.Scene.active_clip:

Scene
=====

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Scene --> Scene`

Camera
   Used to select which camera is used as the active camera.
   You can also set the active camera in the 3D View with :kbd:`Ctrl-0`.

.. _scene-background-set:

Background
   Allows you to use a scene as a background,
   this is typically useful when you want to focus on animating the foreground for example,
   without background elements getting in the way.

   This scene can have its own animation, physics simulations, etc,
   but you will have to select it from the *Scene* data-block menu, if you want to edit any of its contents.

   Sets can themselves have a background set (they're recursively included).
   So you can always make additions to existing scenes by using them as a background
   to a newly created scene where your additions are made.

   .. tip::

      This can also be used in combination with :ref:`Linking to a Scene <data-system-linked-libraries-make-link>`,
      where one blend-file contains the environment, which can be reused in many places.

Active Clip
   Active movie clip for constraints and viewport drawing.


.. _data-scenes-props-units:
.. _bpy.types.UnitSettings:

Units
=====

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Scene --> Units`

Length Presets
   Common unit scales to use.
Length
   None
      Uses :term:`Blender Units`.
   Metric, Imperial
      Standard unit of measurement for lengths.
Angle
   Standard unit for angular measurement.

   Degrees, Radians

   .. tip::

      When you are using *Degrees*, the radian value is also displayed in the tooltip.

Unit Scale
   Scale factor to use when converting between :term:`Blender Units` and *Metric*/*Imperial*.

   .. tip::

      Usually you will want to use the *Length* presets to change to scale factor,
      as this does not require looking up values to use for conversion.

Separate Units
   When *Metric* or *Imperial* display units as multiple values,
   for example, "2.285m" will become "2m 28.5cm".

.. Normally we would avoid documenting long lists of values
   however, this is not displayed anywhere else.

.. list-table:: Imperial Units
   :header-rows: 1
   :stub-columns: 1

   * - Full Name
     - Short Name(s)
     - Scale of a Meter
   * - thou
     - ``mil``
     - 0.0000254
   * - inch
     - ``"``, ``in``
     - 0.0254
   * - foot, feet
     - ``'``, ``ft``
     - 0.3048
   * - yard
     - ``yd``
     - 0.9144
   * - chain
     - ``ch``
     - 20.1168
   * - furlong
     - ``fur``
     - 201.168
   * - mile
     - ``mi``, ``m``
     - 1609.344

.. list-table:: Metric Units
   :header-rows: 1
   :stub-columns: 1

   * - Full Name
     - Short Name(s)
     - Scale of a Meter
   * - micrometer
     - ``um``
     - 0.000001
   * - millimeter
     - ``mm``
     - 0.001
   * - centimeter
     - ``cm``
     - 0.01
   * - decimeter
     - ``dm``
     - 0.1
   * - meter
     - ``m``
     - 1.0
   * - dekameter
     - ``dam``
     - 10.0
   * - hectometer
     - ``hm``
     - 100.0
   * - kilometer
     - ``km``
     - 1000.0


Keying Sets
===========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Scene --> Keying Sets`

See :doc:`/animation/keyframes/keying_sets`.


Color Management
================

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Scene --> Color Management`

Options to control how images appear on the screen.

For :ref:`Color Management settings <render-post-color-management>` for more information.


.. move to audio rendering?

.. _data-scenes-audio:
.. _bpy.ops.sound.bake_animation:
.. _bpy.types.Scene.audio_volume:

Audio
=====

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Scene --> Audio`

Options to control global audio settings.

Volume
   Volume for the scene.
Update Animation Cache
   Updates the audio animation cache. This is useful if you start noticing artifact in the audio.


Distance Model
--------------

Distance Model
   Changes how the sound attenuation is calculated based on the distance.
   Most physically correct is the *Inverse* model,
   but it's also possible to choose a linear and an exponential falloff.
   The clamped modes limit the volume to be lower than 100% (1.0),
   that means if the distance is smaller than the reference distance, the volume is always 100%.
   For an exact description of each option
   see the `OpenAL documentation <https://www.openal.org/documentation/>`__.
Speed
   Speed of the sound for the Doppler effect calculations.
   The typical value is 343.3 m/s in air, in water for example this value is around 1560 m/s.
Doppler
   Controls how strong the Doppler effect is.
   You can exaggerate or attenuate the change of pitch, but physically correct is a factor of 1.0.


.. _bpy.types.FFmpegSettings.audio_mixrate:
.. _bpy.types.FFmpegSettings.audio_channels:

Format
------

These settings, along with the settings found in the
:ref:`Encoding Panel <render-output-video-encoding-panel>`
change how sound is exported while rendering.

To control how sounds plays back from within Blender, see the audio settings
in the :ref:`User Preferences <prefs-system-sound>`.

Channels
   Sets the audio channel count. Available options are:
   *Mono*, *Stereo*, *4 Channels*, *5.1 Surround*, *7.1 Surround*.
Mix Rate
   Sets the audio `sampling rate <https://en.wikipedia.org/wiki/Sampling_(signal_processing)#Sampling_rate>`__.


Gravity
=======

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Scene --> Gravity`

Options to control global gravity used for physics effects.

See the :doc:`Physics chapter </physics/gravity>` for more information.


Rigid Body World
================

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Scene --> Rigid Body World`

The *Rigid Body World* is a group of rigid body objects,
which holds settings that apply to all rigid bodies in this simulation.

See :doc:`Rigid Body World </physics/rigid_body/world>` for more information.


.. _bpy.types.RenderSettings.simplify_subdivision:
.. _data-system-scenes-properties-simplify:

Simplify
========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Properties editor --> Scene --> Simplify`

Subdivision
   Maximum number of *Viewport*/*Render* subdivisions to use for
   the :doc:`Subdivision Modifier </modeling/modifiers/generate/subsurf>`.

Child Particles
   Percentage of :doc:`Child Particles </physics/particles/emitter/children>`
   to see in the *Viewport*/*Render*.

.. seealso::

   There are also renderer specific *Simplify* settings for 
   :ref:`Cycles <render-cycles-settings-scene-simplify>`.
