.. _bpy.types.VoxelDataTexture:

**********
Voxel Data
**********

Voxel data renders a voxel source, working very similarly to an image texture, but in 3D.
Various input data source types are available (such as smoke voxel data, or external files),
as well as various interpolation methods.

The default voxel data source, Smoke, is used for rendering smoke simulations.
Other sources include binary raw formats, and Image Sequence,
which can be used to stack a sequence of images into a 3D representation,
which is a common format for medical volume data such as CT scans.


Settings
========

.. figure:: /images/render_blender-render_textures_types_volume_voxel-data_panel.png

   Voxel Data panel.

File Format
   Blender Voxel
      Default binary voxel file format.
   8 bit RAW
      8 bit gray-scale binary data.
   Image Sequence
      Generate voxels from a sequence of image slices.
   Smoke
      Render voxels from a Blender smoke simulation.

Source Path
   The external source data file to use for 8 bit Raw data and Blender Voxel formats.

Domain Object (Smoke)
   Object used as the smoke simulation domain.

Source
   Smoke
      Use smoke density and color as texture data.
   Flame
      Use flame temperature as texture data.
   Heat
      Use smoke heat as texture data. Values from -2.0 to 2.0 are used.
   Velocity
      Use smoke velocity as texture data.

Resolution
   Resolution of the voxel grid when using 8 bit Raw data.

Interpolation
   Nearest Neighbor
      No interpolation, fast but blocky and low quality.
   Linear
      Good smoothness and speed.
   Quadratic
      Mid-range quality and speed.
   Cubic Catmull-Rom
      Smoothed high-quality interpolation, but slower.

Extension
   Extend
      Extend by repeating edge pixels of the image.
   Clip
      Clip to image size and set exterior pixels as transparent.
   Repeat
      Cause the image to repeat horizontally and vertically.

Intensity
   Multiplier for intensity values.
