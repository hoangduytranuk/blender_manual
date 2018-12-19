
************
Introduction
************

.. figure:: /images/editors_vse_sequencer_strips_introduction_strip-graphic.svg

   Strip schematic.

A strip is a container which carries frames provided by one or more sources (input).
It is defined by a *Start Frame* and a *Length*, and is displayed as a colored horizontal rectangle.


Add
===

.. admonition:: Reference
   :class: refbox

   :Menu:      :menuselection:`Add`
   :Hotkey:    :kbd:`Shift-A`

.. figure:: /images/editors_vse_sequencer_strips_introduction_add-menu.png
   :align: right

   The Add Menu.

The Add menu is the main menu you will be using to add content to the VSE.
In general, you load up your strips, create strips of special transition effects,
and then animate out your sequence by selecting "Do Sequence" and clicking the *Animation* button.
You can use the Add menu in the header,
or hover your mouse cursor over the Sequence workspace and press :kbd:`Shift-A`.

Blender does not care which of these you use; you can freely mix and match any of them.
When you choose to add one of these, it lets you either choose a data-block or
the VSE editor will switch to a File Browser for you to select what you want to add.
Supported files are filtered by default.

The start frame of the newly created strips will be placed at the position of the frame indicator.
When loading multiple files (movie and sound) at the same time each will be add one after the other.


Visualization
=============

They all become a color-coded strip in the VSE:

- Scene strip: Light green.
- Clip strip: Dark blue.
- Mask strip: Red.
- Movie strip: Aquamarine.
- Image strip: Purple.
- Sound strip: Turquoise.

Each of the effect strips has its own color.
