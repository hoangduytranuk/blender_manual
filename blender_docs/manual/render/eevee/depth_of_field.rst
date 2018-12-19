
**************
Depth of Field
**************

Depth of field is done as a post-process in Eevee.

The depth of field effect is using the same :doc:`camera </render/cycles/camera>` settings as Cycles.

.. note::

   Depth of Field only works in Camera View.


Settings
========

.. admonition:: Reference
   :class: refbox

   :Panel:     :menuselection:`Render --> Depth of Field`

Max Size
   Max size of the bokeh shape for the depth of field (lower is faster).

   .. note::

      Because of performance reason, the viewport can exhibit color artifacts when using large bokeh sizes.
      These artifacts are not present in the final render.
