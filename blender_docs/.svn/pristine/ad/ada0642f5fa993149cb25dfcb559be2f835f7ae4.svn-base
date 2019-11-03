.. TODO2.8: Move/split? Move text style toggle to editing.

.. TODO(campbell): Link to curve docs for all shared properties instead of documenting twice.

**********
Properties
**********

Shape
=====

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Properties --> Text --> Shape`

As you can see in the *Shape* panel, texts have most of the same options as
:doc:`Curves </modeling/curves/properties/data>`.

Resolution
   Preview U
      The surface resolution in the U direction to use in the viewport.
   Render U
      The surface resolution in the U direction, set to zero to use the *Preview* resolution.
Fast Editing
   Does not fill polygons while editing text.
Fill Mode
   Determines the way a Curve is filled in when it is extruded and/or beveled.

   Front
      Fills in the front side of the surface.
   Back
      Fills in the back side of the surface.
Fill Deformed
   Fills the curves after applying all modification that might deform the curve (i.e. shape keys and modifiers).


Texture Space
=============

Each Object can have an automatically generated UV map, these maps can be adjusted here.

See :ref:`Generated UV Properties <properties-texture-space>` for more information.


Geometry
========

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Properties --> Font --> Geometry`

Offset
   Alters the space between letters.
Extrude
   Will extrude the text along both the positive and negative local Z axes.
Taper Object
   Used to select a curve object that can be used to cause the characters to get thinner towards one end.
   You can also alter the proportions of the Taper throughout the tapered object by moving/scaling/rotating
   the Control Points of the *Taper Object*. The *Taper Object* can only be a curve.
   Editing the Handles and Control Points of the *Taper Object* will cause the original object to change shape.
Map Taper
   Map taper to the beveled section of the curve.


Bevel
-----

See :ref:`Curve Bevel <modeling-curve-bevel>` for more details.

.. _modeling-text-character:

Font
====

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Properties editor --> Font --> Font`

Bold
   Toggled with the *Bold* button before typing.
   Text can also be set to Bold by selecting it then using the *Bold* button in the Tool Shelf.
Italics
   Toggled with the *Italic* button before typing.
   Text can also be set to Italic by selecting it then using the *Italic* button in the Tool Shelf.
Underline
   Enables underlining, as controlled by the Underline settings above.
Small Caps
   Enable the *Small Caps* option to type characters as small caps.

   The size of the *Small Caps* can be changed with the *Small Caps Scale* setting.
   Note that the *Small Caps Scale* is applied the same to all *Small Caps* formatted characters.



Transform
---------

Size
   Controls the size of the whole text (no way to control each char size independently).
   Note however, that chars with different fonts (different styles, see below) might have different visible sizes.
Shear
   Controls the inclination of the whole text.
   Different to as it may seem, this is not similar to italics style.

   .. figure:: /images/modeling_texts_properties_shear-example.png
      :width: 340px

      Shear example.

Object Font
   Allows individual objects to be used to render fonts.
   This allows you to create/model your own complex font inside Blender!
   This field is used to select the objects prefix name to be used
   to locate the individual characters used for typing.
   This is quite a complex process, so here are detailed steps to follow:

   #. Create the font characters, each character can be any object type (mesh, curve, etc.).
      They must all have a name following the naming schema:
      "common prefix" followed by the "character name" (e.g. "ft.a", "ft.b", etc.).
   #. For the *Text* object, enable
      :doc:`Instancing Vertices </scene_layout/object/properties/instancing/verts>`.
   #. In the *Font* tab, fill the *Object Font* field with the "common prefix" of your "font" objects.
      Now, each time a character in your text matches the *suffix part* of a "font" object's name,
      this object is duplicated on this character.

   .. note::

      The objects are duplicated so that their center is positioned at
      the *lower right corner* of the corresponding characters.

Text on Curve
   Select a curve object for the text object to follow.

   .. figure:: /images/modeling_texts_properties_curved-lowres-example.png
      :width: 360px

      Text on curve.

   .. tip::

      You can also use the :doc:`Curve Modifier </modeling/modifiers/deform/curve>`
      which offers more control.

Underline
   Toggled with the *Underline* button before typing.
   Text can also be set to Underlined by selecting it then using the *Underline* button in the Tool Shelf.
Underline Position
   This allows you to shift vertically the position of the underline.
Underline Thickness
   This controls the thickness of the underline.
Small Caps Scale
   Type small capital text.


Paragraph
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Properties editor --> Font --> Paragraph`

The *Paragraph* Panel has settings for the alignment and spacing of text.


Alignment
---------

Horizontal Alignment
   Left
      Aligns text to left of frames when using them,
      else uses the origin of the *Text* object as the starting point of the text (which grows to the right).
   Center
      Centers text in the frames when using them,
      else uses the origin of the *Text* object as the mid-point of the text
      (which grows equally to the left and right).
   Right
      Aligns text to right of frames when using them,
      else uses the origin of the *Text* object as the ending point of the text (which grows to the left).
   Justify
      Only flushes a line when it is terminated by a word-wrap (**not** by :kbd:`Return`),
      it uses *white-space* instead of *character spacing* (kerning) to fill lines.
   Flush
      Always flushes the line, even when it is still being entered;
      it uses character spacing (kerning) to fill lines.

   .. note:: Both *Justify* and *Flush* only work within frames.

Vertical Alignment
   Top Base-Line
      Aligns the text base-line to top of frames when using them,
      else uses the origin of the *Text* object as the starting point of the text (which grows to the bottom).
   Top
      Aligns top of text to the origin of the *Text* object (which grows to the bottom).
      It behaves as *Top Base-Line* when using frames. *Top* only works without frames.
   Center
      Centers text in the frames when using them,
      else uses the origin of the *Text* object as the mid-point of the text
      (which grows equally to the top and bottom).
   Bottom
      Aligns text to bottom of frames when using them,
      else uses the origin of the *Text* object as the ending point of the text (which grows to the top).


Spacing
-------

Character Spacing
   A factor by which space between each character is scaled in width.
Word Spacing
   A factor by which white-space between words is scaled in width.
   You can also control it by pressing :kbd:`Alt-Left` or :kbd:`Alt-Right`
   to decrease/increase spacing by steps of 0.1.
Line Spacing
   A factor by which the vertical space between lines is scaled.

Offset X/Y
   These settings control the X and Y offset of the text, regarding its relative positioning. Note that with
   `Text Boxes`_, it applies to all frames' content.


.. _bpy.types.TextBox:

Text Boxes
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Properties editor --> Font --> Text Boxes`

Text "Boxes" allow you to distribute the text among rectangular areas within a single text object.
An arbitrary number of freely positionable and re-sizable text frames are allowed per text object.

Text flows continuously from the lowest-numbered frame to the highest-numbered frame with text
inside each frame word-wrapped.
Text flows between frames when a lower-numbered frame cannot fit any more text.
If the last frame is reached, text overflows out of it.

Add Textbox
   Inserts a new frame, just after the current one (in text flow order).
   The new frame will have the same size and position as the selected one.
Delete (X icon)
   Delete the current frame.

Overflow
   TODO2.8.

Size X/Y
   Specifies the width and height of the text box,
   if set to **zero** no word-wrap happens.
Offset X/Y
   Controls the *X* and *Y* offset of the frame.

.. figure:: /images/modeling_texts_properties_frame-example4.png

   Multiple columns, text flowing between boxes.
