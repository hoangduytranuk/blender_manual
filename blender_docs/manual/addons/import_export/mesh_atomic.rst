
************************
Atomic Blender (PDB/XYZ)
************************

.. admonition:: Reference
   :class: refbox

   :Category:  Import-Export
   :Menu:      :menuselection:`File --> Import --> PDB (.pdb)`
               :menuselection:`File --> Import --> XYZ (.xyz)`
   :Panel:     :menuselection:`3D View --> Sidebar --> Create --> Atomic Blender Utilities`


Atomic Blender Utilities
========================

The *Atomic Blender Utilities* panel make your life easier during manipulating atoms of imported structures.


Custom Data File
----------------

A separate custom data file containing all types of radii and colors of the atoms can be loaded.
Such an option is useful when one wants to use predefined values for radii and colors.
An example can be downloaded from here: `Custom data file <http://development.root-1.de/X-Download/atom_info.dat>`__.

The custom data file is an ASCII file, which can be duplicated and modified by the user.
The radius and/or color of the atoms can be permanently changed as follows:
Search the name of the atom and change the radius (``Radius used``).
Do the same with the RGB values for the color.
The value RGB(1.0, 1.0, 1.0) corresponds to white and RGB(0.0, 0.0, 0.0) is black.

The data file needs to be loaded first. The colors and radii are changed after executing *Apply*.
Note that only selected atoms are changed.


Measure Distances
-----------------

This is to measure the distance of two objects in Object Mode but also in Edit Mode. The unit is Ångström.


All Changes Concern
-------------------

This selector determines which objects are subject for changes defined by the options directly below.
The changes are either applied on only selected objects or on all objects in the current scene and layer.


Change Atom Size
----------------

Type of Radii
   Type
      With this selector the type of radii can be chosen.
      Either one uses Predefined, Atomic or Van der Waals radii.
      The default values for Predefined radii are the Atomic radii.
   Charge
      For option *Ionic radii*, the charge state can be chosen and
      the radii of selected objects are instantaneously changed.
      The best is to first select one type of atom (e.g. only all hydrogen ones) and then to apply the charge state.

Radii in pm
   All radii of a specific type of atom can be manipulated.
   Type in the name of the atom (e.g. 'Hydrogen') and choose the radius in picometer.

Radii by Scale
   This modifies the radii of all atoms with one scaling factor.
   Type in the scaling factor and increase or decrease the size of the radii by
   pushing *Bigger* button or *Smaller* button, respectively.


Change Stick Size
-----------------

The diameter of the sticks can be changed, too.
The buttons *Bigger* and *Smaller* allow increasing or decreasing the diameter, respectively.
The scale factor determines, how strong the change of diameter will be.
By using the Outliner, one can apply these operators on only a selection of sticks
(e.g. only the sticks of the hydrogen atoms).


Change Atom Shape
-----------------

It is possible to change the shape (sphere, cube, icosphere, etc.) and material of the atoms.
First, select your atoms in the 3D Viewport or the Outliner.

Shape
   Choose the shape in the first selector.
Material
   Choose one of the materials in the second selector.
   The materials are only examples, further refinements can be done in Materials tab of the Properties editor.
Special
   Here, you can choose an object with a special shape, material, etc.
   Such objects are quite nice to represent defects in atomic structures.
   When choosing such a special object, you cannot anymore separately choose the shape and material from above.
   In Objects and Materials tabs of the Properties editor further changes can be done.

Replace
   After all, push the *Replace* button.
   The shape and/or material of all selected atoms are then changed.
   This option works for objects and dupliverts object structures.

Default
   If you want to have the default values (NURBS spheres and specific element colors and sizes)
   of selected atoms push the *Default* button.


Separate Atoms
--------------

When structures are imported via the PDB or XYZ importer the atoms are put into
a so-called dupliverts structure, somewhat into 'groups' of elements (e.g. all hydrogen atoms).
Single atoms can be deleted or displaced in Edit Mode of Blender
by modifying the properties (position) of the vertices. However,
they are always a part of the structure and are not independent objects.
Sometimes one would like to mark single atoms or replace the atoms by something different:
For example: Imagine you have a NaCl(001) surface where you would like to replace
an atom by an atomic defect in form of a ball with a different color.

To separate single atoms, one needs to select the atom (vertices) first in Edit Mode.
In the *Atomic Blender Utilities* panel, the *Object* selector and the *Separate* button appear at the bottom.
If the selector remains on *Unchanged* the type of object (NURBS, mesh, meta) and its properties will not be changed.
If desired also an other type of object can chosen, which then replaces the standard type of object.

After having chosen the type of object use bottom *Separate Atoms* to separate the selected atoms:
the atoms are then single, new objects, which can be manipulated in any way.
They appear in the Outliner and carry the suffix ``_sep``.

.. hint:: Converting All Atoms of a Dupliverts Structure to Real Objects

   Do the following: Select the whole structure (molecules, surface, etc.) with the mouse.
   Go to objects :menuselection:`Object --> Apply --> Make Instances Real`.
   With this you produce real objects! In the Outliner delete the remaining dupliverts structures,
   named like "Carbon", "Hydrogen", etc.
