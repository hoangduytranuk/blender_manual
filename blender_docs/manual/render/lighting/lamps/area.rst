.. _bpy.types.AreaLight:

****
Area
****

The *Area* lamp simulates light originating from a surface (or surface-like) emitter.
For example, a TV screen, office neon lamps, a window,
or a cloudy sky are just a few types of area lamp. The area lamp produces shadows with
soft borders by sampling a lamp along a grid the size of which is defined by the user.
This is in direct contrast to point-like artificial lights which produce sharp borders.

.. seealso::

   - :doc:`EEVEE Lighting </render/engines/eevee/lighting>`
   - :doc:`Cycles Lighting </render/engines/cycles/lighting>`
   - :doc:`Workbench Lighting </render/engines/workbench/lighting>`


Lamp Options
============

Color, Power, Size
   These settings are common to most types of lamps,
   and are described in :doc:`Light Properties </render/lighting/lamp_panel>`.
Shape
   Shape of the lamp.

   Rectangle
      The shape of the lamp can be represented as a rectangle and changed with the "X" and "Y" values.
   Square
      The shape of the lamp can be represented as a square and changed with the *Size* property.
   Disk
      The shape of the lamp can be represented as a disk and changed with the *Size* property.
   Ellipse
      The shape of the lamp can be represented as an ellipse and changed with the X and Y values.

   .. tip::

      Choosing the appropriate shape for your *Area* light will enhance the believability of your scene.
      For example, you may have an indoor scene and would like to simulate light entering through a window.
      You could place a *Rectangular* area lamp in a window (vertical) or from neons (horizontal)
      with proper ratio for *Size X* and *Size Y*. For the simulation of the light emitted by
      a TV screen, a vertical *Square* area lamp would be better in most cases.

   .. list-table::

      * - .. figure:: /images/render_blender-render_lighting_lamps_area_introduction_square.png

             Square options.

        - .. figure:: /images/render_blender-render_lighting_lamps_area_introduction_rect.png

             Rectangle options.
Size / Size X / Size Y
   Dimensions for the *Square* or *Rectangle*.
