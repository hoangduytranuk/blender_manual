
***********
Text Layout
***********

Text in Blender can be laid out in some relatively advanced ways,
defining columns or blocks of text, using different alignments, and so on.

Those features are similar in concept to what you can find in :abbr:`DTP (DeskTop Publishing)` software
(like `Scribus <https://www.scribus.net/>`__), although at a very basic level currently.


Paragraph
=========

.. admonition:: Reference
   :class: refbox

   :Mode:      All
   :Panel:     :menuselection:`Properties editor --> Font --> Paragraph`

The *Paragraph* Panel has settings for the alignment and spacing of text.

.. figure:: /images/modeling_texts_properties_paragraph-settings.png

   The Paragraph panel.


Alignment
---------

Horizontal Alignment
   Left
      Aligns text to the left of the frames when using them,
      else uses the origin of the *Text* object as the starting point of the text (which grows to the right).
   Center
      Centers text in the frames when using them,
      else uses the origin of the *Text* object as the mid-point of the text
      (which grows equally to the left and right).
   Right
      Aligns text to the right of the frames when using them,
      else uses the origin of the *Text* object as the ending point of the text (which grows to the left).
   Justify
      Only flushes a line when it is terminated by a word-wrap (**not** by a newline),
      and uses *white-space* instead of *character spacing* (kerning) to fill lines.
   Flush
      Always flushes the line, even when it is still being typed-in.
      It uses character spacing (kerning) to fill lines.

   .. note:: Both *Justify* and *Flush* only work within frames.

Vertical Alignment
   Top Base-Line
      - With text boxes, aligns the 'top' base-line of the text to the top of the frames.
      - With no text box, aligns the actual base-line of the text to the origin of the object,
        and grows to the bottom.

      .. note::

         That difference of reference point in the first line
         depending on usage of boxes or not is indeed confusing.

   Top
      - With text boxes, aligns the top of the text to the top of the frames.
      - With no text box, aligns the top of the text to the origin of the object, and grows to the bottom.
   Center
      - With text boxes, centers the text in the frames.
      - With no text box, centers the text on the origin of the object,
        and grows in both top and bottom directions equally.
   Bottom
      - With text boxes, align the bottom of the text to the bottom of the frames.
      - With no text box, align the bottom of the text to the origin of the object, and grows to the top.
   Bottom Base-Line
      - With text boxes, aligns the base-line of the text to the bottom of the frames.
      - With no text box, aligns the base-line of the text to the origin of the object, and grows to the top.


Spacing
-------

Character Spacing
   A factor by which space between each character (kerning) is scaled in width.

   In Edit Mode in the *3D View*, you can also control individual kerning
   at text cursor position by pressing :kbd:`Alt-Left` / :kbd:`Alt-Right` to decrease/increase it.
Word Spacing
   A factor by which white-space between words is scaled in width.
Line Spacing
   A factor by which the vertical space between lines is scaled.

Offset X/Y
   These settings control the X and Y offset of the text position within the object.
   This applies relatively to the object's origin, either to the whole text or, when using text boxes, to each frame.


.. _bpy.types.TextBox:

Text Boxes
==========

.. admonition:: Reference
   :class: refbox

   :Mode:      All
   :Panel:     :menuselection:`Properties editor --> Font --> Text Boxes`

Text boxes (or frames) allow you to distribute the text among rectangular areas within a single text object.
An arbitrary number of freely positionable and re-sizable text frames are allowed per text object.

The text flows continuously from the lowest-numbered frame to the highest-numbered frame with text
inside each frame word-wrapped.
It flows between frames when a lower-numbered frame cannot fit any more text.
If the last frame is reached, text overflows out of it (by default, see options below).


.. figure:: /images/modeling_texts_properties_frame-upperpanel-area.png

   Text Boxes panel.

Add Textbox
   Inserts a new frame, just after the current one (in text flow order).
   The new frame will have the same size and position as the selected one.

Delete ``X``
   Delete the current frame.

Overflow
   How to handle text overflowing available space in the defined boxes.

   Overflow
      Just keep text running out of the last box.

   Scale to Fit
      Scale text to fit into the available space.

   Truncate
      Hide the end of the text that does not fit into the available space.

      .. note::

         It will only truncate in *Object Mode*,
         in *Edit Mode* the whole text remains visible (and overflows as needed).

Size X/Y
   Specifies the width and height of the text box, if set to **zero** no word-wrap happens
   (it is ignored, and the whole text box system is disabled if all are set to a null size).

Offset X/Y
   Controls the *X* and *Y* offset of the frame, i.e. its position.

.. figure:: /images/modeling_texts_properties_frame-example4.png

   Multiple columns, text flowing between boxes.
