
******
Colors
******

.. admonition:: Reference
   :class: refbox

   :Mode:      Stroke Edit Mode
   :Panel:     :menuselection:`Properties region --> Grease Pencil Colors`

Palette
   A :ref:`ui-data-block` to select a palette, which is a set of colors.
   Switching palettes will change all strokes color in all layers if the same colors are linked.

   New ``+``
      If there are more than one palette,
      all colors of the old palette will be transferred to the new selected palette.

      - If the color exist in the new palette (same name),
        the stroke is linked to new color.
      - If the color does not exist in the new palette,
        a new color is added to the palette in order to keep the stroke.
Colors
   A :ref:`ui-list-view` of colors grouped in the palette linked as stroke or fill colors.
   If a color with strokes is removed, all strokes of this color are removed.
   Any change to line color or fill color, will change any stroke of any layer using this color.
   A palette must contain at least one color, so the last one cannot be deleted.

   Lock (padlock icon)
      ToDo 2.78.
   Hide (eye icon)
      ToDo 2.78.
   Ghost (ghost icon)
      ToDo 2.78.

   Specials
      ToDo 2.78.

Stroke
   Sets the line color and the maximum opacity (which is also affected by the brush strength).
Fill
   Sets the color of the interior space enclosed by the strokes.
   Increase the opacity from zero to make the fill visible.
   Fill works best on convex shapes, unless you are using *High Quality Fill* (see below).

Volumetric Strokes
   An alternative drawing technique by drawing strokes as a series of filled screen-aligned disks.
   Get best results with partial opacity and large stroke widths.
High Quality Fill
   Uses a better fill algorithm that works better for concave drawings.
