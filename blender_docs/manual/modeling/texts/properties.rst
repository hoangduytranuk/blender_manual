.. TODO2.8: Move/split? Move text style toggle to editing.

**********
Properties
**********

Shape
=====

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Properties editor --> Text --> Shape`

.. figure:: /images/modeling_texts_properties_shape-settings.png

   The Shape panel.

As you can see in the *Shape* panel, texts have most of the same options as
:doc:`Curves </modeling/curves/properties/data>`.

Resolution
   Preview
      The surface resolution in the U direction to use in the viewport.
   Render
      The surface resolution in the U direction, set to zero to use the *Preview* resolution.
Fill
   Mode
      Determines the way a Curve is filled in when it is extruded and/or beveled.

      Front
         Fills in the front side of the surface.
      Back
         Fills in the back side of the surface.
   Fill Deformed
      Fills the curves after applying all modification that might deform the curve (i.e. shape keys and modifiers).
Display
   Fast Editing
      Does not fill polygons while editing text.


Texture Space
=============

Each Object can have an automatically generated UV map, these maps can be adjusted here.

See :ref:`Generated UV Properties <properties-texture-space>` for more information.


Geometry
========

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Properties editor --> Font --> Geometry`

Modification
   Offset
      Alters the space between letters.
   Extrude
      Will extrude the text along both the positive and negative local Z axes.
Bevel
   Depth
      Changes the size of the bevel.
   Resolution
      Alters the smoothness of the bevel.
Taper Object
   Used to select a curve object that can be used to cause the characters to get thinner towards one end.
   You can also alter the proportions of the Taper throughout the tapered object by moving/scaling/rotating
   the Control Points of the *Taper Object*. The *Taper Object* can only be a curve.
   Editing the Handles and Control Points of the *Taper Object* will cause the original object to change shape.
Bevel Object
   Used to select a curve object that can be used to give custom bevel results.

.. seealso::

   :doc:`Curve geometry </modeling/curves/properties/geometry>` for more details and examples.


