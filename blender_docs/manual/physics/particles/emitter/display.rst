
*******
Display
*******

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Particle System --> Display`

The Display Panel controls how particles are displayed in the 3D View.
This does not necessarily determine how they will appear when rendered.

Draw Method
   None
      The particles are not shown in the 3D View and are not rendered.
      The emitter may be rendered though.
   Point
      Particles are displayed as square points.
      Their size is independent of the distance from the camera.
   Circle
      Particles are displayed as circles that face the view.
      Their size is independent of the distance from the camera.
   Cross
      Particles are displayed as 6-point crosses that align to the rotation of the particles.
      Their size is independent of the distance from the camera.
   Axis
      Particles are displayed as 3-point axes.
      This is useful if you want to see the orientation and rotation of particles in the viewport.
      Increase the *Draw Size* until you can clearly distinguish the axis.

Particles visualized like Point, Circle, Cross and Axis do not have any special options,
but can be very useful when you have multiple particle systems at play,
if you do not want to confuse particles of one system from another
(e.g. in simulations using *Boids* physics).

Display
   Specifies the percentage of all particles to show in the viewport (all particles are still rendered).
Draw Size
   Specifies how large (in pixels) the particles are drawn in the viewport.

Size
   Draw the size of the particles with a circle.
Velocity
   Draw the velocity of the particles with a line that points in the direction of motion,
   and length relative to speed.
Number
   Draw the id-numbers of the particles in the order of emission.


Color
=====

The Color Menu allows you to draw particles according to certain particle properties.

None
   Particles are black.
Material
   Particles are colored according to the material they are given.
Velocity
   Color particles according to their speed.
   The color is a ramp from blue to green to red, Blue being the slowest,
   and Red being velocities approaching the value of *Max* or above.
   Increasing *Max* allows for a wider range of particle velocities.
Acceleration
   Color particles according to their acceleration.
