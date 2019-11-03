.. _composite-nodes-input-index:

###############
  Input Nodes
###############

Input nodes produce information from some source.
For instance, an input could be:

- taken directly from the active camera in a selected scene,
- from a ``JPG``, ``PNG``, etc. file as a static picture,
- a movie clip (such as an image sequence or video),
- or just a color or value.

These nodes generate the information that feeds other nodes.
As such, they have no input-connectors; only outputs.

.. toctree::
   :maxdepth: 1

   bokeh_image.rst
   image.rst
   mask.rst
   movie_clip.rst
   render_layers.rst
   rgb.rst
   texture.rst
   time.rst
   track_position.rst
   value.rst