Font
====

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Properties editor --> Font --> Font`

The *Font* panel has several options for changing the look of characters.


Loading and Changing Fonts
--------------------------

Blender comes with a *built-in* font by default that is displayed in
each of the four font style data-block menus.
The *built-in* font is always present and shows in this list as "Bfont".
The data-block menu contains a list displaying the currently loaded fonts.
Select one for each font style.

To load a different *Font*, click one of the *Load* buttons
in the *Font* panel and navigate to a font file.
The :doc:`File Browser </editors/file_browser/index>` will give all valid fonts a capital "F" icon.

If you select a font that is unsupported by Blender, you will get the error ``Not a valid font``.

.. note:: Location of Fonts on Unix

   Fonts are typically located under ``/usr/lib/fonts``, or some variant like ``/usr/lib/X11/fonts``,
   but not always. They may be in other locations as well,
   such as ``/usr/share/local`` or ``/usr/local/share``, and possibly related sub-trees.

Remember the same font will be applied to all chars with same style in a text,
but that a separate font is required for each style.
For example, you will need to load an *Italics* font in order to make characters or words italic.
Once the font is loaded you can apply that font "Style" to the selected characters or the whole object.
In all, you would need to load a minimum of four different types of fonts to represent each style
(Normal, Italics, Bold, Bold-Italics).

It is important to understand, that Blender does not care what font
you load for "normal", "bold", etc., styles.
This is how you can have up to four different fonts in use in the same text,
but you have to choose between different styles of a same font, or different fonts.
Blender has a number of typographic controls for changing the style and layout of text,
found in the *Font* panel.


Size and Shear
--------------

Size
   Controls the size of the whole text (no way to control each char size independently).
   Note however, that chars with different fonts (different styles, see below) might have different visible sizes.
Shear
   Controls the inclination of the whole text.
   Different to as it may seem, this is not similar to italics style.

   .. figure:: /images/modeling_texts_properties_shear-example.png
      :width: 340px

      Shear example.


Objects as Fonts
----------------

You can also "create" your own "font" inside Blender! This is quite a complex process,
so let us detail it:

#. First, you must create your chars. Each char, of any type, is an object (mesh, curve, meta...).
   They all must have a name following the schema:
   *common prefix* followed by the *char name* (e.g. "ft.a", "ft.b", etc.).
#. Then, for the *Text* object, you must enable the *Dupli Vertices* button
   (:menuselection:`Object --> Animation Settings` panel).
#. In the *Font* tab, fill the *Object Font* field with the *common prefix* of your "font" objects.

Now, each time a char in your text matches the *suffix part* of a "font" object's name,
this object is duplicated on this char. The original chars remain visible. The objects are
duplicated so that their center is positioned at the *lower right corner* of the
corresponding characters.

Text on Curve
   Used to select a curve for the text object to follow.

   .. figure:: /images/modeling_texts_properties_curved-lowres-example.png
      :width: 360px

      Text on curve.

   .. tip::

      You can also use the :doc:`Curve Modifier </modeling/modifiers/deform/curve>`
      which offers more control.

Underline
   Toggled with the *Underline* button before typing.
   Text can also be set to Underlined by selecting it then using the *Underline* button in the Tool Shelf.

   Position
      This allows you to shift vertically the position of the underline.
   Thickness
      This controls the thickness of the underline.


.. _modeling-text-character:

Character
---------

.. figure:: /images/modeling_texts_properties_font-settings.png
   :width: 290px

   Character options to, for example, type bold text.

Bold
   Toggled with the *Bold* button before typing.
   Text can also be set to Bold by selecting it then using the *Bold* button in the Tool Shelf.
Italics
   Toggled with the *Italic* button before typing.
   Text can also be set to Italic by selecting it then using the *Italic* button in the Tool Shelf.
Underline
   Enables underlining, as controlled by the Underline settings above.
Small Caps
   Type small capital text.

Blender's *Bold* and *Italic* buttons do not work the same way as other applications,
as they also serve as placeholders for you to load up other fonts manually,
which get applied when you define the corresponding style; see `Font`_.

To apply the Bold/Italics/Underline attribute to a set of characters, you either turn on
*Bold* / *Italics* / *Underline* prior to typing characters,
or highlight (select) first and then toggle Bold/Italics/Underline.


Setting Case
------------

You can change the text case by selecting it then clicking the *To Upper* or
*To Lower* in the Tool Shelf.

Enable the *Small Caps* option to type characters as small caps.

The size of the *Small Caps* can be changed with the *Small Caps Scale* setting.
Note that the *Small Caps Scale* is applied the same to all *Small Caps* formatted characters.


Paragraph
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      All Modes
   :Panel:     :menuselection:`Properties editor --> Font --> Paragraph`

The *Paragraph* Panel has settings for the alignment and spacing of text.

.. figure:: /images/modeling_texts_properties_paragraph-settings.png
   :width: 290px

   The Paragraph panel.


Horizontal Alignment
--------------------

Left
   Aligns text to left of frames when using them,
   else uses the center point of the *Text* object as the starting point of the text (which grows to the right).
Center
   Centers text in the frames when using them,
   else uses the center point of the *Text* object as the mid-point of the text
   (which grows equally to the left and right).
Right
   Aligns text to right of frames when using them,
   else uses the center point of the *Text* object as the ending point of the text (which grows to the left).
Justify
   Only flushes a line when it is terminated by a word-wrap (**not** by :kbd:`Return`),
   it uses *white-space* instead of *character spacing* (kerning) to fill lines.
Flush
   Always flushes the line, even when it is still being entered;
   it uses character spacing (kerning) to fill lines.

Both *Justify* and *Flush* only work within frames.


Vertical Alignment
------------------

Top Base-Line
   Aligns the text base-line to top of frames when using them,
   else uses the center point of the *Text* object as the starting point of the text (which grows to the bottom).
Top
   Aligns top of text to the center point of the *Text* object (which grows to the bottom).
   It behaves as *Top Base-Line* when using frames. *Top* only works without frames.
Center
   Centers text in the frames when using them,
   else uses the center point of the *Text* object as the mid-point of the text
   (which grows equally to the top and bottom).
Bottom
   Aligns text to bottom of frames when using them,
   else uses the center point of the *Text* object as the ending point of the text (which grows to the top).


Spacing
-------

Character
   A factor by which space between each character is scaled in width.
Word
   A factor by which white-space between words is scaled in width.
   You can also control it by pressing :kbd:`Alt-Left` or :kbd:`Alt-Right`
   to decrease/increase spacing by steps of 0.1.
Line
   A factor by which the vertical space between lines is scaled.


Offset
------

X offset and Y offset
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

.. figure:: /images/modeling_texts_properties_frame-upperpanel-area.png

   Text Boxes panel.

Dimensions
   Specifies the *Width* and *Height* of the frame.
   If set to **zero** no word-wrap happens.
Offset
   Controls the *X* and *Y* offset of the frame.
Add Textbox
   Inserts a new frame, just after the current one (in text flow order).
   The new frame will have the same size and position as the selected one.
Delete (X icon)
   Delete the current frame.

.. figure:: /images/modeling_texts_properties_frame-example4.png

   Multiple columns, text flowing between boxes.
