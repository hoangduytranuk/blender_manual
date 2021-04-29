#!/usr/bin/env python3
import re
import os
import json
from collections import OrderedDict, defaultdict

import datetime
import math
from collections import deque
from difflib import SequenceMatcher as SM
from pprint import pprint as PP
# import html
import subprocess as sub

from translation_finder import TranslationFinder
from ignore import Ignore as IG
from fuzzywuzzy import fuzz

from sphinx_intl import catalog as c
from pytz import timezone
from common import Common as cm
from matcher import MatcherRecord
from definition import Definitions as df

from pprint import pprint
from reftype import RefType
from reflist import RefList
import copy as CP

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

#Leave the variables here to make them obvious and easier to change
YOUR_NAME = "Hoang Duy Tran"
YOUR_EMAIL = "hoangduytran1960@gmail.com"
YOUR_ID = "{} <{}>".format(YOUR_NAME, YOUR_EMAIL)
YOUR_TRANSLATION_TEAM = "London, UK <{}>".format(YOUR_EMAIL)
YOUR_LANGUAGE_CODE = "vi"
TIME_ZONE='Europe/London' # this value can be optained using the code 'import pytz; for entry in pytz.all_timezones(); print(entry)'

#header default values, for internal uses only
default_first_author = "FIRST AUTHOR"
default_mail_address = "MAIL@ADDRESS"
default_year = ", YEAR."

home_dir = os.environ['DEV_TRAN']

long_t = '''
 -- Links to an entry in the :doc:
!=
\"
\"Agent\"
\"You have to select a string of connected vertices too\"
\"auto\" <curve-handle-type-auto>
\"fr\": \"Fran&ccedil;ais\",
\"fr\": \"Français\"
#
####
#blender-coders
#blender-coders <https://blender.chat/channel/blender-coders>
#cos(frame)
#declare
#docs
#docs <https://blender.chat/channel/docs>
#fmod(frame, 24) / 24
#frame
#frame / 20.0
#include
#python <https://blender.chat/channel/python>
#sin(frame)
#today <https://blender.chat/channel/today>
$XDG_CONFIG_HOME
'
'locale' is not under version control
(
(Crepuscular Rays) <https://en.wikipedia.org/wiki/Crepuscular_rays>
(De)select First/Last
(LW)POLYGON
(LW)POLYLINE
(X)
(origin, vertex_coordinates)
(sin( )*4)
*
**
*-0001.jpg
*-0002.jpg
*-0003.jpg
*.avi
*.blend
*.blend1
*.blend2
*.jpg
*.png
*Mirror*
+
+<frame>
+C
+WT
+WT2
+q1
+q11
,
,.?!:;
-
--
--addons
--app-template
--background
--cycles-device CPU
--cycles-print-stats
--debug
--debug-all
--debug-cycles
--debug-depsgraph
--debug-depsgraph-build
--debug-depsgraph-eval
--debug-depsgraph-no-threads
--debug-depsgraph-pretty
--debug-depsgraph-tag
--debug-depsgraph-time
--debug-depsgraph-uuid
--debug-events
--debug-exit-on-error
--debug-ffmpeg
--debug-fpe
--debug-freestyle
--debug-ghost
--debug-gpu
--debug-gpu-force-workarounds
--debug-gpu-shaders
--debug-gpumem
--debug-handlers
--debug-io
--debug-jobs
--debug-libmv
--debug-memory
--debug-python
--debug-value
--debug-wm
--debug-xr
--debug-xr-time
--disable-abort-handler
--disable-autoexec
--disable-crash-handler
--enable-autoexec
--enable-event-simulate
--engine
--env-system-datafiles
--env-system-python
--env-system-scripts
--factory-startup
--factory-startup --debug-all
--frame-end
--frame-jump
--frame-start
--help
--log
--log \"*,^wm.operator.*\"
--log \"wm.*\"
--log-file
--log-level
--log-show-backtrace
--log-show-basename
--log-show-timestamp
--no-native-pixels
--no-window-focus
--python
--python-console
--python-exit-code
--python-expr
--python-text
--python-use-system-env
--render-anim
--render-format
--render-frame
--render-frame 1
--render-output
--scene
--start-console
--threads
--use-extension
--verbose
--version
--window-border
--window-fullscreen
--window-geometry
--window-maximized
-<frame>
-D
-E
-E CYCLES
-E help
-F
-F OPEN_EXR
-M
-P
-R
-S
-W
-Y
-a
-b
-ba
-con
-d
-e
-f
-f -2
-f 10
-h
-j
-m
-m \"message\"
-noaudio
-o
-o /project/renders/frame_#####
-p
-r
-s
-s 10 -e 500
-setaudio
-t
-t 2
-v
-w
-x
-y
.
.*
.*rabbit.*
..
...
... is not a valid Win32 application.
...@bone_name
./Blender.app/Contents/MacOS/Blender
./autosave/ ...
./config/ ...
./config/bookmarks.txt
./config/recent-files.txt
./config/startup.blend
./config/userpref.blend
./config/{APP_TEMPLATE_ID}/startup.blend
./config/{APP_TEMPLATE_ID}/userpref.blend
./datafiles/ ...
./datafiles/locale/{language}/
./python/ ...
./resources/theme/js/version_switch.js
./scripts/ ...
./scripts/addons/*.py
./scripts/addons/modules/*.py
./scripts/addons_contrib/*.py
./scripts/addons_contrib/modules/*.py
./scripts/modules/*.py
./scripts/presets/interface_theme/
./scripts/presets/{preset}/*.py
./scripts/startup/*.py
./scripts/templates_osl/*.osl
./scripts/templates_py/*.py
.001
.MTL
.app
.avi
.bashrc
.bat
.bin
.blend
.blend1
.blend2
.bmp
.btx
.bw
.cin
.dae
.dpx
.dv
.dvd
.eps
.exr
.flv
.gif
.glb
.gltf
.hdr
.html
.inc
.j2c
.jp2
.jpeg
.jpg
.mdd
.mkv
.mov
.mp4
.mpeg
.mpg
.ogg
.ogv
.osl
.oso
.pc2
.pdb
.png
.po
.py
.pyd
.rgb
.rst
.sab
.sat
.sgi
.sh
.so
.srt
.svg
.svn
.tga
.tif
.tiff
.uni
.vdb
.velocities
.vob
.webm
.xxxx
.xyz
.zip
/
//
//render/my-anim-
//render_
//render_####
//render_0001.png
/?
/EXIT
/branches
/fr
/tmp
/tmp/
/usr/lib/X11/fonts
/usr/lib/fonts
/usr/local
/usr/local/cuda/include/host_config.h
/usr/local/share
/usr/share/local
0
0 +
0 + (cos(frame / 8) * 4)
0 + (sin(frame / 8) * 4)
0.1
0.8
0001.jpg
1
1.0
10
10/5+4
1000
1000x500
1001
1002
1010
1011
10km
16
16:9
1:1
1cm
1m 3mm
1m, 3mm
2
2 /
2 / Width
2.285m
2.2mm + 5' / 3\" - 2yards
2.30 <https://archive.blender.org/development/release-logs/blender-230/>
2.31 <https://archive.blender.org/development/release-logs/blender-231/>
2.32 <https://archive.blender.org/development/release-logs/blender-232/>
2.33 <https://archive.blender.org/development/release-logs/blender-233/>
2.34 <https://archive.blender.org/development/release-logs/blender-234/>
2.35 <https://archive.blender.org/development/release-logs/blender-235a/>
2.36 <https://archive.blender.org/development/release-logs/blender-236/>
2.37 <https://archive.blender.org/development/release-logs/blender-237a/>
2.40 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.40>
2.41 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.41>
2.42 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.42>
2.43 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.43>
2.44 <https://archive.blender.org/development/release-logs/blender-244/index.html>
2.45 <https://archive.blender.org/development/release-logs/blender-245/index.html>
2.46 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.46>
2.47 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.47>
2.48 <https://archive.blender.org/development/release-logs/blender-248/index.html>
2.49 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.49>
2.5x <https://www.blender.org/download/releases/#25-series-2009-2011>
2.60 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.60>
2.61 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.61>
2.62 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.62>
2.63 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.63>
2.64 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.64>
2.65 <https://archive.blender.org/wiki/index.php/Dev:Ref/Release_Notes/2.65>
2.66 <https://www.blender.org/download/releases/2-66>
2.67 <https://www.blender.org/download/releases/2-67>
2.68 <https://www.blender.org/download/releases/2-68>
2.69 <https://www.blender.org/download/releases/2-69>
2.70 <https://www.blender.org/download/releases/2-70>
2.71 <https://www.blender.org/download/releases/2-71>
2.72 <https://www.blender.org/download/releases/2-72>
2.73 <https://www.blender.org/download/releases/2-73/>
2.74 <https://www.blender.org/download/releases/2-74/>
2.75 <https://www.blender.org/download/releases/2-75/>
2.76 <https://www.blender.org/download/releases/2-76/>
2.77 <https://www.blender.org/download/releases/2-77/>
2.78 <https://www.blender.org/download/releases/2-78/>
2.79 <https://www.blender.org/download/releases/2-79/>
2.80 <https://www.blender.org/download/releases/2-80>
2.81 <https://www.blender.org/download/releases/2-81/>
2.82 <https://www.blender.org/download/releases/2-82/>
2.83 <https://www.blender.org/download/releases/2-83/>
20 /
210-group
21:9
23cm
256×256
2D Cursor <graph_editor-2d-cursor>
2ft
2m 28.5cm
3*2
3001
3D cursor <editors-3dview-3d_cursor>
3DFACE
3DSOLID
3dview-fly-walk
3dview-multi-object-mode
3dview-nav-zoom-region
3ft/0.5km
4 / Narrowness
43756265
43756265_xxxxxx_yy.bphys
47
4:3
5 × 60 × 30 = 9000
500
6
7200.jpg
9000 / 1.25 = 7200 = 5 × 60 × 24
:
::::
:abbr:
:kbd:
:linenos:
:menuselection:
:term:
<
<-->
<->
<=
<Matrix>
<addon(s)>
<bool>
<code>
<engine>
<expression>
<extra>
<file(s)>
<filename>
<format>
<fps-base>
<fps>
<frame>
<frames>
<h>
<instance_node>
<level>
<lines>
<match>
<name>
<node>
<options>
<path of original footage>/BL_proxy/<clip name>
<path>
<polylist>
<sx>
<sy>
<template>
<threads>
<value>
<verbose>
<vertices>
<w>
==
>
>=
>>>
@
@CTRL
@DEF
@MCH
A
A detailed guide <https://www.miikahweb.com/en/articles/dynamic-paint-guide>
A step-by step introduction <https://www.miikahweb.com/en/articles/blender-dynamicpaint-basics>
AAC <https://en.wikipedia.org/wiki/Advanced_Audio_Coding>
AC3 <https://en.wikipedia.org/wiki/Dolby_Digital>
ACES <https://www.oscars.org/science-technology/sci-tech-projects/aces>
ACES configuration <https://opencolorio.readthedocs.io/en/latest/configurations/_index.html>
ACIS
AMD Drivers and Support Website <https://www.amd.com/en/support>
AMD website <https://www.amd.com/en/support>
API Introduction <https://docs.blender.org/api/current/info_quickstart.html>
API documentation <https://docs.blender.org/api/blender_python_api_current/info_quickstart.html#custom-properties>
API documentation <https://docs.blender.org/api/current/info_overview.html#registration>
ARC
ASE <https://wiki.fysik.dtu.dk/ase/>
AUTO
AVI
AVI <https://en.wikipedia.org/wiki/Audio_Video_Interleave>
AVIJPEG
AVIRAW
Accent Characters
Accuracy
Action <bpy.types.Action>
Action <dopesheet-action-action>
Action or NLA Editor <actions-workflow>
Adaptive Sampling
Add Hook <bpy.ops.object.hook_add_selob>
Add-ons project <https://developer.blender.org/project/profile/3/>
Adding Text
Adding/Removing Layers
Adjust Last Operation <ui-undo-redo-adjust-last-operation>
Advanced Brush Settings <sculpt-tool-settings-brush-settings-advanced>
Advanced Rig Generation
Aim
Alembic home page <https://www.alembic.io/>
Aligned Inherit Scale <bone-relations-inherit-settings>
Animating Cameras <bpy.ops.marker.camera_bind>
Animation <grease-pencil-animation-tools-interpolation>
Animation <https://vimeo.com/1865817>
Animation <https://vimeo.com/1866538>
Animation Player <render-output-animation_player>
Animation player <prefs-file_paths-animation_player>
Animation player <render-output-animation_player>
Annotate <tool-annotate>
Anti-Aliasing Threshold <bpy.types.SceneGpencil.antialias_threshold>
Antialias_Threshold=n.n
Apply <bpy.ops.object.transform_apply>
Applying <bpy.ops.object.transform_apply>
Arc <tool-grease-pencil-draw-arc>
Arccosine <https://en.wikipedia.org/wiki/Inverse_trigonometric_functions>
Arcsine <https://en.wikipedia.org/wiki/Inverse_trigonometric_functions>
Arctangent <https://en.wikipedia.org/wiki/Inverse_trigonometric_functions>
Armature Layers <bpy.types.Armature.layers>
Armature Modifier <bpy.types.ArmatureModifier>
Armatures <armatures-index>
Ask Us Anything! <https://wiki.blender.org/wiki/Reference/AskUsAnything>
Atomic Blender Utilities panel
Attributes
Audio Output <render-output-video-encoding-audio>
Audio Panel <data-scenes-audio>
Audio Preferences <prefs-system-sound>
Auto Completion
Auto Depth <prefs-auto-depth>
Auto Face Map Widgets add-on <https://developer.blender.org/diffusion/BAC/browse/master/object_facemap_auto/>
Auto Handle Smoothing <graph_editor-auto-handle-smoothing>
Auto IK
Auto Normalize <weight-painting-auto-normalize>
Auto Run Python Scripts <prefs-auto-execution>
Auto Save <troubleshooting-file-recovery>
Auto Save Preferences <prefs-auto-save>
Auto Saves <troubleshooting-file-recovery>
Auto Smooth <auto-smooth>
Auto-Keyframing <animation-editors-timeline-autokeyframe>
Auto-Offset. A workflow enhancement for Blender's node editors <https://vimeo.com/135125839>
Auto-Perspective Preference <prefs-interface-auto-perspective>
BEZIER
BLENDER_SYSTEM_DATAFILES
BLENDER_SYSTEM_PYTHON
BLENDER_SYSTEM_SCRIPTS
BLOCK
BMP
BODY
Background Set <scene-background-set>
Bake <physics-bake>
Barcelona Pavilion <https://en.wikipedia.org/wiki/Barcelona_Pavilion>
Batch Rename tool <bpy.ops.wm.batch_rename>
Beer-Lambert law <https://en.wikipedia.org/wiki/Beer%E2%80%93Lambert_law#Expression_with_attenuation_coefficient>
Bendy Bones <bendy-bones>
Best practices for attribution <https://wiki.creativecommons.org/wiki/Marking/Users>
Bevel <bpy.types.Curve.bevel>
Bevel <tool-mesh-bevel>
Bevel Depth <bpy.types.Curve.bevel_depth>
Bevel Resolution <bpy.types.Curve.bevel_resolution>
Bevel Weights <bpy.ops.transform.edge_bevelweight>
Bisect <tool-mesh-bisect>
Blade <tool-blade>
Blend Modes <bpy.types.Material.blend_method>
Blend Modes <https://docs.gimp.org/en/gimp-concepts-layer-modes.html>
Blend-file available here <https://wiki.blender.org/uploads/5/51/Derotest.blend>
Blender 2.78 <https://www.blender.org/download/releases/2-78>
Blender <https://www.blender.org>
Blender API Overview <https://docs.blender.org/api/blender_python_api_current/info_overview.html>
Blender API Quickstart <https://docs.blender.org/api/blender_python_api_current/info_quickstart.html>
Blender Artists <https://blenderartists.org/>
Blender Artists forum <https://blenderartists.org/t/1197801>
Blender Artists: Python Support Forum <https://blenderartists.org/c/coding/python-support>
Blender Cloud <https://cloud.blender.org/>
Blender Cloud add-on <https://archive.blender.org/wiki/index.php/Extensions:2.6/Py/Scripts/System/BlenderCloud/>
Blender Development (Wiki) <https://wiki.blender.org>
Blender FAQ <https://www.blender.org/support/faq/>
Blender Hair Basics <https://www.youtube.com/watch?v=kpLaxqemFU0>
Blender ID <https://id.blender.org/>
Blender ID <https://id.blender.org>
Blender ID site <https://id.blender.org/>
Blender License <https://www.blender.org/about/license/>
Blender Open Data <https://opendata.blender.org/>
Blender Publisher <https://download.blender.org/release/Publisher2.25/>
Blender Python API <https://docs.blender.org/api/current/>
Blender Versions
Blender Wiki <https://wiki.blender.org/wiki/Process/Addons/Rigify>
Blender translation howto <https://wiki.blender.org/wiki/Dev:Doc/How_to/Translate_Blender>
Blender website <https://www.blender.org/download/>
Blender's API documentation <https://docs.blender.org/api/current/>
Blender.app
Blender/Python API Overview <https://docs.blender.org/api/blender_python_api_current/info_overview.html>
Blending <bpy.types.AnimData.action_blend_type>
Blending Mode <bpy.types.Material.blend_method>
Blosc
Bone Envelopes <armature-bones-envelope>
Bounding Volume Hierarchy <https://en.wikipedia.org/wiki/Bounding_volume_hierarchy>
Bounds <bpy.types.Object.show_bounds>
Box <tool-grease-pencil-draw-box>
Box Select <tool-select-box>
Bridge Edge Loops <modeling-meshes-editing-bridge-edge-loops>
Brush <grease-pencil-draw-brushes>
Brush Display <sculpt-paint-brush-display>
Brushes panel <grease-pencil-draw-common-options>
Bug report T34665 <https://developer.blender.org/T34665>
Build from Source <https://wiki.blender.org/wiki/Building_Blender>
Bézier
Bézier Handles <editors-graph-fcurves-settings-handles>
Bézier curves <curve-bezier-handle-type>
Bézier curves <curve-bezier>
C
C:\\blender_docs
C:\\blender_docs\\build\\html
CG Cookie: Blender 2.8 Python Scripting Superpowers for Non-Programmers <https://cgcookie.com/articles/blender-2-8-python-scripting-superpowers-for-non-programmers>
CINEON
CIRCLE
COLOR
COM
CPU
CTRL
CUBE.001
CUDA
CUDA+CPU
CYCLES_CUDA_EXTRA_CFLAGS
Cache Settings
Calculate To Frame <calc-physics-bake-to-frame>
Camera Parent Lock <prefs-camera-parent-lock>
Carve library <https://code.google.com/archive/p/carve/>
Catmull-Clark <https://en.wikipedia.org/wiki/Catmull%E2%80%93Clark_subdivision_surface>
Catmull-Clark subdivision surface <https://en.wikipedia.org/wiki/Catmull%E2%80%93Clark_subdivision_surface>
Caustics <https://en.wikipedia.org/wiki/Caustic_(optics)>
Certified Trainers <https://www.blender.org/certification/>
Cessen's Rigify Extensions <https://github.com/cessen/cessen_rigify_ext>
ChainPredicateIterator
ChainSilhouetteIterator
Chains of Bones
Channels Region
Chebychev distance metric <https://en.wikipedia.org/wiki/Chebyshev_distance>
Checker Deselect
Checker Deselect <bpy.ops.mesh.select_nth>
Child Of <bpy.types.ChildOfConstraint>
Cineon & DPX
Circle <tool-grease-pencil-draw-circle>
Circle Select <tool-select-circle>
Clamp setting <render-cycles-integrator-clamp-samples>
Clear <bpy.ops.object.*clear>
Clear Parent Inverse <bpy.ops.object.parent_clear>
Clear Sculpt-Mask Data
Clip Display <clip-editor-clip-display-label>
Cloth flag with wind and self-collisions <https://wiki.blender.org/wiki/File:Cloth-flag2.blend>
Cloth self-collisions <https://wiki.blender.org/wiki/File:Cloth-regression-selfcollisions.blend>
Collada Importer
Collections in the Outliner <editors-outliner-editing-collections>
Color <grease-pencil-draw-color>
Color Palette <ui-color-palette>
Color management <render-post-color-management>
Command Line Launching <command_line-launch-index>
Common
Common Image Settings <editors-image-image-settings-common>
Common Object Options <object-common-options>
Common Options <spline-common-options>
Common Settings section <force-field-common-settings>
Communicating <contribute-contact>
Compress file <files-blend-compress>
Constraints <constraints-index>
Contacts
Containers <files-video-containers>
Contribute to this Manual <about-user-contribute>
Control Points
Convex and concave polygons <https://en.wikipedia.org/wiki/Convex_and_concave_polygons>
Copy As New Driver <drivers-copy-as-new>
Cosine <https://en.wikipedia.org/wiki/Trigonometric_functions>
Crease <modeling-edges-crease-subdivision>
Create Face <modeling-mesh-make-face-edge-dissolve>
Creating Add-ons <https://wiki.blender.org/wiki/Process/Addons/Guidelines>
Creative Commons Attribution-ShareAlike 4.0 International License <https://creativecommons.org/licenses/by-sa/4.0/>
Cross
Ctrl Shift C
Cube
Cube.001
Cube.location.x
Curve <tool-grease-pencil-draw-curve>
Curve Edit Mode <curve-toolbar-index>
Curve widget <ui-curve-widget>
Custom Orientations
Custom Properties
Custom Properties <files-data_blocks-custom-properties>
Custom Split Normals of Meshes
Custom Weight Paint Range <prefs-system-weight>
Custom data file <https://development.root-1.de/X-Download/atom_info.dat>
Cutter <tool-grease-pencil-draw-cutter>
Cycle-Aware Keying <timeline-keying>
Cycles website <https://www.cycles-renderer.org/>
D
D. -3.0000 (3.0000) Global
DDS
DEF
DEF-
DNxHD <https://en.wikipedia.org/wiki/Avid_DNxHD>
DOI 10.1111/j.1467-8659.2010.01805.x <https://doi.org/10.1111/j.1467-8659.2010.01805.x>
DPX
DV <https://en.wikipedia.org/wiki/DV>
DWAA
Daily Builds <https://builder.blender.org/download>
Dashed Line
Data ID <ui-data-id>
Data ID menu <ui-data-id>
Data-Block <ui-data-block>
Data-Block Menu <ui-data-block>
Data-Block menu <ui-data-block>
Data-block menu <ui-data-block>
Debug Value <bpy.ops.wm.debug_menu>
Defocus node <bpy.types.CompositorNodeDefocus>
Delete
Delta Transform <bpy.types.Object.delta>
Delta Transformations <bpy.types.Object.delta>
Demo and benchmark files <https://www.blender.org/download/demo-files/>
Demonstration video <https://www.youtube.com/watch?v=GTlmmd13J1w>
DensityUP1D
Depth Troubleshooting <troubleshooting-depth>
DevTalk <https://devtalk.blender.org/tag/python>
Developer Community <https://devtalk.blender.org>
Developer Extras <prefs-interface-dev-extras>
Developer Preview <https://store.steampowered.com/newshub/app/250820/view/2396425843528787269>
Devtalk <https://devtalk.blender.org/c/documentation/12>
Differential Coordinates for Interactive Mesh Editing <https://igl.ethz.ch/projects/Laplacian-mesh-processing/Laplacian-mesh-editing/diffcoords-editing.pdf>
Diffusion <https://developer.blender.org/diffusion/BM/>
Directory Layout <blender-directory-layout>
Displace modifier <bpy.types.DisplaceModifier>
Display <sculpt-paint-brush-display>
Display Mode
Dissolve Vertices
Dissolved <bpy.ops.mesh.dissolve>
Distributed Memory Across Devices <prefs-system-cycles-distributive-memory>
Dive Into Python <http://getpython3.com/diveintopython3/index.html>
Docutils reStructuredText Reference <https://docutils.sourceforge.io/rst.html>
DoubleSided
Download Latest AMD Drivers <https://www.amd.com/en/support>
Download Latest Intel Drivers <https://downloadcenter.intel.com/product/80939/Graphics-Drivers>
Download Latest Nvidia Drivers <https://www.nvidia.com/Download/index.aspx>
Download an example <https://wiki.blender.org/wiki/File:Uvproject.blend>
Download example file <https://wiki.blender.org/wiki/File:25-Manual-Modifiers-example.blend>
Download the full manual (zipped HTML files) <blender_manual.zip>
Downloading the Repository
Draw <bpy.ops.curve.draw>
Draw <tool-grease-pencil-draw-draw>
Driver Variables
Driver Variables <drivers-variables-rotation-modes>
Drivers <animation-drivers-index>
Duplicating <modeling_surface_editing_duplicating>
Dynamic_1
Dyntopo <bpy.types.Brush.topology_rake_factor>
E
ELLIPSE
EPS
EXR
Edge Creases <bpy.ops.transform.edge_crease>
Edge Creases <modifiers-generate-subsurf-creases>
Edge Loop Selection <bpy.ops.mesh.loop_multi_select>
Edge Loops <bpy.ops.mesh.loop_multi_select>
Edge Marks
Edge Rings <modeling-meshes-selecting-edge-rings>
Edge Slide <tool-mesh-edge_slide>
Edge Slide tool <modeling-meshes-editing-edge-slide>
Edge bevel weight <modeling-edges-bevel-weight>
Edit Mode <modeling-meshes-editing-vertices-shape-keys>
Edit Texture Space <modeling_transform_edit-texture-space>
Editing
Editing Armatures: Naming conventions <armature-editing-naming-conventions>
Editing Markers <animation-markers-editing>
Enable SteamVR beta updates <https://www.vive.com/us/support/vive/category_howto/optin-to-steamvr-beta.html>
Encoding Panel <render-output-video-encoding-panel>
Envelope Multiply <armature-bones-envelope>
Eoan, Focal <https://launchpad.net/~monado-xr/+archive/ubuntu/monado>
Erase <tool-grease-pencil-draw-erase>
Euclidean distance metric <https://en.wikipedia.org/wiki/Euclidean_distance>
Euler's number <https://en.wikipedia.org/wiki/E_(mathematical_constant)>
Euler(...)
Example blend-file <https://en.blender.org/uploads/0/03/Blender2.65_motion_blur.blend>
Example blend-file <https://en.blender.org/uploads/b/b7/Blender2.65_cycles_anisotropic.blend>
Examples
Expand/Contract Selection
Experimental Feature Set <cycles-experimental-features>
Experimental Rigs by Alexander Gavrilov <https://github.com/angavrilov/angavrilov-rigs>
Expressions
Extending Blender with Python <scripting-index>
Extrapolation <bpy.types.AnimData.action_extrapolation>
Extrapolation <editors-graph-fcurves-settings-extrapolation>
Extrude <modeling-curves-extrude>
Extrude Individual <tool-mesh-extrude_individual>
Extrude Region <tool-mesh-extrude_region>
Extrude To Cursor <tool-mesh-extrude_cursor>
Eyedropper <tool-grease-pencil-draw-eyedropper>
F-curve Extrapolation <editors-graph-fcurves-settings-extrapolation>
FC0
FFCC00
FFmpeg -b:v <https://ffmpeg.org/ffmpeg.html#Description>
FFmpeg video codec #1 <https://en.wikipedia.org/wiki/FFV1>
FLAC <https://en.wikipedia.org/wiki/FLAC>
FS_floral_brush.png
Face Loop Selection <modeling-meshes-selecting-face-loops>
Face Loops <modeling-meshes-selecting-face-loops>
Face Map <bpy.types.FaceMaps>
Face Selection Masking <bpy.types.Mesh.use_paint_mask>
Face Set <sculpting-editing-facesets>
Face Sets <sculpting-editing-facesets>
Face-Map <bpy.types.FaceMaps>
False
Features reference <https://www.gdquest.com/docs/power-sequencer/reference/>
Femto-ST institute <https://www.femto-st.fr/en>
File Format Variations
File.py
File:AtvBuggy.zip <https://wiki.blender.org/wiki/File:AtvBuggy.zip>
File:M-130Blueprint.zip <https://wiki.blender.org/wiki/File:M-130Blueprint.zip>
File:Manual-2.6-Render-Freestyle-PrincetownLinestyle.pdf <https://wiki.blender.org/wiki/File:Manual-2.6-Render-Freestyle-PrincetownLinestyle.pdf>
File:Mato_sus304_cut02.zip <https://wiki.blender.org/wiki/File:Mato_sus304_cut02.zip>
File:Parent_-_Object_(Keep_Transform)_(Demo_File).blend <https://wiki.blender.org/wiki/File:Parent_-_Object_(Keep_Transform)_(Demo_File).blend>
Fill <modeling-meshes-editing-fill>
Fill <tool-grease-pencil-draw-fill>
Filter
Filter Glossy <render-cycles-integrator-filter-glossy>
Final <bpy.types.FluidDomainSettings.cache_type>
Flash <https://en.wikipedia.org/wiki/Flash_Video>
Flash Video <https://en.wikipedia.org/wiki/Flash_Video>
Flow Object <bpy.types.FluidFlowSettings.flow_type>
Fly/Walk Navigation <3dview-fly-walk>
Fly/walk Navigation <3dview-fly-walk>
Follow Path <curve-path-animation>
Fraction <https://en.wikipedia.org/wiki/Rational_function>
Frame Overlay <bpy.types.SequenceEditor.show_overlay>
Free Bake <free-physics-bake>
Freestyle Face Marks <bpy.ops.mesh.mark_freestyle_face>
Freestyle Renders <bpy.types.Freestyle>
From Instancer <cycles-nodes-input-texture-coordinate-from-instancer>
G.debug_value
GNU GPL <https://www.gnu.org/licenses/gpl.html>
GNU GPL License <https://www.gnu.org/licenses/gpl.html>
GNU General Public License <http://www.gnu.org/licenses/gpl.html>
GNU Project website <https://www.gnu.org/licenses/licenses.html#GPL>
GROUPS
Gamma correction <https://en.wikipedia.org/wiki/Gamma_correction>
Ge2Kwy5EGE0
Generated
Generated Image <image-generated>
Generated UV Properties <properties-texture-space>
Generated UVs <properties-texture-space>
Geometry Mapping
Get Involved <https://www.blender.org/get-involved/>
Getting Started <about-getting-started>
Getting Started Guide for OpenXR <https://docs.microsoft.com/en-us/windows/mixed-reality/openxr-getting-started>
Getting Started Guides <https://gitlab.freedesktop.org/monado/monado/-/blob/master/README.md>
Getting started <https://www.gdquest.com/docs/power-sequencer/getting-started/>
Gimbal <https://en.wikipedia.org/wiki/Gimbal>
Gimbal lock <https://blender.stackexchange.com/questions/469>
Gimbal lock <https://en.wikipedia.org/wiki/Gimbal_lock>
Github repository <https://github.com/ChrisHinde/MaterialUtilities/blob/master/README.md>
Github repository <https://github.com/nutti/Magic-UV/wiki>
Gizmo Preferences <prefs-viewport-gizmo-size>
Global/Local <modeling-mesh-transform-panel>
Glossy Filter <render-cycles-integrator-filter-glossy>
Goal Weight <curves-weight>
Goal Weight <surface-goal-weight>
GoodTextures.com <https://www.goodtextures.com/>
Graphics Tablet <hardware-tablet>
Grease Pencil Draw <gpencil_draw-toolbar-index>
Grease Pencil Edit <gpencil_edit-toolbar-index>
Grease Pencil Sculpting <gpencil_sculpt-toolbar-index>
Grease Pencil Weight Paint <gpencil_weight_paint-toolbar-index>
Grid Fill <modeling-meshes-editing-grid-fill>
Group of Pictures <https://en.wikipedia.org/wiki/Group_of_pictures>
H.264
H.264 <https://en.wikipedia.org/wiki/H.264>
HDR
HDRI <https://en.wikipedia.org/wiki/HDRI>
HELIX
HH:MM:SS.FF
HMD <hardware-head-mounted-displays>
Hair Dynamics <hair-dynamics>
Halos <particle-halo>
Handle <editors-graph-fcurves-settings-handles>
Handles & Interpolation Display <keyframe-handle-display>
Harkyman on the development of the Maintain Volume constraint <http://www.harkyman.com/2010/03/16/maintaining-bone-volume-a-new-constraint/>
Head-Mounted Displays (HMD) <hardware-head-mounted-displays>
Heat Buoyancy <bpy.types.FluidDomainSettings.beta>
Histogram
Hold Offset <sequencer-duration-hard>
Holdout Collections <bpy.ops.outliner.collection_holdout_set>
Houdini Ocean Toolkit <https://code.google.com/archive/p/houdini-ocean-toolkit/>
How to Think Like a Computer Scientist <http://interactivepython.org/courselib/static/thinkcspy/index.html>
How to install it <translations-fuzzy-strings>
HuffYUV <https://en.wikipedia.org/wiki/Huffyuv>
Humane Rigging <https://www.youtube.com/playlist?list=PLE211C8C41F1AFBAB>
Hyperbolic Cosine <https://en.wikipedia.org/wiki/Hyperbolic_functions>
Hyperbolic Sine <https://en.wikipedia.org/wiki/Hyperbolic_functions>
Hyperbolic Tangent <https://en.wikipedia.org/wiki/Hyperbolic_functions>
ID
IK Arm Example <https://wiki.blender.org/wiki/File:IK_Arm_Example.blend>
IK bones <bone-constraints-inverse-kinematics>
ILM's OpenEXR <https://www.openexr.com/>
INSERT
INSERT(ATTRIB+XDATA)
IRIS
IRIZ
Image <bpy.types.Object.empty_image>
Import PDB/XYZ
Importance sampling <https://en.wikipedia.org/wiki/Importance_sampling>
Increment Snap <transform-snap-element>
Influence <bpy.types.constraint.influence>
Initial Temperature <bpy.types.FluidFlowSettings.temperature>
Inserting Text
Inset Faces <tool-mesh-inset_faces>
Install from Zip
Install from blender.org
Installing Dependencies
Installing Python
Installing SVN and Downloading the Repository
Interface <prefs-interface-color-picker-type>
Interface0D
Interface1D
Interpolation <editors-graph-fcurves-settings-interpolation>
Interpolation Mode <editors-graph-fcurves-settings-interpolation>
Invalid Selection, Disable Anti-Aliasing <troubleshooting-3dview-invalid-selection>
Inverse Kinematics <bone-constraints-inverse-kinematics>
Inverse Tangent <https://en.wikipedia.org/wiki/Inverse_trigonometric_functions>
IvyGen program <http://graphics.uni-konstanz.de/~luft/ivy_generator/>
JACK
JP2
JPEG
Joining objects <object-join>
Julien Deswaef <https://github.com/xuv>
KHR_draco_mesh_compression
KHR_lights_punctual
KHR_materials_clearcoat
KHR_materials_pbrSpecularGlossiness
KHR_materials_transmission
KHR_materials_unlit
KHR_mesh_quantization
KHR_texture_transform
Keying popover <timeline-keying>
Keymap Editor <prefs-input-keymap-editor>
Knife <tool-mesh-knife>
LAYER
LAYER_frozen
LAYER_locked
LAYER_on
LIGHT
LINE
LOCAL directory <blender-directory-layout>
LOCAL, SYSTEM
LOCAL, USER
LOCAL, USER, SYSTEM
LWPOLYLINE
Laplacian Surface Editing (Original paper) <https://igl.ethz.ch/projects/Laplacian-mesh-processing/Laplacian-mesh-editing/laplacian-mesh-editing.pdf>
Laplacian Surface Editing <https://igl.ethz.ch/projects/Laplacian-mesh-processing/Laplacian-mesh-editing/laplacian-mesh-editing.pdf>
Latest Stable Release <https://www.blender.org/download/>
Layers <bpy.types.Armature.layers>
Learn More Here <https://docs.microsoft.com/en-us/windows-hardware/drivers/display/timeout-detection-and-recovery>
Learn the benefits of right-click-select <https://vimeo.com/76335056>
Length2DBP1D
Life Time
Light Paths <render-cycles-integrator-light-paths>
Light Portals <render-cycles-lights-area-portals>
Limitations
Limitations <eevee-limitations-ao>
Limitations <eevee-limitations-dof>
Limitations <eevee-limitations-materials>
Limitations <eevee-limitations-reflections>
Limitations <eevee-limitations-shadows>
Limitations <eevee-limitations-sss>
Limitations <eevee-limitations-volumetrics>
Line <tool-grease-pencil-draw-line>
Link to publication <https://onlinelibrary.wiley.com/doi/abs/10.1002/ese3.174>
Link to publication <https://pubs.acs.org/doi/abs/10.1021/jp501738c>
Linking to a Scene <data-system-linked-libraries-make-link>
List View <ui-list-view>
List view <ui-list-view>
Live Unwrap <bpy.types.SpaceUVEditor.use_live_unwrap>
Live Unwrap <bpy.types.ToolSettings.use_edge_path_live_unwrap>
Living Room
Load UI <file-load-ui>
Lock Camera to View <3dview-lock-camera-to-view>
Lock Relative <weight-painting-auto-normalize>
Loop Cut <tool-mesh-loop_cut>
Loop Cut and Slide <bpy.ops.mesh.loopcut_slide>
Loop Cut and Slide Options <modeling-meshes-editing-edge-loopcut-slide-options>
M
MCH
MCH-
MESH
MP2 <https://en.wikipedia.org/wiki/MPEG-1_Audio_Layer_II>
MP3 <https://en.wikipedia.org/wiki/MP3>
MPEG
MPEG H.264
MPEG-1 <https://en.wikipedia.org/wiki/MPEG-1>
MPEG-2 <https://en.wikipedia.org/wiki/MPEG-2>
MPEG-4 <https://en.wikipedia.org/wiki/MPEG-4>
MPEG-4(DivX) <https://en.wikipedia.org/wiki/MPEG-4>
MTEXT
Mailing List <https://lists.blender.org/mailman/listinfo/bf-docboard>
Main View
MajorControl
MajorRadius
Makefile
Mango Open Movie <https://mango.blender.org/>
Manhattan distance metric <https://en.wikipedia.org/wiki/Taxicab_geometry>
Manual Index <genindex>
Markers Menu
Mask <dope-sheet-mask>
Mask Feathers <mask-feather>
Mask Mode <dope-sheet-mask>
Masked <sculpt-mask-menu>
Masked Geometry <sculpt-mask-menu>
Masks <sculpt-mask-menu>
MatCap <render-workbench-matcap>
Material Preview <3dview-material-preview>
Material Slot <material-slots>
Math module reference <https://docs.python.org/3/library/math.html>
Matrix(...)
Matroska <https://en.wikipedia.org/wiki/Matroska>
MaxGradient
Measure <tool-measure>
Menus <ui-header-menu>
Mesh Display Viewport Overlays panel <mesh-display-normals>
Mesh Edit Mode <mesh-toolbar-index>
Mesh Smoothing <modeling-meshes-editing-normals-shading>
Mesh Symmetry <modeling_meshes_tools-settings_mirror>
MetaPlane
MetaThing
MetaThing.001
MetaThing.round
Metaball Edit Mode <meta-toolbar-index>
Microsoft Store <https://www.microsoft.com/en-us/p/mixed-reality-portal/9ng1h8b3zc7m>
Minkowski distance metric <https://en.wikipedia.org/wiki/Minkowski_distance>
MinorControl
MinorRadius
Mirror Vertex Group <bpy.ops.object.vertex_group_mirror>
Mirroring a Selection <fig-mesh-duplicating-mirror-selection>
Mist section <render-cycles-integrator-world-mist>
Modifiers Interface <bpy.types.Modifier.show>
Modular <bpy.types.FluidDomainSettings.cache_type>
Monado <https://monado.dev/>
Movie
Movie Clip Editor Proxy settings <clip-editor-proxy>
Multi-Paint <weight-painting-auto-normalize>
Multiple Selection Modes
Multiplexing <https://www.afterdawn.com/glossary/term.cfm/multiplexing>
MyCache_xxxxxx_yy.bphys
N-poles & E-poles <https://blender.stackexchange.com/a/133676/55>
NDOF device <hardware-ndof>
NLA blending <bpy.types.AnimData.action_blend_type>
NULL
NUMBER
NURBS
NURBS <curve-nurbs>
NURBS Curves <modeling-curve-order>
NURBS Splines <curve-nurbs>
NURBS curves <curve-nurbs>
NVidia Website <https://www.nvidia.com/Download/index.aspx>
Naming bones <armature-editing-naming-bones>
Narrow Band FLIP for Liquid Simulations <https://www.in.tum.de/cg/research/publications/2016/narrow-band-flip-for-liquid-simulations/>
Navigation Gizmo <navigation-gizmo>
No Caustics <render-cycles-integrator-no-caustics>
Nodes
Non-Uniform Scale
Normal <bpy.types.FluidFlowSettings.velocity_normal>
Normal Mode
Normal Properties <modeling_meshes_editing_normals_properties>
Normalize All <bpy.ops.object.vertex_group_normalize_all>
Normals <https://en.wikipedia.org/wiki/Normal_(geometry)>
Normals <modeling-meshes-structure-normals>
Not a valid font
Notes section <shader-white-noise-notes>
Nvidia CUDA Installation Guide for Linux <https://docs.nvidia.com/cuda/archive/10.2/cuda-installation-guide-linux/index.html>
O
OHA Studio <http://oha-studios.com/>
OPENAL
OPENCL
OPENCL+CPU
OPEN_EXR
OPEN_EXR_MULTILAYER
OPTIX
ORG
ORG-
OSL specification <https://github.com/imageworks/OpenShadingLanguage/blob/master/src/doc/osl-languagespec.pdf>
OSL-file <https://github.com/imageworks/OpenShadingLanguage>
Object <movie-clip-tracking-properties-object>
Object Color <bpy.types.Object.color>
Object Modifiers <modifiers-index>
Object Parent <object-parenting>
Object Selector <ui-data-id>
Objects <object-common-options>
Occlusion
Oculus <https://www.oculus.com/>
Oculus Rift software <https://www.oculus.com/setup/>
Offset Edge Loop Cut <bpy.ops.mesh.offset_edge_loops_slide>
Ogg <https://en.wikipedia.org/wiki/Ogg>
Ogg container <files-video-containers>
Olav3D Tutorials: 3D Programming for Beginners Using Python <https://www.youtube.com/watch?v=rHzf3Dku_cE>
Opacity <bpy.types.GPencilLayer.opacity>
Open <files-blend-open>
Open Babel <https://openbabel.org/docs/dev/FileFormats/XYZ_cartesian_coordinates_format.html>
Open Content License <https://web.archive.org/web/19981206111937/http://www.opencontent.org/opl.shtml>
Open Image Denoise <https://www.openimagedenoise.org/>
Open Shading Language <https://github.com/imageworks/OpenShadingLanguage>
OpenAL documentation <https://www.openal.org/documentation/>
OpenColorIO <https://opencolorio.org/>
OpenColorIO website <https://opencolorio.org/>
OpenEXR
OpenFootage.net <https://www.openfootage.net/?p=986>
OpenGL <https://en.wikipedia.org/wiki/OpenGL>
OpenSubdiv library <http://graphics.pixar.com/opensubdiv/docs/intro.html>
OpenVDB <https://www.openvdb.org/>
Operator
Operator Preset <ui-presets>
Operator Search <bpy.ops.wm.search_operator>
Operators.bidirectional_chain()
Operators.chain()
Operators.chain(), Operators.bidirectional_chain()
Operators.create()
Operators.recursiveSplit()
Operators.select()
Operators.sequentialSplit()
Operators.sequential_split(), Operators.recursive_split()
Operators.sort()
OptiX <render-cycles-gpu-optix>
Opus <https://en.wikipedia.org/wiki/Opus_(audio_format)>
Orbit <bpy.ops.view3d.view_orbit>
Orbit Style Preference <prefs-input-orbit-style>
Original paper <http://graphics.pixar.com/library/HarmonicCoordinatesB/>
Origins <bpy.types.ToolSettings.use_transform_data_origin>
Outliner <bpy.ops.outliner.orphans_purge>
Outliner <editors-outliner-editing-collections>
Overscan <https://en.wikipedia.org/wiki/Overscan>
PATH
PCM <https://en.wikipedia.org/wiki/PCM>
PIP <https://pip.pypa.io/en/latest/installing/>
PIZ
PLANESURFACE
PLAY
PNG
PNG <https://en.wikipedia.org/wiki/Portable_Network_Graphics>
POINT
POLYFACE
POLYLINE
POLYMESH
POV-Ray Wiki <http://wiki.povray.org/content/Category:Command-Line_and_INI-File_Options>
POV-Ray Wiki <http://wiki.povray.org/content/Documentation:Tutorial_Section_3.3#Gamma_Handling>
POV-Ray Wiki <http://wiki.povray.org/content/HowTo:Use_radiosity>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Blob>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Box>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Cone>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Cylinder>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Finish#Diffuse>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Height_Field>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Isosurface>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Lathe>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Parametric>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Plane>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Prism>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Rainbow>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Sphere>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Sphere_Sweep>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Superquadric_Ellipsoid>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Torus>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Tracing_Options#Anti-Aliasing_Options>
POV-Ray Wiki <http://wiki.povray.org/content/Reference:Tracing_Options#BSP_Bounding>
PXR24
PYTHONPATH
Paint Mask <sculpt-mask-menu>
Panels <ui-panels>
Pans the 3D Viewport <bpy.ops.view3d.view_pan>
Parent Inverse
Parent Inverse matrix <parent-inverse-matrix>
Parent Particles <bpy.types.ParticleSettings.use_parent_particles>
Particle Radius <bpy.types.FluidDomainSettings.particle_radius>
Particle Radius <bpy.types.FluidDomainSettings.resolution_max>
Paste Driver Variables <drivers-variables>
Path Animation panel <curve-path-animation>
Path/Curve-Deform <curve-shape-path-curve-deform>
Pie Menu on Drag <keymap-pref-py_menu_on_drag>
Pie menu settings <prefs-pie-menu>
Pixel Coordinates <bpy.types.SpaceUVEditor.show_pixel_coords>
Playhead & 2D Cursor
Poedit <https://poedit.net/>
Poly Build <tool-mesh-poly-build>
Polyline <tool-grease-pencil-draw-polyline>
Preference <editors_preferences_input_ndof>
Preferences <prefs-editing-duplicate-data>
Preferences <prefs-menu>
Preferences <prefs-system-sound>
Presets <ui-presets>
Primal-Dual Optimization for Fluids <https://ge.in.tum.de/publications/2017-cgf-eckert/>
Primitives
ProfilCreate.py
Project Apricot <https://apricot.blender.org/>
Project Orange <https://orange.blender.org/>
Project Page <https://developer.blender.org/project/profile/53/>
Project Peach <https://peach.blender.org/>
Project Workboard <https://developer.blender.org/project/board/53/>
Project from View
Projection Painting <painting-texture-index>
Properties
Proportional Editing <3dview-transform-control-proportional-edit-falloff>
Protected <data-system-datablock-fake-user>
Prototype Release <https://developer.oculus.com/blog/openxr-for-oculus/>
Proxy <object-proxy>
Proxy Render Size <proxy-render-size>
Proxy Settings
Push Down Action <bpy.ops.nla.action_pushdown>
Push/Pull <tool-transform-push_pull>
Python <https://www.python.org/>
Python <https://www.python.org>
Python <scripting-index>
Python API Reference <https://docs.blender.org/api/blender_python_api_current/>
Python API: Quickstart <https://docs.blender.org/api/current/info_quickstart.html>
Python installation package <https://www.python.org/downloads/>
Python.org <https://www.python.org/>
QT rle / QT Animation <https://en.wikipedia.org/wiki/QuickTime_Animation>
Quality <http://wiki.povray.org/content/Reference:Tracing_Options#Quality_Settings>
QuantitativeInvisibilityUP1D
Quantization <https://en.wikipedia.org/wiki/Quantization>
Quaternion(...)
Quick Liquid and Quick Smoke <bpy.ops.object.quick>
Quick Set Up Process <splash-quick-start>
Quicktime
Quicktime <https://en.wikipedia.org/wiki/.mov>
RAWTGA
RCSB <https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html>
RCSB site <https://www.rcsb.org/>
RCSB site <https://www.rcsb.org/pages/thirdparty/molecular_graphics>
README
REGION
RENDER
RGB
RLE
ROT
RRGGBB
Radiance HDR
Radiosity (computer graphics) <https://en.wikipedia.org/wiki/Radiosity_%28computer_graphics%29>
Radius <modeling-curve-radius>
Radius used
Random seed <https://en.wikipedia.org/wiki/Random_seed>
Randomize <tool-mesh-smooth>
Randomize Transform <bpy.ops.object.randomize_transform>
Rate
Ray Casting <https://en.wikipedia.org/wiki/Ray_casting>
Read more about this function <https://archive.blender.org/wiki/index.php/Doc:2.4/Manual/Composite_Nodes/Types/Convertor/#Quantize.2FRestrict_Color_Selection>
Read prefs: {DIR}/userpref.blend
Redo Panel <ui-undo-redo-adjust-last-operation>
Reducing Noise <render-cycles-reducing-noise-clamp-samples>
Refraction limitations <eevee-limitations-refraction>
Refresh All <bpy.ops.sequencer.refresh_all>
Regression blend-file <https://wiki.blender.org/wiki/File:Cloth-regression-armature.blend>
Regression blend-file <https://wiki.blender.org/wiki/File:Cloth_anim_vertex.blend>
Regression blend-file <https://wiki.blender.org/wiki/File:Cloth_dynamic_paint.blend>
Regular Expressions <https://en.wikipedia.org/wiki/Regular_expression>
Related thread on Blender artists <https://blenderartists.org/t/499364>
Relations panel <bone-relations-bone-group>
Relations panel <bone-relations-parenting>
Relative Paths <files-blend-relative_paths>
Release Guide <about-contribute-guides-release>
Rename Active Item
Rename tool <tools_rename-active>
Render Dimensions Panel <render-tab-dimensions>
Render Region <editors-3dview-navigate-render-region>
Render Regions <editors-3dview-navigate-render-region>
Render perspective <camera-lens-type>
Rendered <3dview-rendered>
Report a Bug <https://developer.blender.org/maniphest/task/edit/form/1/>
Resolution Divisions <bpy.types.FluidDomainSettings.resolution_max>
Resolution Divisions<bpy.types.FluidDomainSettings.resolution_max>
Resolution does not match
Restriction Columns
Restrictions <editors-outliner-interface-restriction_columns>
Retina
Rip <bpy.ops.mesh.rip_move>
Rip Edge <tool-mesh-rip_edge>
Rip Region <tool-mesh-rip_region>
Roll <tool-bone-role>
Rolling Shutter <https://en.wikipedia.org/wiki/Rolling_shutter>
Rotation Channel Modes
Rotation Channel Modes <drivers-variables-rotation-modes>
Rotation Mode <rotation-modes>
Run Script button <editors-text-run-script>
Running Scripts
S
SCALE
SDL
SOLID
STYLE
SURFACE
SVG
Safe Areas <camera-safe-areas>
Sample blend-file <https://en.blender.org/uploads/6/62/Manual-Modifier-Displace-Slime01.blend>
Sample blend-file <https://en.blender.org/uploads/9/9e/Manual-Modifier-Displace-Example01.blend>
Sample blend-file <https://wiki.blender.org/wiki/File:25-manual-meshsmooth-example.blend>
Sample blend-file <https://wiki.blender.org/wiki/File:263-Cast-Modifier.blend>
Sample blend-file <https://wiki.blender.org/wiki/File:Dev-ArrayModifier-Chain01.blend>
Sample blend-file <https://wiki.blender.org/wiki/File:Dev-ArrayModifier-Fractal01.blend>
Sample blend-file <https://wiki.blender.org/wiki/File:Manual-Modifier-Array-Tentacle01.blend>
Save & Load <prefs-save-load>
Save <files-blend-save>
Save As... <files-blend-save>
Save Buffers <render_properties_save-buffers>
Saves <files-blend-save>
Scale Cage <tool-scale-cage>
Scale Transform <bpy.ops.transform.resize>
Scene Audio <data-scenes-audio>
Scene Units <bpy.types.UnitSettings>
Scribus <https://www.scribus.net/>
Select <tool-select-tweak>
Select Box <tool-select-box>
Select Circle <tool-select-circle>
Select Control Point Row
Select Edge Loops <bpy.ops.mesh.loop_multi_select>
Select Grouped <bpy.ops.object.select_grouped>
Select Lasso <tool-select-lasso>
Select Linked
Select Linked <bpy.ops.mesh.select_linked>
Select More/Less
Select Next/Previous
Select Non-Manifold <bpy.ops.mesh.select_non_manifold>
Select Random
Select Random <bpy.ops.mesh.select_random>
Select Shortest Path <bpy.ops.mesh.shortest_path_select>
Select Similar
Select Similar <bpy.ops.mesh.select_similar>
Select With Mouse Button <keymap-blender_default-prefs-select_with>
Selection Mode <bpy.types.ToolSettings.uv_select_mode>
Selection Modes <bpy.types.ToolSettings.mesh_select_mode>
Self-Collision <physics-softbody-settings-self-collision>
Separate Atoms
Set Origin <bpy.ops.object.origin_set>
Set Origin to Geometry <bpy.ops.object.origin_set>
Set as default
Setting up the Build Environment
Shader AOV <render-cycles-passes-aov>
Shader Script <bpy.types.ShaderNodeScript>
Shape Key Editor <dope-sheet-shape-key>
Shape Keys <animation-shape_keys-index>
Sharing scripts <https://wiki.blender.org/wiki/Process/Addons>
Sharp Edges <bpy.ops.mesh.mark_sharp>
Shear <tool-transform-shear>
Shortest Path <bpy.ops.mesh.shortest_path_select>
Shrink/Flatten <tool-mesh-shrink-fatten>
Sidebar <ui-region-sidebar>
Simple Expression <drivers-simple-expressions>
Simple Expressions
Simple Expressions <drivers-simple-expressions>
Simple UVs <bpy.ops.paint.add_simple_uvs>
Simple and Table Feline: Fast Elliptical Lines for Anisotropic Texture Mapping <https://www.hpl.hp.com/techreports/Compaq-DEC/WRL-99-1.pdf>
Sine <https://en.wikipedia.org/wiki/Sine>
Skin Modifier Development at Blender Nation <https://www.blendernation.com/2011/03/11/skin-modifier-development/>
Small Caps Scale setting <modeling-text-character-underline>
Smooth
Smooth <tool-mesh-smooth>
Smooth Maximum <https://en.wikipedia.org/wiki/Smooth_maximum>
Smooth Minimum <https://en.wikipedia.org/wiki/Smooth_maximum>
Smooth Normals <bpy.ops.object.shade_smooth>
Smooth Shading <bpy.ops.object.shade_smooth>
Smooth Shading <modeling-meshes-editing-normals-shading>
Smooth tool <bpy.ops.mesh.vertices_smooth>
Snap <https://snapcraft.io/>
Snap Element <transform-snap-element>
Sobol sequence <https://en.wikipedia.org/wiki/Sobol_sequence>
Soft Body Edges <physics-softbody-settings-aerodynamics>
Soft Body Edges settings <physics-softbody-settings-edges>
Soft Body Goal settings <physics-softbody-settings-goal>
Soft Body Solver settings <physics-softbody-settings-solver>
Solve Camera Motion <editors-movie-clip-tracking-clip-solve-motion>
Solve object Motion <editors-movie-clip-tracking-clip-solve-motion>
Sort Mesh Elements <mesh-edit-sort-elements>
Sound Crossfade <bpy.ops.sequencer.crossfade_sounds>
Spacebar Action <keymap-blender_default-spacebar_action>
Specials <ui-specials-menu>
Sphinx RST Primer <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>
Sphinx reference <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>
Spin <tool-mesh-spin>
Spin Duplicate <tool-mesh-spin>
Splash Screen <splash>
Spline Types
Spring <https://cloud.blender.org/p/spring/>
Stabilize Stroke <grease-pencil-draw-brushes-stabilizer>
Stack Exchange <https://blender.stackexchange.com/>
Stanford Bunny <https://en.wikipedia.org/wiki/Stanford_Bunny>
Startup File <startup-file>
State Colors <animation-state-colors>
Steam client <https://store.steampowered.com/>
SteamVR <https://www.steamvr.com/>
Sticky Selection Mode <bpy.types.SpaceUVEditor.sticky_select_mode>
Straight Skeleton <https://en.wikipedia.org/wiki/Straight_skeleton>
Stretch To <constraints-stretch-to-volume-preservation>
Strip Proxies <bpy.types.SequenceProxy>
SubRip <https://en.wikipedia.org/wiki/SubRip>
Subdivide <bpy.ops.mesh.subdivide>
Submit Patches <contribute-patch_submit>
Subsamples
Subsurface Translucency <bpy.types.Material.use_sss_translucency>
Subversion <https://subversion.apache.org/>
Sun + HDRI Texture Mode
Super
Support <https://www.blender.org/support>
Surface Edit Mode <surface-toolbar-index>
Surface editing <bpy.ops.curve.spin>
Swing and X/Y/Z Twist <drivers-variables-rotation-modes>
Switch Direction <modeling_surfaces_editing_segments_switch-direction>
Switching Select Mode
Sync Selection <bpy.types.ToolSettings.use_uv_select_sync>
System Preferences <editors_preferences_cycles>
T
TEMP
TEXT
TGA
TIFF
TMP
TMP_DIR
Tangent <https://en.wikipedia.org/wiki/Trigonometric_functions>
Targa
Technical Details
Technical Details and Hints
Technical Terms
Template Menu
Texture Mask <bpy.types.BrushTextureSlot.mask>
Texture Space <properties-texture-space>
Texture Spaces <properties-texture-space>
The Modifier Stack
The Pixelary <https://blog.thepixelary.com/post/160451378592/denoising-in-cycles-tested>
The Subset Option <bpy.ops.object.vertex_group_levels>
The Subset Option <sculpt-paint_weight-paint_editing_subset>
The Wikipedia Page <https://en.wikipedia.org/wiki/Polynomial>
The blend-file <https://wiki.blender.org/wiki/File:ManModifiersWeightVGroupEx.blend>
Theora <https://en.wikipedia.org/wiki/Theora>
This Thread <https://blender.stackexchange.com/questions/14262#14267>
This video <https://vimeo.com/15837189>
Tilt <modeling-curve-tilt>
Timeline Keyframe Control <animation-editors-timeline-autokeyframe>
Timeline editor header <animation-editors-timeline-headercontrols>
Tint <tool-grease-pencil-draw-tint>
To Sphere <tool-transform-to_sphere>
To Sphere Transform <bpy.ops.transform.tosphere>
Too few selections to merge
Tool Settings
Toolbar <ui-region-toolbar>
TortoiseSVN <https://tortoisesvn.net/downloads.html>
Tracking Axis <bpy.types.Object.track_axis>
Transform Cache Constraint <bpy.types.TransformCacheConstraint>
Transform Snapping <transform-snap>
Translation Preferences <prefs-interface-translation>
Triangulate <bpy.ops.mesh.quads_convert_to_tris>
Troubleshooting Depth Buffer Glitches <troubleshooting-depth>
True
Tutorials
Tutorials <https://www.blender.org/support/tutorials>
Tweak <tool-select-tweak>
TypeError: an integer is required (got type str)
Types
UDIM Tiles
UI Template List Enhancement <https://archive.blender.org/wiki/index.php/User:Mont29/UI_Template_List_Enhancement/>
USD issue #542 <https://github.com/PixarAnimationStudios/USD/issues/542>
UV Editor <editors-uv-index>
UV Mapping <editors-uv-index>
UV Mapping section <editors-uv-index>
UV maps list <uv-maps-panel>
UV texturing <editors-uv-index>
UVMap
Unit Circle <https://en.wikipedia.org/wiki/Unit_circle>
Unpack <pack-unpack-data>
Upload the diff file here <https://developer.blender.org/differential/diff/create/>
Upres Factor <bpy.types.FluidDomainSettings.mesh_scale>
Usage
Use The Terminal <https://docs.blender.org/api/blender_python_api_current/info_tips_and_tricks.html#use-the-terminal>
User Communities <https://www.blender.org/community/>
User Stories page <https://www.blender.org/about/user-stories/>
Using Cloth for soft bodies <https://wiki.blender.org/wiki/File:Cloth-sb1.blend>
Utah Teapot <https://en.wikipedia.org/wiki/Utah_teapot>
VIEW
VPORT
Vector(...)
Velocity Source<bpy.types.FluidDomainSettings.guide_source>
Vertex Mapping
Vertex Slide <tool-mesh-vertex-slide>
Vertex Weight Edit modifier <modeling-modifiers-weight-edit-influence-mask-options>
Vertex Weight modifiers <bpy.types.VertexWeightEditModifier>
Vertex count after removing doubles
Vertex merging <vertex-merging>
Vesta <https://jp-minerals.org/vesta/en/>
Video Output
Video Playlist <https://www.youtube.com/playlist?list=PLQAfj95MdhTJ7zifNb5ab-n-TI0GmKwWQ>
Videos
View Animation <topbar-render-view_animation>
View Dolly <3dview-nav-zoom-dolly>
View Layer Properties <render-layers-denoising-optix>
View Menu <dope-sheet-view-menu>
ViewEdge
ViewEdgeIterator
Viewport Overlays <3dview-overlay-grease-pencil>
Viewport Renders <bpy.ops.render.opengl>
Viewport denoising <render-cycles-settings-viewport-denoising>
Visibility properties <grease_pencil-object-visibility>
Visibility properties <render-cycles-object-settings-visibility>
Volume Limitation <eevee-limitations-volumetrics>
Vorbis <https://en.wikipedia.org/wiki/Vorbis>
Vorticity <bpy.types.FluidDomainSettings.vorticity>
WAV
WEBM / VP9 <https://en.wikipedia.org/wiki/VP9>
WGT-
Walk/Fly Navigation <3dview-fly-walk>
Watermark images
Wavelength
Wavelet Turbulence for Fluid Simulation <http://www.cs.cornell.edu/~tedkim/WTURB/>
WebM <https://en.wikipedia.org/wiki/WebM>
Weight <clip-tracking-weight>
Weight <curves-weight>
When should N-gons be used, and when shouldn't they? <https://blender.stackexchange.com/questions/89>
Whole Character keying set <whole-character-keying-set>
Why should triangles be avoided for character animation? <https://blender.stackexchange.com/questions/2931>
Widgets
Wikipedia <https://en.wikipedia.org/wiki/Protein_Data_Bank_(file_format)>
Wikipedia <https://en.wikipedia.org/wiki/XYZ_file_format>
Wikipedia page <https://en.wikipedia.org/wiki/Catmull%E2%80%93Clark_subdivision_surface>
Wikipedia page <https://en.wikipedia.org/wiki/NURBS>
Windows <https://github.com/pyproj4/pyproj>
Windows Mixed Reality <https://www.microsoft.com/windows/windows-mixed-reality>
Windows Mixed Reality PC Check <https://www.microsoft.com/en-us/p/windows-mixed-reality-pc-check/9nzvl19n7cnc>
Windows-Key
Workspace controls <workspaces-controls>
World tab <render-cycles-integrator-world-mist>
Worley Noise <https://en.wikipedia.org/wiki/Worley_noise>
Wrap <https://en.wikipedia.org/wiki/Rounding>
X-Axis Mirror Pose Mode <bpy.types.Pose.use_mirror_x>
X-ray <3dview-shading-xray>
XYZ
ZIP
ZIPS
Zip
Zoom to Mouse Position <prefs-zoom-mouse-pos>
Zooms the 3D Viewport <editors_3dview_navigation_zoom>
[\"Agent\"]
[\"prop_name\"]
[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
[1, 2, 3, 4, 5, 6]
[1, 2, 3]
[1.0, 2.0, 3.0]
[327, 47]
[47]
[Vector(...), Vector(...), ...]
[[1, 2, 3], [4, 5], [6]]
\\
\\build\\html\\index.html
\\n
^
__call__
__init__.py
_page<number>.svg
_sep
_socket
_socket.py
_socket.pyd
abs
absorption()
acos
active clip <scene-active-clip>
active object <object-active>
add-ons section <addons-io>
addons
addons/
addons_contrib
affects light paths somewhat differently <render-cycles-light-paths-transparency>
ambient_occlusion()
analemma
analemma <https://en.wikipedia.org/wiki/Analemma>
and
angle_y
angular diameter <https://en.wikipedia.org/wiki/Angular_diameter#Use_in_astronomy>
anim_cycles
anim_render
anim_screen_switch
anim_time_max
anim_time_min
animate <bpy.ops.anim.keyframe_insert>
animation player <render-output-animation_player>
animation-shapekeys-relative-vs-absolute
animation-state-colors
animation_##_test.png
animation_01_test.png
any type of node <tab-node-tree-types>
application template <app_templates>
armature-bone-roll
as in the 3D Viewport <3dview-view-clip>
ashikhmin_shirley(N, T, ax, ay)
ashikhmin_velvet(N, roughness)
asin
atan
atan2
author's Github repository <https://github.com/waylow/add_camera_rigs>
author's site <http://www.dragoneex.com/downloads/dynamic-skyadd-on>
author's site <https://sites.google.com/site/aleonserra/home/scripts/matlib-vx-5-6>
authors site <http://gregzaal.github.io/auto-tile-size/>
authors site <https://www.blenderkit.com/>
auto-bones naming <armature-editing-naming-bones>
automatic Bézier handles <editors-graph-fcurves-settings-handles>
automatic curve handles <editors-graph-fcurves-settings-handles>
avi
background()
background{}
basic.copy_chain
basic.pivot
basic.raw_copy
basic.super_copy
below <Would multiple GPUs increase available memory?>
bevel weight <modeling-edges-bevel-weight>
bin
bind_mat
bit rate <https://en.wikipedia.org/wiki/Bit_rate>
bl*er
bl_idname
bl_info
bl_label
bl_math
blend-file <https://download.blender.org/demo/test/FreeStyle_demo_file.blend.zip>
blend-file <https://en.blender.org/uploads/0/03/Blender2.65_motion_blur.blend>
blend-file <https://en.blender.org/uploads/4/44/Apinzonf_Shape_Enhanced_camel.blend>
blend-file <https://en.blender.org/uploads/4/47/Apinzonf_GSOC_2012_Media_femme_side.blend>
blend-file <https://en.blender.org/uploads/5/54/Apinzonf_GSOC_2012_Media_cube_smooth.blend>
blend-file <https://en.blender.org/uploads/8/8d/CollidingVertices.blend>
blend-file <https://en.blender.org/uploads/8/8f/Apinzonf_GSOC_2012_Media_femme_front.blend>
blend-file <https://en.blender.org/uploads/a/a2/Apinzonf_Deform_Horse_example1.blend>
blend-file <https://wiki.blender.org/uploads/b/b4/Render_freestyle_modifier_crease_angle.blend>
blend-file <https://wiki.blender.org/wiki/File:25-Manual-World-Mist-Example1.blend>
blend-file <https://wiki.blender.org/wiki/File:Blender_272_textured_strokes_in_cycles.blend>
blend-file <https://wiki.blender.org/wiki/File:CreaseAngle.zip>
blend-file <https://wiki.blender.org/wiki/File:EdgeType.zip>
blend-file <https://wiki.blender.org/wiki/File:HiddenCreaseEdgeMark.zip>
blend-file <https://wiki.blender.org/wiki/File:Lilies_Color_Material.zip>
blend-file <https://wiki.blender.org/wiki/File:Lily_Broken_Topology.zip>
blend-file <https://wiki.blender.org/wiki/File:LineStyles.zip>
blend-file <https://wiki.blender.org/wiki/File:ManAnimationTechsUsingConstraintsExSolarSys.blend>
blend-file <https://wiki.blender.org/wiki/File:QI-Range.zip>
blend-file <https://wiki.blender.org/wiki/File:Render_freestyle_modifier_curvature_3d.blend>
blend-file <https://wiki.blender.org/wiki/File:Toycar_Calligraphy.zip>
blend-file <https://wiki.blender.org/wiki/File:Toycar_Guiding_Line.zip>
blend-file <https://wiki.blender.org/wiki/File:Toycar_Sinus.zip>
blend-file <https://wiki.blender.org/wiki/File:Toycar_Three_Contours.zip>
blend-file <https://wiki.blender.org/wiki/File:Turning_Pages.zip>
blend-file <https://wiki.blender.org/wiki/File:toycar_bezier.zip>
blend-file example <https://en.blender.org/uploads/2/2a/Bilateral_blur_example_01.blend>
blend-file example <https://wiki.blender.org/uploads/7/79/Doftest.blend>
blendcache_[filename]
blender
blender -E help
blender -d
blender -r
blender-chat
blender-directory-layout
blender-v{VERSION}-release
blender.chat <https://blender.chat>
blender.crash.txt
blender.org <https://www.blender.org/download/>
blender.org/about/license <https://www.blender.org/about/license/>
blender.org/community <https://www.blender.org/community>
blender_debug_gpu.cmd
blender_debug_gpu_workaround.cmd
blender_debug_log.cmd
blender_debug_log.txt
blender_docs
blender_factory_startup.cmd
blender_oculus
blog article <https://freestyleintegration.wordpress.com/2014/07/07/line-color-priority/>
blog post <http://lacuisine.tech/blog/2018/07/19/2d-camera-rig/>
blogger
bone envelopes <armature-bones-envelope>
bone locking <animation_armatures_bones_locking>
bone page <armature-bone-influence>
bone-relations-parenting
box selection <tool-select-box>
bpy
bpy.
bpy.app
bpy.app.debug = True
bpy.app.driver_namespace
bpy.app.handlers.load_factory_preferences_post
bpy.app.handlers.load_factory_startup_post
bpy.context
bpy.context <https://docs.blender.org/api/current/bpy.context.html>
bpy.context.active_object
bpy.context.mode
bpy.context.object
bpy.context.scene
bpy.context.scene.frame_current
bpy.context.selected_objects
bpy.data
bpy.ops <https://docs.blender.org/api/current/bpy.ops.html>
bpy.ops.armature.bone_layers
bpy.ops.armature.flip_names
bpy.ops.curve.select_row
bpy.ops.mesh.dissolve_faces
bpy.ops.mesh.extrude_edges_move
bpy.ops.mesh.extrude_vertices_move
bpy.ops.mesh.loopcut_slide
bpy.ops.mesh.remove_doubles
bpy.ops.node.read_viewlayers
bpy.ops.object.duplicates_make_real
bpy.ops.object.make_single_user
bpy.ops.object.select_linked
bpy.ops.screen.screen_full_area
bpy.ops.sculpt.face_set_edit
bpy.ops.uv.cube_project
bpy.ops.uv.cylinder_project
bpy.ops.uv.follow_active_quads
bpy.ops.uv.lightmap_pack
bpy.ops.uv.smart_project
bpy.ops.uv.sphere_project
bpy.ops.uv.unwrap
bpy.ops.view3d.edit_mesh_extrude_move_normal
bpy.ops.view3d.edit_mesh_extrude_move_shrink_fatten
bpy.ops.wm <https://docs.blender.org/api/current/bpy.ops.wm.html>
bpy.ops.wm.search_menu
bpy.types.Armature.use_mirror_x
bpy.types.UnitSettings
bpy.types.Window.event_simulate
breadth first search <https://en.wikipedia.org/wiki/Breadth-first_search>
bssrdf_cubic(N, radius, texture_blur, sharpness)
bssrdf_gaussian(N, radius, texture_blur)
build
build/html
build/html/contents_quicky.html
build/html/index.html
bullseye <https://packages.debian.org/bullseye/libopenxr1-monado>
camera_for_shot_ZXY_36x24.chan
cartoon.py
cd
cd C:\\blender_docs
ceil
ch
chains of bones <armature-bone-chain>
change_placeholders.sh
chapter_subsection_sub-subsection_id.png
check this out <http://blender.stackexchange.com/questions/15620>
children <object-parenting>
circle icon
circle selection <tool-select-circle>
clamp
clipping distance <camera-clipping>
clipping range <3dview-view-clip>
cm
cmd
code and documentation <https://github.com/ampas/aces-dev>
collision physics <physics-collision-soft-bodt-cloth>
color
color picker widget <ui-color-picker>
color ramp <ui-color-ramp-widget>
color_picking
colors.inc
command-line arguments <command_line-args>
command_line-args
command_line-launch-index
common constraint properties <bpy.types.constraint.influence>
common constraint properties <rigging-constraints-interface-common-space>
common constraint properties <rigging-constraints-interface-common-target>
common masking options <modifiers-common-options-masking>
conf.py
conf.py: blender_version
config
configured in the preferences <prefs-lights-studio>
configuring peripherals <hardware-ndof>
contact <contribute-contact>
context
context menu <editors-outliner-editing-context_menu>
context.scene
converting meshes to curves <bpy.ops.object.convert>
cos
crease <modeling-edges-crease-subdivision>
create a task <https://developer.blender.org/maniphest/task/edit/form/default/?project=PHID-PROJ-c4nvvrxuczix2326vlti>
cube
cube.
cube.001
cube?
curvature <https://en.wikipedia.org/wiki/Curvature>
curve <ui-curve-widget>
curve-bezier
curve-convert-type
curve-nurbs
curved-POLYLINE
curves <modeling-curves-extrude>
curves <modeling-curves-make-segment>
curves <modeling-curves-subdivision>
curves <modeling-curves-toggle-cyclic>
custom normals <modeling_meshes_normals_custom>
custom set of data <modeling-modifiers-generate-skin-data>
custom split normals <modeling_meshes_normals_custom>
cycles/
dam
data
data ID <ui-data-id>
data-block <ui-data-block>
data-block menu <ui-data-block>
data-block menus <ui-data-block>
data-block type <data-system-datablock-types>
data-blocks types <data-system-datablock-types>
data-scenes-props-units
data-system-datablock-make-single-user
data_path
decoder bitstream buffer <https://en.wikipedia.org/wiki/Video_buffering_verifier>
default
default keymap preferences <keymap-blender_default-prefs>
default_byte
default_float
default_sequencer
deg
degrees
delete <bpy.ops.armature.delete>
delta transform <bpy.types.Object.delta>
delta transforms <bpy.types.Object.delta>
demo blend-file <https://wiki.blender.org/wiki/File:Manual_-_Explode_Modifier_-_Exploding_Cube_-_2.5.blend>
demo.py
denoiser <render-cycles-settings-viewport-denoising>
denoising <render-cycles-settings-viewport-denoising>
density
dev
developer's site <https://development.root-1.de/Atomic_Blender_PDB_XYZ.php>
developer.blender.org
developer.blender.org <https://developer.blender.org/>
development builds <https://builder.blender.org/download/>
dictionaries <https://docs.python.org/3/tutorial/datastructures.html#dictionaries>
differential coordinates <https://igl.ethz.ch/projects/Laplacian-mesh-processing/Laplacian-mesh-editing/diffcoords-editing.pdf>
diffuse(N)
diffuse_ramp(N, colors[8])
diffuse_toon(N, size, smooth)
dir()
directory_name/
discussion <http://news.povray.org/povray.general/thread/%3Cweb.4d77b443f36cbfe281c811d20%40news.povray.org%3E/>
disp_####.exr
display_render
diurnal
dm
documentation <https://docs.python.org/>
documentation <https://github.com/s-leger/archipack/wiki>
documentation workboard <https://developer.blender.org/project/board/53/>
does not count as a normal \"bounce\" <render-cycles-light-paths-transparency>
doi:10.1111/cgf.12830 <https://doi.org/10.1111/cgf.12830>
doi:10.1111/j.1467-8659.2011.01976.x <https://doi.org/10.1111/j.1467-8659.2011.01976.x>
dot icon
download <http://www.povray.org/download/>
driver namespace example <driver-namespace>
easing mode <editors-graph-fcurves-settings-easing>
easings <editors-graph-fcurves-settings-easing>
edge loop selection <bpy.ops.mesh.loop_multi_select>
edge loops <modeling-mesh-structure-edge-loops>
edited <properties-texture-space-editing>
editing <meta-ball-editing>
editors-3dview-index
editors-graph-fcurves-settings-handles
editors-graph-fcurves-settings-interpolation
editors-sequencer-index
emission()
envelopes <armature-bones-envelope>
example <fig-sequencer-strips-effects-add>
example blend-file <http://download.blender.org/ftp/mont29/persistent_data/sapling_CN.blend>
example blend-file <https://en.blender.org/uploads/4/48/Manual_-_Modifiers_-_Particle_Instance_Modifiers_-_Split_Plane.blend>
example blend-file <https://wiki.blender.org/wiki/File:Blender3D Quads-BE-Stiffness.blend>
execute()
exp
experimental builds <https://builder.blender.org/download/>
exported <bpy.ops.sequencer.export_subtitles>
exr
exterior forces <physics-softbody-forces-exterior-aerodynamics>
exterior forces <physics-softbody-forces-exterior-goal>
extrapolation <editors-graph-fcurves-settings-extrapolation>
extras
eyedropper <ui-eyedropper>
fabs
faces.super_face
families <meta-ball-object-families>
family <meta-ball-object-families>
fig-collision-soft-plane
fig-constraints-transformation-extrapolate
fig-curves-editing-open-close
fig-curves-extrude-taper-curve
fig-curves-extrude-taper1
fig-curves-extrude-taper2
fig-curves-extrude-taper3
fig-dope-sheet-action
fig-interface-redo-last-edit-mode
fig-interface-redo-last-object-mode
fig-interpolation-type
fig-mesh-basics-add-one
fig-mesh-deform-mirror-cursor
fig-mesh-deform-mirror-origins
fig-mesh-deform-to-sphere-monkey
fig-mesh-screw-angle
fig-mesh-screw-circle
fig-mesh-screw-clock
fig-mesh-screw-duplicate
fig-mesh-screw-error-info
fig-mesh-screw-error-popup
fig-mesh-screw-generated-mesh
fig-mesh-screw-interactive-panel
fig-mesh-screw-profile
fig-mesh-screw-ramp
fig-mesh-screw-spindle
fig-mesh-screw-spring
fig-mesh-screw-start
fig-mesh-screw-start-mesh
fig-mesh-screw-transform-panel
fig-mesh-screw-wood
fig-mesh-select-advanced-loop-ring
fig-mesh-select-intro-selection-modes
fig-mesh-spin-glass
fig-mesh-spin-glass-top
fig-mesh-spin-profile
fig-mesh-topo-loop
fig-meta-ball-base
fig-meta-ball-example
fig-meta-ball-scale
fig-meta-intro-underlying
fig-modifiers-panel-layout
fig-particle-child-kink
fig-rig-bone-active-tip
fig-rig-bone-connected-root
fig-rig-bone-disconnected-tip
fig-rig-bone-duplication
fig-rig-bone-intro-bbone
fig-rig-bone-intro-same
fig-rig-bone-mirror
fig-rig-bone-select-deselect
fig-rig-bones-extrusion
fig-rig-pose-edit-scale
fig-rig-properties-switch
fig-softbody-collision-plane1
fig-softbody-collision-plane2
fig-softbody-force-interior-bending
fig-softbody-force-interior-connection
fig-softbody-force-interior-no-bending
fig-softbody-force-interior-stiff
fig-softbody-force-interior-with
fig-softbody-force-interior-without
fig-surface-edit-extruding
fig-surface-edit-join-complete
fig-surface-edit-join-ready
fig-surface-edit-select-point
fig-surface-edit-select-row
fig-surface-intro-order
fig-surface-intro-surface
fig-surface-intro-weight
fig-troubleshooting-file-browser
fig-view3d-median-point-edit-mode
fig-view3d-median-point-object-mode
fig-view3d-mode-select
fig-view3d-parent-bone-parent
fig-view3d-parent-bone-parent-child
fig-view3d-parent-bone-parent-relative
fig-view3d-parent-scene-no
file
file.blend
file_01.blend
file_02.blend
filename + frame number + .extension
files-blend-relative_paths
files-data_blocks-custom-properties
files-linked_libraries-known_limitations-compression
files-media-index
filter
filter <editors-outliner-interface-filter>
float
floor
fmod
foam_####.exr
font hinting <https://en.wikipedia.org/wiki/Font_hinting>
forearm
found bundled python: {DIR}
fr
frame
frame/8
ft
functions.wolfram.com <https://functions.wolfram.com/>
fur
g
geom:curve_intercept
geom:curve_tangent_normal
geom:curve_thickness
geom:dupli_generated
geom:dupli_uv
geom:generated
geom:is_curve
geom:name
geom:numpolyvertices
geom:polyvertices
geom:trianglevertices
geom:uv
getattribute()
getmessage
getmessage(\"trace\", ..)
glTF 2.0 extensions <https://github.com/KhronosGroup/glTF/tree/master/extensions>
glTF GitHub repository <https://github.com/KhronosGroup/glTF>
glTF Settings
glTF-Blender-IO repository <https://github.com/KhronosGroup/glTF-Blender-IO>
glossy_toon(N, size, smooth)
graph-preview-range
graph-view-menu
graph_editor-view-properties
gravity <bpy.types.Sculpt.gravity>
grease-pencil-draw-common-options
grease-pencil-modifier-influence-filters
hair_reflection(N, roughnessu, roughnessv, T, offset)
hair_transmission(N, roughnessu, roughnessv, T, offset)
handle type <editors-graph-fcurves-settings-handles>
hard-coded 24 FPS <https://developer.blender.org/T55288#754358>
hardware-ndof
headers <ui-region-header>
held_object
help-menu
henyey_greenstein(g)
here <bpy.types.Mesh.use_mirror_topology>
here <curve-switch-direction>
here <https://wiki.blender.org/wiki/File:ManGreasePencilConvertToCurveDynamicExample.blend>
here <https://wiki.blender.org/wiki/File:Manual-2.5-Duplifaces-Example01.blend>
here <https://www.blender.org/download/>
hide and reveal <curves-show-hide>
highlighted
hm
holdout()
horizontal line icon
hostname <https://en.wikipedia.org/wiki/Hostname>
hour:minute:second
how to combine shape keys and drivers <shapekey-driver-example>
html
https://developer.blender.org
https://svn.blender.org/svnroot/bf-manual/trunk/blender_docs
https://www.youtube.com/watch?v=Ge2Kwy5EGE0
iTaSC IK Solver <rigging-armatures_posing_bone-constraints_ik_model_itasc>
image formats <files-media-image_formats>
image-formats-open-sequence
image-generated
image0001.png
image_##_test.png
image_01_test.png
in
in development <https://code.blender.org/2013/12/how-blender-started-twenty-years-ago/>
increasing the radius <modeling-curve-radius>
index.rst
influence <meta-ball-editing-negative-influence>
injected
injected,held_object
inputs
int
inter-frame <https://en.wikipedia.org/wiki/Inter-frame>
interface_splash_current.png
interface_undo-redo_last.png
interface_undo-redo_repeat-history-menu.png
interpolation algorithm <bpy.types.Spline.tilt_interpolation>
interpolation mode <editors-graph-fcurves-settings-interpolation>
introduction.rst
inverse kinematics feature <bone-constraints-inverse-kinematics>
island_abbreviation: edge_number
join <bpy.ops.object.join>
jpeg
jpg
kConstantScope
kFacevaryingScope
kUniformScope
kUnknownScope
kVaryingScope
kVertexScope
keyframe-type
keymap-customize
km
known compatibility issues <https://wiki.blender.org/wiki/Reference/Compatibility>
languages codes <https://www.gnu.org/software/gettext/manual/html_node/Usual-Language-Codes.html>
lasso selection <tool-select-lasso>
later page <bone-constraints-inverse-kinematics>
layer samples <render-cycles-integrator-layer-samples>
layername_3Dfaces
left/right <armature-editing-naming-conventions>
lerp
libsdl.org <https://www.libsdl.org>
limbs.simple_tentacle
limbs.super_finger
limbs.super_limb
limbs.super_palm
limitation of FFmpeg <https://trac.ffmpeg.org/ticket/8344>
limitations <eevee-limitations-volumetrics>
link <data-system-linked-libraries-make-link>
list <ui-list-view>
list of GCN generations <https://en.wikipedia.org/wiki/Graphics_Core_Next#Generations>
list of Nvidia graphics cards <https://developer.nvidia.com/cuda-gpus#compute>
list view <ui-list-view>
lists <ui-list-view>
living room
loaded in the preferences <prefs-lights-matcaps>
local, system and user paths <blender-directory-layout>
locale
locale/fr
locale/fr/LC_MESSAGES/getting_started/about_blender/introduction.po
location.x
location[0]
locks pie menu <bpy.ops.object.vertex_group_lock>
log
m
macOS <http://www.ia.arch.ethz.ch/wp-content/uploads/2013/11/pyproj.zip>
mailing lists <https://lists.blender.org/mailman/listinfo>
main task of the project <https://developer.blender.org/T53500>
make
make modifiers
make.bat
manual
manual/getting_started/about_blender/introduction.rst
manual/images
marked as sharp <bpy.ops.mesh.mark_sharp>
master
material indices <bi-multiple-materials>
material slot <material-slots>
material slots <material-slots>
material:index
materials/
math
math <https://docs.python.org/3.8/library/math.html>
max
mesh counterpart <bpy.ops.mesh.decimate>
mesh-faces-tristoquads
mesh-unsubdivide
meta family <meta-ball-object-families>
metaballs <https://en.wikipedia.org/wiki/Metaballs>
meter
meters
mi
microfacet_beckmann(N, roughness)
microfacet_beckmann_aniso(N, T, ax, ay)
microfacet_beckmann_refraction(N, roughness, ior)
microfacet_ggx(N, roughness)
microfacet_ggx_aniso(N, T, ax, ay)
microfacet_ggx_refraction(N, roughness, ior)
mil
min
minimum and recommended requirements <https://www.blender.org/download/requirements/>
minimum requirements <https://www.blender.org/download/requirements/>
mm
mode
mode='RENDER'
model <https://www.scratchapixel.com/lessons/procedural-generation-virtual-worlds/simulating-sky/simulating-colors-of-the-sky>
modeling-mesh-analysis
modeling-mesh-make-face-edge-dissolve
modeling-meshes-editing-fill
modeling-text-character
modeling_meshes_normals_custom
modeling_modifiers_deform_shrinkwrap_methods
modifier stack <modifier-stack>
modifiers-generate-subsurf-creases
module owners page <https://wiki.blender.org/wiki/Process/Module_Owners/List>
modules
modules/
more details see here <render-cycles-reducing-noise-glass-and-transp-shadows>
mov
mp3
msgstr
multiple applications <https://opencolorio.org/#supported_apps>
my_app_template
my_scripts
name
name_frame_index.bphys
naming conventions <armature-editing-naming-conventions>
new_length = real_length / speed_factor
no icon
non-highlighted
non-local means <https://en.wikipedia.org/wiki/Non-local_means>
normal_####.exr
not
object setting <render-cycles-settings-object-motion-blur>
object-convert-to
object-data <properties-data-tabs>
object-proxy
object-show-hide
object.show_name
object:index
object:location
object:random
objects types <objects-types>
offsetting nodes <editors-nodes-usage-auto-offset>
old Wiki <https://archive.blender.org/wiki/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Align_Tools/>
old Wiki <https://archive.blender.org/wiki/index.php/Extensions:2.6/Py/Scripts/Modeling/Extra_Tools/>
old Wiki <https://archive.blender.org/wiki/index.php/Extensions:2.6/Py/Scripts/Modeling/Inset-Polygon/>
old Wiki <https://archive.blender.org/wiki/index.php/Extensions:2.6/Py/Scripts/Modeling/LoopTools/>
old Wiki <https://archive.blender.org/wiki/index.php/Extensions:2.6/Py/Scripts/Nodes/Nodes_Efficiency_Tools/>
old Wiki <https://archive.blender.org/wiki/index.php/Extensions:2.6/Py/Scripts/Object/CellFracture/>
old Wiki <https://archive.blender.org/wiki/index.php/Extensions:2.6/Py/Scripts/Paint/Palettes/>
online calculator <https://www.esrl.noaa.gov/gmd/grad/solcalc>
open source <https://opensource.org/>
or
oren_nayar(N, roughness)
outputs
overview on ReStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>
pack islands operator <editors-uv-editing-layout-pack_islands>
pack or unpack external Data <pack-unpack-data>
pack-unpack-data
paint mask <sculpt-mask-menu>
painting-sculpting-index
painting-weight-index
panoramic camera <cycles-panoramic-camera>
paper <https://cgg.mff.cuni.cz/projects/SkylightModelling/>
paper <https://doi.org/10.1145/311535.311545>
parallelepiped <https://en.wikipedia.org/wiki/Parallelepiped>
parenting <bpy.ops.object.parent_set>
particle:age
particle:angular_velocity
particle:index
particle:lifetime
particle:location
particle:size
particle:velocity
passes <render-cycles-passes>
path:ray_length
per-light override <bpy.types.Light.cutoff_distance>
performed manually <bpy.ops.mesh.edge_split>
phong_ramp(N, exponent, colors[8])
physics-cloth-introduction-springs
pi
pinned <bpy.ops.uv.pin>
pip
pip3
pivot-point-index
plane track <clip-tracking-plane>
png
pose marker <marker-pose-add>
pot
pov/inc/mcr/ini
pow
pre-version <https://archive.blender.org/development/release-logs/blender-256-beta>
prefs-auto-execution
prefs-file-paths
prefs-index
prefs-interface-translation
prefs-menu
prefs-save-load
preset <ui-presets>
presets
presets/
previews <file_browser-previews>
previous section <Write the Add-on (Simple)>
principled_hair(N, absorption, roughness, radial_roughness, coat, offset, IOR)
print()
project site <http://www.povray.org/download/>
properties switching/enabling/disabling <armature-bone-properties>
properties-material-viewport-display
properties-object-viewport-display
proxies <object-proxy>
quantum chemical calculators <https://en.wikipedia.org/wiki/List_of_quantum_chemistry_and_solid-state_physics_software>
quit.blend
rad_def
rad_def.inc
radians
ray visibility <cycles-ray-visibility>
reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>
recently <other-file-open-options>
reflection(N)
refraction(N, ior)
refresh <bpy.ops.sequencer.refresh_all>
region <render-output-dimensions-region>
register
register an extension prefix <https://github.com/KhronosGroup/glTF/blob/master/extensions/Prefixes.md>
register for one <https://developer.blender.org/auth/register/>
register()
relations page <bone-relations-parenting>
relative file path <files-blend-relative_paths>
relative shape keys mix additively <animation-shapekeys-relative-vs-absolute>
release cycle <https://wiki.blender.org/wiki/Process/Release_Cycle>
release notes <https://wiki.blender.org/wiki/Reference/Release_Notes/2.81/Library_Overrides>
release notes <https://www.blender.org/download/releases/>
remarks <https://development.root-1.de/Atomic_Blender_PDB_XYZ_Remarks.php>
render
render output path <render-tab-output>
render pass <render-cycles-passes>
render-cycles-gpu-optix
render-cycles-integrator-world-settings
render-cycles-reducing-noise-mis
render-materials-settings-viewport-display
render-output-postprocess
render-tab-dimensions
rendered shading <view3d-viewport-shading>
rendering animation <command_line-render>
rendering/
report a bug <https://developer.blender.org/maniphest/task/edit/form/1/>
report the problem <https://developer.blender.org/maniphest/task/edit/form/default/?project=PHID-PROJ-c4nvvrxuczix2326vlti>
requirements.txt
resolution <bpy.types.Curve.resolution_u>
resolution <bpy.types.Curve.resolution_v>
resolution_x
resources/versions.json
rest_mat
rig_ui
rig_ui.py
rigged <animation-rigging>
roll rotation <armature-bone-roll>
root
rotation_x
rotation_y
rotation_z
round
row <modeling-surfaces-rows-grids>
rst
sampling rate <https://en.wikipedia.org/wiki/Sampling_(signal_processing)#Sampling_rate>
save <files-blend-save>
saving images <bpy.types.ImageFormatSettings>
scale transformation <bpy.ops.transform.resize>
scaled <bpy.ops.transform.resize>
scene dicing rate <cycles-subdivision-rate>
scene settings <data-scenes-audio>
scene settings <data-scenes-props-units>
scene's active camera<scene-camera>
scene-wide bounce settings <cycles-bounces>
scene_linear
script <http://www.apexbow.com/randd.html>
script homepage <https://sites.google.com/site/bartiuscrouch/looptools>
scripting <scripting-index>
scripts
sculpt-mask-menu
sculpt_mask_clear-data
search_path
section_1.rst
section_2.rst
see example blend-file <https://en.blender.org/uploads/a/ad/Data_Transfer_Normal_Torus.blend>
see the example on GitHub <https://github.com/KhronosGroup/glTF-Blender-IO/tree/master/example-addons/example_gltf_extension>
see this <https://www.mathworks.com/help/vision/ug/interpolation-methods.html>
selecting <object-select-menu>
selection states <object-active>
self
self.location.x
sequencer-edit-change
setmessage
several independent websites <https://www.blender.org/community/>
shape <bpy.types.Curve.dimensions>
sharp edges <modeling_meshes_normals_sharp_edge>
sid <https://packages.debian.org/sid/libopenxr1-monado>
simplify panel <render-cycles-settings-scene-simplify>
sin
sin(frame/8)
sin(x)/x
sky_sphere{}
smooth shading <modeling-meshes-editing-normals-shading>
smoothstep
snap tools <bpy.ops.view3d.snap>
source code <https://developer.blender.org/diffusion/B/browse/master/source/blender/blenkernel/BKE_global.h>
sphere_sweep
spines.super_spine
splash
splash.png
split normals <auto-smooth>
sqrt
sqrt(2)
square(frame)
st
stack <modifier-stack>
startup
startup.blend
startup/
strip option <sequencer-sound-waveform>
support page <https://www.blender.org/support/>
supported platforms
svn
svn add /path/to/file
svn rm /path/to/file
svn status
svn update
sys.argv
sys.path
sys.stdin
system-info.txt
tab-view3d-modes
tan
targa
temp-dir
temperature
test-######.png
test-000001.png
test.blend
test.crash.txt
test_blender_file.blend
text editing <ui-text-editing>
texture {}
textured brush pack <https://cloud.blender.org/p/gallery/5f235cc297f8815e74ffb90b>
their documentation <bpy.ops.object.make_single_user>
this Pixar paper <https://graphics.pixar.com/library/MultiJitteredSampling/paper.pdf>
this Pixar paper <https://graphics.pixar.com/library/ProgressiveMultiJitteredSampling/paper.pdf>
this blend <https://wiki.blender.org/wiki/File:Manual-2.5-DupliVerts-Examples.blend>
this page <https://blender.stackexchange.com/questions/26643>
this pdf <https://wiki.blender.org/wiki/File:Manual-2.6-Render-Freestyle-PrincetownLinestyle.pdf>
this picture <https://commons.wikimedia.org/wiki/File:Analemma_fishburn.tif>
this post <https://blenderartists.org/forum/showthread.php?323358-DXF-Importer&p=2664492&viewfull=1#post2664492>
this section <render-layers>
tilt <modeling-curve-tilt>
timeline-playback
timeline-view-menu
todo
tool-annotate
tool-mesh-extrude_individual
tool-select-circle
top -o %MEM
top -o MEM
topbar-app_menu
topbar-render
total
trace(point pos, vector dir, ...)
trackball rotation <view3d-transform-trackball>
transform-numeric-input-advanced
transform-numeric-input-simple
transformations <bpy.ops.object.transform_apply>
translucent(N)
transparent()
trivially cyclic curves <bpy.types.FModifierCycles>
troubleshooting-gpu-index
trunc
turntable.blend
ui-color-palette
ui-color-picker
ui-color-ramp-widget
ui-curve-widget
ui-data-block
ui-data-id
ui-direction-button
ui-eyedropper
ui-list-view
ui-operator-buttons
ui-undo-redo-adjust-last-operation
ui_template_list diff
um
underline settings <modeling-text-character-underline>
unit system <data-scenes-props-units>
unregister
unregister()
userpref.blend
uv-image-rotate-reverse-uvs
uv-maps-panel
v
value <animation-shapekey-relative-value>
var all_langs = {..};
vertex snapping <transform-snap-element>
video codec <files-video-codecs>
view3d-transform-plane-lock
view3d-viewport-shading
volumes.rst
water bottle <https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/WaterBottle>
water bottle sample model <https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/WaterBottle>
weasel words <https://en.wikipedia.org/wiki/Weasel_word>
weight <curves_structure_nurbs_weight>
weight <modeling-surfaces-weight>
weight = 1
weight-painting-bones
wireframe <3dview-shading-rendered>
wm.call_menu
wm.call_menu_pie
wm.call_panel
wm.context_
wm.context_cycle_enum
wm.context_menu_enum
wm.context_modal_mouse
wm.context_pie_enum
wm.context_scale_float
wm.context_toggle
wm.context_toggle_enum
wm.operators.*
wm.set_stereo_3d
x
x-ray <3dview-shading-xray>
yd
zoom level <editors_3dview_navigation_zoom>
{BLENDER_SYSTEM_SCRIPTS}/startup/bl_app_templates_system
{BLENDER_USER_SCRIPTS}/startup/bl_app_templates_user
{base path}/{file name}{frame number}.{extension}
|
|BLENDER_VERSION|
~
~/.blender/|BLENDER_VERSION|/config/startup.blend
~/blender_docs
~/blender_docs/build/html
~/blender_docs/toos_maintenance
~/software        
'''

msg = "Adaptivity"
t_list = {
    "Affine": "",
    "After/Remained": "",
    "Agent": "",
    "Airbrush": "",
    "Alexander": "",
    "Align": "",
    "Alignment": "",
    "America": "",
    "Anisotropic": "",
    "Annotate": "",
    "Applying": "",
    "April": "",
    "Arc": "",
    "Arccosine": "",
    "Arcsine": "",
    "Arctangent": "",
    "Array": "",
    "Assign": "",
    "Attributes": "",
    "Audio": "",
    "August": "",
    "AutoName": "",
    "Autosave": "",
    "Autoscale": "",
    "Average": "",
    "Averaged": "",
    "Awards": "",
    "Axes": "",
    "Axon": "",
    "Azimuth": "",
    "B": "",
    "B&W": "",
    "B-value": "",
    "B.x": "",
    "B.y": "",
    "BSDFs": "",
    "Back": "",
    "Backbone": "",
    "Backdrop": "",
    "Backface": "",
    "Barcelona": "",
    "Blender": "",
    "Blender's": "",
    "Blendphys": "",
    "Blue": "",
    "Boid": "",
    "Bunny": "",
    "Button": "",
    "Bézier": "",
    "CBTB16]_": "",
    "COM": "",
    "CPU": "",
    "Cessen's": "",
    "ChainPredicateIterator": "",
    "ChainSilhouetteIterator": "",
    "Check": "",
    "Clemens": "",
    "Collada": "",
    "Compositor": "",
    "Concave": "",
    "Convex": "",
    "Courant–Friedrichs–Lewy": "",
    "Cycles": "",
    "D": "",
    "DEF": "",
    "DOI": "",
    "DTP": "",
    "DV": "",
    "Daniel": "",
    "Dealga": "",
    "Deltas": "",
    "DensityUP1D": "",
    "Derivative": "",
    "Deswaef": "",
    "Disney": "",
    "DolphinDream": "",
    "Drivers": "",
    "EFHLA11]_": "",
    "Edit": "",
    "Editor": "",
    "Eoan": "",
    "Epsilon": "",
    "Euler's": "",
    "F-curves": "",
    "FC0": "",
    "FFCC00": "",
    "FFmpeg": "",
    "FK": "",
    "FPS": "",
    "False": "",
    "Feline": "",
    "Femto-ST": "",
    "Fran&ccedil;ais": "",
    "Frank": "",
    "Français": "",
    "Fweeb": "",
    "G": "",
    "GCC": "",
    "GCN": "",
    "GL": "",
    "GPL'd": "",
    "GTAO": "",
    "Gavrilov": "",
    "Gen": "",
    "GitHub": "",
    "Grease": "",
    "Green": "",
    "Gridlines": "",
    "HS": "",
    "HV": "",
    "Harkyman": "",
    "Heterogeneous": "",
    "IK": "",
    "IO": "",
    "IPO": "",
    "Intel": "",
    "Interface0D": "",
    "Interface1D": "",
    "JONSWAP": "",
    "Julien": "",
    "Kr": "",
    "LW": "",
    "LWPOLYLINE": "",
    "Lara": "",
    "Leaf": "",
    "Length2DBP1D": "",
    "Lichtso": "",
    "LightBWK": "",
    "Lightwave": "",
    "Lines": "",
    "Lozac'h": "",
    "MTEXT": "",
    "MacBook": "",
    "Maintain": "",
    "MajorControl": "",
    "MajorRadius": "",
    "Mango": "",
    "Martinez": "",
    "Material": "",
    "MaxGradient": "",
    "McArdle": "",
    "MetaPlane": "",
    "MetaThing": "",
    "Mickael": "",
    "Microsoft": "",
    "MinorControl": "",
    "MinorRadius": "",
    "Mirror": "",
    "Mix": "",
    "Mode": "",
    "Modifier": "",
    "Monado": "",
    "Multiplexing": "",
    "N": "",
    "N-gon": "",
    "N-gons": "",
    "NURBS": "",
    "Narrow": "",
    "Narrowness": "",
    "Nation": "",
    "Newton's": "",
    "Notepad": "",
    "Nouveau": "",
    "Nvidia": "",
    "OHA": "",
    "ORG": "",
    "OS-specific": "",
    "OXZ": "",
    "Oculus": "",
    "OpenColorIO": "",
    "OpenType": "",
    "OpenXR": "",
    "Operator": "",
    "Otherwise": "",
    "Outliner": "",
    "P": "",
    "P1": "",
    "PC": "",
    "PLANESURFACE": "",
    "PNG": "",
    "POLYFACE": "",
    "PYTHONPATH": "",
    "Palmino": "",
    "Pancakes": "",
    "Pavilion": "",
    "Pencil": "",
    "Phillips": "",
    "Photons": "",
    "Physical": "",
    "Pierson-Moskowitz": "",
    "Pixar": "",
    "Pointcache": "",
    "Pontiac": "",
    "PostScript": "",
    "Preferences": "",
    "Programming": "",
    "Progressive": "",
    "Projection": "",
    "Properties": "",
    "Proportional": "",
    "Prototype": "",
    "Prune": "",
    "Publisher": "",
    "Python": "",
    "Python's": "",
    "Quadriflow": "",
    "QuantitativeInvisibilityUP1D": "",
    "Quest": "",
    "R": "",
    "README": "",
    "RNG": "",
    "RRGGBB": "",
    "Rebake": "",
    "Rectangular": "",
    "Reducing": "",
    "Regression": "",
    "Represent": "",
    "Restore": "",
    "Retina": "",
    "Retopology": "",
    "Rift": "",
    "SL": "",
    "SV": "",
    "Safe": "",
    "Sapling": "",
    "Screw": "",
    "Scribus": "",
    "Sealed": "",
    "Seams": "",
    "Sector": "",
    "Security": "",
    "Self": "",
    "Shade": "",
    "Shared": "",
    "Shift": "",
    "Short": "",
    "Sidebar": "",
    "Solution": "",
    "Special": "",
    "Spline": "",
    "Stable": "",
    "Stan": "",
    "Stanford": "",
    "Steam": "",
    "SteamVR": "",
    "Studios": "",
    "SubDivR": "",
    "SubDivV": "",
    "Subsamples": "",
    "Substitute": "",
    "Suzanne": "",
    "T": "",
    "T34665": "",
    "TL;DR": "",
    "TV": "",
    "Teapot": "",
    "Termination": "",
    "Terrain": "",
    "Tessellate": "",
    "Tex": "",
    "The": "",
    "Thread": "",
    "Thumbnail": "",
    "Toolbar": "",
    "Torso": "",
    "Trainers": "",
    "Transfer": "",
    "Translucent": "",
    "TrueType": "",
    "TrumanBlending": "",
    "Turing": "",
    "Turnaround": "",
    "UI": "",
    "UV": "",
    "Unchanged": "",
    "Unfold": "",
    "Unicode": "",
    "Unlit": "",
    "Unsupported": "",
    "Unwrapping": "",
    "Utah": "",
    "V": "",
    "VPORT": "",
    "VX": "",
    "Van": "",
    "Vanishing": "",
    "Velvet": "",
    "Vesta": "",
    "Video": "",
    "View": "",
    "ViewEdge": "",
    "ViewEdgeIterator": "",
    "ViewMap": "",
    "Viewport": "",
    "Views": "",
    "Volume": "",
    "WDAS": "",
    "Waals": "",
    "Wahooney": "",
    "Walt": "",
    "Website": "",
    "Whole": "",
    "Wiki": "",
    "Wikipedia": "",
    "Window": "",
    "Workaround": "",
    "Worley": "",
    "X": "",
    "Y": "",
    "YZ": "",
    "Z": "",
    "Z-buffer": "",
    "Zenith": "",
    "\\frac{a}{2}": "",
    "\\n": "",
    "_sep": "",
    "a": "",
    "about": "",
    "above": "",
    "abs": "",
    "absolute": "",
    "absorption": "",
    "accented": "",
    "accepts": "",
    "according": "",
    "account": "",
    "accuracy": "",
    "accurate": "",
    "acos": "",
    "action": "",
    "action's": "",
    "activate": "",
    "activated": "",
    "active": "",
    "add": "",
    "adding": "",
    "addon": "",
    "adjusted": "",
    "advanced": "",
    "affect": "",
    "affected": "",
    "affecting": "",
    "affects": "",
    "after": "",
    "air": "",
    "al": "",
    "algorithm": "",
    "aligned": "",
    "all": "",
    "alone": "",
    "along": "",
    "along/around": "",
    "also": "",
    "although": "",
    "always": "",
    "ambient": "",
    "amount": "",
    "an": "",
    "anaglyph": "",
    "analysis": "",
    "and": "",
    "and/or": "",
    "angle": "",
    "angles": "",
    "angular": "",
    "animate": "",
    "animated": "",
    "animation": "",
    "animations": "",
    "annotation": "",
    "annotations": "",
    "another": "",
    "antonioya": "",
    "any": "",
    "apex": "",
    "appear": "",
    "append": "",
    "appending": "",
    "application": "",
    "applications": "",
    "applied": "",
    "apply": "",
    "are": "",
    "area": "",
    "areas": "",
    "aren't": "",
    "arm": "",
    "armature": "",
    "armatures": "",
    "around": "",
    "arrange": "",
    "arrow": "",
    "arrows": "",
    "artifacts": "",
    "artists": "",
    "as": "",
    "aspect": "",
    "assets": "",
    "assigned": "",
    "at": "",
    "atomic": "",
    "atoms": "",
    "attempting": "",
    "attribute": "",
    "auto": "",
    "automatic": "",
    "available": "",
    "avoid": "",
    "avoided": "",
    "avoids": "",
    "ax": "",
    "axis": "",
    "ay": "",
    "background": "",
    "background{": "",
    "bake": "",
    "baked": "",
    "base": "",
    "be": "",
    "been": "",
    "before": "",
    "beginning": "",
    "behavior": "",
    "below": "",
    "between": "",
    "bevel": "",
    "binding": "",
    "bl": "",
    "black": "",
    "blend": "",
    "blend-file": "",
    "blender_api:bpy": "",
    "blender_api:mathutils": "",
    "blending": "",
    "blur": "",
    "bone": "",
    "bone's": "",
    "bones": "",
    "bool": "",
    "both": "",
    "bottom": "",
    "box": "",
    "bpy": "",
    "breadth": "",
    "bright/dark": "",
    "brighter": "",
    "brikbot": "",
    "brush": "",
    "brushes": "",
    "bullseye": "",
    "but": "",
    "by": "",
    "cP": "",
    "cache": "",
    "cage": "",
    "called": "",
    "calligraphy": "",
    "camera": "",
    "capsule": "",
    "cartoon": "",
    "cases": "",
    "cause": "",
    "center": "",
    "chains": "",
    "change": "",
    "channel": "",
    "chapter": "",
    "character": "",
    "children": "",
    "circle": "",
    "clear": "",
    "closed": "",
    "cm": "",
    "collections": "",
    "colliding": "",
    "color": "",
    "colors": "",
    "comes": "",
    "command": "",
    "compatible": "",
    "compiler": "",
    "computationally": "",
    "computed": "",
    "conf.py": "",
    "consequently": "",
    "constraint": "",
    "consumed": "",
    "context": "",
    "controls": "",
    "coordinate": "",
    "coordinates": "",
    "cos": "",
    "cotejrp1": "",
    "could": "",
    "crazy": "",
    "creates": "",
    "current": "",
    "cursor": "",
    "curve": "",
    "cut": "",
    "cwolf3d": "",
    "cyclic": "",
    "dark": "",
    "data": "",
    "data-block": "",
    "data-blocks": "",
    "default": "",
    "deflection": "",
    "deleted": "",
    "der": "",
    "destination": "",
    "detail": "",
    "dev": "",
    "dictionary": "",
    "different": "",
    "differently": "",
    "direction": "",
    "directions": "",
    "displays": "",
    "distance": "",
    "diurnal": "",
    "do": "",
    "doesn't": "",
    "dommetysk": "",
    "don't": "",
    "dot": "",
    "down": "",
    "drag": "",
    "drawn": "",
    "duration": "",
    "e.g": "",
    "each": "",
    "edge": "",
    "edges": "",
    "editing": "",
    "editors": "",
    "effect": "",
    "el": "",
    "element": "",
    "empty": "",
    "enabled": "",
    "end": "",
    "endpoint": "",
    "ends": "",
    "errors": "",
    "et": "",
    "etc": "",
    "even": "",
    "every": "",
    "exactly": "",
    "example": "",
    "exclusively": "",
    "execution": "",
    "existing": "",
    "exp": "",
    "expected": "",
    "explanation": "",
    "exporter": "",
    "eyelids": "",
    "fabs": "",
    "face": "",
    "factor": "",
    "families": "",
    "family": "",
    "far": "",
    "favorites": "",
    "field": "",
    "file": "",
    "files": "",
    "first": "",
    "flat": "",
    "flower": "",
    "fluid": "",
    "fmod": "",
    "focus": "",
    "footage": "",
    "for": "",
    "forearm": "",
    "foreground": "",
    "former": "",
    "found": "",
    "frame": "",
    "free": "",
    "from": "",
    "full": "",
    "fully": "",
    "functionality": "",
    "garden": "",
    "geometry": "",
    "getattribute": "",
    "getmessage": "",
    "getting": "",
    "give": "",
    "glTF": "",
    "gray": "",
    "grid": "",
    "group": "",
    "half": "",
    "hand": "",
    "handL": "",
    "handR": "",
    "has": "",
    "have": "",
    "head": "",
    "header": "",
    "heading": "",
    "height": "",
    "hidden": "",
    "high": "",
    "hold": "",
    "hook": "",
    "horizontal": "",
    "hydrogen": "",
    "i.e": "",
    "icon": "",
    "ideasman42": "",
    "identifier": "",
    "if": "",
    "image": "",
    "improve": "",
    "in": "",
    "influence": "",
    "info": "",
    "inside": "",
    "intact": "",
    "intermediary": "",
    "into": "",
    "is": "",
    "isn't": "",
    "it": "",
    "item": "",
    "its": "",
    "itself": "",
    "joints": "",
    "just": "",
    "karab44": "",
    "key": "",
    "keyboard": "",
    "keys": "",
    "kg": "",
    "last": "",
    "lattice": "",
    "law": "",
    "layer": "",
    "layers": "",
    "least": "",
    "left": "",
    "length": "",
    "lerp": "",
    "let": "",
    "level": "",
    "library": "",
    "light": "",
    "lights": "",
    "like": "",
    "limb": "",
    "lime": "",
    "line": "",
    "linked": "",
    "linking": "",
    "list": "",
    "listed": "",
    "loading": "",
    "local": "",
    "location": "",
    "loolarge": "",
    "loop": "",
    "lower": "",
    "lying": "",
    "m": "",
    "magnitude": "",
    "main": "",
    "mano-wii": "",
    "manually": "",
    "many": "",
    "map": "",
    "mapping": "",
    "mathematical": "",
    "matte": "",
    "matter": "",
    "may": "",
    "menu": "",
    "mesh": "",
    "mesh's": "",
    "metacarpus": "",
    "metalliandy": "",
    "methodology": "",
    "middle": "",
    "model": "",
    "modes": "",
    "modified": "",
    "modulo": "",
    "moment": "",
    "monkey": "",
    "more": "",
    "motor": "",
    "motorsep": "",
    "move": "",
    "moved": "",
    "name": "",
    "named": "",
    "need": "",
    "negative": "",
    "neighborhood": "",
    "newline": "",
    "next": "",
    "no": "",
    "node": "",
    "noise": "",
    "nominal": "",
    "non-Euclidean": "",
    "normal": "",
    "normals": "",
    "not": "",
    "note": "",
    "now": "",
    "null": "",
    "number": "",
    "numeric": "",
    "object": "",
    "object's": "",
    "objects": "",
    "occur": "",
    "occurs": "",
    "of": "",
    "off": "",
    "offset": "",
    "on": "",
    "once": "",
    "one": "",
    "ones": "",
    "online": "",
    "only": "",
    "open": "",
    "operand": "",
    "optics": "",
    "option": "",
    "options": "",
    "or": "",
    "orders": "",
    "oriental": "",
    "origin": "",
    "original": "",
    "orthogonal": "",
    "other": "",
    "others": "",
    "outcome": "",
    "outside": "",
    "overload": "",
    "owner": "",
    "page": "",
    "panel": "",
    "parallelepiped": "",
    "parallelepipedal": "",
    "parametrizations": "",
    "parent": "",
    "parenting": "",
    "parents": "",
    "particles": "",
    "path": "",
    "paths": "",
    "pattern": "",
    "paw": "",
    "peaks": "",
    "perpendicular": "",
    "petals": "",
    "pheomelanin": "",
    "photograph": "",
    "phymec": "",
    "physically": "",
    "picture": "",
    "pieces": "",
    "pioverfour": "",
    "pipette": "",
    "pivot": "",
    "pixels": "",
    "place": "",
    "plane": "",
    "planes": "",
    "plural": "",
    "point": "",
    "polylines": "",
    "polylist": "",
    "pops": "",
    "pose": "",
    "position": "",
    "positive": "",
    "potter": "",
    "pow": "",
    "precedes": "",
    "preceding": "",
    "precise": "",
    "precisely": "",
    "predicates": "",
    "present": "",
    "pressing": "",
    "prevalent": "",
    "prevent": "",
    "preventing": "",
    "principal": "",
    "probably": "",
    "problem": "",
    "problems": "",
    "produce": "",
    "produces": "",
    "product": "",
    "profiles": "",
    "program": "",
    "progresses": "",
    "proportion": "",
    "proportionally": "",
    "proprietary": "",
    "public": "",
    "publication": "",
    "puppet": "",
    "purple": "",
    "pydriven": "",
    "pydrivers": "",
    "pyramid": "",
    "quadrant": "",
    "quality": "",
    "quantitative": "",
    "quite": "",
    "radiance": "",
    "radius": "",
    "railroad": "",
    "rails": "",
    "range": "",
    "ranges": "",
    "rather": "",
    "ratio": "",
    "ray": "",
    "realistic": "",
    "reason": "",
    "rec": "",
    "recall": "",
    "receive": "",
    "recognize": "",
    "recommended": "",
    "reconnect": "",
    "red": "",
    "reduce": "",
    "reduces": "",
    "reference": "",
    "referred": "",
    "referring": "",
    "refers": "",
    "reflects": "",
    "regardless": "",
    "regex": "",
    "region": "",
    "registration": "",
    "regrouped": "",
    "relationship": "",
    "relative": "",
    "relevant": "",
    "remain": "",
    "remains": "",
    "remarks": "",
    "ren": "",
    "render": "",
    "rendered": "",
    "renderer": "",
    "rendering": "",
    "renders": "",
    "repetitions": "",
    "repository": "",
    "represents": "",
    "reproducible": "",
    "researcher": "",
    "resources": "",
    "respective": "",
    "respectively": "",
    "result": "",
    "resulting": "",
    "retinal": "",
    "returned": "",
    "returns": "",
    "reusable": "",
    "revolutions": "",
    "right": "",
    "rigs": "",
    "rivalry": "",
    "roofs": "",
    "root": "",
    "rotation": "",
    "rule": "",
    "run": "",
    "same": "",
    "saturated": "",
    "scale": "",
    "scene": "",
    "scenes": "",
    "school": "",
    "scientific": "",
    "scope": "",
    "screen": "",
    "screenshot": "",
    "seam": "",
    "second": "",
    "section": "",
    "see": "",
    "seen": "",
    "select": "",
    "selected": "",
    "selection": "",
    "sensitive": "",
    "sentences": "",
    "sequence": "",
    "set": "",
    "sets": "",
    "setting": "",
    "settings": "",
    "shaky": "",
    "shall": "",
    "shape": "",
    "share": "",
    "sheet": "",
    "shield": "",
    "shin": "",
    "shorten": "",
    "shortened": "",
    "shortening": "",
    "shorter": "",
    "shots": "",
    "should": "",
    "shoulder": "",
    "shouldn't": "",
    "shown": "",
    "shrink": "",
    "sid": "",
    "side": "",
    "sides": "",
    "sideways": "",
    "silently": "",
    "simulation": "",
    "sin(": "",
    "since": "",
    "single": "",
    "size": "",
    "sketch": "",
    "skin": "",
    "slower": "",
    "smaller": "",
    "smallest": "",
    "snowflake": "",
    "so": "",
    "socket": "",
    "solver": "",
    "some": "",
    "somehow": "",
    "somewhat": "",
    "soon": "",
    "space": "",
    "spandex": "",
    "speaking": "",
    "specified": "",
    "spikes": "",
    "sqrt(0.5": "",
    "stability": "",
    "stack": "",
    "stacking": "",
    "stage": "",
    "stairway": "",
    "stamp": "",
    "standard": "",
    "stands": "",
    "start": "",
    "startup": "",
    "statistically": "",
    "staying": "",
    "stemming": "",
    "still": "",
    "streams": "",
    "stretch": "",
    "strips": "",
    "stroke": "",
    "strokes": "",
    "submenu": "",
    "subpanel": "",
    "substituted": "",
    "suitable": "",
    "sunglasses": "",
    "supposed": "",
    "surface": "",
    "surfaces": "",
    "surprise": "",
    "surrounded": "",
    "sweep": "",
    "sx": "",
    "sy": "",
    "syntax": "",
    "syrux": "",
    "system": "",
    "tabletop": "",
    "tail": "",
    "take": "",
    "taking": "",
    "tangent": "",
    "taper": "",
    "target": "",
    "targets": "",
    "task": "",
    "technique": "",
    "techniques": "",
    "temple": "",
    "tentacle": "",
    "term": "",
    "terminal": "",
    "tessellation": "",
    "tested": "",
    "texel": "",
    "text": "",
    "texture": "",
    "than": "",
    "that": "",
    "theater": "",
    "them": "",
    "theme": "",
    "then": "",
    "theoretical": "",
    "thereby": "",
    "they": "",
    "thigh": "",
    "this": "",
    "those": "",
    "though": "",
    "thousands": "",
    "three": "",
    "through": "",
    "tiles": "",
    "time": "",
    "to": "",
    "toe": "",
    "too": "",
    "tool": "",
    "top": "",
    "topmost": "",
    "towards": "",
    "track": "",
    "tracker": "",
    "tracking": "",
    "trackpad": "",
    "traditional": "",
    "transformations": "",
    "translucency": "",
    "transparent": "",
    "treatment": "",
    "trees": "",
    "trick": "",
    "tricky": "",
    "trivially": "",
    "trouble": "",
    "true": "",
    "trunc": "",
    "tuple": "",
    "turn": "",
    "turned": "",
    "turns": "",
    "twice": "",
    "two": "",
    "type": "",
    "types": "",
    "typical": "",
    "typically": "",
    "uberPOV": "",
    "unaffected": "",
    "unavailable": "",
    "unconnected": "",
    "under": "",
    "underlying": "",
    "underscore": "",
    "undone": "",
    "uneven": "",
    "unfolded": "",
    "units": "",
    "unlimited": "",
    "unofficial": "",
    "unselectable": "",
    "unselected": "",
    "untouched": "",
    "up": "",
    "upon": "",
    "upside": "",
    "usage": "",
    "use": "",
    "used": "",
    "using": "",
    "usual": "",
    "value": "",
    "values": "",
    "variations": "",
    "varkenvarken": "",
    "vector": "",
    "veins": "",
    "velocity": "",
    "verify": "",
    "versa": "",
    "versus": "",
    "vertex": "",
    "vertices": "",
    "very": "",
    "vibrates": "",
    "vice": "",
    "virtual": "",
    "vs": "",
    "wall": "",
    "water": "",
    "water-tight": "",
    "way": "",
    "ways": "",
    "we": "",
    "websites": "",
    "weights": "",
    "well": "",
    "when": "",
    "where": "",
    "which": "",
    "whichever": "",
    "whose": "",
    "widescreen": "",
    "width": "",
    "width/height": "",
    "will": "",
    "with": "",
    "within": "",
    "world": "",
    "would": "",
    "wrench": "",
    "wrong": "",
    "xaire": "",
    "you": "",
    "your": "",
    "zanqdo": "",
    "zeffii": "",
    "zero": "",
    "|kg/m3": "",
    "|rewind": "",
    "~0.03mb": "",
    }

def readJSON(file_path):
    with open(file_path) as in_file:
        dic = json.load(in_file, object_pairs_hook=OrderedDict)
    return dic

def writeJSON(file_path, data):
    with open(file_path, 'w+', newline='\n', encoding='utf8') as out_file:
        json.dump(data, out_file, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))

def getTextWithinBracket(
        start_bracket:str,
        end_bracket:str,
        text:str,
        is_include_bracket:bool =False,
        replace_internal_start_bracket:str = None,
        replace_internal_end_bracket:str = None
    ) -> list:

    is_same_brakets = (start_bracket == end_bracket)
    if is_same_brakets:
        print(f'getTextWithinBracket() - WARNING: start_bracket and end_braket is THE SAME {start_bracket}. '
              f'ERRORS might occurs!')

    sentence_list = []

    # 1. find positions of start bracket
    if is_same_brakets:
        p_txt = r'\%s' % start_bracket
    else:
        p_txt = r'\%s|\%s' % (start_bracket, end_bracket)

    p = re.compile(p_txt, flags=re.I|re.M)

    word_dict={}
    m_list = p.finditer(text)
    for m in m_list:
        s = m.start()
        e = m.end()
        w = m.group(0)
        entry = {(s, e): w}
        word_dict.update(entry)

    if not word_dict:
        return sentence_list

    q = deque()
    for loc, bracket in word_dict.items():
        s, e = loc
        is_open = (bracket == start_bracket)
        is_close = (bracket == end_bracket)
        if is_open:
            q.append(s)
        if is_close:
            if not q:
                raise Exception(f'getTextWithinBracket(): Invalid close bracket at {s, e}')

            last_s = q.pop()
            ss = (last_s if is_include_bracket else last_s + 1)
            ee = (e if is_include_bracket else e - 1)
            txt_line = text[ss:ee]

            # replace_internal_start_bracket:str = None,
            # replace_internal_end_bracket:str = None
            is_replace_internal_bracket = (replace_internal_start_bracket and (start_bracket in txt_line))
            if is_replace_internal_bracket:
                txt_line = txt_line.replace(start_bracket, replace_internal_start_bracket)

            if is_same_brakets:
                sentence_list.append(txt_line)
                continue

            is_replace_internal_bracket = (replace_internal_end_bracket and (end_bracket in txt_line))
            if is_replace_internal_bracket:
                txt_line = txt_line.replace(end_bracket, replace_internal_end_bracket)

            sentence_list.append(txt_line)
    return sentence_list

def patternMatchAllAsDictNoDelay(pat, text):
    try:
        return_dict = {}
        for m in pat.finditer(text):
            original = ()
            # break_down = []

            s = m.start()
            e = m.end()
            orig = m.group(0)
            original = (s, e, orig)
            entry = {(s,e): orig}
            return_dict.update(entry)

            for g in m.groups():
                if g:
                    i_s = orig.find(g)
                    ss = i_s + s
                    ee = ss + len(g)
                    v=(ss, ee, g)
                    # break_down.append(v)
                    entry = {(ss, ee): g}
                    return_dict.update(entry)
    except Exception as e:
        _("patternMatchAll")
        _("pattern:", pat)
        _("text:", text)
        _(e)
    return return_dict

def patternMatchAllToDict(pat, text):
    matching_list = {}
    for m in pat.finditer(text):
        s = m.start()
        e = m.end()
        orig = m.group(0)
        k = (s, e)
        entry = {k: orig}
        matching_list.update(entry)
    return matching_list

REMOVABLE_SYMB_FULLSET_FRONT = re.compile(r'^[\s\:\!\'$\"\\\(\{\|\[\*\?\<\`\-\+\/\#\&]+')
REMOVABLE_SYMB_FULLSET_BACK = re.compile(r'[\s\:\!\'$\"\\\)\}\|\]\*\?\>\`\-\+\/\#\&\,\.]+$')

def removeLeadingTrailingSymbs(txt):
    leading_set = REMOVABLE_SYMB_FULLSET_FRONT.findall(txt)

def isBalancedSymbol(symb_on, symb_off, txt):
    p_str = f'\{symb_on}([^\{symb_on}\{symb_off}]+)\{symb_off}'
    p_exp = r'%s' % (p_str.replace("\\\\", "\\"))
    pattern = re.compile(p_exp)
    p_list = patternMatchAllToDict(pattern, txt)
    has_p_list = (len(p_list) > 0)
    if has_p_list:
        temp_txt = str(txt)
        for loc, txt in p_list.items():
            s, e = loc
            left = temp_txt[:s]
            right = temp_txt[e:]
            temp_txt = left + right
        return not ((symb_on in temp_txt) or (symb_off in temp_txt))
    else:
        return True

    # default_last_i = 0xffffffff
    # counter = 0
    # last_i = default_last_i
    # off_happened_first = False
    # for i, c in enumerate(txt):
    #     is_on = (i != last_i) and (c == symb_on)
    #     if is_on:
    #         counter += 1
    #         last_i = i
    #     else:
    #         is_off = (i != last_i) and (c == symb_off)
    #         if is_off:
    #             off_happened_first = (last_i == default_last_i)
    #             counter -= 1
    #             last_i = i
    #
    # return (counter == 0) and not (off_happened_first)

class POCache(defaultdict):
    def __init__(self, file_path, extension):
        self.cach_file = os.path.join(home_dir, 'pofilerecord.json')
        self.file_list = []
        self.file_path = file_path
        self.extension = extension

    def getFileList(self):
        file_list = []      
        for root, dirnames, filenames in os.walk(self.file_path):
            if root.startswith('.'):
                continue

            for filename in filenames:
                is_found  = (filename.lower().endswith(self.extension))
                if not is_found:
                    continue
                full_path = os.path.join(root, filename)
                is_file_readable = os.path.isfile(full_path)
                if not is_file_readable:
                    print(f'UNABLE to read:[{full_path}]')
                                
                self.file_list.append(full_path)

    def loadPOFiles(self):
        line_list = []
        for f in self.file_list:
            rec = POFileRecord(f)
            data = c.load_po(f)
            for index, m in enumerate(data):
                if index == 0:
                    continue
                msgid = m.id
                msgstr = m.string
                rec.addLine(msgid, tran=msgstr)
            entry = {f: rec}
            self.update(entry)

    def save(self):
        writeJSON(self.cach_file, self)

    def load(self):
        data = readJSON(self.cach_file)
        self.clear()
        self.update(data)

class POFileRecord(defaultdict):
    def __init__(self, file_path):
        self.file_name = file_path
    
    def addLines(self, lines):
        for line in lines:
            self.addLine(line)
    
    def addLine(self, line, tran=None):
        tran_txt = (tran if tran else "")
        entry = {line: tran}
        self.update(entry)
    
class TextMap(OrderedDict):
    def __init__(self, text=None, dic=None):
        self.dictionary = dic
        self.text = text
        self.wordsep = re.compile(r'[^\ ]+', re.I)

    def genmap(self):
        self.clear()
        part_list = []
        loc_dic = getLocationList(self.wordsep, self.text)
        loc_key = list(loc_dic.keys())

        max_len = len(loc_dic)
        for step in range(1, max_len):
            for i in range(0, max_len):
                l=[]
                for k in range(i, min(i+step, max_len)):
                    loc = loc_key[k]
                    # print(f'step:{step}; i:{i}; k:{k}, loc:{loc}')
                    l.append(loc_key[k])

                s = []
                for loc in l:
                    word = loc_dic[loc]
                    s.append(word)
                t = " ".join(s)
                print(f's location:{l}, text:{t}')

                s_len = len(s)
                ss = l[0][0]
                ee = l[s_len-1][1]
                k = (len(t), ee)
                v = ((ss, ee), t)
                entry=(k, v)
                is_in = (entry in part_list)
                if not is_in:
                    part_list.append(entry)

        sorted_partlist = list(reversed(sorted(part_list)))
        for e in sorted_partlist:
            k, v = e
            dict_entry = {k: v}
            self.update(dict_entry)

    def blindTranslation(self, text=None, dic=None):
        translated_dic = OrderedDict()
        is_new_text = (self.text != text)

        if is_new_text:
            self.text = text
            self.genmap()

        if dic:
            self.dictionary = dic

        translated_dic = OrderedDict()
        for k, v in self.items():
            loc, orig_sub_text = v
            has_tran = (orig_sub_text in self.dictionary)
            if not has_tran:
                continue
            tran_sub_text = self.dictionary[orig_sub_text]
            ss, ee = loc
            entry = {ee: (ss, ee, tran_sub_text)}
            translated_dic.update(entry)

        sored_translated = list(reversed(sorted(translated_dic.items())))

        tran_msg = str(msg)
        for k, v in sored_translated:
            ss, ee, tran_sub_text = v
            left = tran_msg[:ss]
            right = tran_msg[ee:]
            tran_msg = left + tran_sub_text + right

        return tran_msg


class WCKLCIOrderedDict(defaultdict):
    class Key(str):
        def __init__(self, key):
            str.__init__(key)

        def __hash__(self):
            k = self.lower()
            hash_value = hash(k)
            # _(f'key:{k}, hash_value:{hash_value}')
            return hash_value

        def __eq__(self, other):
            local = self.lower()
            extern = other.lower()
            cond = (local == extern)
            # _(f'__eq__: local:{local} extern:{extern}')
            return cond

    def __init__(self, data=None):
        super(WCKLCIOrderedDict, self).__init__()
        if data is None:
            data = {}
        for key, val in data.items():
            self[key] = val

    def __contains__(self, key):
        key = self.Key(key)
        is_there = super(WCKLCIOrderedDict, self).__contains__(key)
        # _(f'__contains__:{key}, is_there:{is_there}')
        return is_there

    def __setitem__(self, key, value):
        key = self.Key(key)
        super(WCKLCIOrderedDict, self).__setitem__(key, value)


    def __getitem__(self, key):
        key = self.Key(key)
        return super(WCKLCIOrderedDict, self).__getitem__(key)

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]

#import AdvancedHTMLParser as AH
#from sphinx_intl import catalog as c
#from Levenshtein import distance as DS
#from PO.common import Common as cm
#from nltk import sent_tokenize

#p =re.compile(r':[\w]+:\`(?![\s\)\\.(]+)([\w \-]+)(\<([^<]+)\>)*(?<!([\s\:]))\`')
#GA_REF = re.compile(r'(:[\w]+:)*[\`]+(?![\s\)\.\(]+)([^\`\("\'\*\<]+)(((\s\<([^<]+)\>)*)|(\(([^(]+)\))*)(?<!([\s\:]))([\`]+)([\_]+)*')
#GA_REF = re.compile(r'(:\w+:)*[\`]+([^\`\<\>\<\(\)]+)(((\s\<([^\<\>]+)\>)*)|(\(([^(]+)\))*)(?<!([\s\:]))([\`]+)([\_]+)*')
#GA_REF = re.compile(r'[\`]*(:\w+:)*[\`]+(?![\s]+)([^\`\<\>\(\)]+)(((\s\<([^\<\>]+)\>)*)|(\([^\(\)]+\)))[\`]+')

GA_REF = re.compile(r'[\`]*(:\w+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*')
#ARCH_BRAKET = re.compile(r'[\(]+(?![\s\.\,\`]+)([^\(\)]+)[\)]+(?<!([\s\.\,]))')
AST_QUOTE = re.compile(r'[\*]+(?![\s\.\,\`\"]+)([^\*]+)[\*]+(?<!([\s\.\,\`\"]))')
DBL_QUOTE = re.compile(r'[\"]+(?![\s\.\,\`]+)([^\"]+)[\"]+(?<!([\s\.\,]))')
SNG_QUOTE = re.compile(r'[\']+(?![\`\s\.(s|re|ll|t)]+)([^\']+)[\']+')

LINK_WITH_URI=re.compile(r'([^\<\>\(\)]+\w+)[\s]+[\<\(]+([^\<\>\(\)]+)[\>\)]+[\_]*')
MENU_PART = re.compile(r'(?![\s]?[-]{2}[\>]?[\s]+)(?![\s\-])([^\<\>]+)(?<!([\s\-]))') # working but with no empty entries

WORD_ONLY_FIND = re.compile(r'\b[\w\-\_\']+\b')

ENDS_WITH_EXTENSION = re.compile(r'\.([\w]{2,5})$')
MENU_KEYBOARD = re.compile(r':(kbd|menuselection):')
MENU_TYPE = re.compile(r'^([\`]*:menuselection:[\`]+([^\`]+)[\`]+)$')
KEYBOARD_TYPE = re.compile(r'^([\`]*:kbd:[\`]+([^\`]+)[\`]+)$')
KEYBOARD_SEP = re.compile(r'[^\-]+')

WORD_ONLY = re.compile(r'\b([\w\.\/\+\-\_]+)\b')
REF_SEP = ' -- '
NON_WORD_ONLY = re.compile(r'^([\W]+)$')
NON_WORD = re.compile(r'([\W]+)')


DEBUG=True


def pp(object, stream=None, indent=1, width=80, depth=None, *args, compact=False):
    if DEBUG:
        pprint(object, stream=stream, indent=indent, width=width, depth=depth, *args, compact=compact)
        print('-' * 30)

def _(*args, **kwargs):
    if DEBUG:
        print(args, kwargs)
        print('-' * 30)

ignore_list = [
        "(htt)([ps]{1}).*",
        "Poedit",
        "([.*]{1})",  # single anything
        "bpy\.([\w\.\-\_]+)",
        "\:([\w\-\_]+)\:$",
        "\|([\w\-\_]+)\|$",
        "[\W]{1}$",
        "Diffusion",
        "Subversion",
        "LookDev HDRIs",
        "AVI Jpeg",
        "AVX",
        "AVX2",
        "AaBbCc",
        "Acrylic",
        "Albedo",
        "Alembic",
        "Alembic([\s\W|abc]+)*",
        "PAINT_GPENCILEDIT_GPENCILSCULPT_.*",
        "Alpha",
        "Alt",
        "Apple macOS",
        "Arch Linux",
        "Ascii",
        "Ashikhmin-Shirley",
        "B-Spline",
        "BSDF",
        "BSSRDF",
        "BU",
        "BVH",
        "Bezier",
        "Bindcode",
        "Bit",
        "Bits",
        "BkSpace",
        "Bksp",
        "Blackman-Harris",
        "Blender([\ \d\.]+)",
        "Blosc",
        "Boolean",
        "Byte([s]*)",
        "Bytecode",
        "Bézier",
        "CPU",
        "CUDA",
        "Catmull-Clark",
        "Catmull-Rom",
        "Catrom",
        "Chebychev",
        "Christensen-Burley",
        "Cineon",
        "Collada",
        "Ctrl",
        "Cycles",
        "Cycles:",
        "DNxHD",
        "DOF",
        "Debian/Ubuntu",
        "Deflate",
        "Del",
        "Del",
        "Delta",
        "Delta( \w)*",
        "Djv",
        "Doppler",
        "Dpi",
        "Dots/BU",
        "EWA",
        "Epsilon",
        "Esc",
        "FELINE",
        "FFT",
        "FSAA",
        "Flash",
        "FrameCycler",
        "GGX",
        "GGX",
        "GLSL",
        "GPU([s|:])*",
        "GPUs",
        "Gamma([s|:])*",
        "Gizmo( \w+)",
        "Gizmo([s|:])*",
        "H.264",
        "HDR(I)*",
        "HSV/HSL",
        "Hosek \/ Wilkie",
        "HuffYUV",
        "ITU (\d+)",
        "Ins",
        "Ins",
        "JPEG( \d+)*",
        "K1, K2",
        "Kirsch",
        "Laplace",
        "Laplacian",
        "Laptops",
        "Lennard-Jones",
        "LimbNode",
        "Linux",
        "Log",
        "Look Dev",
        "LookDev",
        "MIS",
        "MPEG([\-|\d]+)*(.*)",
        "MPlayer",
        "MS-Windows",
        "Manhattan",
        "MatCap",
        "MatCaps",
        "Matroska",
        "Mega",
        "Microsoft Windows",
        "Minkowski.*",
        "Mitch",
        "Mono",
        "Musgrave",
        "NDOF",
        "NURBS",
        "Nabla",
        "Ndof.*",
        "Null",
        "OBJ",
        "OSkey",
        "Ogawa",
        "Ogg Theora",
        "Ogg",
        "OpenAL",
        "OpenCL",
        "OpenEXR",
        "OpenGL",
        "OpenMP",
        "OpenSubdiv",
        "OpenVDB",
        "Opus",
        "PLY",
        "PYTHONPATH",
        "Pack Bits",
        "Page Down",
        "Page Up",
        "Pause",
        "Pause",
        "Preetham",
        "Prewitt",
        "Python",
        "QuickTime",
        "RGB(\w)*",
        "RK4",
        "RRT",
        "Redhat/Fedora",
        "SDL",
        "SSE2",
        "SSE3",
        "SSE41",
        "STL",
        "SVG",
        "ShaderFX",
        "Shift",
        "Sigma",
        "Sigma",
        "Sin",
        "Sobel",
        "Sobol",
        "Stucci",
        "Studio",
        "Tab",
        "Targa Raw",
        "Targa",
        "Theora",
        "TxtIn",
        "URL",
        "UV",
        "UVs",
        "Uv:",
        "VD16",
        "VRML2",
        "Verlet",
        "Vorbis",
        "Voronoi F([\d]+)?(\-F([\d]+))*",
        "Voronoi",
        "WEBM / VP9",
        "Web3D",
        "WebM",
        "Win",
        "Windows Ink",
        "Wintab",
        "ID",
        "X",
        "X/Y",
        "XYZ",
        "Xvid",
        "Y",
        "YCC",
        "YCC",
        "YCbCr (ITU 601)",
        "YCbCr (ITU 709)",
        "YCbCr (Jpeg)",
        "YCbCr",
        "YCbCr.*",
        "Z",
        "Zip",
        "ac3",
        "alt",
        "bItasc",
        "bit",
        "bits",
        "bpy.context",
        "bpy.data",
        "bpy.ops",
        "byte([s]?)",
        "ctrl",
        "dx",
        "eevee",
        "esc",
        "f(\d+)",
        "fBM",
        "flac",
        "glTF 2.0",
        "iTaSC",
        "kbd",
        "macOS",
        "menuselection",
        "mp(\d+)",
        "Makefile",
        "pagedown",
        "pageup",
        "pgdown",
        "pgup",
        "sin\(x\)\ \/\ x",
        "tab",
        "wav",
        "blender_docs",
        "pip3",
        "pip",
        "FBX",
        "fr",
        "fr/",
        "\|[^\|]+\|",  # |BLENDER_...|
        "#[\w\-\_]+",  # blender-coders <literal>#blender-coders</literal>
        "Babel",
        "Ge2Kwy5EGE0",
        "([\+\-])*(([\d\.]+))",  # simple number
        "TortoiseSVN",
        "Poedit",
        "\:sup\:\`™\`",
        "(([\w]+)\.([^\.]+))+",
        "rst",
        "pot",
        "html",
        "^svn$",
        "^git$",
        "msgstr",
        "\.bashrc",
        "bin",
        "Français",
        "Redhat/Fedora",
        "Arch Linux",
        "\"fr\": \"Fran&ccedil;ais\"",
        "[\-]*\d+(\.[\w]{2,5})", # -0001.jpg
        "\*(\.[\w]{2,5})",  # *.jpg
        "(\.[\w]{2,5})",  # .jpg, .so
        "(mil|mile|millimeter|meter|meters|mi|location[0]|cd|ch|cm|asin|atan|atan2|st|sRGB)",
        "(k[\w]+)",
        "(:math:)\`[^\`]+\`",
        "(([\w]+[\s]*[\+\-\*\/\%][\s]*)*([\w]+[\s]*[=][\s]*[\w]+))", #formular a + b * c = d
        "([\w]+[\s]*[=][\s]*[\w]+)*(([\s]*[\+\-\*\/\%][\s]*[\w]+)+)", #formular a = b * c / d
    ]

FORMULAR = re.compile(r'([\=\+\-\%\*\/])')



def getLocationList(pat, text):
    matching_list = {}
    for m in pat.finditer(text):
        s = m.start()
        e = m.end()
        orig = m.group(0)
        k = (s, e)
        entry = {k: orig}
        matching_list.update(entry)
    return matching_list


class HoldString(list):
    GLOBAL_COUNT: int = 0
    def __init__(self, txt):
        self.name = str(self.getNextCount())
        if txt:
            self.append(txt)

    def getNextCount(self):
        c = HoldString.GLOBAL_COUNT + 1
        HoldString.GLOBAL_COUNT = c
        return c
        #p = FORMULAR.search("1 + 2 - 3")
        #print(p)
        #return 1

    def __repr__(self):
        result = "[" + self.name + "]"
        result += "{"
        result += ", ".join(self)
        result += "}"
        return result

class test(object):
    timenow=None

    def __init__(self):
        self.your_name="Hoang Duy Tran"
        self.your_email="hoangduytran1960@googlemail.com"
        self.your_id="{} <{}>".format(self.your_name, self.your_email)
        self.translation_team="London, UK {}".format(self.your_email)
        self.language_code="vi"
        self.re_language_code="\"Language: \\\\n\"\n".format(self.language_code)
        self.is_file_name_printed = False
        self.count=0
        self.dic = {
            #"^Standard image input.$":"Đầu vào tiêu chuẩn của hình ảnh.",
            #"^Standard image output.$":"Đầu ra tiêu chuẩn của hình ảnh.",
            "FIRST AUTHOR.*SS>":self.your_id,
            "Last-Translator.*>":"Last-Translator: {}".format(self.your_id),
            #"PO-Revision-Date.*[[:digit:]]\{4\}":self.timeNow(),
            #"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE":self.timeNow(),
            "Language-Team:.*>":"Language-Team: {}".format(self.translation_team),
            "\"MIME-Version":"{}\"MIME-Version".format(self.re_language_code)
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
            #"":"",
        }

        self.YOUR_NAME="Hoang Duy Tran"
        self.YOUR_EMAIL="hoangduytran1960@googlemail.com"
        self.YOUR_ID="{} <{}>".format(self.YOUR_NAME, self.YOUR_EMAIL)
        self.YOUR_TRANSLATION_TEAM="London, UK <{}>".format(self.YOUR_EMAIL)
        self.YOUR_LANGUAGE_CODE="vi"

        #the replace string for revision date, which include the time_now value
        self.po_revision_date_value="PO-Revision-Date: {}".format(self.getTimeNow())

        #the list of pattern to find and the value strings to be replaced
        #"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n
        self.pattern_list= {
            r"FIRST AUTHOR.*SS\>":self.YOUR_ID,
            r"Last-Translator.*\>":"Last-Translator: {}".format(self.YOUR_ID),
            r"PO-Revision-Date.*[[:digit:]]\{4\}":self.po_revision_date_value,
            r"PO-Revision-Date: YEAR.*ZONE":self.po_revision_date_value,
            r"Language-Team:.*\>":"Language-Team: {}".format(self.YOUR_TRANSLATION_TEAM)
        }

        #This is for the language line. This line is required by POEdit, if you're using it for editing PO files.
        #Inserting this line before the MIME-Version.
        self.re_language_code=r'Language:.*{}'.format(self.YOUR_LANGUAGE_CODE)
        self.language_code=r'"Language: {}\\n"\n'.format(self.YOUR_LANGUAGE_CODE)
        self.pattern_insert={
            r"\"MIME-Version":"{}\"MIME-Version".format(self.language_code)
        }

        self.RE_COMMENTED_LINE=r'^#~.*$'


    def getTimeNow(self):
        local_time=timezone('Europe/London')
        fmt='%Y-%m-%d %H:%M%z'
        loc_dt=local_time.localize(datetime.datetime.now())
        formatted_dt=loc_dt.strftime(fmt)
        return formatted_dt

    def isFormular(self, msg):
        result = FORMULAR.split(msg)
        print(msg, result)
        return result

    def isIgnoredWord(self, text_line : str):
        if (text_line is None) or (len(text_line) == 0):
            return True

        try:
            for x in ignore_list:
                m = re.compile(r'^{}$'.format(x), flags=re.I)
                is_found = (m.search(text_line) is not None)
                if is_found:
                    _("[{}] matched [{}]".format(text_line, x))
                    return True
        except Exception as e:
            _(e)
            _("isIgnoredWord ERROR:", text_line)
        return False

    def timeNow(self):
        if (test.timenow == None):
            local_time=timezone('Europe/London')
            fmt='%Y-%m-%d %H:%M%z'
            loc_dt=local_time.localize(datetime.datetime.now())
            formatted_dt=loc_dt.strftime(fmt)
            test.timenow = formatted_dt
        return test.timenow

    def test01(self):
        index = 0
        for key, value in self.dic.items():
            is_first = (index == 0)
            if (is_first):
                print("Dealing with first:{} => {}".format(key, value))
            else:
                print("Dealing with:{} => {}".format(key, value))
            index += 1

    def readText(self, file_path):
        try:
            with open(file_path) as in_file:
                data = in_file.read()
                in_file.close()
            return data
        except Exception as e:
            print("Exception readText:{}".format(file_path))
            raise e

    def getByKeyword(self, keyword, text):
        #<title>Import</title>
        result_list=[]
        pattern = r"<{}[^>]*>([^\.\!<]+)</{}>".format(keyword, keyword)
        titles = re.compile(pattern)
        m  = titles.findall(text)

        pattern = r"<{}[^>]*>([^\.\!<]+)*<".format(keyword)
        titles = re.compile(pattern)
        n  = titles.findall(text)

        is_found_m = (m != None)
        is_found_n = (n != None)

        if (is_found_m):
            result_list= result_list + m

        if (is_found_n):
            result_list= result_list + n

        is_found = (len(result_list) > 0)
        if (is_found):
            result_list = sorted(result_list)
            #print("sorted:{}".format(result_list))
            unique_set = sorted(set(result_list))
            #print("set:{}".format(unique_set))
            result_list = sorted(list(unique_set))
            #print("back to list:{}".format(result_list))
            return result_list
        else:
            return None

    def test_0001(self):
        file_name = "/home/htran/example_rst_content.txt"
        data = self.readText(file_name)

        kw = ['title', 'field_name', 'term', 'strong', 'rubric']
        l = []
        for k in kw:
            result = self.getByKeyword(k, data)
            if (result != None):
                l.extend(result)
        l = sorted(l)
        print(l)

    def test_0002(self):
        t1="-s"
        t2="``{}``".format(t1)
        t3="--"
        t4="``{}``".format(t3)
        t5="-12345.67"
        t6="``{}``".format(t5)
        t7="-a and -b"
        t8="``{}``".format(t7)


        pf=re.compile(r"(?P<rst_box>[\`]+)(.*?)(?P=rst_box)$")
        po=re.compile(r"(^[-]+)([a-zA-Z]{0,1})$")

        pp = re.compile(r"(^[-]+)([a-zA-Z]{0,1})$")
        #test_item=t4
        #ml = pf.findall(test_item)
        #print("ml:{}".format(ml))
        #if (len(ml) > 0):
            #found_item=ml[0][1]
            #print("ml[0][1]:{}".format(ml[0][1]))
            #mo=po.search(found_item)
            #if (mo != None):
                #print("mo[0]:{}".format(mo[0]))
        #else:
            #print("test_item:{}".format(test_item))
            #mo=po.search(test_item)
            #if (mo != None):
                #print("mo[0]:{}".format(mo[0]))

    def test_0003(self):
        t = "(:menuselection:`Armature --> Bone Roll --> Recalculate`)"
        p = re.compile(r":menuselection:`(.*)`")
        m = p.findall(t)
        tt = m[0]
        print("m:{}".format(m[0]))
        ll = tt.split("-->")
        print("ll:{}".format(ll))
        for w in ll:
            w = w.strip()
            wrp = "({})".format(w)
            if (t.find(wrp) < 0):
                t = (t.replace(w, wrp))
        print("new t:{}".format(t))

    def test_0004(self):
        p= re.compile(r"(?<=:doc:`\/)(.*)`$")
        t1=":doc:`/sculpt_paint/index/what/is/this`"
        t2=":doc:`Glossary </glossary/index>`"
        m = p.search(t2)
        print(m)

    def test_0005(self):
        t_list = ["Đổi Tỷ Lệ Mép Nhòe :kbd:`Alt-S`",
        "Móc :kbd:`K`",
        "Hiển Thị Tay Cầm :kbd:`Ctrl-H`",
        "Hiển Thị/Ẩn Giấu Cảnh Kết Xuất :kbd:`F11`",
        "Sức Mạnh/Cường Độ :kbd:`Shift-F`",
        "Bật/Tắt Khả Năng Biên Soạn của Kênh :kbd:`Tab`",
        "Lật Đảo Tự Do/Thẳng Hàng :kbd:`V T`",
        "Tùy Chọn của Người Dùng :kbd:`Ctrl-Alt-U`; :kbd:`Ctrl-Alt-A`",
        "Hiển thị tất cả các Trình tự :kbd:`Home`",
        "Thu-Phóng :kbd:`Ctrl-MMB`, :kbd:`Wheel`",
        "Hiển Thị Toàn Bộ  -- Show All :kbd:`Alt-H`",
        ":kbd:`LMB`",
        ":kbd:`MMB`",
        ":kbd:`Numpad0`",
        ":kbd:`Wheel`",
        ":kbd:`NumpadPlus`",
        ":kbd:`OS-Key`",
        ":kbd:`D-LMB`",
        "Cường Độ -- Strength :kbd:`Ctrl-F`/:kbd:`Shift-Bánh Xe (Wheel)`",
        ":kbd:`Shift`, :kbd:`Ctrl`, :kbd:`Alt`",
        ":kbd:`Bàn Số 0` (`Numpad0`) tới :kbd:`Bàn Số 9` (`Numpad9`), :kbd:`Bàn Số +` (`NumpadPlus`)",
        ":kbd:`Bánh Xe`",
        "Phím Chức Năng (F-Keys) (:kbd:`F5` - :kbd:`F10`)",
        "Phím Hệ Điều Hành (:kbd:`OS-Key`) (còn được biết với những cái tên khác như *phím Cửa Sổ* (``Windows-Key``), phím Lệnh (``Cmd``) hoặc phím Quản Lý (``Super``))",
        ":kbd:`Ctrl-Alt-T`"
        "Use Grab/Move :kbd:`G`, Rotate :kbd:`R`, Scale :kbd:`S`, to transform the cube."
        ]

        p= re.compile(r":kbd:`.*`")
        #p= re.compile(r"(:kbd:`)(?P<word>[\w\d]+)(\-(?P=word))*(`)")
        p1=re.compile(r":kbd:`(?P<key>[\w\d]+)|(?P<modifier>(Enter|Ctrl|Alt|Shift|Home|Insert|PageUp|PageDown|Delete)+[-+](?P=key))*`")
        pex_vn_part=re.compile(r"(NCT)|(NCP)|(NCG)|(LMB)|(MMB)|(RMB)|(Numpad)|(Wheel)|(OS)|(Win)")
        pdel=re.compile(r"(\.)|(,)|(;)|(and)|(or)|(--)")


        is_remove_pattern = False
        for text_line in t_list:
            found_string = ""
            has_trans=(text_line.find(" -- ") > 1)
            if (has_trans):
                text_line = text_line.split(" -- ")[0]
            m = p.search(text_line)
            if (m != None):
                is_remove_pattern = True
                print("Any Pattern:[{}]".format(m.group(0)))
                found_string=m.group(0)
                n=pex_vn_part.search(found_string)
                if (n != None):
                    print("Exclude Pattern:[{}]".format(n.group(0)))
                    is_remove_pattern = False

            print("Text line before remove:[{}]".format(text_line))
            if (is_remove_pattern):
                text_line = text_line.replace(found_string, "").strip()
                print("Text line after removed:[{}]".format(text_line))
            #m1 = p1.search(found_string)
            #print(m1.group(0))

    def fuzzyTermMatch(self, s1, s2):
        match_pat=re.compile(r".*({}).*".format(s1))
        match_m = match_pat.search(s2)
        is_found = (match_m != None)
        if (is_found):
            return match_m.group(0)
        else:
            return None

    def fuzzyWordMatch(self, s1, s2):
        pat=re.compile(r"\W*(\w+)\W*")
        s1_word_list=pat.findall(s1)
        s2_word_list=pat.findall(s2)
        #for each word in s1_word_list, find occurence in S2 and distance between matches in s2, the closer have higher match rate
        s2_string = " ".join(s2_word_list)
        s2_word_list_len = len(s2_string)
        distance_list=[]
        for s1_w in s1_word_list:
            try:
                index = s2_string.index(s1_w)
            except ValueError as e:
                index = s2_word_list_len
            percentage = (index / s2_word_list_len) * 100
            distance_list.append(percentage)

        fuzzyDistance = 100
        for dist in distance_list:
            fuzzyDistance -= dist
        fuzzyDistance = max(0.0, fuzzyDistance)
        return fuzzyDistance
        #print("s1_word_list:{}".format(s1_word_list))
        #print("s2_word_list:{}".format(s2_word_list))
        #print("distance_list:{}".format(distance_list))
        #print("fuzzyDistance:{}".format(fuzzyDistance))
        #print("=" * 50)

    def fuzzySearch(self, search_text_line, possible_list):
        match_list=[]
        for index, entry in enumerate(possible_list):
            candicate, ratio = entry
            fuzzy_dist = self.fuzzyWordMatch(search_text_line, candicate)
            match_list.append((fuzzy_dist, index))
        sorted_list = sorted(match_list, reverse=True)
        print("sorted_list:{}".format(sorted_list))
        return match_list

    def test_0006(self):
        data_list=[('Examples',
                    44,':ref:`Shape Keys <animation-shape_keys-index>`',
                    39,':ref:`Armatures <armatures-index>`',
                    26,':ref:`Constraints <constraints-index>`',
                    23,':ref:`Drivers <animation-drivers-index>`',
                    18,':ref:`Object Modifiers <modifiers-index>`',
                    17,'To control the kinds of motions that make sense and add functionality to the rig.',
                    16,'To support different target shapes *(such as facial expressions)* to be controlled.',
                    16,'Rigging often involves using one or more of the following features:',
                    11,'This allows mesh objects to have flexible joints and is often used for skeletal animation.',
                    10,'Mesh deformation can be quite involved, there are multiple modifiers that help control this.',
                    10,'So your rig can control many different values at once, as well as making some properties automatically update based on changes elsewhere.',
                    10,'An armature is often used with a modifier to deform a mesh for character animation.',
                    9,'Rigging can be as advanced as your project requires, rigs are effectively defining own user interface for the animator to use, without having to be concerned the underlying mechanisms.',
                    7,'Rigging is a general term used for adding controls to objects, typically for the purpose of animation.',
                    5,'A camera rig can be used instead of animating the camera object directly to simulate real-world camera rigs *(with a boom arm, mounted on a rotating pedestal for example, effects such as camera jitter can be added too).*',
                    5,"The content of this chapter is simply a reference to how rigging is accomplished in Blender. It should be paired with additional resources such as Nathan Vegdahl's excellent (and free!) introduction to the fundamental concepts of character rigging, `Humane Rigging <https://www.youtube.com/playlist?list=PL3wFcRXImVPOQpi-wi7uriXBkykXVUntv>`__.",
                    5)]
        search_term="Shape Keys"

        self.fuzzySearch(search_term, data_list)

    def binaryWord(self, search_word_list, data_word_list):
        binary_data_list=[]
        for index, data_word in enumerate(data_word_list):
            if (data_word in search_word_list):
                binary_data_list.append("1")
            else:
                binary_data_list.append("0")
        return "".join(binary_data_list)

    # def binaryDistance(self, search_word_binary_present):
    #     distance=0
    #     line_len = len(binary_present)
    #     letter_weight=(100.0/line_len)
    #
    #     is_on=False
    #     distance=0
    #     for index, char in enumerat(binary_present):
    #         digit = (int(char))
    #         #is_on = (True if (is_on))
    #
    # def calculateDistance(search_word_list, candicate_list):
    #     sep_pat = re.compile(r"(\w+)")
    #     search_word_binary_present = self.binaryWord(search_word_list, search_word_list)
    #     for candicate_line in enumerate(candicate_list):
    #         candicate_line_word_list = sep_pat.findall(candicate_line)
    #         binary_present = self.binaryWord(search_word_list, candicate_line_word_list)


    def test_0010(self):
        s=":menuselection:`Collapse`"
        data_list=[
            ":menuselection:`Mesh --> Delete`", \
            ":kbd:`Alt-M`, :menuselection:`Collapse`", \
            ":kbd:`Alt-M`, :menuselection:`Collapse` and this is another text",
        ]

        data_list=[":kbd:`Alt-M`, :menuselection:`Collapse`", \
                    ":menuselection:`Mesh --> Delete`", \
                    "Edge Collapse", \
                    "Edge ring collapsed.", \
                    ":kbd:`X`, :kbd:`Delete`", \
                    ":kbd:`Ctrl-X`", \
                    "Selected edge loop.", \
                    "Reference", \
                    "Delete", \
                    "Limited Dissolve", \
                    "Selected edge ring.", \
                    ":ref:`mesh-unsubdivide`.", \
                    "Vertices", \
                    "Only Edges & Faces", \
                    "Only Faces", \
                    "Dissolve", \
                    "Tear Boundaries", \
                    "Dissolve Faces", \
                    "Original mesh.", \
                    "All Boundaries", \
                    "Edge Loop", \
                    "Deleting & Dissolving", \
                    "Edit Mode", \
                    "Panel", \
                    "Menu", \
                    "Dissolve Vertices", \
                    "Examples", \
                    "Dissolve Edges", \
                    "Max Angle", \
                    "Delimit", \
                    "Edge loop deleted.", \
                    "Mode", \
                    "Hotkey", \
                    "Edges", \
                    "Faces", \
                    "Face Split", \
                    "Dissolve (Context-Sensitive)", \
                    "Example", \
                    ":ref:`mesh-faces-tristoquads`.", \
                    "Result of Limited Dissolve.", \
                    ":menuselection:`Mesh --> Delete --> Edge Collapse`", \
                    ":menuselection:`Mesh --> Delete --> Edge Loop`"
        ]

        # #sep_pat = re.compile(r"(\w+)")
        # sep_pat = re.compile(r"([^\W]+)")
        #
        # s_word_list=sep_pat.findall(s)
        # print("s_word_list:{}".format(s_word_list))
        # has_words = (len(s_word_list) > 0)
        # if (not has_words): return
        #
        # search_pat = []
        # for word in s_word_list:
        #     search_pat.append("{}.*".format(word))
        # search_pat = "".join(search_pat)
        #
        # matched_lines = []
        # p = re.compile(search_pat)
        # for line in data_list:
        #     m = p.search(line)
        #     if (m != None): matched_lines.append(line)
        #
        # print("matched_lines:{}".format(matched_lines))
        #
        # for line in matched_lines:
        #     #d = fz.ratio(s, line)
        #     d = distance(s, line)
        #     print("d:{}; line:{}".format(d, line))

        #binary_data_list={}
        #for line in data_list:
            #data_word_list = sep_pat.findall(line)
            #bin_line=self.binaryWord(s_word_list, data_word_list)
            #k=bin_line
            #v=line
            #binary_data_list.update({k:v})

        #has_matches_data_list=[]
        #for k, v in binary_data_list.items():
            #has_match=("1" in k)
            #if (has_match):
                #has_matches_data_list.append({k:v})
                #print("k:{}, v:{}".format(k, v))



    def test_0011(self):
        transtable = {
                "A":"Một",
                "About":"Về",
                "Always":"Luôn Luôn",
                "And":"Và",
                "Anti-Aliasing":"Chống Răng Cưa",
                "Approximate":"Ước Lượng",
                "Array":"Mảng",
                "Aspect":"Tương Quan",
                "Assigning":"Chỉ Định",
                "Assignment":"Sự Chỉ Định",
                "At":"Tại",
                "Attract":"Hấp Dẫn",
                "Available":"Có Thể Sử Dụng",
                "Axis/Angle":"Trục/Góc",
                "Backbone":"Xương Lưng",
                "Be":"Làm",
                "Bent":"Bị Bẻ Cong",
                "Best":"Tốt Nhất",
                "Blackbody":"Vật Đen",
                "Blender'S":"Của Blender",
                "Body":"Thân Thể",
                "Brick":"Gạch",
                "Button":"Nút",
                "Bézier":"Bézier",
                "Caches":"Bộ Đệm Nhớ",
                "Calculate":"Tính Toán",
                "Calculating":"Tính Toán",
                "Calculation":"Tính Toán",
                "Cascade":"",
                "Cascaded":"",
                "Chain":"Dây Chuyền",
                "Changing":"Thay Đổi",
                "Check":"Kiểm Tra",
                "Checkbox":"Hộp Kiểm",
                "Checkboxes":"Hộp Kiểm",
                "Clearing":"Làm Sạch/Dọn Dẹp",
                "Click":"Bấm",
                "Close":"Đóng/Kín/Gần",
                "Clump":"Khóm",
                "Clumping":"Khóm Lại",
                "Comparison":"So Sánh",
                "Compilation":"Biên Dịch",
                "Computer":"Máy Tính",
                "Concave":"Lõm",
                "Config":"Cấu Hình",
                "Continuous":"Tiếp Tục",
                "Cpu":"Bộ Xử Lý",
                "Datafile":"Tập Tin Dữ Liệu",
                "Datafiles":"Tập Tin Dữ Liệu",
                "Decrease":"Giảm",
                "Delete":"Xóa",
                "Deleting":"Xóa",
                "Depend":"Tùy Thuộc",
                "Deselection":"Hủy Chọn",
                "Different":" Khác",
                "Dimensional":"Kích Thước",
                "Directory":"Thư Mục",
                "Do":"Làm",
                "Does":"Làm",
                "Done":"Xong",
                "Elliptical":"Hình Elip",
                "Equal":"Bằng",
                "Error":"Lỗi",
                "Every":"Mỗi",
                "Example":"Ví Dụ",
                "Fail":"Thất Bại",
                "Failed":"Thất Bại",
                "Firefly":"Đom Đóm",
                "For":"Cho",
                "Glitch":"Hỏng Hóc",
                "Glitches":"Hỏng Hóc",
                "Group":"Nhóm",
                "Horse":"Con Ngựa",
                "In":"Trong",
                "Invalid":"Bất Hợp Lệ",
                "Is":"Là",
                "It":"Nó",
                "Kernel":"Ruột",
                "Locking":"Khóa",
                "Map":"Ánh Xạ",
                "Match":"Khớp",
                "Match":"Khớp",
                "Memory":"Bộ Nhớ",
                "Memory":"Bộ Nhớ",
                "Might":"Có Thể",
                "N-Gon":"Đa Giác",
                "Need":"Cần Thiết",
                "Not":"Không",
                "Numpad":"Bảng Số",
                "Numpadperiod":"Dấu Chấm Trên Bảng Số",
                "Of":"Của",
                "On":"Trên",
                "Only":"Duy",
                "Only":"Duy",
                "Order":"Trật Tự",
                "Panel":"Bảng",
                "Please":"Làm Ơn",
                "Point":"Điểm",
                "Preferable":"Ưa Hơn",
                "Problem":"Vấn Đề/Sự Cố",
                "Processing":"Xử Lý",
                "Profiles":"Mặt Cắt",
                "Progress":"Tiến Trình",
                "Projective":"Dự Phóng",
                "Provide":"Cung Cấp",
                "Sample":"Mẫu Vật",
                "Sampling":"Lấy Mẫu Vật",
                "Set":"Đặt",
                "Shader":"Bộ Tô Bóng",
                "Simulation":"Mô Phỏng",
                "So":"Hầu Cho",
                "Spring":"Lò Xo",
                "Start":"Bắt Đầu",
                "State":"Trạng Thái",
                "Structure":"Cấu Trúc",
                "Take":"Lấy",
                "The":"Cái",
                "Time":"Thời Gian",
                "Type":"Thể Loại",
                "Unknown":"Chưa Biết",
                "Use":"Sử Dụng",
                "Used":"Sử Dụng",
                "Using":"Dùng",
                "Variation":"Biến Thể",
                "When":"Khi",
                "While":"Trong Khi",
                "With":"Với",
                "Workaround":"Phương Pháp Khắc Phục",
                "X/Y":"X/Y",
                "Zero":"Zê-Rô",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                "":"",
                }

        # p = re.compile(r'(?<!\\")"(.*?)"')
        # m = p.findall(long_t)
        # print(m)
        # p = re.compile(r'(<[^<>]+>)', flags=re.MULTILINE)
        # word_list = cm.findInvertSimple(p, t)
        # for w in word_list:
        #     print(w)
        # t = "``:term:`Manifold``` -- Links to an entry in the :doc:`Glossary </glossary/index>`."
        # p = re.compile(r'[\`]*(:[^\:]+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*')
        # print(t)
        # m = p.findall(t)
        # print(m)
        t = "The *Transform Orientations* panel, found in the header of the 3D Viewport, " \
            "can be used to manage transform orientations: selecting the active orientation, " \
            "adding (\"+\" icon), deleting (\"X\" icon) and rename custom orientations."

        t = "When you have completed arranging and stitching, you will end up with a consolidated " \
            "UV map, like that shown to the right, arranged such that a single image will cover, " \
            "or paint, all of the mesh that needs detailed painting. All the detailed instructions on " \
            "how to do this are contained in the next section. The point of this paragraph is to show " \
            "you the ultimate goal. Note that the mesh shown is Mirrored along the Z axis, so the " \
            "right side of the face is virtual; it is an exact copy of the right, so only one set of " \
            "UVs actually exist. (If more realism is desired, the Mirror Modifier would be applied, " \
            "resulting in a physical mirror and a complete head. You could then make both side physically " \
            "different by editing one side and not the other. Unwrapping would produce a full set of " \
            "UVs (for each side) and painting could thus be different for each side of the face, " \
            "which is more realistic). and (this (is the second one) but not here) and (another one)"


        t = ''' 
        C:\\blender_docs
        with space in front build/html/contents_quicky.html
        '''

        # word_list = getTextWithinBracket('(', ')', t, is_include_bracket=False, replace_internal_start_bracket='[', replace_internal_end_bracket=']')
        # print(word_list)

        # print(t)
        # # p = re.compile(r'(?P<word>[^\\\/]+)([\\\/]{1,2}(?P=word))*?(?P<ext>\.[\w]{2,5})')
        # p = re.compile(r'(?:[^\\\/\:\s]+?[/\\])*\w+\.\w{2,5}')
        # # m = p.search(t)
        # m = p.findall(long_t)
        # print(m)

        # p = re.compile(r'(?!\).*?\()\(.*?\)')
        # p = re.compile(r'(?:(?!\).*?\().)*')
        # print(t)
        # m = p.findall(t)
        # print(m)
        # from collections import deque
        # word_dict={}
        # m_list = re.finditer(r'\(|\)', t)
        # for m in m_list:
        #     s = m.start()
        #     e = m.end()
        #     w = m.group(0)
        #     entry = {(s, e): w}
        #     word_dict.update(entry)
        #
        # print(word_dict)
        #
        # sentence_list = []
        # q = deque()
        # for loc, bracket in word_dict.items():
        #     s, e = loc
        #     is_open = (bracket == '(')
        #     is_close = (bracket == ')')
        #     if is_open:
        #         q.append(s)
        #     if is_close:
        #         if not q:
        #             raise Exception(f'Invalid close bracket at {s, e}')
        #         last_s = q.pop()
        #         ss = last_s + 1
        #         ee = e - 1
        #         txt_line = t[ss:ee]
        #         sentence_list.append(txt_line)
        # print(sentence_list)

        # print(word_list)

        # t_dict = {0: [{(0, 3): '"D"'}, {(1, 2): 'D'}], 15: [{(15, 21): '"dash"'}, {(16, 20): 'dash'}], 23: [{(23, 26): '"G"'}, {(24, 25): 'G'}], 38: [{(38, 43): '"gap"'}, {(39, 42): 'gap'}]}
        # t_dict = {11: [{(11, 56): ':menuselection:`View --> Show Curve Extremes`'}, {(11, 26): ':menuselection:'}, {(27, 55): 'View --> Show Curve Extremes'}]}
        t_dict = {10: [((10, 16), '*Path*'), ((11, 15), 'Path')]}
        t_dict = {11: [((11, 56), ':menuselection:`View --> Show Curve Extremes`'), ((11, 26), ':menuselection:'), ((27, 55), 'View --> Show Curve Extremes')]}
        for k, v in t_dict.items():
            v_len = len(v)
            if v_len > 2:
                orig, sub_type, sub_content = v
            else:
                sub_type = None
                orig, sub_content = v

            (o_ss, o_ee), o_txt = orig
            print(f'{o_ss}, {o_ee} {o_txt}')
            print(f'orig:{orig} sub_type:{sub_type} sub_content:{sub_content}')
            # for index, item in enumerate(v):
            #     # print(f'index:{index} item:{item}')
            #     if index == 0:
            #         print(f'orig: {item}')
            #     if index == 1:
            #         print(f'sub/type: {item}')
            #     if index == 2:
            #         print(f'sub text: {item}')

            # v_len = len(v)
            # orig = v[0]
            # sub = v[1]
            #
            # ok = list(orig.keys())[0]

            # ov = list(orig.values())[0]
            #
            # sk = list(sub.keys())[0]
            # sv = list(sub.values())[0]
            #
            # print(f'O: {ok} {ov}')
            # print(f'S: {sk} {sv}')

    def test_capt_0001(self):
        string = 'abababacb'
        p = re.compile(r'(?:b)(a)(?:b)', flags=re.MULTILINE)
        m = p.search(string)
        m = p.findall(string)

        p = re.compile(r'(?<=b)(a)(?=b)')
        m = p.search(string)
        print(m)
        m = p.findall(string)
        print(m)

        string = 'I love cherries, apples, strawberries.'
        p = re.compile(r'(\w+)(?:\.|,)')
        m = p.search(string)
        print(m)
        m = p.findall(string)
        print(m)

        password1 = 'AZN#3232!abbb32..'
        password2 = 'AZN#3232abbb3232'
        # make sure that ALL lower
        # upper number symbols are matched
        # first before capture using \S+
        # Non-capturing ?=.* will start from the position where cursor was and check ahead, without capturing.

        pass_pattern = re.compile('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!?.])\S+')

        m = pass_pattern.search(password1)
        print(m)
        m = pass_pattern.findall(password1)
        print(m)

        m = pass_pattern.search(password2)
        print(m)
        m = pass_pattern.findall(password2)
        print(m)

    def binSearch(self, sorted_list , item_to_find):
        #print("sorted_list: {}, len:{}".format(sorted_list, len(sorted_list)))
        lo  = 0
        hi  = len(sorted_list)
        mid = -1
        while (lo < hi):
            mid  = (lo + hi) // 2
            item_on_sorted_list, trans = sorted_list[mid]
            #print("mid:{}, item_on_sorted_list: {}".format(mid, item_on_sorted_list))
            if (item_on_sorted_list == item_to_find):
                return trans
            elif (item_on_sorted_list < item_to_find):
                lo = mid + 1  # range in the higher part
            else:
                hi = mid  # range in the lower part
        return None

    def test_0012(self):
        s=":kbd:`NCT` one :ref:`irc-chat <irc-channels>` two  :doc:`History </interface/undo_redo>` three ``#blenderwiki`` four '`Mailing list <https://lists.blender.org/mailman/listinfo/bf-docboard>`__ five :abbr:`SSAO (Screen Space Ambient Occlusion)` six :menuselection:`File --> Recover Last Session` end"

        s1 = "%s: confirm, %s: cancel, %s: gravity (%s), %s|%s|%s|%s: move around, %s: fast, %s: slow, %s|%s: up and down, %s: teleport, %s: jump, %s: increase speed, %s: decrease speed. And than this!"

        s = "Updating: fk:[templates Not all of the folders have to be present."
        print("-" * 50)
        print(s)
        print("-" * 60)
        s2 = re.sub(r"((:kbd:)|(:ref:)|(:doc:)|(:abbr:)|(:menuselection:)|(:class:))", "", s, flags=re.I)
        print("removed kbd|ref|doc..\n", s2)

        s1 = re.sub(r"(<[^>]*>)", "", s2)
        print("removed <link>:\n", s1)

        s2 = re.sub(r"(%[\d]{0,2}[sfdi]+)", "", s1, flags=re.I)
        print("removed printf flags:\n", s2)

        s1 = re.sub(r"(\(\))|([_]+)", "", s2, flags=re.I)
        print("removed brackets:\n", s1)


        ##p=re.compile(r"([\,\.])|(%[isdf])|(:(kbd)|(ref)|(doc)|(abbr)|(menuselection):)|(<[^>]*>)")
        ##p=re.compile(r"([\,\.])|(%[isdf])|(:(kbd)|(ref)|(doc)|(abbr)|(menuselection):)")
        #ss = re.sub(r"([\,\.]+)", "", s)
        #print(ss)
        #ss = re.sub(r"(:(kbd)|(ref)|(doc)|(abbr)|(menuselection):)", "", ss)
        #print(ss)
        #ss = re.sub(r"(:)|(_)|(`)|([-]+>)|(#[\w]+)", "", ss)
        #print(ss)
        #ss = re.sub(r"(<[^>]*>)", "", ss)
        #print(ss)

        #s2 = "Updating: fk:[:class:`blender_api:bpy.types.KeyMapItems.new`"


        #ss = re.sub(r"(%[\d]{0,2}[sfdi]+)", "", ss, flags=re.I)
        #tt = re.sub(r"[\,\.\:\;]", "", s1)
        #ss = re.sub(r"(<[^>]*>)|(\`[^\`]*\`)", "", s1)
        #ss = re.findall(r"([^\s]+)", tt)
        #ss = re.findall(r"([\(\)\w -']+)", s1)
        word_list = re.findall(r"[^\W]+", s1)
        print("-" * 5)
        pp(s1)
        print("-" * 5)
        pp(word_list)
        print("-" * 5)
        #print(s2, " ==> ", ss)

    def test_0013(self):
        base_dir=os.path.dirname(os.path.realpath(__file__))
        print(base_dir)

    def test_0014(self):
        text = "<field_list classes=\"last\"><field><field_name>Chế Độ -- Mode</field_name><field_body><paragraph>Chế Độ Vật Thể -- Object Mode</paragraph></field_body></field><field><field_name>Bảng -- Panel</field_name><field_body><paragraph><inline classes=\"menuselection\" rawtext=\":menuselection:`Giá Công Cụ (Tool Shelf) --> Hoạt Họa (Animation) --> Hoạt Họa (Animation) --> Khung Khóa: Chèn Thêm (Keyframes: Insert)`\">Giá Công Cụ (Tool Shelf) ‣ Hoạt Họa (Animation) ‣ Hoạt Họa (Animation) ‣ Khung Khóa: Chèn Thêm (Keyframes: Insert)</inline></paragraph></field_body></field><field><field_name>Trình Đơn -- Menu</field_name><field_body><paragraph><inline classes=\"menuselection\" rawtext=\":menuselection:`Vật Thể (Object) --> Hoạt Họa (Animation) --> Chèn Khung Khóa (Insert Keyframe...)`\">Vật Thể (Object) ‣ Hoạt Họa (Animation) ‣ Chèn Khung Khóa (Insert Keyframe...)</inline></paragraph></field_body></field><field><field_name>Phím Tắt -- Hotkey</field_name><field_body><paragraph><literal classes=\"kbd\">I</literal></paragraph></field_body></field></field_list>"

        text = "<field_body><paragraph><inline classes=\"menuselection\" rawtext=\":menuselection:`Tư Thế (Pose) --> Sao Chép Tư Thế Hiện Tại (Copy Current Pose)`\">Tư Thế (Pose) ‣ Sao Chép Tư Thế Hiện Tại (Copy Current Pose)</inline>, <inline classes=\"menuselection\" rawtext=\":menuselection:`Tư Thế (Pose) --> Dán Tư Thế (Paste Pose)`\">Tư Thế (Pose) ‣ Dán Tư Thế (Paste Pose)</inline>, <inline classes=\"menuselection\" rawtext=\":menuselection:`Tư Thế (Pose) --> Dán Tư Thế Đảo-Lật theo Trục X (Paste X-Flipped Pose)`\">Tư Thế (Pose) ‣ Dán Tư Thế Đảo-Lật theo Trục X (Paste X-Flipped Pose)</inline></paragraph></field_body>"

        #/home/htran/blender_documentations/blender_docs/build/rstdoc/rigging/armatures/posing/editing.html
        #/home/htran/blender_documentations/blender_docs/manual/rigging/armatures/posing/editing.rst
        #msgid ":menuselection:`Pose --> Copy Current Pose`, :menuselection:`Pose --> Paste Pose`, :menuselection:`Pose --> Paste X-Flipped Pose`"
        #msgstr ":menuselection:`Tư Thế (Pose) --> Sao Chép Tư Thế Hiện Tại (Copy Current Pose)`, :menuselection:`Tư Thế (Pose) --> Dán Tư Thế (Paste Pose)`, :menuselection:`Tư Thế (Pose) --> Dán Tư Thế Đảo-Lật theo Trục X (Paste X-Flipped Pose)`"

        #Copy/Paste Pose
        #===============

        #.. admonition:: Reference
        #:class: refbox

        #:Mode:      Pose Mode
        #:Header:    Copy/Paste (|copy-paste|)
        #:Panel:     :menuselection:`Tool Shelf --> Tool --> Pose Tools --> Pose: Copy, Paste`
        #:Menu:      :menuselection:`Pose --> Copy Current Pose`,
        #:menuselection:`Pose --> Paste Pose`,
        #:menuselection:`Pose --> Paste X-Flipped Pose`

        #Blender allows you to copy and paste a pose, either through the *Pose* menu, or
        #directly using the three copy/paste buttons found at the right part of the 3D View's header:

        # soup = BS(text, "html.parser")
        # data_output = soup.prettify()
        # print(data_output)
        #
        # para = soup.find_all('paragraph')
        # men = soup.find_all('inline', {'classes' : 'menuselection'})
        # kbd = soup.find_all('literal', {'classes' : 'kbd'})
        # txt = soup.text

        #is_parent_field_body = (p.parent.name == 'field_body')
        #if (not is_parent_field_body):
        #print("not is_parent_field_body:{}".format(p.text))
        #continue

        #print("p={}".format(p))
        #print("p.text={}".format(p.text))
        #print("p.parent={}".format(p.parent))
        #print("type(p.parent)={}".format(type(p.parent)))
        #print("p.parent.name={}".format(p.parent.name))

        #print("para:{}".format(para))
        #print("men:{}".format(men))
        #print("kbd:{}".format(kbd))
        #print("txt:{}".format(txt))

        # data=[]
        # for p in para:
        #     t = p.text
        #     use_para_text = True
        #     men = p.find_all('inline', {'classes' : 'menuselection'})
        #     kbd = p.find_all('literal', {'classes' : 'kbd'})
        #
        #     for k in kbd:
        #         k.replaceWith(":kbd:`{}`".format(k.text))
        #
        #     for m in men:
        #         rawtext = "{}".format(m['rawtext'])
        #         rawtext = html.unescape(rawtext)
        #         m.replaceWith(rawtext)
        #         #print("rawtext:{}".format(rawtext))
        #
        #     #print("use_para_text:{}".format(use_para_text))
        #     data.append(p.text)
        #     #print("para.text:[{}]".format(p.text))
        #
        # print(", ".join(data))

    def test_0015(self):
        #text = ":kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`, :kbd:`Numpad8`, \
        #:kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`"
        #text = ":kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`, :kbd:`(Numpad8)`, \
        #:kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`"
        text = ":menuselection:`Góc Nhìn (View) --> Điều Hướng (Navigation) --> Xoáy (Roll)`"
        wl = re.findall("[^\:\`\,\s \(\)]+", text, re.M)
        pp(wl)
        ntext = str(text)
        for w in wl:
            is_kbd = (w == 'kbd')
            if (is_kbd): continue
            nw = "({})".format(w)

            if (not nw in ntext):
                ntext = ntext.replace(w, nw)
        print(ntext)

    def test_0016(self):
        q = []
        l=["this", "that", "here", "there"]
        for ll in l:
            q.append(ll)
        pp(q)
        last = len(q)
        i = last-1
        print(q[i])
        q.remove("there")
        pp(q)


    def test_0017(self):
        text = "<field_body><paragraph><inline classes=\"menuselection\" rawtext=\":menuselection:`Tư Thế (Pose) --> Sao Chép Tư Thế Hiện Tại (Copy Current Pose)`\">Tư Thế (Pose) ‣ Sao Chép Tư Thế Hiện Tại (Copy Current Pose)</inline>, <inline classes=\"menuselection\" rawtext=\":menuselection:`Tư Thế (Pose) --> Dán Tư Thế (Paste Pose)`\">Tư Thế (Pose) ‣ Dán Tư Thế (Paste Pose)</inline>, <inline classes=\"menuselection\" rawtext=\":menuselection:`Tư Thế (Pose) --> Dán Tư Thế Đảo-Lật theo Trục X (Paste X-Flipped Pose)`\">Tư Thế (Pose) ‣ Dán Tư Thế Đảo-Lật theo Trục X (Paste X-Flipped Pose)</inline></paragraph></field_body>"

        text = "<section ids=\"animation-playback-options\" names=\"animation\ playback\ options\"><title>Animation Playback Options</title><definition_list><definition_list_item><term><literal>-a</literal> <literal><options></literal> <literal><file(s)></literal></term><definition><paragraph>Playback <literal><file(s)></literal>, only operates this way when not running in background.</paragraph><definition_list><definition_list_item><term><literal>-p</literal> <literal><sx></literal> <literal><sy></literal></term><definition><paragraph>Open with lower left corner at <literal><sx></literal>, <literal><sy></literal>.</paragraph></definition></definition_list_item><definition_list_item><term><literal>-m</literal></term><definition><paragraph>Read from disk (Do not buffer).</paragraph></definition></definition_list_item><definition_list_item><term><literal>-f</literal> <literal><fps></literal> <literal><fps-base></literal></term><definition><paragraph>Specify FPS to start with.</paragraph></definition></definition_list_item><definition_list_item><term><literal>-j</literal> <literal><frame></literal></term><definition><paragraph>Set frame step to <literal><frame></literal>.</paragraph></definition></definition_list_item><definition_list_item><term><literal>-s</literal> <literal><frame></literal></term><definition><paragraph>Play from <literal><frame></literal>.</paragraph></definition></definition_list_item><definition_list_item><term><literal>-e</literal> <literal><frame></literal></term><definition><paragraph>Play until <literal><frame></literal>.</paragraph></definition></definition_list_item></definition_list></definition></definition_list_item></definition_list></section>"

        html_file="/home/htran/blender_documentations/blender_docs/build/rstdoc/advanced/command_line/arguments.html"
        # parser = AH.AdvancedHTMLParser()
        # #parser.parseFile(html_file)
        # parser.parseStr(text)
        # items = parser.getAllNodes()
        # print("items:{}".format(items))
        # print("type(items):{}".format(type(items)))
        # print("dir(items):{}".format(dir(items)))
        # print("len(items):{}".format(len(items)))
        #
        # '''
        # dir(item):['_AdvancedTag__rawGet', '_AdvancedTag__rawSet', '__class__', '__copy__', '__deepcopy__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_attributes', '_classNames', '_indent', '_old__str__', 'addClass', 'append', 'appendBlock', 'appendBlocks', 'appendChild', 'appendInnerHTML', 'appendNode', 'appendText', 'asHTML', 'attributes', 'attributesDOM', 'attributesDict', 'attributesList', 'blocks', 'childBlocks', 'childElementCount', 'childNodes', 'children', 'classList', 'className', 'classNames', 'cloneNode', 'contains', 'containsUid', 'filter', 'filterAnd', 'filterOr', 'firstChild', 'firstElementChild', 'getAllChildNodeUids', 'getAllChildNodes', 'getAllNodeUids', 'getAllNodes', 'getAttribute', 'getAttributesDict', 'getAttributesList', 'getBlocksTags', 'getBlocksText', 'getChildBlocks', 'getChildren', 'getElementById', 'getElementsByAttr', 'getElementsByClassName', 'getElementsByName', 'getElementsCustomFilter', 'getElementsWithAttrValues', 'getEndTag', 'getFirstElementCustomFilter', 'getHTML', 'getParentElementCustomFilter', 'getPeers', 'getPeersByAttr', 'getPeersByClassName', 'getPeersByName', 'getPeersCustomFilter', 'getPeersWithAttrValues', 'getStartTag', 'getStyle', 'getStyleDict', 'getTagName', 'getUid', 'hasAttribute', 'hasChild', 'hasChildNodes', 'hasClass', 'innerHTML', 'innerText', 'insertAfter', 'insertBefore', 'isEqualNode', 'isSelfClosing', 'isTagEqual', 'lastChild', 'lastElementChild', 'nextElementSibling', 'nextSibling', 'nextSiblingElement', 'nodeName', 'nodeType', 'nodeValue', 'outerHTML', 'ownerDocument', 'parentElement', 'parentNode', 'peers', 'previousElementSibling', 'previousSibling', 'previousSiblingElement', 'remove', 'removeAttribute', 'removeBlock', 'removeBlocks', 'removeChild', 'removeChildren', 'removeClass', 'removeNode', 'removeText', 'removeTextAll', 'setAttribute', 'setAttributes', 'setStyle', 'setStyles', 'style', 'tagBlocks', 'tagName', 'text', 'textBlocks', 'textContent', 'toHTML', 'uid']
        # '''
        # for item in items:
        #     print("type(item):{}".format(type(item)))
        #     print("item:{}".format(item))
        #     print("-" * 50)
        #
        #     #print("type(item):{}".format(type(item)))
        #     #print("dir(item):{}".format(dir(item)))
        #     #exit(0)


    def test_0018(self):
        n1=34
        n2=65
        n3=11
        m_of=5

        list_of_combinations=[]
        list_of_op = ['+','-','*','/']
        m1, m2 = None, None
        for m1 in range(0,4):
            op1 = list_of_op[m1]
            for m2 in range(0, 4):
                op2 = list_of_op[m2]
                list_of_combinations.append((n1, op1, n2, op2, n3))
                print('res = ', n1, op1, n2, op2, n3)

        #pp(list_of_combinations)

        res =  34 + 65 + 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 + 65 + 11")
        res =  34 + 65 - 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 + 65 - 11")
        res =  34 + 65 * 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 + 65 * 11")
        res =  34 + 65 / 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 + 65 / 11")
        res =  34 - 65 + 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 - 65 + 11")
        res =  34 - 65 - 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 - 65 - 11")
        res =  34 - 65 * 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 - 65 * 11")
        res =  34 - 65 / 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 - 65 / 11")
        res =  34 * 65 + 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 * 65 + 11")
        res =  34 * 65 - 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 * 65 - 11")
        res =  34 * 65 * 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 * 65 * 11")
        res =  34 * 65 / 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 * 65 / 11")
        res =  34 / 65 + 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 / 65 + 11")
        res =  34 / 65 - 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 / 65 - 11")
        res =  34 / 65 * 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 / 65 * 11")
        res =  34 / 65 / 11
        is_found = ((res % 5) == 0)
        if (is_found):
            print("Found", "34 / 65 / 11")

    def test_0019(self):
        po_file="/home/htran/blender_documentations/blender_docs/locale/vi/LC_MESSAGES/modeling/meshes/editing/vertices.po"
        po_data = c.load_po(po_file)
        s2=":menuselection:Mesh --> Vertices"
        found_list=[]
        for m in po_data:
            s1=m.id
            distance = DS(s1, s2)
            found_list.append((distance, s1))
            #print("distance:{}; s1=[{}]; s2=[{}]".format(distance, s1, s2))
        sorted_found_list=sorted(found_list)
        pp(sorted_found_list)


    def test_0020(self):
        #html    :[:kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`, :kbd:`Numpad8`, :kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`]
        #html-hex:
        s1="3a6b62643a604d4d42602c203a6b62643a604e756d70616432602c203a6b62643a604e756d70616434602c203a6b62643a604e756d70616436602c0a3a6b62643a604e756d70616438602c203a6b62643a604374726c2d416c742d576865656c602c203a6b62643a6053686966742d416c742d576865656c60"

        #po      :[:kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`, :kbd:`Numpad8`, :kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`]
        #po-hex  :
        s2="3a6b62643a604d4d42602c203a6b62643a604e756d70616432602c203a6b62643a604e756d70616434602c203a6b62643a604e756d70616436602c203a6b62643a604e756d70616438602c203a6b62643a604374726c2d416c742d576865656c602c203a6b62643a6053686966742d416c742d576865656c60"
        is_found = (s1 == s2)

        length = len(s1)
        for i in range(0, length):
            s1_c = s1[i]
            s2_c = s2[i]
            is_equal = (s1_c == s2_c)
            range_size=3
            if (not is_equal):
                print("[{}]: s1_c=[{}]; s2_c=[{}]".format(i, s1_c, s2_c))
                start_index = (i-range_size if (i > range_size) else 0)
                end_index = (i+range_size if (i < length-(range_size+1)) else length-1)
                s1_s = s1[start_index:end_index]
                s2_s = s2[start_index:end_index]
                print("[{}]: s1_s=[{}]; s2_s=[{}]".format(i, s1_s, s2_s))
                break

        print("is_found:{}".format(is_found))

    def test_0021(self):
        k_list={
            ":kbd:`A`": "",
            ":kbd:`Alt-B`": "",
            ":kbd:`Alt-C`": "",
            ":kbd:`Alt-Comma`": "",
            ":kbd:`Alt-D`": "",
            ":kbd:`Alt-E`": "",
            ":kbd:`Alt-F1`": "",
            ":kbd:`Alt-F3`": "",
            ":kbd:`Alt-F`": "",
            ":kbd:`Alt-G`": "",
            ":kbd:`Alt-G`, :kbd:`Alt-R`, :kbd:`Alt-S`": "",
            ":kbd:`Alt-G`, :kbd:`Alt-S`, :kbd:`Alt-R`, :kbd:`Alt-O`": "",
            ":kbd:`Alt-I`": "",
            ":kbd:`Alt-J`": "",
            ":kbd:`Alt-M`": "",
            ":kbd:`Alt-M`, :menuselection:`Collapse`": ":kbd:`Alt-M`, :menuselection:`Thu Lại (Collapse)`",
            ":kbd:`Alt-O`": "",
            ":kbd:`Alt-P`": "",
            ":kbd:`Alt-Period`": "",
            ":kbd:`Alt-RMB`": "",
            ":kbd:`Alt-RMB` or :kbd:`Shift-Alt-RMB` for modifying existing selection": "",
            ":kbd:`Alt-RMB`, or :kbd:`Shift-Alt-RMB` for modifying existing selection": "",
            ":kbd:`Alt-R`": "",
            ":kbd:`Alt-S`": "",
            ":kbd:`Alt-Spacebar`": "",
            ":kbd:`Alt-V`": "",
            ":kbd:`B`": "",
            ":kbd:`C`": "",
            ":kbd:`Comma`": "",
            ":kbd:`Ctrl-A`": "",
            ":kbd:`Ctrl-Alt-A`": "",
            ":kbd:`Ctrl-Alt-C`": "",
            ":kbd:`Ctrl-Alt-D`": "",
            ":kbd:`Ctrl-Alt-Numpad0`": "",
            ":kbd:`Ctrl-Alt-P`": "",
            ":kbd:`Ctrl-Alt-Q`": "",
            ":kbd:`Ctrl-Alt-RMB`": "",
            ":kbd:`Ctrl-Alt-RMB`, or :kbd:`Shift-Ctrl-Alt-RMB` for modifying existing selection": "",
            ":kbd:`Ctrl-Alt-S`": "",
            ":kbd:`Ctrl-Alt-Spacebar`": "",
            ":kbd:`Ctrl-Alt-T`": "",
            ":kbd:`Ctrl-Alt-Z`": "",
            ":kbd:`Ctrl-B`": "",
            ":kbd:`Ctrl-B`, :kbd:`Ctrl-Alt-B`": "",
            ":kbd:`Ctrl-Comma`": "",
            ":kbd:`Ctrl-D`": "",
            ":kbd:`Ctrl-E`": "",
            ":kbd:`Ctrl-F3`": "",
            ":kbd:`Ctrl-F`": "",
            ":kbd:`Ctrl-G`": "",
            ":kbd:`Ctrl-G`, etc.": "",
            ":kbd:`Ctrl-H`": "",
            ":kbd:`Ctrl-J`": "",
            ":kbd:`Ctrl-LMB`": "",
            ":kbd:`Ctrl-LMB`, :kbd:`Shift-Ctrl-LMB`": "",
            ":kbd:`Ctrl-L`": "",
            ":kbd:`Ctrl-MMB`, :kbd:`Wheel`, :kbd:`NumpadPlus`, :kbd:`NumpadMinus`": "",
            ":kbd:`Ctrl-M`": "",
            ":kbd:`Ctrl-N`": "",
            ":kbd:`Ctrl-N` and :kbd:`Shift-Ctrl-N`": "",
            ":kbd:`Ctrl-Numpad0`": "",
            ":kbd:`Ctrl-NumpadPlus` / :kbd:`Ctrl-NumpadMinus`": "",
            ":kbd:`Ctrl-NumpadPlus`, :kbd:`Ctrl-NumpadMinus`": "",
            ":kbd:`Ctrl-O` or :kbd:`F1`": "",
            ":kbd:`Ctrl-P`": "",
            ":kbd:`Ctrl-P`, :kbd:`Alt-P`": "",
            ":kbd:`Ctrl-Period`": "",
            ":kbd:`Ctrl-RMB`": "",
            ":kbd:`Ctrl-R`": "",
            ":kbd:`Ctrl-Spacebar`": "",
            ":kbd:`Ctrl-T`": "",
            ":kbd:`Ctrl-T`, :kbd:`Alt-T`": "",
            ":kbd:`Ctrl-Tab`": "",
            ":kbd:`Ctrl-U`": "",
            ":kbd:`Ctrl-V`": "",
            ":kbd:`Ctrl-W`, :kbd:`Shift-Alt-A`, ...": "",
            ":kbd:`Ctrl-X`": "",
            ":kbd:`Ctrl-Z`": "",
            ":kbd:`Ctrl` and/or :kbd:`Shift`": "",
            ":kbd:`E-LMB`": "",
            ":kbd:`E`": "",
            ":kbd:`E`, :kbd:`Ctrl-LMB`": "",
            ":kbd:`E`, :kbd:`Shift-E`": "",
            ":kbd:`F3`": "",
            ":kbd:`F6`": "",
            ":kbd:`F`": "",
            ":kbd:`G`": "",
            ":kbd:`G`, :kbd:`R`, :kbd:`S`": "",
            ":kbd:`I`": "",
            ":kbd:`J`": "",
            ":kbd:`K`": "",
            ":kbd:`K` or :kbd:`Shift-K`": "",
            ":kbd:`LMB`": ":kbd:`NCT`",
            ":kbd:`L`": "",
            ":kbd:`L`, :kbd:`Ctrl-L`, :kbd:`Shift-L`": "",
            ":kbd:`MMB`": ":kbd:`NCG`",
            ":kbd:`MMB`, :kbd:`Numpad2`, :kbd:`Numpad4`, :kbd:`Numpad6`, :kbd:`Numpad8`, :kbd:`Ctrl-Alt-Wheel`, :kbd:`Shift-Alt-Wheel`": "",
            ":kbd:`M`": "",
            ":kbd:`M` or :kbd:`Ctrl-Alt-M` in the VSE editor": "",
            ":kbd:`Numpad0`": "",
            ":kbd:`Numpad0` to :kbd:`Numpad9`, :kbd:`NumpadPlus`": ":kbd:`Bàn Số 0` (`Numpad0`) tới :kbd:`Bàn Số 9` (`Numpad9`), :kbd:`Bàn Số +` (`NumpadPlus`)",
            ":kbd:`Numpad5`": "",
            ":kbd:`NumpadSlash`": "",
            ":kbd:`OS-Key` (also known as the ``Windows-Key``, ``Cmd`` or ``Super``)": "Phím Hệ Điều Hành (:kbd:`OS-Key`) (còn được biết với những cái tên khác như *phím Cửa Sổ* (``Windows-Key``), phím Lệnh (``Cmd``) hoặc phím Quản Lý (``Super``))",
            ":kbd:`O`": "",
            ":kbd:`O`, :kbd:`Alt-O`, :kbd:`Shift-O`": "",
            ":kbd:`P`": "",
            ":kbd:`P`, :kbd:`Alt-P`": "",
            ":kbd:`Period`": "",
            ":kbd:`Q`": "",
            ":kbd:`RMB`": ":kbd:`NCP` - Nút Chuột Phải",
            ":kbd:`RMB` and :kbd:`Shift-RMB`": "",
            ":kbd:`RMB`, :menuselection:`Online Manual`": ":kbd:`NCP`, :menuselection:`Hướng dẫn sử dụng trực tuyến, trên mạng (Online Manual)`",
            ":kbd:`R`": "",
            ":kbd:`S`": "",
            ":kbd:`Shift-A`": "",
            ":kbd:`Shift-Alt-F`": "",
            ":kbd:`Shift-Alt-G`, :kbd:`Shift-Alt-R`, and :kbd:`Shift-Alt-S`": "",
            ":kbd:`Shift-Alt-S`": "",
            ":kbd:`Shift-B`": "",
            ":kbd:`Shift-Ctrl-A`": "",
            ":kbd:`Shift-Ctrl-Alt-C`": "",
            ":kbd:`Shift-Ctrl-Alt-S`": "",
            ":kbd:`Shift-Ctrl-B` (vertex-only)": "",
            ":kbd:`Shift-Ctrl-C`": "",
            ":kbd:`Shift-Ctrl-MMB`": "",
            ":kbd:`Shift-Ctrl-M`": "",
            ":kbd:`Shift-Ctrl-R`": "",
            ":kbd:`Shift-Ctrl-T`": "",
            ":kbd:`Shift-Ctrl-Tab`": "",
            ":kbd:`Shift-Ctrl-Z`": "",
            ":kbd:`Shift-D`": "",
            ":kbd:`Shift-E`": "",
            ":kbd:`Shift-F1` or :kbd:`Ctrl-Alt-O`": "",
            ":kbd:`Shift-F`": "",
            ":kbd:`Shift-G`": "",
            ":kbd:`Shift-K`": "",
            ":kbd:`Shift-LMB`": "",
            ":kbd:`Shift-L`": "",
            ":kbd:`Shift-MMB`, :kbd:`Ctrl-Numpad2`, :kbd:`Ctrl-Numpad4`, :kbd:`Ctrl-Numpad6`, :kbd:`Ctrl-Numpad8`": "",
            ":kbd:`Shift-M`": "",
            ":kbd:`Shift-Numpad4`, :kbd:`Shift-Numpad6`, :kbd:`Shift-Ctrl-Wheel`": "",
            ":kbd:`Shift-R`": "",
            ":kbd:`Shift-S`": "",
            ":kbd:`Shift-T`, :kbd:`Shift-Alt-T`": "",
            ":kbd:`Shift-Tab`": "",
            ":kbd:`Shift-V`": "",
            ":kbd:`Shift-W`": "",
            ":kbd:`Shift-W`, :kbd:`Shift-Ctrl-W`, :kbd:`Alt-W`": "",
            ":kbd:`Shift-X`, :kbd:`Shift-Y`, :kbd:`Shift-Z` or :kbd:`Shift-MMB` after moving the mouse in the desired direction.": "",
            ":kbd:`Shift`, :kbd:`Ctrl`, :kbd:`Alt`": "",
            ":kbd:`T`": "",
            ":kbd:`Tab`": "",
            ":kbd:`Tab`, :kbd:`Ctrl-Tab`": "",
            ":kbd:`U`": "",
            ":kbd:`V`": "",
            ":kbd:`W`": "",
            ":kbd:`Wheel`": ":kbd:`Bánh Xe`",
            ":kbd:`X`": "",
            ":kbd:`X` or :kbd:`Delete`, :menuselection:`Edge Loop`": ":kbd:`X` or :kbd:`Delete`, :menuselection:`Vòng Mạch (Edge Loop)`",
            ":kbd:`X`, :kbd:`Delete`": "",
            ":kbd:`X`, :kbd:`Delete`; :kbd:`Ctrl-X`": "",
            ":kbd:`X`, :kbd:`Y`, :kbd:`Z` or :kbd:`MMB` after moving the mouse in the desired direction.": "",
            ":kbd:`Y`": "",
        }

        #SINGLE_KEY_KEYBOARD_DEF = re.compile(r"^:kbd:`\
        #(?P<single_key>(([\w])|(Tab)|(F[\d])|(Delete)){1})|\
        #((?P<modifier>(Alt)|(Ctrl)|(Shift))-\
        #(?P=single_key))*\
        #`$")

        #|
        #((?P<modifier>((Ctrl)|(Alt)|(Shift)))
        #((?P=modifier)|(?P=single_key)))
        p = r"""
                ^:kbd:`[^`]
                (?P<single_key>(
                    ([\w])|
                    ([\+\-\/\\/|/~/#/?/,/./]])|
                    (F[\d])|
                    (Space)|
                    (Spacebar)|
                    (Enter)|
                    (Return)|
                    (Esc)|
                    (Escape)|
                    (Del)|
                    (Delete)|
                    (Ins)|
                    (Insert)|
                    (Home)|
                    (End)|
                    (PgUp)|
                    (PageUp)|
                    (PgDown)|
                    (PageDown)|
                    ){1,1})|
                (?P<modifier>((Ctrl)|(Alt)|(Shift)))\-((?P=modifier)|(?P=single_key))
                `$"""
        SINGLE_KEY_KEYBOARD_DEF = re.compile(p, re.VERBOSE)


        keyboard_def=r":kbd:`[^`]*`"
        only_keyboard_def = r"^{}$".format(keyboard_def)
        special_def = r"((Wheel)|(Numpad)|(MMB)|(LMB)|(RMB)|(Period))"
        #pattern = ":kbd:`(?P<single_key>[\w]{1})|((?P<modifier><(Alt)|(Ctrl)|(Shift))-(?P=single_key))*`"

        for k,v in k_list.items():
            print(k)

            word_list=re.findall(keyboard_def, k)
            pp(word_list)
            for w in word_list:
                w = re.sub("[,;\. ]", "", w)
                w = w.strip()
                #is_single_key = (SINGLE_KEY_KEYBOARD_DEF.search(w) != None)
                is_only_keyboard = (re.search(only_keyboard_def, w) != None)
                is_keep = (is_only_keyboard) and (re.search(special_def, w) != None)
                print(w, is_keep)
            print("-" * 50)

    def test_0022(self):
        text = ":abbr:`SDLS (Selective Damped Least Square)`, :abbr:`DLS (Damped Least Square)`"
        text = "this is another"
        pattern = r"\(([^\)]*)\)"
        word_list = re.findall(pattern, text);
        has_list = (len(word_list) > 0)

        print(word_list)
        if (not has_list):
            print(text)
            return text

        new_word_list = []
        for w in word_list:
            new_word = "-- {}".format(w)
            new_word_list.append((w, new_word))

        new_text = str(text)
        for w, n_w in new_word_list:
            new_text = new_text.replace(w, n_w)

        print(word_list, new_word_list)
        print(new_text)


    def test_0023(self):
        t = ":kbd:`Shift-MMB`, :kbd:`Ctrl-Numpad2`, :kbd:`Ctrl-Numpad4`, :kbd:`Ctrl-Numpad6`, :kbd:`Ctrl-Numpad8`"
        t = "You can increase or decrease the radius of the proportional editing influence with the mouse wheel :kbd:`WheelUp`, :kbd:`WheelDown` or :kbd:`PageUp`, :kbd:`PageDown`, :kbd:`Wheel` respectively. As you change the radius, the points surrounding your selection will adjust their positions accordingly."
        nt = self.translateKeyBoard(t)
        print(t, nt)

    def test_0024(self):
        t = [
            "When mapping transform properties to location (i.e. Location, Destination button is enabled),",
            "Square Power of Two",
            "In order to save in a blend-user a custom brush, set a Fake User."
        ]
        p = re.compile(r"([\W]{1,1})$")
        for tt in t:
            is_end_with_symbol = (p.search(tt) != None)
            print("{}; is_end_with_symbol:{}".format(tt, is_end_with_symbol))

    def test_0026(self):
        pat="(\w+)(_[\w]+)*"
        pt=r'^{}$'.format(pat)
        p=re.compile(pt, re.I)
        t="TOPBAR_MT_edit_curve_add"
        print(p.search(t))

    def test_0027(self):
        d = {'one':1, 'two':2}
        for e in d.items():
            print(e)


    #case NODE_MATH_PINGPONG: {
    #if (in1 == 0.0f) {
    #*out = 0.0f;
    #}
    #else {
    #*out = fabsf(fractf((in0 - in1) / (in1 * 2.0f)) * in1 * 2.0f - in1);
    #}
    #break;
    #}

    #case NODE_MATH_WRAP: {
    #float in2 = tex_input_value(in[2], p, thread);
    #*out = wrapf(in0, in1, in2);
    #break;
    #}


    #/* Adapted from godotengine math_funcs.h. */
    #MINLINE float wrapf(float value, float max, float min)
    #{
    #float range = max - min;
    #return (range != 0.0f) ? value - (range * floorf((value - min) / range)) : min;
    #}

    def test_0028(self):
        def wrapf(value : float, f_max: float, f_min: float):
            f_range : float = (f_max - f_min)
            if (f_range != 0.0):
                wrap_value = value - (f_range * math.floor((value - f_min) / f_range))
            else:
                wrap_value = f_min
            return wrap_value

        range_min = 1.0
        range_max = 3.0
        v = 0.5
        wrap_value = wrapf(v, range_min, range_max)
        print("wrap_value:{}, {}, {}".format(v, range_min, range_max))
        print(wrap_value)

    def test_0029(self):
        CONTAINT_AST = re.compile(r'[\*\"]+(?![\s\)\(\.]+)([^\*\"]+)(?<!([\s\:]))[\*\"]+')
        t="Bones have an extra \"mirror extruding\" tool, called by pressing :kbd:`Shift-E`. By default, it behaves exactly like the standard extrusion. But once you have enabled the `X-Axis Mirror`_ editing option, each extruded tip will produce *two new bones*, having the same name except for the \"_L\"/ \"_R\" suffix (for left/right, see the :ref:`next page <armature-editing-naming-conventions>`). The \"_L\" bone behaves like the single one produced by the default extrusion -- you can move/rotate/scale it exactly the same way. The \"_R\" bone is its mirror counterpart (along the armature's local X axis), see Fig. :ref:`fig-rig-bone-mirror`."
        f_list = CONTAINT_AST.findall(t)
        print(f_list)

    def patternMatchAll(self, pat, text):
        original=[]
        break_down=[]
        try:
            for i, m in enumerate(pat.finditer(text)):
                s = m.start()
                e = m.end()
                orig = m.group(0)
                original.append((s, e, orig))

                for i, g in enumerate(m.groups()):
                    if g:
                        i_s = orig.find(g)
                        ss = i_s + s
                        ee = ss + len(g)
                        v=(ss, ee, g)
                        break_down.append(v)
        except Exception as e:
            _("patternMatchAll")
            _("pattern:", pat)
            _("text:", text)
            _(e)
        return original, break_down

    #def patternMatchAll(self, pat, text):
    #find_list= defaultdict(OrderedDict)
    #try:
    #for i, m in enumerate(pat.finditer(text)):
    #s = m.start()
    #e = m.end()
    #orig = m.group(0)

    #v=[(s, e, orig)]
    #k = s
    #entry={k:v}
    #find_list.update(entry)
    #for i, g in enumerate(m.groups()):
    #if g:
    #i_s = orig.find(g)
    #ss = i_s + s
    #ee = ss + len(g)
    #v=(ss, ee, g)
    #find_list[k].append(v)
    #except Exception as e:
    #_("patternMatchAll")
    #_("pattern:", pat)
    #_("text:", text)
    #_(e)
    #return find_list

    def getListOfLocation(self, find_list):
        loc_list={}
        for k,v in find_list.items():
            s = v[0][0]
            e = v[0][1]
            t = v[0][2]
            entry={k:[s, e, t]}
            loc_list.update(entry)
        return loc_list

    def inRange(self, item, ref_list):
        i_s, i_e, i_t = item
        for k, v in ref_list.items():
            r_s, r_e, r_t = v
            is_in_range = (i_s >= r_s) and (i_e <= r_e)
            if is_in_range:
                return True
        else:
            return False

    def diffLocation(self, ref_list, keep_list):
        loc_keep_list={}
        for k, v in keep_list.items():
            in_forbiden_range = self.inRange(v, ref_list)
            if not in_forbiden_range:
                s, e, txt = v
                ee = (s, e, txt)
                entry={s:[ee]}
                loc_keep_list.update(entry)

        return loc_keep_list

    def getTextListForMenu(self, text_entry):
        #print("getTextListForMenu", text_entry, txt_item)
        entry_list = []


        its, ite, txt = text_entry
        print("menu_list: its, ite, txt")
        print(its, ite, txt)

        menu_list = self.patternMatchAll(MENU_PART, txt)
        print("menu_list")
        pp(menu_list)
        for mk, mi in menu_list.items():
            ms, me, mtxt = mi[0]
            is_empty = (ms == me)
            if (is_empty):
                continue
            ss = its + ms
            se = ss + len(mtxt)
            entry=(ss, se, mtxt)
            entry_list.append(entry)

        return entry_list


    def getTextListForURI(self, text_entry, uri_list):
        #print("getTextListForURI", text_entry, uri_list)
        entry_list = []
        for uri_k, uri_v in uri_list.items():
            uri_orig_text, uri_text, uri_link = uri_v
            tes, tee, text = text_entry
            uris, urie, uritext = uri_text
            uss = tes + uris
            use = uss + len(uritext)
            entry=(uss, use, uritext)
            entry_list.append(entry)
        return entry_list

    def getTextListForABBR(self, text_entry):
        entry_list = []

        s, e, txt = text_entry
        abbr_list = self.patternMatchAll(LINK_WITH_URI, txt)
        has_abbr = (len(abbr_list) > 0)
        if has_abbr:
            for abbr_k, abbr_v in abbr_list.items():
                abbr_orig_text, abbr_text, abbr_full_text = abbr_v

                tes, tee, text = text_entry
                abbr_s, abbr_e, abbr_entry_text = abbr_full_text

                print("abbr_s, abbr_e, abbr_entry_text")
                print(abbr_s, abbr_e, abbr_entry_text)

                abr_s = tes + abbr_s
                abr_e = s + len(abbr_entry_text)
                entry=(abr_s, abr_e, abbr_entry_text)
                entry_list.append(entry)
        print("exit from entry_list:", entry_list)
        return entry_list


    def refEntry(self, ref_list):
        entry_list = {}
        k, v = None, None
        v_len = -1
        s = e = ss = se = xs = xe = 0
        txt = xtype = origin_entry = type_entry = text_entry = None
        try:
            for k, v in ref_list.items():
                orig = v[0]
                o_s, o_e, o_txt = orig
                key = o_s
                entry={o_s:[(o_s, o_e, o_txt)]}
                entry_list.update(entry)
                #print("ORIGINAL ENTRY:", entry)
                v_len = len(v)
                s, e, txt, xtype = None, None, None, None
                if (v_len == 1):
                    #print("v_len == 1")
                    #print(v_len, v)
                    s, e, txt = orig
                    text_entry = (s, e, txt)
                elif (v_len == 2):
                    origin_entry, text_entry = v
                    s, e, txt = text_entry
                elif (v_len == 3):  # :kbd:,
                    origin_entry, type_entry, text_entry = v
                    xs, xe, xtype = type_entry
                    s, e, txt = text_entry
                else:
                    raise Exception("Impossible List, there are more items than expected!")


                has_xtype = (xtype is not None)
                has_menu = has_xtype and ("menuselection" in xtype)
                has_abbr = has_xtype and ("abbr" in xtype)
                has_kbd = has_xtype and ("kbd" in xtype)
                uri_list = self.patternMatchAll(LINK_WITH_URI, txt)
                has_uri = (len(uri_list) > 0)
                if has_uri and not (has_abbr or has_menu):
                    print("has_uri and not has_abbr")
                    uri_entry_list = self.getTextListForURI(text_entry, uri_list)
                    entry_list[key].append(uri_entry_list)
                    #print("has_uri:", uri_entry_list)
                elif has_xtype:
                    if has_abbr:
                        print("has_abbr")
                        abbr_list = self.getTextListForABBR(text_entry)
                        entry_list[key].append(abbr_list)
                        print(entry_list[key])
                    elif has_menu:
                        print("has_menu")
                        menu_text_list = self.getTextListForMenu(text_entry)
                        pp(menu_text_list)
                        entry_list[key].append(menu_text_list)
                    elif has_kbd:
                        has_commond_keyboard = NORMAL_KEYBOARD_COMBINATION.search(o_txt)
                        if (has_commond_keyboard):
                            print("has_commond_keyboard:", o_txt)
                            print(has_commond_keyboard)
                    else:
                        print("has_xtype but NOT ABBR OR MENU:", txt)
                        entry_list[key].append([text_entry])
                else:
                    entry_list[key].append([text_entry])
        except Exception as e:
            print(ref_list)
            print("k, v, v_len")
            print(k, v, v_len)
            raise e
        return entry_list

    def filteredTextList(self, ref_list, norm_list):
        loc_ref_list = self.getListOfLocation(ref_list)
        loc_norm_list = self.getListOfLocation(norm_list)
        keep_norm_list = self.diffLocation(loc_ref_list, loc_norm_list)
        return keep_norm_list


    def mergeTwoLists(self, primary, secondary):

        loc_primary_list = self.getListOfLocation(primary)
        loc_secondary_list = self.getListOfLocation(secondary)
        keep_list = self.diffLocation(loc_primary_list, loc_secondary_list)

        #pp(keep_list)
        for k, v in keep_list.items():
            keep_v = secondary[k]
            entry={k:keep_v}
            primary.update(entry)

        return primary


    #def checkParenth(self, str):
    #stack = Stack()
    #pushChars, popChars = "<({[", ">)}]"
    #for c in str:
    #if c in pushChars:
    #stack.push(c)
    #elif c in popChars:
    #if stack.isEmpty():
    #return False
    #else:
    #stackTop = stack.pop()
    ## Checks to see whether the opening bracket matches the closing one
    #balancingBracket = pushChars[popChars.index(c)]
    #if stackTop != balancingBracket:
    #return False
    #else:
    #return False

    #return not stack.isEmpty()

    #def parseArchedBrackets(self, msg:str, para_list:list):

    #is_valid = self.checkParenth(msg)
    #print("is_valid:", is_valid)
    #return {}

    ##ref_item: RefItem = None
    ##para = []
    ##end_loc = start_loc
    ##msg_length = len(msg)
    ##for i in range(start_loc, msg_length):
    ##char = msg[i]
    ##para.append(char)
    ##print("char:", char, "i:", i)
    ##is_open = ('(' == char)
    ##is_close = (')' == char)
    ##if is_open:
    ##para.clear()
    ##self.parseArchedBrackets(msg, i+1, para_list)
    ##elif is_close:
    ##end_loc = i
    ##valid_close = (start_loc < end_loc) and (para is not None) and (len(para) > 0)
    ##if valid_close:
    ##parsed_para = (start_loc, end_loc, "".join(para))
    ##para_list.append(parsed_para)
    ##return


    def parsePair(self, open_char, close_char, msg):
        valid = (open_char is not None) and (close_char is not None) and (msg is not None) and (len(msg) > 0)
        if not valid:
            return None

        loc_list:list = []
        b_list=[]
        l = len(msg)
        s = e = 0
        k = -1
        for i in range(0, l):
            c = msg[i]
            is_open = (c == open_char)
            is_close = (c == close_char)
            if is_open:
                b_list.append(i)
            elif is_close:
                try:
                    last_s = b_list[-1]
                    b_list.pop()
                    txt = msg[last_s:i+1]
                    loc_list_entry=(last_s, i+1, txt)
                    loc_list.append(loc_list_entry)
                except Exception as e:
                    raise Exception("Unbalanced pair [{},{}] at location:{}".format(open_char, close_char, i))

        has_unprocessed_pair = (len(b_list) > 0)
        if has_unprocessed_pair:
            raise Exception("Unbalanced pair [{},{}] at location:{}".format(open_char, close_char, b_list))

        has_loc = (len(loc_list) > 0)
        sorted_loc_list = sorted(loc_list, key=lambda x: x[0])
        return sorted_loc_list

    def parseArchedBrackets(self, msg):
        loc_list = self.parsePair('(',')', msg)

        pp(loc_list)
        for s, e, txt in loc_list:
            n_txt = msg[s:e]
            print(s, e, n_txt)

    def test_0030(self):

        t = ":doc:`command line </advanced/command_line/index>`"
        #t = ':menuselection:`Sidebar region --> Item`, :menuselection:`Bones tab --> Bones panel`'
        #t = "Render frame ``<frame>`` and save it. ``+<frame>`` start frame relative, ``:kbd:`LMB``` -- keyboard and mouse shortcuts. ``*Mirror*`` -- interface labels. ``:menuselection:`3D View --> Add --> Mesh --> Monkey``` -- menus."
        t = '''
        Render frame ``<frame>`` and save it. ``+<frame>`` start frame relative, ``-<frame>`` end frame relative. press :kbd:`Ctrl-G`, :menuselection:`Group --> Make Group`; :Description: Save and restore user defined views, :abbr:`POV (Point Of View)` and camera locations. ::kbd:`Shift-LMB` toggle the use of :ref:`Stabilizer <grease-pencil-draw-brushes-stabilizer>`; See also `Importance sampling <https://en.wikipedia.org/wiki/Importance_sampling>`__ on Wikipedia; Visually, the result is to zero the reds and bring up (by \"symmetry\" -- the real values remain unchanged!); (e.g. ``*-0001.jpg``, ``*-0002.jpg``, ``*-0003.jpg``, etc, of any image format), you have a choice:; which can act as subtitles, to a `SubRip <https://en.wikipedia.org/wiki/SubRip>`__ file (``.srt``);Now the tool calculates the average weight of all connected **and** unselected vertices; is connected to one unselected vertex with ``weight = 1``;  When Factor is set to 0.0 then the `Smooth`_ tool does not do anything; For example 5.25 would allow the following weights ``[0.0, 0.2, 0.4, 0.6, 0.8, 1.0]``. The bone automatically scales together with its parent in *Pose Mode*. For more details, see the :ref:`relations page <bone-relations-parenting>`. When you add a single still image (``*.jpg``, ``*.png``, etc.), Blender creates a 25 frames long strip which will show this image along the strips range. Most bones' properties (except the transform ones) are regrouped in each bone's panels, in the *Bones* tab in *Edit Mode*. Let us detail them. you can filter the Bright/Contrast modifier by placing a Mask modifier -- In the 3D View; (also :kbd:`Shift-W` :menuselection:`--> (Deform, ...)`). (also :kbd:`Shift-W` :menuselection:`--> (Multiply Vertex Group by Envelope, ...)`). and ``#docs`` :ref:`blender-chat`; :Maintainer: Brendon Murphy (meta-androcto); Blender has a tool called *UV Layout* (:menuselection:`UV Editor --> UVs --> Export UV Layout`); :Menu:      :menuselection:`Pose --> Bone Groups --> ...`; :Menu:      :menuselection:`File --> Export --> Pointcache (.pc2)`; :Menu:      :menuselection:`Armature --> Names --> AutoName Left/Right, Front/Back, Top/Bottom`, :Menu:      :menuselection:`Pose --> Bone Groups --> ...`

        :menuselection:`Properties --> Object Data --> Geometry Data --> Clear Sculpt-Mask Data`,
        :menuselection:`Sculpt`
        See `N-poles & E-poles <https://blender.stackexchange.com/a/133676/55>`__.
        in Fig. :ref:`fig-mesh-screw-wood` and Fig. :ref:`fig-mesh-screw-spring`
        as we're here; and 'here' but not 'in this place' and I couln't refuse what shouldn't for he's not she's

        :kbd:`Shift-'` -- Link only to selected nodes that have the same name/label as active node (:kbd:`Shift-'` to replace existing links)
        <->
        <=
        <Matrix>
        <file(s)>
        <fps-base>
        <instance_node>
        <w>
        @CTRL
        @MCH

        timeline-view-menu
        tool-select-box
        tool-select-circle
        resolution_x
        rest_mat
        rig_ui
        object:index
        kUniformScope
        kVertexScope
        keyframe-type

        result = previous + value * influence

        :menuselection:`File --> Import/Export --> X3D Extensible 3D (.x3d/.wrl)`


        '''

        t = '''
        Selects all objects whose name matches a given pattern. Supported wild-cards: \* matches everything, ? matches any single character, [abc] matches characters in "abc", and [!abc] match any character not in "abc". As an example \*house\* matches any name that contains "house", while floor\* matches any name starting with "floor".
        '''


        #t = ":Menu:      :menuselection:`File --> Export --> Pointcache (.pc2)`"
        #t = ":Menu:      :menuselection:`Armature --> Names --> AutoName Left/Right, Front/Back, Top/Bottom`"
        #t = ":Menu:      :menuselection:`Pose --> Bone Groups --> ...`"
        #t = ":Menu:      :menuselection:`Object --> Animation --> Insert Keyframe...`"
        #t = "(also :kbd:`Shift-W` :menuselection:`--> (Multiply Vertex Group by Envelope, ...)`)."
        #t = "'msgid:', '(also :kbd:`Shift-W` :menuselection:`--> (Multiply Vertex Group by Envelope, ...)`). :doc:`command line </advanced/command_line/index>`"
        #t = "::kbd:`Shift-LMB` toggle the use of :ref:`Stabilizer <grease-pencil-draw-brushes-stabilizer>`"
        #t = ":Location: :menuselection:`Properties --> Armature, Bone`, :menuselection:`3D View --> Tools panel`, also :kbd:`Shift-W` :menuselection:`--> (Locked, ...)`) This will prevent all editing of the bone in *Edit Mode*; see :doc:`previous page </animation/armatures/bones/editing/bones>`"
        #t = ":Location: :menuselection:`3D View --> Edit Mode Context Menu --> Relax`"
        #t = ":Description: Save and restore user defined views, :abbr:`POV (Point Of View)` and camera locations."
        #l = map(lambda x: x.group(), p.finditer(t))
        #t = "also :kbd:`Shift-W` :menuselection:`--> (Locked, ...)`) This will prevent all editing of the bone in *Edit Mode*; see :doc:`previous page </animation/armatures/bones/editing/bones>`."

        #t="ranging from 0.0 to 1.0 from the left to right side and bottom to top of the render. This is well suited for blending two objects"

        #t = "For Factor > 0 the weights of the affected vertices gradually shift from their original value towards the average weight of all connected **and** unselected vertices (see examples above)"
        #t = "To clear the mask of areas with the *Lasso Mask* tool, first invert the mask,"
        #t = "To hide a part of a mesh inside the selection. This works similar to :ref:`Box Select <tool-select-box>` tool."
        #t = "Save and restore user defined views, :abbr:`POV (Point Of View)` and camera locations."
        #t = ":doc:`modifier </modeling/modifiers/modify/data_transfer>`"
        #t = "Unit Circle <https://en.wikipedia.org/wiki/Unit_circle>"

        t = "Transformations (without translation): ``Quaternion(...)``/ ``Euler(...)``"
        t = "To clear (the mask of areas) with (the (Lasso Mask) tool), first invert the mask,"
        t = '''(something glTF allows multiple animations per file, with animations targeted to particular objects at time of export. To ensure that an animation is included, either (a) make it the active Action on the object, (b) create a single-strip NLA track, or (c) stash the action.

        Camera: ``POINT`` or ``VIEW`` or ``VPORT`` or (wip: ``INSERT(ATTRIB+XDATA)``)

        3D View: (wip: ``VIEW``, ``VPORT``)'''


        #elem_list=[]
        #self.parseArchedBrackets(t, elem_list)
        #print(elem_list)

        s = "(c>5 or (p==4 and c<4))"

        #s = "(online) or URL (in print)"

        ##It's pyparsing.printables without ()
        #r = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'*+,-./:;<=>?@[\]^_`{|}~'
        #parens = nestedExpr( '(', ')',  content=Word(r))
        #parens.setParseAction(lambda locn,tokens: (locn, tokens[0]))

        ##res = parens.parseString(s)[0].asList()
        #res = parens.parseString(s)
        #print(res.asList())

        #GREED = Word(alphas) + "," + Word(alphas) + "!"
        #greeting = GREED.parseString("Hello, world!")

        #SIGN=Word("+-", max=1)
        #INTEGER = Combine(SIGN[0,1] + Word(nums))
        #VARIABLE = Word(alphas, max=1)
        #ARITH_OP = Word("+-*/%", max=1)
        #REAL_NUM = Combine(SIGN[0,1] + Word(nums) + '.' + Word(nums))
        #EXPRESSION = (INTEGER|REAL_NUM) + (ARITH_OP + (INTEGER|REAL_NUM))[0, ...]
        #EQUATION = VARIABLE + "=" + EXPRESSION[1, ...]

        #eq = EQUATION.parseString("a = 3.0 * 2 + 1.005")
        #print(eq)

        #print("text:", t)
        #result_list = self.patternMatchAll(LINK_WITH_URI, t)
        ##result_list = self.patternMatchAll(URI, t)
        #pp(result_list)

        #ARCH_BRAKET = re.compile(r'[\(]+(?![\s\.\,\`]+)([^\)]+)[\)]+(?<!([\s\.\,]))')
        #ARCH_BRAKET = re.compile(r'[\(]+([^\)]+)(\([^\)]+\))*([^\)]+)?[\)]+')
        EXTRA_WORD = r'([^\s\,\.\:\;]+)?'
        #ARCH_BRAKET_LOOKAHEAD = r'(?=' + EXTRA_WORD + r'\([^)]+\)' + EXTRA_WORD + r')'
        ARCH_BRAKET_LOOKAHEAD = r'(?=\([^)]+\))'
        #ARCH_BRAKET_PATTERN = EXTRA_WORD + r'[\(]+' + ARCH_BRAKET_LOOKAHEAD + r'(.*)' + r'[\)]+' + EXTRA_WORD
        #ARCH_BRAKET_PATTERN = r'[\(]+' + r'(.*)' + r'[\)]+'
        # (?=(\([^)]+\)))
        #ARCH_BRAKET_PATTERN = r'[\(]+(([^\)]+)|(.*))[\)]+([^\s]+\))*'
        #ARCH_BRAKET_PATTERN = r'[\(]+(([^)])|(.*))[\)]+'
        # ARCH_BRAKET_PATTERN = r'[\(]+([^)])[\)]+'
        # (?!([\s\:\,\.]))
        #ARCH_BRAKET_PATTERN = r'(?=[\(][^\)]+[\)])([\(]+(.*)[\)]+)'
        #ARCH_BRAKET_PATTERN = r'([\(]+(.*)[\)]+)'
        #ARCH_BRAKET_PATTERN = r'([\(]+([^\)]+)[\)]+)'
        #ARCH_BRAKET_PATTERN = r'([\(]+(.*)[\)]+)'

        #ARCH_BRAKET_PATTERN = r'[\(]+((\([^\)]+\))*|(.*))[\)]+'
        ARCH_BRAKET_PATTERN = r'[\(]+(.*)[\)]+'
        ARCH_BRAKET = re.compile(ARCH_BRAKET_PATTERN)

        #t = None
        #filename="/home/htran/arched_brakets.log"
        #with open(filename, encoding='utf8') as f:
        #t = f.read()

        self.parseArchedBrackets(t)

        #ref_list = self.patternMatchAll(ARCH_BRAKET, t)
        #pp(ref_list)
        #for k, v in ref_list.items():
        #orig = v[0]
        #print("orig:", orig)

        #c = Counter(orig)
        #brack_count = c['(']
        #if (brack_count > 1):
        #sub_ref_list = self.patternMatchAll(ARCH_BRAKET, t)
        #for k, v in sub_ref_list.items():
        #sub_orig = v[0]
        #print("sub_orig:", sub_orig)


        #pp(ref_list, width=4096, compact=False, indent=0)

        #t = "Mr. James told me Dr. Brown is not available today. I will try tomorrow."
        #t_list = sent_tokenize(t)
        #pp(t_list)
        #for par in t_list:
        #print(par)
        #print()

        #t="1a + 2b - 3d / 400 = 5abc"

        #t=":math:`((420 + 180) modulo 360) - 180 = 60 - ...`"
        #is_ignore = self.isFormular(t)
        #print(t, is_ignore)

        #split_list = re.split(r'[\n][\s]+', t)
        #print("split_list")
        #pp(split_list)
        #for t in split_list:
        ##is_ignore = self.isIgnoredWord(t)
        ##print(t, is_ignore)

        #ref_list = self.patternMatchAll(GA_REF, t)
        ##ref_list = self.patternMatchAll(PARAMS, t)
        #print("ref_list")
        #pp(ref_list)

        ##norm_txt_list = self.patternMatchAll(NORMAL_TEXT, t)
        ##pp(norm_txt_list)

        ##filtered_txt_list = self.filteredTextList(ref_list, norm_txt_list)
        ##print("filtered_txt_list")
        ##pp(filtered_txt_list)

        #ref_norm_list = self.refEntry(ref_list)
        #print("ref_norm_list")
        #pp(ref_norm_list)

        #txt_norm_list = self.refEntry(filtered_txt_list)
        #print("txt_norm_list")
        #pp(txt_norm_list)

        #pp(ref_list)
        #pp(norm_list)

        #filtered_list = self.refEntry(ref_list)
        #print("filtered_list:")
        #pp(filtered_list)

    def test_0031(self):
        t = "1,000,000.00"
        #t = "1, 2, 3, 4"
        p = re.compile(r"^(([\d]+)([\,\.]?[\s]?[\d]+)*)+$")
        is_number = p.search(t)
        print(is_number)

    def test_0032(self):
        h = None
        for t in ignore_list:
            h = HoldString(t)
            print(hex(id(h)), h)

        print("last one", h)


    def test_0033(self):
        GA_REF = re.compile(r'[\`]*(:\w+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*')
        GA_REF_ONLY = re.compile(r'^[\`]*(:\w+:)*[\`]+(?![\s]+)([^\`]+)(?<!([\s\:]))[\`]+[\_]*$')
        t='''
        debugging :abbr:, ``:kbd:`LMB```, ``*Mirror*``, ``:menuselection:`3D View --> Add --> Mesh --> Monkey```
        '''
        # t = '``:kbd:`LMB```'
        # t = '``:menuselection:`3D View --> Add --> Mesh --> Monkey```'
        orig, break_down = self.patternMatchAll(GA_REF_ONLY, t)
        pp(break_down)


    def cmdline(self, command):
        process = Popen(
            args=command,
            stdout=PIPE,
            shell=True
        )
        return process.communicate()[0]

    def cmd_out(self, command):
        result = sub.run(command, stdout=sub.PIPE, stderr=sub.PIPE, universal_newlines=True, shell=True)
        return result.stdout

    def test_0034(self):
        out1=self.cmdline("cat /etc/services")
        out2=self.cmdline('ls')
        #out3=self.cmdline('rpm -qa | grep "php"')
        out4=self.cmdline('nslookup google.com')

        print(out2)

    def test_0035(self):
        my_output = self.cmd_out("echo hello world")
        print(my_output)
        my_output = self.cmd_out("ls -l")
        print(my_output)
        my_output = self.cmd_out("git status | grep \'modified\' | awk \'{ print $2 }\' | grep \".po\"")
        print(my_output)
        my_output = self.cmd_out("svn status | grep \"^M\" | awk \'{ print $2 }\' | grep \".po\"")
        #print(my_output)
        #print(type(my_output))
        #file_list = my_output.split()
        #print(type(file_list))
        #print(file_list)
        #pp(file_list)

        #my_output = self.cmd_out("find . -type f -name \"*.po\" -exec ls -al --time-style=+%D\ %H:%M:%S \{\} \; | grep \`$date_bin +%D\` | awk \'{ print $6,$7,$8 }\' | sort | tail -1 | awk \'{ print $3 }\'")

        my_output = self.cmd_out("find . -maxpath 1 -name \"*.po\" -mtime -1 -print")

        #my_output = self.cmd_out("**/*.po")
        print(my_output)

        changed_file = "/home/htran/new_vi.po"
        sha256_cmd = "sha256sum " + changed_file + " |  awk '{ print $1 }'"
        my_output = self.cmd_out(sha256_cmd)

        #output = sub.check_output("ls **/*.po", shell=True)
        print(my_output)


        #my_output = self.cmd_out(["echo", "hello world"])
        #print(my_output)


    def writeTextFile(self, file_name, data):
        with open(file_name, "w+") as f:
            f.write(data)

    def readTextFile(self, file_name):
        data=None
        with open(file_name) as f:
            data = f.read();
        return data

    def test_0036(self):
        changed_file = "/home/htran/test_index.po"
        new_changed_file = "/home/htran/test_index_new.po"
        data = self.readTextFile(changed_file)
        old_data = str(data)
        for k, v in self.pattern_list.items():
            # print("k:[{}], v:[{}]".format(k, v))
            data, number_of_changes = re.subn(k, v, data)
            if number_of_changes > 0:
                changed = True
                print("Pattern: [{}], replaced with: [{}]".format(k, v))

        has_language_code = (re.search(self.re_language_code, data) != None)
        if not has_language_code:
            for k, v in self.pattern_insert.items():
                data, number_of_changes = re.subn(k, v, data)
                if number_of_changes > 0:
                    changed = True
                    print("Pattern: [{}], replaced with: [{}]".format(k, v))

        if changed:
            self.writeTextFile(changed_file, data)
            print("Wrote changed to:", changed_file)

    def test_0037(self):
        t = "'to_space -- tới không gian' '%s' I'd to do it's and I'll là không hợp lệ khi chưa được cung cấp xương tư thế nào cả 'but this'"
        SNG_QUOTE = re.compile(r'[\']+([^\']+)[\']+(?!([\w]))')
        find_all_list = re.findall(SNG_QUOTE, t)
        pp(find_all_list)



    def test_0038(self):
        t = '''
To clear (the mask of areas) with (the (Lasso Mask) tool), first invert the mask,
(something glTF allows multiple animations per file, with animations targeted to particular objects at time of export. To ensure that an animation is included, either          (a) make it the active Action on the object, (b) create a single-strip NLA track, or (c) stash the action.
Camera: ``POINT`` or ``VIEW`` or ``VPORT`` or (wip: ``INSERT(ATTRIB+XDATA)``)
3D View: (wip: ``VIEW``, ``VPORT``)
            '''
        # p = re.compile(r'[\.\,\:\!](\s+)?')
        # part_list = p.split(t)
        # pp(part_list)
        part_list = split_into_sentences(t)
        pp(part_list)

    def test_0039(self):
        p = re.compile(r'(?!\s)([^\(\)]+)(?<!\s)')
        t = 'ABBREV (something: other)'
        found_text = p.findall(t)
        print(found_text)

        p = re.compile(r'([^\`]+)\s\-\-\s([^\<]+)(?<![\s])')
        t = 'REF -- and something <and/link>'
        found_text = p.findall(t)
        print(found_text)

        p = re.compile(r'(?!\s)([^\(\)\-\>]+)(?<!\s)')
        t = '''
        Góc Nhìn 3D (MENU 3D View) --> Cộng Thêm (Add) --> Khung Lưới (Mesh)
        '''
        found_text = p.findall(t)
        print(found_text)


    def test_0040(self):
        p = re.compile(r'\b[\w\-\_\']+\b')
        t = '''
        Góc Nhìn 3D (MENU 3D View) --> Cộng Thêm (Add) --> Khung Lưới (Mesh)
        '''
        word_list = p.findall(t)
        print(word_list)

    def patternMatchAllToDict(self, pat, text):
        matching_list = {}
        for m in pat.finditer(text):
            s = m.start()
            e = m.end()
            orig = m.group(0)
            k = (s, e)
            entry = {k: orig}
            matching_list.update(entry)
        return matching_list

    def test_0041(self):
        t = '''
        Góc Nhìn 3D (MENU 3D View) --> Cộng Thêm (Add) --> Khung Lưới (Mesh) --> And Add to (Mesh)
        and this one mesh at the end of menu item to add (mesh)
        '''
        str = re.escape('(Mesh)')
        p = re.compile(str, re.I)
        matching_dict = self.patternMatchAllToDict(p, t)
        print(matching_dict)

    def test_0042(self):
        wl = ['this', 'thinking', 'the']
        dd = {}
        for w in wl:
            dd.update({len(w): w})
        k_list = reversed(sorted(list(dd.keys())))

        v_list = []
        for k in k_list:
            print(k)
            v_list.append(dd[k])

        pp(v_list)

    def test_0043(self):
        t = {
            "#docs": "#tài liệu",
            "#today": "#hôm nay",
            "$xdg_config_home": "THƯ MỤC CẤU HÌNH GỐC của XDG",
            "%.2f fps": "%.2f khung hình/giây",
            "%.4g fps": "%.4g khung hình/giây",
            "%d %s mirrored": "%d %s được đối xứng",
            "%d %s mirrored, %d failed": "%d %s được đối xứng, %d bị thất bại"
        }

        dict = WCKLCIOrderedDict(t)
        # dict.update(t)
        # pp(dict.keys())
        print('Listing:')
        for k, v in dict.items():
            print(f'k:{k}; v:{v}')

        print('selective:')
        f_word=['#docs']
        select_set = dict.getSetUpToWordCount(3, first_word=f_word, is_reversed=True)
        for k, v in select_set.items():
            print(f'k:{k}; v:{v}')

    def test_0044(self):
        t = {
            "#docs": "#tài liệu",
            "#today": "#hôm nay",
            "$xdg_config_home": "THƯ MỤC CẤU HÌNH GỐC của XDG",
            "%.2f fps": "%.2f khung hình/giây",
            "%.4g fps": "%.4g khung hình/giây",
            "%d %s mirrored": "%d %s được đối xứng",
            "%d %s mirrored, %d failed": "%d %s được đối xứng, %d bị thất bại",
            "zoom in/out": "Thu-Phóng Vào/Ra",
            "zoom in/out in the view": "Thu-phóng vào/ra trong khung nhìn",
            "zoom in/out the background image": "Phóng to/thu nhỏ hình ảnh nền",
            "zoom in/out the image": "Thu nhỏ/phóng to hình ảnh",
            "zoom in/out the view": "Thu-Phóng vào/ra góc nhìn",
            "zoom keyframes": "Số Khung Khóa Thu-Phóng",
            "zoom method": "Phương Pháp Thu-Phóng",
            "zoom options": "Tùy Chọn về Thu-Phóng",
            "zoom out": "lùi xa ra, thu nhỏ",
            "zoom out eight zoom levels (:kbd:`numpadminus` -- eight times)": "Thu ra tám lần (bấm phím :kbd:`Dấu Trừ (-) Bàn Số (NumpadMinus)` -- tám lần)",
            "zoom out the image (centered around 2d cursor)": "Thu nhỏ hình ảnh (trung tâm là con trỏ 2D)",
            "zoom out the view": "Thu nhỏ góc nhìn",
            "zoom path": "Đường Dẫn cho Thu-Phóng",
            "zoom preview to fit in the area": "Thu-phóng vùng duyệt thảo cho khít vừa diện tích",
            "zoom ratio": "Tỷ Lệ Thu-Phóng",
            "zoom ratio, 1.0 is 1:1, higher is zoomed in, lower is zoomed out": "Tỷ lệ thu-phóng, 1.0 nghĩa là 1:1, lớn hơn nghĩa là phóng to gần vào, nhỏ hơn là thu nhỏ ra",
            "zoom region": "Thu-Phóng trên Khu Vực",
            "zoom seconds": "Số Giây Thu-Phóng",
            "zoom style": "Mốt Thu-Phóng",
            "zoom the sequencer on the selected strips": "Thu-phóng bộ phối hình trên các dải được chọn",
            "zoom the view in/out": "Thu-phóng vào/ra góc nhìn",
            "zoom to border": "Phóng vào Đường Ranh Giới",
            "zoom to frame type": "Kiểu Thu-Phóng vào Khung Hình",
            "zoom to mouse position": "Thu-Phóng vào Vị Trí của Chuột",
            "zoom to the maximum zoom level (hold :kbd:`numpadplus` or :kbd:`ctrl-mmb` or similar)": "Phóng vào đến mức tối đa (bấm và giữ xuống :kbd:`Dấu Cộng (+) Bàn Số (NumpadPlus)` hoặc :kbd:`Ctrl-NCG (MMB)` hoặc tương tự)",
            "zoom using opposite direction": "Thu-phóng dùng hướng nghịch chiều",
            "zoom view": "Thu Phóng Khung Nhìn",
            "zooming": "Thu-Phóng"
        }
        l = WCKLCIOrderedDict(t)
        # for k, v in t.items():
        #     word_list = k.split()
        #     first_word = word_list[0]
        #     wc = len(word_list)
        #     length = len(k)
        #     wc_dict_entry={(length, first_word): k}
        #     wc_key = f'{wc}'
        #     wc_dict = hasattr(l, wc_key)
        #     if not wc_dict:
        #         setattr(l, wc_key, {})
        #     wc_dict = getattr(l, wc_key)
        #     wc_dict.update(wc_dict_entry)

        print(l)
        k = 'zoom region'
        v = l[k]
        print(f'{k}; {v}')

        t = 'zoom region to #docs'
        tran = l.blindTranslation(t)
        print(f'{t}: {tran}')



        # set_2 = l.getWCDict(2)
        # for k, v in reversed(sorted(set_2.items())):
        #     print(f'{k}:{v}')
        print('Paused')


    def test_0045(self):
        t = {
            "#docs": "#tài liệu",
            "#today": "#hôm nay",
            "$xdg_config_home": "THƯ MỤC CẤU HÌNH GỐC của XDG",
            "%.2f fps": "%.2f khung hình/giây",
            "%.4g fps": "%.4g khung hình/giây",
            "%d %s mirrored": "%d %s được đối xứng",
            "%d %s mirrored, %d failed": "%d %s được đối xứng, %d bị thất bại",
            "zoom in/out": "Thu-Phóng Vào/Ra",
            "zoom in/out in the view": "Thu-phóng vào/ra trong khung nhìn",
            "zoom in/out the background image": "Phóng to/thu nhỏ hình ảnh nền",
            "zoom in/out the image": "Thu nhỏ/phóng to hình ảnh",
            "zoom in/out the view": "Thu-Phóng vào/ra góc nhìn",
            "zoom keyframes": "Số Khung Khóa Thu-Phóng",
            "zoom method": "Phương Pháp Thu-Phóng",
            "zoom options": "Tùy Chọn về Thu-Phóng",
            "zoom out": "lùi xa ra, thu nhỏ",
            "zoom out eight zoom levels (:kbd:`numpadminus` -- eight times)": "Thu ra tám lần (bấm phím :kbd:`Dấu Trừ (-) Bàn Số (NumpadMinus)` -- tám lần)",
            "zoom out the image (centered around 2d cursor)": "Thu nhỏ hình ảnh (trung tâm là con trỏ 2D)",
            "zoom out the view": "Thu nhỏ góc nhìn",
            "zoom path": "Đường Dẫn cho Thu-Phóng",
            "zoom preview to fit in the area": "Thu-phóng vùng duyệt thảo cho khít vừa diện tích",
            "zoom ratio": "Tỷ Lệ Thu-Phóng",
            "zoom ratio, 1.0 is 1:1, higher is zoomed in, lower is zoomed out": "Tỷ lệ thu-phóng, 1.0 nghĩa là 1:1, lớn hơn nghĩa là phóng to gần vào, nhỏ hơn là thu nhỏ ra",
            "zoom region": "Thu-Phóng trên Khu Vực",
            "zoom seconds": "Số Giây Thu-Phóng",
            "zoom style": "Mốt Thu-Phóng",
            "zoom the sequencer on the selected strips": "Thu-phóng bộ phối hình trên các dải được chọn",
            "zoom the view in/out": "Thu-phóng vào/ra góc nhìn",
            "zoom to border": "Phóng vào Đường Ranh Giới",
            "zoom to frame type": "Kiểu Thu-Phóng vào Khung Hình",
            "zoom to mouse position": "Thu-Phóng vào Vị Trí của Chuột",
            "zoom to the maximum zoom level (hold :kbd:`numpadplus` or :kbd:`ctrl-mmb` or similar)": "Phóng vào đến mức tối đa (bấm và giữ xuống :kbd:`Dấu Cộng (+) Bàn Số (NumpadPlus)` hoặc :kbd:`Ctrl-NCG (MMB)` hoặc tương tự)",
            "zoom using opposite direction": "Thu-phóng dùng hướng nghịch chiều",
            "zoom view": "Thu Phóng Khung Nhìn",
            "zooming": "Thu-Phóng",
            "should do": "Nên làm",
            "is": "Là/được",
            "what": 'Cái gì',
            "you": 'bạn',
            "on": "trên, tại"
        }
        dic = WCKLCIOrderedDict(t)

        part_list = []
        # msg = 'zoom out on zoom view is what you should do'
        msg = ' is '
        # t = 'z-buffer input, but could also be a (grayscale) image used as a mask, or a single value input'
        print(t)

        wordsep = re.compile(r'[^\ ]+', re.I)
        loc_dic = getLocationList(wordsep, msg)
        print(loc_dic)

        # word_list = t.split(' ')
        loc_key = list(loc_dic.keys())
        print(loc_key)
        # exit(0)

        max_len = len(loc_dic)

        print(f'max_len:{max_len}')
        step = 1
        is_finished = False
        while not is_finished:
            for i in range(0, max_len):
                l=[]
                for k in range(i, min(i+step, max_len)):
                    loc = loc_key[k]
                    # print(f'step:{step}; i:{i}; k:{k}, loc:{loc}')
                    l.append(loc_key[k])

                s = []
                for loc in l:
                    word = loc_dic[loc]
                    s.append(word)
                t = " ".join(s)
                print(f's location:{l}, text:{t}')

                s_len = len(s)
                ss = l[0][0]
                ee = l[s_len-1][1]
                k = (len(t), ee)
                v = ((ss, ee), t)
                entry=(k, v)
                is_in = (entry in part_list)
                if not is_in:
                    part_list.append(entry)
            step += 1
            is_finish = (step > max_len)
            if is_finish:
                break

        sorted_partlist = list(reversed(sorted(part_list)))
        text_dic = OrderedDict()
        for e in sorted_partlist:
            k, v = e
            dict_entry = {k: v}
            text_dic.update(dict_entry)

        print('-' * 30)
        PP(text_dic)

        translated_dic = OrderedDict()
        for k, v in text_dic.items():
            loc, orig_sub_text = v
            has_tran = (orig_sub_text in dic)
            if not has_tran:
                continue
            tran_sub_text = dic[orig_sub_text]
            ss, ee = loc
            entry = {ee: (ss, ee, tran_sub_text)}
            translated_dic.update(entry)

        print('-' * 30)
        sored_translated = list(reversed(sorted(translated_dic.items())))
        PP(sored_translated)
        print(msg)

        tran_msg = str(msg)
        for k, v in sored_translated:
            ss, ee, tran_sub_text = v
            left = tran_msg[:ss]
            right = tran_msg[ee:]
            tran_msg = left + tran_sub_text + right
        print('-' * 30)
        print(tran_msg)

    def getOverlap(self, a, b):
        return max(0, min(a[1], b[1]) - max(a[0], b[0]))

    from operator import itemgetter, attrgetter, methodcaller

    def test_0046(self):
        def distKey(x):
            dist = (x[1] - x[0])
            return dist
        def removeOverlapped(loc_list, len):
            sample_str = (" "*len)
            marker='¶'
            len_list = []
            # for loc in loc_list:
            #     length = (loc[1] - loc[0])
            #     key = (length, loc)
            #     len_list.append(key)
            sorted_loc = sorted(loc_list, key=lambda x: x[1]-x[0], reverse=True )
            # sorted_loc = sorted_len_list
            # sorted_loc = []
            # for k_loc in sorted_len_list:
            #     key, loc = k_loc
            #     sorted_loc.append(loc)

            retain_l = []
            for loc in sorted_loc:
                substr = sample_str[loc[0]:loc[1]]
                is_overlapped = (marker in substr)
                if not is_overlapped:
                    maker_substr = (marker * (loc[1] - loc[0]))
                    left_part = sample_str[:loc[0]]
                    right_part = sample_str[loc[1]:]
                    sample_str = left_part + maker_substr + right_part
                    retain_l.append(loc)
            # sorted_retain_l = list(reversed(sorted(retain_l)))
            # return sorted_retain_l
            return retain_l

        l = [(0, 63), (4, 10), (11, 13), (14, 21), (22, 25), (26, 32), (26, 126), (33, 41), (42, 44), \
             (45, 53), (45, 63), (54, 63), (64, 67), (64, 126), (68, 78), (68, 89), (83, 89), (90, 92), (96, 102), \
             (103, 107), (108, 113), (114, 126), (117, 126), (127, 132), (127, 251), (138, 143), (144, 146), \
             (147, 155), (147, 164), (156, 164), (165, 168), (176, 186), (187, 191), (192, 198), (205, 207), (208, 212), (228, 230), (245, 251)]

        retain_l = removeOverlapped(l, 251)
        print(sorted(retain_l))


    def test_0047(self):
        COMMON_SENTENCE_BREAKS = re.compile(r'(?!\s)([^\.\,\:\!]+)\s?(?<!\s)')
        t = "A new Blender version is targeted to be released every 3 months. The actual `release cycle <https://wiki.blender.org/wiki/Process/Release_Cycle>`__ for a specific release is longer, and overlaps the previous and next release cycle."
        text_list = self.patternMatchAllToDict(COMMON_SENTENCE_BREAKS, t)
        for loc, text in text_list.items():
            print(f'{loc} = [{text}]')

    def test_0048(self):
        MSG_WITH_ID_PATTERN = re.compile(r'(msgid|msgstr)\s"(.*)"')
        # p = re.compile(r'((?<![\\])[\'\"])((?:.(?!(?<![\\])\1))*.?)\1')
        # p = re.compile(r'((?<![\\])[\'"])((?:.(?!(?<![\\])\1))*.?)\1')
        # p = re.compile(r'((?<![\\])[\'"])((?:.)*.?)\1')
        # p = re.compile(r'((msgid|msgstr)\s((?<![\\])[\'"])"(.?)"')
        p = re.compile(r'"(?:[^\\"]|\\.)*"')
        t = '''
        # SOME DESCRIPTIVE TITLE.# Copyright (C) : This page is licensed under a CC-BY-SA 4.0 Int. License# This file is distributed under the same license as the Blender 2.79 Manual# package.# Hoang Duy Tran <hoangduytran1960@gmail.com>, 2018.##, fuzzymsgid ""msgstr """Project-Id-Version: Blender 2.79 Manual 2.79\n""Report-Msgid-Bugs-To: \n""POT-Creation-Date: 2020-06-01 12:14+1000\n""PO-Revision-Date: 2020-06-14 04:43+0100\n""Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>\n""Language: vi\n""Language-Team: London, UK <hoangduytran1960@gmail.com>\n""Plural-Forms: nplurals=1; plural=0\n""MIME-Version: 1.0\n""Content-Type: text/plain; charset=utf-8\n""Content-Transfer-Encoding: 8bit\n""Generated-By: Babel 2.8.0\n"#: ../../manual/about/index.rst:5msgid "Contribute Documentation"msgstr "Đóng Góp Tài Liệu -- Contribute Documentation"#: ../../manual/about/index.rst:7msgid "The Blender Manual is a community driven effort to which anyone can contribute. Whether you like to fix a tiny spelling mistake or rewrite an entire chapter, your help with the Blender manual is most welcome!"msgstr "Bản Hướng Dẫn Sử Dụng Blender là một cố gắng do cộng đồng điều vận và ai ai cũng có thể đóng góp phần mình vào được. Cho dù bạn muốn sửa đổi một lỗi đánh vần nhỏ, hoặc muốn viết lại toàn bộ nội dung của một chương đi chăng nữa, thì sự giúp đỡ của bạn với bản Hướng Dẫn Sử Dụng Blender cũng sẽ rất được hoan nghênh!"#: ../../manual/about/index.rst:11msgid "If you find an error in the documentation, please `report the problem <https://developer.blender.org/maniphest/task/edit/form/default/?project=PHID-PROJ-c4nvvrxuczix2326vlti>`__"msgstr "Nếu bạn tìm thấy một lỗi nào đó trong bản tài liệu thì xin làm ơn `báo cáo vấn đề -- report the problem <https://developer.blender.org/maniphest/task/edit/form/default/?project=PHID-PROJ-c4nvvrxuczix2326vlti>`__ cho chúng tôi biết"#: ../../manual/about/index.rst:14msgid "Get involved in discussions through the any of the project `Contacts`_"msgstr "Xin bạn hãy tham gia các cuộc bàn luận thông qua các `Đầu Mối Liên Lạc -- Contacts`_ của đề án"#: ../../manual/about/index.rst:20msgid "Getting Started"msgstr "Khởi Đầu -- Getting Started"#: ../../manual/about/index.rst:22msgid "The following guides lead you through the process."msgstr "Hướng dẫn sau đây sẽ dẫn dắt bạn qua toàn bộ quá trình."#: ../../manual/about/index.rst:35msgid "Guidelines"msgstr "Hướng Dẫn -- Guidelines"#: ../../manual/about/index.rst:46msgid "Translations"msgstr "Phiên Dịch -- Translations"#: ../../manual/about/index.rst:58msgid "Contacts"msgstr "Mối Liên Lạc -- Contacts"#: ../../manual/about/index.rst:60msgid "`Project Page <https://developer.blender.org/project/profile/53/>`__."msgstr "`Trang Của Đề Án -- Project Page <https://developer.blender.org/project/profile/53/>`__."#: ../../manual/about/index.rst:61msgid "An overview of the documentation project."msgstr "Một số khái quá về đề án viết tài liệu."#: ../../manual/about/index.rst:62msgid "`Mailing list <https://lists.blender.org/mailman/listinfo/bf-docboard>`__"msgstr "`Danh Sách Liên Lạc Thư Điện Tử -- Mailing list <https://lists.blender.org/mailman/listinfo/bf-docboard>`__"#: ../../manual/about/index.rst:63msgid "A mailing list for discussing ideas, and keeping track of progress."msgstr "Một bản danh sách liên lạc qua thư từ để bàn bạc các ý tưởng, đồng thời cũng là nơi để theo dõi sự tiến triển của của chúng."#: ../../manual/about/index.rst:65msgid "`Devtalk <https://devtalk.blender.org/c/documentation/12>`__"msgstr "`Trò Chuyện về Xây Dựng Phần Mềm -- Devtalk <https://devtalk.blender.org/c/documentation/12>`__"#: ../../manual/about/index.rst:65msgid "A forum based discussions on writing and translating documentation. This includes the user manual, wiki, release notes, and code docs."msgstr "Bàn luận trên diễn đàn về viết và dịch tài liệu. Tài liệu ở đây bao gồm bản hướng dẫn sử dụng, trang bách khoa toàn thư mở wiki, các các tài liều về mã nguồn."#: ../../manual/about/index.rst:67msgid ":ref:`blender-chat`"msgstr ""#: ../../manual/about/index.rst:68msgid "``#docs`` channel for informal discussions in real-time."msgstr "Kênh ``#docs`` (*tài liệu*) là kênh dùng cho các cuộc bàn bạc thân thiện, không chính thức, thời gian thật."#: ../../<generated>:1msgid "`Project Workboard <https://developer.blender.org/project/board/53/>`__"msgstr "`Bảng Phân Công Nhiệm Vụ Của Đề Án -- Project Workboard <https://developer.blender.org/project/board/53/>`__"#: ../../manual/about/index.rst:70msgid "Manage tasks such as bugs, todo lists, and future plans."msgstr "Quản lý các nhiệm vụ, như các lỗi trong phần mềm, danh sách những việc cần làm, và các kế hoạch trong tương lai."
getMsgAsDict:{(251, 4678): '""msgstr """Project-Id-Version: Blender 2.79 Manual 2.79\\n""Report-Msgid-Bugs-To: \\n""POT-Creation-Date: 2020-06-01 12:14+1000\\n""PO-Revision-Date: 2020-06-14 04:43+0100\\n""Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>\\n""Language: vi\\n""Language-Team: London, UK <hoangduytran1960@gmail.com>\\n""Plural-Forms: nplurals=1; plural=0\\n""MIME-Version: 1.0\\n""Content-Type: text/plain; charset=utf-8\\n""Content-Transfer-Encoding: 8bit\\n""Generated-By: Babel 2.8.0\\n"#: ../../manual/about/index.rst:5msgid "Contribute Documentation"msgstr "Đóng Góp Tài Liệu -- Contribute Documentation"#: ../../manual/about/index.rst:7msgid "The Blender Manual is a community driven effort to which anyone can contribute. Whether you like to fix a tiny spelling mistake or rewrite an entire chapter, your help with the Blender manual is most welcome!"msgstr "Bản Hướng Dẫn Sử Dụng Blender là một cố gắng do cộng đồng điều vận và ai ai cũng có thể đóng góp phần mình vào được. Cho dù bạn muốn sửa đổi một lỗi đánh vần nhỏ, hoặc muốn viết lại toàn bộ nội dung của một chương đi chăng nữa, thì sự giúp đỡ của bạn với bản Hướng Dẫn Sử Dụng Blender cũng sẽ rất được hoan nghênh!"#: ../../manual/about/index.rst:11msgid "If you find an error in the documentation, please `report the problem <https://developer.blender.org/maniphest/task/edit/form/default/?project=PHID-PROJ-c4nvvrxuczix2326vlti>`__"msgstr "Nếu bạn tìm thấy một lỗi nào đó trong bản tài liệu thì xin làm ơn `báo cáo vấn đề -- report the problem <https://developer.blender.org/maniphest/task/edit/form/default/?project=PHID-PROJ-c4nvvrxuczix2326vlti>`__ cho chúng tôi biết"#: ../../manual/about/index.rst:14msgid "Get involved in discussions through the any of the project `Contacts`_"msgstr "Xin bạn hãy tham gia các cuộc bàn luận thông qua các `Đầu Mối Liên Lạc -- Contacts`_ của đề án"#: ../../manual/about/index.rst:20msgid "Getting Started"msgstr "Khởi Đầu -- Getting Started"#: ../../manual/about/index.rst:22msgid "The following guides lead you through the process."msgstr "Hướng dẫn sau đây sẽ dẫn dắt bạn qua toàn bộ quá trình."#: ../../manual/about/index.rst:35msgid "Guidelines"msgstr "Hướng Dẫn -- Guidelines"#: ../../manual/about/index.rst:46msgid "Translations"msgstr "Phiên Dịch -- Translations"#: ../../manual/about/index.rst:58msgid "Contacts"msgstr "Mối Liên Lạc -- Contacts"#: ../../manual/about/index.rst:60msgid "`Project Page <https://developer.blender.org/project/profile/53/>`__."msgstr "`Trang Của Đề Án -- Project Page <https://developer.blender.org/project/profile/53/>`__."#: ../../manual/about/index.rst:61msgid "An overview of the documentation project."msgstr "Một số khái quá về đề án viết tài liệu."#: ../../manual/about/index.rst:62msgid "`Mailing list <https://lists.blender.org/mailman/listinfo/bf-docboard>`__"msgstr "`Danh Sách Liên Lạc Thư Điện Tử -- Mailing list <https://lists.blender.org/mailman/listinfo/bf-docboard>`__"#: ../../manual/about/index.rst:63msgid "A mailing list for discussing ideas, and keeping track of progress."msgstr "Một bản danh sách liên lạc qua thư từ để bàn bạc các ý tưởng, đồng thời cũng là nơi để theo dõi sự tiến triển của của chúng."#: ../../manual/about/index.rst:65msgid "`Devtalk <https://devtalk.blender.org/c/documentation/12>`__"msgstr "`Trò Chuyện về Xây Dựng Phần Mềm -- Devtalk <https://devtalk.blender.org/c/documentation/12>`__"#: ../../manual/about/index.rst:65msgid "A forum based discussions on writing and translating documentation. This includes the user manual, wiki, release notes, and code docs."msgstr "Bàn luận trên diễn đàn về viết và dịch tài liệu. Tài liệu ở đây bao gồm bản hướng dẫn sử dụng, trang bách khoa toàn thư mở wiki, các các tài liều về mã nguồn."#: ../../manual/about/index.rst:67msgid ":ref:`blender-chat`"msgstr ""#: ../../manual/about/index.rst:68msgid "``#docs`` channel for informal discussions in real-time."msgstr "Kênh ``#docs`` (*tài liệu*) là kênh dùng cho các cuộc bàn bạc thân thiện, không chính thức, thời gian thật."#: ../../<generated>:1msgid "`Project Workboard <https://developer.blender.org/project/board/53/>`__"msgstr "`Bảng Phân Công Nhiệm Vụ Của Đề Án -- Project Workboard <https://developer.blender.org/project/board/53/>`__"#: ../../manual/about/index.rst:70msgid "Manage tasks such as bugs, todo lists, and future plans."msgstr "Quản lý \\"các nhiệm vụ\\", như các lỗi trong phần mềm, danh sách những việc cần làm, và các kế hoạch trong tương lai."
                 

        '''
        # all_list = self.patternMatchAllToDict(MSG_WITH_ID_PATTERN, t)
        all_list = self.patternMatchAllToDict(p, t)
        print(all_list)
        exit(0)
        result_dict = {}
        count=0
        entry=None
        msgid_part = msgstr_part = None
        for loc, v in all_list.items():
            msg = v[1:-1]
            msg = msg.replace('"', '\\"')
            msg = msg.replace("'", "\\'")
            is_even_line_index = (count % 2 == 0)
            if is_even_line_index:
                msgid_part = msg
            else:
                msgstr_part = msg
                entry = {msgid_part: msgstr_part}
                result_dict.update(entry)
            count += 1

        print(result_dict)



    def test_0049(self):
        def cleanForward(txt, pair_dict, leading_set):
            temp_txt = str(txt)
            count = 0
            for sym_on in leading_set:
                is_sym_on_in_dict = (sym_on in pair_dict)
                if not is_sym_on_in_dict:
                    continue

                sym_off = pair_dict[sym_on]
                temp = temp_txt[1:]
                is_balance = isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                leading_set = leading_set[count:]
            return temp_txt, leading_set

        def cleanBackward(txt, pair_dict, trailing_set):
            temp_txt = str(txt)
            count = 0
            for sym_off in reversed(trailing_set):
                is_controlled = (sym_off in pair_dict)
                if not is_controlled:
                    temp_txt = temp_txt[:-1]
                    count += 1
                    continue

                sym_on = pair_dict[sym_off]
                temp = temp_txt[:-1]
                is_balance = isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                trailing_set = trailing_set[:-count]
            return temp_txt, trailing_set

        def cleanBothEnds(txt, pair_dict, leading_set, trailing_set):
            count = 0
            temp_txt = str(txt)
            symbol_set = leading_set + trailing_set
            for sym_on in symbol_set:
                is_sym_off_there = (sym_on in pair_dict)
                if not is_sym_off_there:
                    break

                sym_off = pair_dict[sym_on]
                is_both_ends = (temp_txt.startswith(sym_on) and temp_txt.endswith(sym_off))
                if not is_both_ends:
                    continue

                temp = temp_txt[1:-1]
                is_balance = isBalancedSymbol(sym_on, sym_off, temp)
                if is_balance:
                    temp_txt = temp
                    count += 1
            if count > 0:
                leading_set = leading_set[count:]
                trailing_set = trailing_set[:-count]
            return temp_txt, leading_set, trailing_set

        txt = '   ({this}....,!'
        txt = '(also :kbd:`Shift-W` :menuselection:`--> (Locked, ...)`) This will prevent all editing of the bone in *Edit Mode*; see :ref:`bone locking <animation_armatures_bones_locking>`'
        txt = '(Top/Side/Front/Camera...)'
        txt = '**this**'
        txt = "'I'd like to have this cleaned'"
        txt = txt.strip()

        pair_list = [('{', '}'), ('[', ']'), ('(', ')'), ('<', '>'), ('$', '$'),(':', ':'), ('*', '*'), ('\'', '\''), ('"', '"'), ('`', '`'),]
        pair_dict = {}
        for p in pair_list:
            s, e = p
            entry_1 = {s:e}
            entry_2 = {e:s}
            pair_dict.update(entry_1)
            pair_dict.update(entry_2)

        leading_set = REMOVABLE_SYMB_FULLSET_FRONT.findall(txt)
        if leading_set:
            leading_set = leading_set[0]

        trailing_set = REMOVABLE_SYMB_FULLSET_BACK.findall(txt)
        if trailing_set:
            trailing_set = trailing_set[0]

        temp_txt = str(txt)
        temp_txt, leading_set, trailing_set = cleanBothEnds(temp_txt, pair_dict, leading_set, trailing_set)

        temp_txt, leading_set = cleanForward(temp_txt, pair_dict, leading_set)
        temp_txt, trailing_set = cleanBackward(temp_txt, pair_dict, trailing_set)

        temp_txt, _, _ = cleanBothEnds(temp_txt, pair_dict, leading_set, trailing_set)
        print(f'temp_txt:[{temp_txt}]')

    def test_0050(self):
        quoted_msg = re.compile(r'((?<![\\])[\'"])((?:.)*.?)')
        text = '2.2 An :ref:`Object Selector <ui-eyedropper>` to select an object (usually an empty), which position and rotation will be used to define mirror planes (instead of using the ones from the modified object) $1,200.00.'
        #s_pat = re.compile(r'(?<!\w\.\w.)(?<!\w\.)(?<=\.|\?)\s')
        # s_pat = re.compile(r'(?<![\.\,]\w)((?:.)*.?)')\
        # t_list = re.split(r'(?<=[^\w]\.[.?]) +(?=[\w])', t)
        # t_list = s_pat.findall(t)
        # s_pat = re.compile(r'([^\.\,]+)')
        # t_list = patternMatchAllToDict(s_pat, t)
        t_list = re.findall(r'\S+([\,\.]\S+)', text)
        # t_list = re.split('(?<!\w[\.\,]\w.)(?<![\w\d]\.)(?<=\.|\,|\?)(\s|[A-Z].*)',text)
        # t_list = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', text)
        print(t_list)
        # text = ":abbr:`CSG (Constructive solid geometry: Hình Học Lập Thể [Đặc] Suy Diễn)`"
        # ABBREV_PATTERN_PARSER = re.compile(r':abbr:[\`]+([^(]+)\s\(([^\)]+)(:[^\)]+)?\)[\`]+')
        # abbrev_dic = patternMatchAllAsDictNoDelay(ABBREV_PATTERN_PARSER, text)
        # # t_list = ABBREV_PATTERN_PARSER.findall(text)
        #
        # abbrev_list = list(abbrev_dic.items())
        # orig = abbrev_list[0]
        # loc, txt = orig
        # print(f'{orig}\n{loc}\n{txt}\n')
        #
        # orig = abbrev_list[1]
        # loc, txt = orig
        # print(f'{orig}\n{loc}\n{txt}\n')
        #
        # orig = abbrev_list[2]
        # loc, txt = orig
        # print(f'{orig}\n{loc}\n{txt}\n')

    def test_0051(self):
        print('Import OK')
        txt = ''':abbr:`SDLS (Selective Damped Least Square)`'''
        tran = tranRef(txt, False)
        print(f'tran is:{tran}')

    def test_0052(self):
        txt = 'Đảo Ngược Tầm Nhìn của Face Set'
        find_pattern = re.compile("Face\ Set")
        sub_pattern = "Bề\ Mặt\ Ấn\ Định"
        find_list = patternMatchAllToDict(find_pattern, txt)
        new_txt, count = find_pattern.subn(sub_pattern, txt)
        print(new_txt)
        # print(find_list)

    def test_0053(self):
        common_ending_list = sorted([
            'ing','ed', 'est', 'er',
            'ies','ly', 'es', 's', 'y',
            'ble', 'ion', 'ful', 'ess'
        ])
        common_ending_list_sorted = sorted(common_ending_list, key=lambda x: len(x), reverse=True)
        common_ending_pattern_list = []
        print(common_ending_list_sorted)

        st = LancasterStemmer()
        for txt in common_ending_list_sorted:
            pat = r'(%s)$' % txt
            common_ending_pattern_list.append(re.compile(pat, flags=re.I))

        test_text = [
            "This is fully practically better prettiest ",
            "general and generalisation communication actually factually",
        ]
        for text_line in test_text:
            word_list = word_tokenize(text_line)
            for word in word_list:
                root_word = st.stem(word)
                print(f'{word} => {root_word}')

            # for word in word_list:
            #     for pat in common_ending_pattern_list:
            #         root_word, count = pat.subn('', word)
            #         is_replaced = (count > 0)
            #         if is_replaced:
            #             print(f'{word} => {root_word}')
            #             break
            #         # root_word = st.stem(word)

    def test_0054(self):
        dic = {
            'err': ['e', 'y', 'ee', 'ear', 'er',],
            'ier': ['y','e','er','a','ie',]
        }
        home_dir = os.environ['HOME']
        test_file = os.path.join(home_dir, 'testing.json')

        writeJSON(test_file, dic)

    def test_0055(self):
        def sort_list_value(dic):
            new_dic = OrderedDict()
            for k, v in dic.items():
                v = list(sorted(v, key=lambda x: len(x), reverse=False))
                entry = {k: v}
                new_dic.update(entry)
            return new_dic

        home_dir = os.environ['DEV_TRAN']
        test_file1 = os.path.join(home_dir, 'blender_manual/prefix_and_filler.json')
        test_file2 = os.path.join(home_dir, 'blender_manual/suffix_transform.json')
        test_out_file = os.path.join(home_dir, 'testing.json')

        dic = readJSON(test_file1)

        sorting = sorted(list(dic.items()))
        sorted_list = list(sorted(sorting, key=lambda x: len(x[0]), reverse=False))
        dic = OrderedDict(sorted_list)
        sorted_dic = sort_list_value(dic)
        writeJSON(test_file1, sorted_dic)

        dic = readJSON(test_file2)
        sorting = sorted(list(dic.items()))
        sorted_list = list(sorted(sorting, key=lambda x: len(x[0]), reverse=False))
        dic = OrderedDict(sorted_list)
        sorted_dic = sort_list_value(dic)
        writeJSON(test_file2, sorted_dic)

        # PP(dic)

    def test_0056(self):
        home_dir = os.environ['DEV_TRAN']
        test_file1 = os.path.join(home_dir, 'blender_manual/ref_dict_backup_0005.json')
        test_out_file = os.path.join(home_dir, 'testing.json')

        dic = readJSON(test_file1)

        sorting = sorted(list(dic.items()))
        sorted_list = list(sorted(sorting, key=lambda x: len(x[0]), reverse=False))
        sorted_dic = OrderedDict(sorted_list)
        writeJSON(test_file1, sorted_dic)

    # /Users/hoangduytran/blender_manual/sorted_temp05.json
    def test_0057(self):
        home_dir = os.environ['DEV_TRAN']
        to_file = os.path.join(home_dir, 'blender_manual/ref_dict_0006.json')
        from_file = os.path.join(home_dir, 'blender_manual/sorted_temp05.json')

        from_dic = readJSON(from_file)
        to_dic = readJSON(to_file)

        del_list=[]
        for f_k, f_v in from_dic.items():
            is_in_target = (f_k in to_dic)
            if is_in_target:
                t_v = to_dic[f_k]
                is_diff = (f_v and (f_v.lower() != t_v.lower()))
                if is_diff:
                    print('-' * 30)
                    print(f'from:{f_v}')
                    print(f'to:{t_v}')
                else:
                    del_list.append(f_k)

        is_updated = (len(del_list) > 0)
        for f_k in del_list:
            print(f'del:{f_k}')
            del from_dic[f_k]

        if is_updated:
            writeJSON(from_file, from_dic)


        # sorting = sorted(list(dic.items()))
        # sorted_list = list(sorted(sorting, key=lambda x: len(x[0]), reverse=False))
        # sorted_dic = OrderedDict(sorted_list)
        # writeJSON(test_file1, sorted_dic)

    def resort_dictionary(self):
        home_dir = os.environ['BLENDER_GITHUB']
        from_file = os.path.join(home_dir, 'ref_dict_0006_0003.json')
        to_file = os.path.join(home_dir, 'ref_dict_0006_0002.json')

        to_dic = readJSON(from_file)
        # l_case_dic = {}
        # clean_dic = {}
        # for k, v in to_dic.items():
        #     l_k = k.lower()
        #     is_in = (l_k in l_case_dic)
        #     if is_in:
        #         old_val = to_dic[k]
        #         print(f'duplicated: [{k}] with old_val:[{old_val}]; new_val[{v}]')
        #
        #     l_v = v.lower()
        #     l_entry = {l_k: l_v}
        #     l_case_dic.update(l_entry)
        #
        #     entry = {k: v}
        #     clean_dic.update(entry)
        #
        # sorting = sorted(list(l_case_dic.items()), key=lambda x: x[0].lower())
        # new_dic = OrderedDict(sorting)
        # out_file = os.path.join(home_dir, 'temp_dict.json')
        # writeJSON(out_file, new_dic)
        #
        # sorting = sorted(list(clean_dic.items()), key=lambda x: x[0].lower())
        # new_dic = OrderedDict(sorting)
        # writeJSON(to_file, new_dic)

        sorting = sorted(list(to_dic.items()), key=lambda x: x[0].lower())
        new_dic = OrderedDict(sorting)

        for t_k, t_v in to_dic.items():
            entry = {t_k: t_v}
            new_dic.update(entry)

        sorting = sorted(list(new_dic.items()), key=lambda x: x[0].lower())
        new_dic = OrderedDict(sorting)

        writeJSON(to_file, new_dic)

    # from leven import levenshtein as LEV
    def test_0059(self):
        class DelRecord(list):
            def __init__(self):
                self.file_name = None

            def show(self):
                count = len(self)
                if count == 0:
                    return

                print(f'file_name:{self.file_name}')
                print('-'*80)
                for entry in self:
                    dist, sim, msgid, msgstr, translated = entry
                    print(f'dist:{dist}, sim:{sim}')
                    print(f'msgid "{msgid}"')
                    print(f'msgstr "{msgstr}"')
                    if translated:
                        print(f'{translated}')
                    print('-'*10)


        home_dir = os.environ['DEV_TRAN']
        from_path = os.path.join(home_dir, 'blender_docs/locale/vi/LC_MESSAGES')

        untran_pat = re.compile(r'^(\s)?[\-]{2}\s')
        tran_pat = re.compile(r'(\w+)\s([\-]{2})\s(\w+)')
        vn_char_tbl = [
            'à', 'á', 'ả', 'ã', 'ạ',
            'â', 'ầ', 'ấ', 'ẩ', 'ẫ', 'ậ',
            'ă', 'ằ', 'ắ', 'ẳ', 'ẵ', 'ặ',
            'è', 'é', 'ẹ', 'ẻ', 'ẽ', 'ẹ',
            'ê', 'ề', 'ế', 'ệ', 'ể', 'ễ', 'ệ',
            'í', 'ì', 'ỉ', 'ĩ', 'ị',
            'ò', 'ó', 'ỏ', 'õ', 'ọ',
            'ô', 'ồ', 'ố', 'ổ', 'ỗ', 'ộ',
            'ơ', 'ờ', 'ớ', 'ở', 'ỡ', 'ợ',
            'ù', 'ú', 'ủ', 'ũ', 'ụ',
            'ư', 'ừ', 'ứ', 'ử', 'ữ', 'ự',
            'đ',
        ]

        acceptable_v = [
            "Khe -- Slot",
            "Phim -- Movie",
            "Lia -- Pan",
            "Sin -- Sinusoidal",
            "Sin -- Sine",
            "Chia -- Divide",
            "Phim -- Film",
            "Gaus -- Gaussian",
            "THTQXMT -- AO",
            "Chung Chung -- General",
            "Newton -- Newtonian",
            "Lang Thang -- Wander",
            "Xa -- Far",
            "Xoay Quatenion -- Quaternion Rotation",
            "các UV -- UVs",
            "Cos -- Cosine",
            "Fresnen -- Fresnel",
            "Loa -- Speaker",
            "Quanh Khung Phim -- Around Frame",
            "XYZ sang RGB -- XYZ to RGB",
            "Phim Video -- Videos",
        ]

        special_cases = {
            "Copy :kbd:`Ctrl-C`": "Sao -- Copy :kbd:`Ctrl-C`"
        }

        def count_similar(k, v):
            return SM(None, k, v).ratio()

        def has_vietnamese_char(v):
            v_lower = v.lower()
            for c in v_lower:
                is_vn_char = (c in vn_char_tbl)
                if is_vn_char:
                    return True
            return False

        for root, dirnames, filenames in os.walk(from_path):
            if root.startswith('.'):
                continue

            for filename in filenames:
                is_found  = (filename.lower().endswith('.po'))
                if not is_found:
                    continue

                is_updated = False
                del_rec = DelRecord()
                po_path = os.path.join(root, filename)
                del_rec.file_name = po_path
                po_cat = c.load_po(po_path)
                for m in po_cat:
                    k = m.id
                    if not k:
                        continue

                    k_len = len(k)
                    v = m.string
                    if not v:
                        continue

                    has_vn_char = has_vietnamese_char(v)
                    dist = LEV(k, v)
                    sim_ratio = count_similar(k, v)
                    too_similar = (sim_ratio > 0.8)
                    no_diff = (dist == 0) or too_similar
                    k_not_translated = (untran_pat.search(v) is not None)
                    k_translated = (tran_pat.search(v) is not None)
                    is_v_english_ascii = (v.isascii())
                    translated = (k_translated and not too_similar) and not is_v_english_ascii
                    # is_del_k = (no_diff or is_v_english_ascii or k_not_translated) and not translated
                    is_acceptable = (v in acceptable_v)
                    is_secial_case = (k in special_cases)
                    if is_secial_case:
                        special_v = special_cases[k]
                        is_secial_case = (v.lower() == special_v.lower())

                    is_del_k = (no_diff or is_v_english_ascii or k_not_translated) and \
                               (not (translated or has_vn_char)) and not (is_acceptable or is_secial_case)

                    # is_debug = ('before the first' in k)
                    # if is_debug:
                    #     _('Debug')
                    #
                    if not is_del_k:
                        continue

                    m.string = ""
                    if m.fuzzy:
                        m.flags = set() # clear the fuzzy flags

                    if translated:
                        entry = (dist, sim_ratio, k, v, 'TRANSLATED')
                    else:
                        entry = (dist, sim_ratio, k, v, '')
                    del_rec.append(entry)

                is_updated = (len(del_rec) > 0)
                if is_updated:
                    local_time = timezone(TIME_ZONE)
                    time_now = local_time.localize(datetime.datetime.now())
                    po_cat.revision_date = time_now
                    po_cat.last_translator = YOUR_ID
                    po_cat.language_team = YOUR_TRANSLATION_TEAM

                    # temp_dir = os.path.join(home_dir, "temp")
                    # from_path = os.path.join(temp_dir, filename)
                    c.dump_po(po_path, po_cat)
                    del_rec.show()
                    print(f'OUTPUT:{po_path}')

    def test_0060(self):
        class WordRecord(list):
            def __init__(self):
                self.file_name = None

            def show(self):
                count = len(self)
                if count == 0:
                    return

                print(f'file_name:{self.file_name}')
                print('-'*80)
                for entry in self:
                    msgid, not_word_list = entry
                    print(f'msgid "{msgid}"')
                    print(f'not_word_list "{not_word_list}"')
                    print('-'*10)


        home_dir = os.environ['DEV_TRAN']
        from_path = os.path.join(home_dir, 'blender_docs/locale/vi/LC_MESSAGES')
        WORD_SEP = re.compile(r'[\s\;\:\.\,\/\!\-\_\<\>\(\)\`\*\"\|\']')
        SYMBOLS = re.compile(r'^[\W\s]+$')
        en_us = ENC.Dict('en_US')

        for root, dirnames, filenames in os.walk(from_path):
            if root.startswith('.'):
                continue

            for filename in filenames:
                is_found  = (filename.lower().endswith('.po'))
                if not is_found:
                    continue

                is_updated = False
                word_rec = WordRecord()
                po_path = os.path.join(root, filename)
                word_rec.file_name = po_path
                po_cat = c.load_po(po_path)
                not_word_list=None
                for m in po_cat:
                    k = m.id
                    if not k:
                        continue

                    word_list = WORD_SEP.split(k)
                    not_word_list = []
                    for word in word_list:
                        try:
                            is_in_dict = en_us.check(word)
                            is_symbols = (SYMBOLS.search(word) is not None)
                            is_ignored = (is_in_dict or is_symbols)
                            if not is_ignored:
                                not_word_list.append(word)
                        except Exception as e:
                            continue

                    if not_word_list:
                        entry= (k, not_word_list)
                        word_rec.append(entry)
                if len(word_rec) > 0:
                    word_rec.show()




    def test_0062(self):
        import nltk
        from nltk.stem import WordNetLemmatizer as LEM
        from nltk.corpus import wordnet

        lem = LEM()

        def pos_tagger(nltk_tag: str):
            if nltk_tag.startswith('J'):
                return wordnet.ADJ
            elif nltk_tag.startswith('V'):
                return wordnet.VERB
            elif nltk_tag.startswith('N'):
                return wordnet.NOUN
            elif nltk_tag.startswith('R'):
                return wordnet.ADV
            else:
                return None

        sentence = 'the cat is sitting with the bats on the striped mat under badly flying geese'
        sentence = "If set too low this can cause missing highlights in the image, which might be useful to preserve for camera effects such as bloom or glare. To mitigate this conundrum it's often useful to clamp only indirect bounces, leaving highlights directly visible to the camera untouched."
        print(f'{sentence}')
        pos_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
        print(pos_tagged)

        wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged ))
        print(wordnet_tagged)

        lem_sentence = []
        for word, tag in wordnet_tagged:
            if tag is None:
                lem_sentence.append(word)
            else:
                lem_sentence.append( lem.lemmatize(word, tag))
        lemmed_sentence = ' '.join(lem_sentence)
        print(lemmed_sentence)

    def test_0063(self):
        from pyparsing import nestedExpr

        source = 'this (one ((four) two)) and (three)'
        # define parser
        parser = nestedExpr('(',')')("content")

        # search input string for matching keyword and following braced content
        matches = parser.searchString(source)

        list_of_matches = (' '.join(map(str, sl)) for sl in matches)
        final_list = []
        for entry in list_of_matches:
            list_entry = ''.join(entry)
            string_entry = list_entry.replace('[', '(')
            string_entry = string_entry.replace(']', ')')
            string_entry = string_entry.replace('\'', '')
            final_list.append(string_entry)
        print(final_list)

        # for elem in matches:
        #     ee = p(*elem)
        #     print(*ee)

        # # remove quotation marks
        # return [[qs.strip('"') for qs in r[0].asList()] for r in matches]

    def sorting_temp_05(self):
        home_dir = os.environ['DEV_TRAN']
        dic_file = os.path.join(home_dir, 'blender_manual/ref_dict_0006_0001.json')
        temp_file = os.path.join(home_dir, 'blender_manual/sorted_temp05.json')
        out_file = os.path.join(home_dir, 'blender_manual/sorted_temp05_01.json')

        dic_data = readJSON(dic_file)
        temp_data = readJSON(temp_file)

        out_dic = {}
        for t_k, t_v in temp_data.items():
            is_in_dic = (t_k in dic_data)
            if is_in_dic:
                tran = dic_data[t_k]
                print(f'Removing: {t_k}=>{tran}')
                continue

            entry = {t_k: t_v}
            out_dic.update(entry)

        sorted_out_ascending = list(sorted(list(out_dic.items()), key=lambda x: x[0]))
        sorted_out_length = list(sorted(sorted_out_ascending, key=lambda x: len(x[0])))
        out_dic = OrderedDict(sorted_out_length)
        writeJSON(out_file, out_dic)

    def recur(self, k):
        if (k > 0):
            return (k + self.recur(k -1))
        else:
            return 0

    def parseSVG(self):
        from svg.path import parse_path
        from svg.path import Line
        from xml.dom.minidom import parse
        import xml.etree.ElementTree as ET

        def get_all_text(node):
            if node.nodeType == node.TEXT_NODE:
                return node.data
            else:
                text_string = ""
                for child_node in node.childNodes:
                    text_string += get_all_text(child_node)
                return text_string

        def printOneFile(file_name):
            home = os.environ['HOME']
            svg_file = os.path.join(home, file_name)
            data = None
            with open(svg_file) as f:
                data = f.read()
            # print(data)
            pat = re.compile(r'\>([^\<\>]+)\<')

            find_list = pat.findall(data)
            chosen_list = []
            for item in find_list:
                itm = item.strip()
                if len(itm) > 0:
                    chosen_list.append(itm)
            final_string = ' '.join(chosen_list)
            print(final_string)
            d_char = re.compile(r'\bD\b')
            pc_pt_number = re.compile(f'(pc|pt)\d+')



        file_list=['0001.svg']
        for f in file_list:
            printOneFile(f)

        # datasource = open(svg_file)
        # doc = parse(datasource)
        # elem_list = doc.getElementsByTagName('text')
        # doc.unlink()
        # print(elem_list)

        # tree = ET.parse(svg_file)
        # root = tree.getroot()
        # for item in root.findall('path'):
        #     print(dir(item))
        # doc = parse(svg_file)
        # elem_list = doc.getElementsByTagName('tspan')
        # # print(x_string_list)
        # doc.unlink()

        # for elem in elem_list:
        #     print(f'{elem.toxml()}')

    def translate_po_file(self):
        fuzzy_str = 'fuzzy'
        home = os.environ['HOME']
        tf = TranslationFinder()

        def update_dic():
            po_input = os.path.join(home, 'test_output_0003.po')
            input_po_cat = c.load_po(po_input)

            new_list = {}
            changed = False
            for m in input_po_cat:
                k = m.id
                is_ignore = (not k)
                if is_ignore:
                    continue

                v = m.string
                dic_trans = tf.isInDict(k)
                must_mark = False
                if not dic_trans:
                    tf.addDictEntry((k, v), True)
                    # entry = {k:v}
                    # new_list.update(entry)
                    changed = True
                else:
                    is_same = (v == dic_trans)
                    if is_same:
                        continue

                    # looking for :.*:, ie. :abbr:
                    has_ref = (df.GA_REF_PART.search(k) is not None)
                    if has_ref: # leave the old ref as is
                        continue

                    tf.addDictEntry((k, v), True)
                    # changed = True

                    print('Correct existing:')
                    print('-'*30)
                    print(f'key:"{k}"')
                    print(f'dic_tran:"{dic_trans}"')
                    print(f'new_tran:"{v}"')
                print('-'*30)

            if changed:
                print('Update dictionary')
                tf.saveMasterDict()

        def test_cases():
            # po_input = os.path.join(home, 'test_output.po')
            po_input = os.path.join(home, 'blender_manual/gui/2.9x/po/vi.po')
            # po_output = os.path.join(home, 'test_output_0004.po')
            po_output = os.path.join(home, 'test_output_0007.po')
            # dic_file = os.path.join(home, 'blender_manual/ref_dict_0006_0002.json')
            input_po_cat = c.load_po(po_input)
            changed = False
            for m in input_po_cat:
                k:str = m.id
                is_ignore = (not k)
                if is_ignore:
                    continue

                is_ignored_term = IG.isIgnored(k)
                if is_ignored_term:
                    continue

                v:str = m.string
                # k_upper_count = sum(1 for c in k if c.isupper())
                # v_upper_count = sum(1 for c in v if c.isupper())
                # is_diff = (k_upper_count != v_upper_count)

                k_is_title = k.istitle()
                k_is_upper = k.isupper()
                k_is_lower = k.islower()

                v_is_title = v.istitle()
                v_is_upper = v.isupper()
                v_is_lower = v.islower()

                is_diff = (k_is_title and not v_is_title) or (k_is_upper and not v_is_upper) or (k_is_lower and not v_is_lower)

                if is_diff:
                    print('-'*30)
                    print(f'msgid \"{k}\"')
                    print(f'msgstr \"{v}\"')


        def translating_po():
            # po_input = os.path.join(home, 'Documents/working.txt')
            # po_input = os.path.join(home, 'test_output.po')

            # po_input = os.path.join(home, 'test_output.po')
            po_input = os.path.join(home, 'test_output_0005.po')
            # po_output = os.path.join(home, 'test_output_0004.po')
            po_output = os.path.join(home, 'test_output_0006.po')
            # dic_file = os.path.join(home, 'blender_manual/ref_dict_0006_0002.json')
            input_po_cat = c.load_po(po_input)
            changed = False
            for m in input_po_cat:
                k = m.id
                is_ignore = (not k)
                if is_ignore:
                    continue

                is_ignored_term = IG.isIgnored(k)
                if is_ignored_term:
                    print('-'*30)
                    print(f'IGNORED msgid \"{k}\"')
                    print('*'*30)
                    print("")

                    v = m.string
                    is_value_empty = (not v)
                    is_fuzzy = m.fuzzy

                    if not is_value_empty:
                        m.string = ""
                        changed = True
                    if is_fuzzy:
                        m.flags.remove(fuzzy_str)
                        changed = True
                    continue

                v = m.string
                is_value_empty = (not v)
                is_fuzzy = m.fuzzy

                is_translate = (is_value_empty or is_fuzzy)
                if not is_translate:
                    continue

                trans = tf.isInDict(k)
                must_mark = False
                if not trans:
                    trans = tf.blindTranslation(k)
                    must_mark = True

                if trans:
                    trans = tf.removeTheWord(trans)
                    trans = cm.matchCase(k, trans)
                    m.string = trans

                    print('-'*30)
                    print(f'msgid \"{k}\"')
                    print(f'msgstr \"{trans}\"')
                    if must_mark and not is_fuzzy:
                        if m.flags is None:
                            m.flags = set() # init
                        m.flags.add(fuzzy_str) # set the fuzzy flags
                        print('marked fuzzy')
                    elif not must_mark and is_fuzzy:
                        m.flags.remove(fuzzy_str) # clear the fuzzy flags
                        print('CLEAR fuzzy')

                    changed = True

            if changed:
                print(f'Wrote changes to {po_output}')
                c.dump_po(po_output, input_po_cat)

        # translating_po()
        test_cases()

    def test_pattern_0001(self):
        msg = "RGBA byte"
        msg1 = ", RGB byte"

        p = re.compile(r'^(\,\s)?(RGB[A]?)(\s(byte))?$', re.I)
        # p = re.compile(r'^Blender\s(\d+[\d\.]+)$', re.I)
        m = p.search(msg)
        print(m)


    def test_insert_abbr(self):
        dic_list = {
            "per-bone": ":abbr:` ()`",
            "per-curve": "",
            "per-frame": "",
            "per-hair": "",
            "per-item": "",
            "per-layer": "",
            "per-light": "",
            "per-name": "",
            "per-object": "",
            "per-path": "",
            "per-pixel": "",
            "per-point": "",
            "per-shader": "",
            "per-vertex": "",
        }

        # for k, v in dic_list.items():
        #     v = f'`',
        #     print(f'"{k}": ":abbr:` ({k})`",')

        p = re.compile(r'\`+([^\`\<]+)\s\<[^\<\>]+\>\`[\_]?')
        p = re.compile(r':[^\:]:+[\`]+([^\`\<\>]+)[\`]+[\_]*')
        p = re.compile(r'\`([^\`]+?)\s\<[^\>]+\>\`[\_]') # `Wikipedia <https://en.wikipedia.org/wiki/XYZ_file_format>`__
        p = re.compile(r'(\:\w+\:)?[\`]+([^\`]+)[\`]+[\_]*?') # :menuselection:`Select --> Mirror`

        t = "Description of the XYZ file format: `Wikipedia <https://en.wikipedia.org/wiki/XYZ_file_format>`__ and `Open Babel <https://openbabel.org/docs/dev/FileFormats/XYZ_cartesian_coordinates_format.html>`__."
        t = ":kbd:`Shift-Alt-L`"
        t = ":math:`\\lvert q \\rvert = \\sqrt{X^2 + Y^2 + Z^2 + W^2}`"
        t = '''
            To interact with Blender, scripts can make use of the tightly integrated :abbr:`API (Application Programming Interface)`.
            To understand this, look at Fig. :ref:`fig-rig-bone-select-deselect`. 
            With this script you'll notice we're doing some math with the object location and cursor, 
            `Wikipedia <https://en.wikipedia.org/wiki/XYZ_file_format>`__ and 
            `Open Babel <https://openbabel.org/docs/dev/FileFormats/XYZ_cartesian_coordinates_format.html>`__.
            this works because both are 3D :class:`blender_api:mathutils.Vector` instances, a convenient 
            class provided by the :mod:`blender_api:mathutils` module which allows vectors to be multiplied 
            by numbers and matrices.
            :menuselection:`Pose --> Motion Paths`    
            :kbd:`Ctrl-I`
            ``MajorRadius``, ``MinorRadius``
            :doc:`Display panel page </animation/armatures/properties/display>`
        '''
        # m = p.findall(t)
        # print(m)

        t = '''node editor --> Sidebar --> Trees
--> (Deform, ...)
Add --> Remove Meta-Strips
Face --> Intersect (Boolean)
File --> Import/Export --> Stl (.stl)
'''
        # print(t)
        #
        # p_sep = '$$'
        # p = re.compile(r'(\s?[\-]{2}\>\s)')
        #
        # # m = p.search(t)
        # # print(m)
        # # m = p.findall(t)
        # # print(m)
        #
        # # this is the simplest solution
        # word_list = t.split('--> ')
        # print(word_list)

        # p_sep = '$$'
        # # p = re.compile(r'\s?[\-]{2}\>\s?')
        # p = re.compile(r'(\w)|(\w\-\w)')
        # tt = t.split('\n')
        # t = p_sep.join(tt)
        # print(t)
        # m = p.findall(t)
        # print(m)
        # no_sep = p.sub(p_sep, t)
        # word_list = no_sep.split(p_sep)
        # m = p.findall(t)
        # print(word_list)

        t = '''Pixel <Pixel>
Focal Length <Focal Length>
Fireflies
IOR
'''
        # p = re.compile(r'(<[^<>]+>)')
        # word_list = cm.findInvert(p, t)
        # print(word_list)

        # p = re.compile(r'([^\<\>]+)')
        # p = re.compile(r'(?!\<*\>).*')
        # p = re.compile(r'(?P<words>[^<>\n]+)(?!\s<.*>\s)?')
        # p = re.compile(r'([^<>\n]+)\s?(?:<.*>)?', flags=re.M)
        # m = p.findall(t)
        # print(m)
        # print(m.group('words'))
        # p = re.compile(r'(\<?[^\<\>]+\>?)')
        # print(t)
        # m = p.finditer(t)
        # for i in m:
        #     print(i)
        #         # re.compile( r"(?P<quote>['\"])(?P<string>.*?)(?<!\\)(?P=quote)")
        #         # menu_p = re.compile(r'(?P<menu_sep>\s?-->\s?)?(?P<string>[^\`]+)((?P=menu_sep)(?P=string))*')
        #         # menu_p = re.compile(r'(?P<menu_sep>\s?-->\s?)?(?P<string>[^\`]+)((?P=menu_sep)(?P=string))*?')
        #         print(t)
        #         # menu_p = re.compile(r'((?!\-\-\>).)*', flags=re.M)
        #         # menu_p = re.compile(r'(\s?[\-]{2}\>\s?)', flags=re.MULTILINE)
        #         # temp_str = menu_p.sub('$$', t)
        #         # word_list = temp_str.split('$$')
        #         # print(word_list)
        #
        #         term_p = re.compile(r'(?P<string>[^\`]+)\s\<(?P=string)\>')
        #         m = term_p.findall(t)
        #         print(m)

        t_list = {"Security": ""}
        tran_list={}
        for k, v in t_list.items():
            tran, fuzzy, ignore = tf.translate(k)
            print(f'{k} => {tran}')
            if not tran:
                entry = {k: ""}
                # else:
                #     entry = {k: tran}
                tran_list.update(entry)
        home = os.environ['HOME']
        out_file = os.path.join(home, 'test_py.json')
        writeJSON(out_file, tran_list)
        # pp(tran_list)

    def test_refs_0001(self):
        msg = "see the :doc:`Particle Physics </physics/particles/emitter/physics/index>` page"
        msg = " constraint, or, through a driver, "
        msg = "--log \"wm.*\""
        msg = 'Add --> Armature'
        msg = 'Properties --> Bone --> Deform Panel'
        msg = "Refers to the general color decomposition resulting in *Y* (Luminance) and *C* (Chrominance) channels, whereas the chrominance is represented by: U = ( Blue minus Luminance ) and V = ( Red minus Luminance )."
        msg = "//render_"

        dict_tf = TranslationFinder()
        # trans, is_fuzzy, is_ignore = dict_tf.translate(msg)
        ref_list: RefList = None
        ref_list = RefList(msg=msg, keep_orig=False, tf=dict_tf)
        ref_list.parseMessage()
        ref_list.translateRefList()
        trans = ref_list.getTranslation()
        is_ignore = (ref_list.isIgnore())
        is_fuzzy = (ref_list.isFuzzy())
        print(f'"{msg}"')
        print(f'"{trans}"')

    def test_0064(self):
        t = "/files/blend/open_save"
        t = "/compositing/types/distort/plane_track_deform"
        # t = "bone-relations-parenting"
        d = "scene dicing rate"
        p = re.compile(r'^(?P<sep>[\/])?[^.*(?P=sep)]+(.*(?P=sep).*[^(?P=sep)]+){2,}$')
        p = re.compile(r'[\\\/\-\_\.]')
        wp = re.compile(r'^[^\\\/\-\_\.]+$')

        delim = ["\\", "/", "-", "_", "."]
        splitter = '|'.join(map(re.escape, delim))
        print(splitter)

        w_list = cm.findInvert(p, d)
        print(w_list)
        w_count = len(w_list)
        is_path = False
        if w_count > 2:
            is_path = True
            for k, v in w_list.items():
                loc, word = v
                is_just_word = wp.search(word)
                if not is_just_word:
                    is_path = False
                    break
        if is_path:
            print(f'is_path')
        else:
            print(f'NOT is_path')

    def test_0065(self):
        t = "With the \"traditional\" representation of three bytes, like RGB(124, 255, 56), the multiplications give far too high results, like RGB(7316, 46410, 1848), that have to be normalized (brought back) by dividing them by 256 to fit in the range of (0 to 255)... RGBA(7316, 46410, 1848, 0xff)"
        p = re.compile(r'(RGB[A]?)\(([^\)]+)\)')
        m = p.findall(t)
        print(m)

    def test_0066(self):
        t = "With the \"traditional\" representation of three bytes, like RGB(124, 255, 56), the multiplications give far too high results, like RGB(7316, 46410, 1848), that have to be normalized (brought back) by dividing them by 256 to fit in the range of (0 to 255)... RGBA(7316, 46410, 1848, 0xff)"
        p = re.compile(r'(?:^|\s)\(.*\)')
        m = p.findall(t)
        print(m)

    def test_0067(self):
        class bracket_record:
            def __init__(self, filename, list_of_bracket):
                self.file_name = filename
                self.list_of_bracket = list_of_bracket

            def __repr__(self):
                str_list = []
                if not self.list_of_bracket:
                    return str_list

                if self.file_name:
                    str_list.append(self.file_name)
                    str_list.append('-' * 80)
                str_list.append(self.list_of_bracket)
                return '\n'.join(str_list)

        def parseBracket(pat, text_line, external_list):
            found_list = pat.findall(text_line)
            if not found_list:
                external_list.append(text_line)
                return
            else:
                for line in found_list:
                    parseBracket(pat, line, external_list)

        home_dir = os.environ['DEV_TRAN']
        from_path = os.path.join(home_dir, 'blender_docs/build/gettext')
        p = re.compile(r'(?:^|\s)(\(.*\))')

        word = r'(\w+)'
        path_sep = r'([\\\/\_\-\.\:\*\{\}]+)'
        no_space = r'(?!\w\s)'
        path = r'(%s|%s)?((%s%s)+)+' % (word, path_sep, path_sep, word)
        path_pattern = r'^(%s)%s?$' % (path, path_sep)
        # pat_full = r'^(((\w+)?(\:)?)|([\.]{1,2})?(\w+){2,})+([*\.](\w{2,5})|[\*])?$'

        PATH_CHECKER = df.PATH_CHECKER

        file_list = []
        list_of_brackets = []
        # text_line = "One advantage of using the command line is that we do not need a graphical display (no need for X server on Linux for example) and consequently we can render via a remote shell (typically SSH)."
        # parseBracket(p, text_line, list_of_brackets)
        # exit(0)
        for root, dirnames, filenames in os.walk(from_path):
            if root.startswith('.'):
                continue

            b_list_for_file = []
            for filename in filenames:
                is_found  = (filename.lower().endswith('.pot'))
                if not is_found:
                    continue

                file_path = os.path.join(root, filename)
                file_list.append(file_path)

        for file_path in file_list:
            is_updated = False
            po_cat = c.load_po(file_path)

            for m in po_cat:
                text_line = m.id
                if text_line:
                    parseBracket(p, text_line, b_list_for_file)

            if b_list_for_file:
                b_rec = bracket_record(file_path, b_list_for_file)
                list_of_brackets.append(b_rec)

        print(list_of_brackets)

    def test_0068(self):

        def bracketParser(text):
            def error_msg(item, text_string):
                return f'Imbalanced parenthesis! Near the "{item}" text_string:[{text_string}]'

            _tokenizer = re.compile(r'\s*([()])\s*').split
            def tokenize(text_line: str):
                return list(filter(None, _tokenizer(text_line)))

            def _helper(tokens):
                outside_brackets = []
                bracketed = []
                q = []
                max = len(tokens)
                chosen_items = []
                start_loc = end_loc = 0
                for i in range(0, max):
                    item = tokens[i]
                    if item == '(':
                        q.append(i)
                    elif item == ')':
                        if not q:
                            raise ValueError(error_msg(item, text))
                        q.pop()
                        bracketed.extend(chosen_items)
                        chosen_items = []
                    else:
                        start_loc = text.find(item, end_loc)
                        end_loc = start_loc + len(item)
                        loc = (start_loc, end_loc)
                        entry = (loc, item)
                        if q:
                            chosen_items.append(entry)
                        else:
                            outside_brackets.append(entry)
                if q:
                    raise ValueError(error_msg(item, text))
                return bracketed, outside_brackets
            tokens = tokenize(text)
            bracketed_list, outside_bracket_list = _helper(tokens)
            return bracketed_list, outside_bracket_list

        text_line = "One advantage of using the RGB(123, 123, 123) command line is that we do not need a graphical display (no need for X server on Linux (for example)) and ((consequently we) can render) () via a remote shell (typically SSH)."
        # text_line = "One advantage of using the RGB"
        print(text_line)
        l, o = bracketParser(text_line)
        for loc, txt in l:
            s, e = loc
            print(f'bket: {loc} @ "{text_line[s:e]}"')

        for loc, txt in o:
            s, e = loc
            print(f'ouside: {loc} @ "{text_line[s:e]}"')

        print(l)

    def test_0069(self):
        def func1(name):
            print(f'func1: name:{name}')

        def func2(name, index):
            print(f'func2: name:{name}; index:{index}')

        func_list=[func1, func2]

        for index, f in enumerate(func_list):
            if index == 0:
                f('hoang')
            if index == 1:
                f('hanh', index)

    def test_0070(self):
        p1 = re.compile(r'[\w\-\_\*]+\.\w+')
        p = re.compile(r'(?:[^\+\-\=\s])[\w\-\_\*]+\.\w+$')

        leading=r'([\`\<]+)'
        ending=r'([\`\>]+)'
        word = r'([\w\d\#]+)'
        sep = r'([<>\\\/\-\_\.{}:]+)'
        pat = r'(%s((%s?(%s%s)+)*%s?)%s)|(%s%s%s)' % (leading, word, sep, word, sep, ending, sep, word, sep)
        only_sep = r'^(%s|%s|%s)$' % (sep, leading, ending)
        only_sep_pat = re.compile(only_sep)

        # p1 = re.compile(r'(([\w\d]+)?[\\\/\-\_\.]+([\w\d]+))+')
        p1 = re.compile(pat)
        leading_pat = re.compile(leading)

        from_path = os.path.join(home_dir, 'blender_docs/build/gettext')
        total_list = []
        file_list = []
        for root, dirnames, filenames in os.walk(from_path):
            if root.startswith('.'):
                continue

            b_list_for_file = []
            for filename in filenames:
                is_found  = (filename.lower().endswith('.pot'))
                if not is_found:
                    continue

                file_path = os.path.join(root, filename)
                file_list.append(file_path)

        for file_path in file_list:
            is_updated = False
            po_cat = c.load_po(file_path)

            result_list=[]
            for m in po_cat:
                text_line = m.id
                if not text_line:
                    continue

                # t = '-3.0000'
                # t1 = 'this.that'
                # m = p.search(t)
                # m1 = p.search(t1)
                # print(f'm:{m}')
                # print(f'm1:{m1}')

                for m in p1.finditer(text_line):
                    found_orig = m.group(0)
                    s = m.start()
                    e = m.end()
                    loc = (s, e)

                    is_only_sep = (only_sep_pat.search(text_line) is not None)
                    if found_orig and not is_only_sep:
                        entry = (loc, found_orig, text_line)
                        result_list.append(entry)

                    # found_orig_with_leading = None
                    # if (s-1 >= 0):
                    #     found_orig_with_leading = text_line[s-1:e]
                    
                    # is_considering = False
                    # if found_orig_with_leading:
                    #     is_considering = (leading_pat.search(found_orig_with_leading) is not None)

                    # if is_considering:                        
                    #     entry = (loc, found_orig, text_line)
                    #     result_list.append(entry)
                
                # m1 = p1.search(text_line)
                # # m = p.findall(text_line)

                # if not m1:
                #     continue

                # entry=(m1.group(0), text_line)
                # result_list.append(entry)

                # if m1:
                #     result_list.append('possible:')
                #     result_list.extend(m1)
                # result_list.append('definitely:')
                # result_list.extend(m)

            if not result_list:
                continue

            print(f'file: {file_path}')
            print('*' * 50)
            prev_text_line=None
            for entry in result_list:
                loc, found_orig, text_line = entry
                is_new_line = (text_line != prev_text_line)
                if is_new_line:
                    print(f'------ [{text_line}]')
                    prev_text_line = text_line                    

                print(f'[{found_orig}]')
                entry=(text_line, found_orig)
                total_list.append(entry)
            print('-' * 50)

        print('*' * 50)
        total_list.sort()
        for entry in total_list:
            print(f'[{entry}]')
        print('-' * 50)

    def getHome(self):
        dir = os.environ['HOME']
        return dir

    def getDevTran(self):
        dir = os.environ['DEV_TRAN']
        return dir

    def getBlenderGithub(self):
        dir = os.path.join(self.getDevTran(), 'blender_manual')
        return dir

    def get29xViPoPath(self):
        dir = os.path.join(self.getBlenderGithub(), 'gui/2.9x/po/vi.po')
        return dir

    def cleanDictionary(self):
        def canSafelyRemoveBrackets(s_start, s_end, txt: str):
            p = r'\s*[\%s\%s]\s*' % (s_start, s_end)
            pat = re.compile(p)
            has_brackets = (pat.search(txt) is not None)
            if not has_brackets:
                return False

            is_start = txt.startswith(s_start)
            is_end = txt.endswith(s_end)
            is_process = (is_start and is_end)
            if not is_process:
                return False

            q = []
            last_index = len(txt) - 1
            first_index = 0
            for index, token in enumerate(txt):
                is_start = (token == s_start)
                is_end = (token == s_end)

                if is_start:
                    q.append(index)

                if is_end:
                    if q:
                        open_index = q.pop()
                        is_last = (index == last_index) and (open_index == 0)
                        if is_last:
                            return True
                    else:
                        raise ValueError(f'ERROR! Imbalance brackets - text_line:[{txt}]')
            return False

        home = self.getHome()
        dict_path = os.path.join(home, 'Dev/tran/blender_manual/ref_dict_0006_0001.json')
        json_dict = readJSON(dict_path)

        symbol_pairs = [
            # '()',
            # '[]',
            '""',
        ]

        new_dict = {}
        k: str = None
        v: str = None
        changed = False
        for bk_set in symbol_pairs:
            bk_s = bk_set[0]
            bk_e = bk_set[1]
            for k, v in json_dict.items():
                has_bk_s = (bk_s in k)
                has_bk_v = (bk_e in k)
                can_process = (has_bk_s and has_bk_v)
                if not can_process:
                    continue

                is_debug = ('auto' in k)
                if is_debug:
                    print('debug')

                new_k = k
                new_v = v

                can_remove_brackets_in_k = canSafelyRemoveBrackets(bk_s, bk_e, k)
                can_remove_brackets_in_v = canSafelyRemoveBrackets(bk_s, bk_e, v)
                can_remove_brackets = (can_remove_brackets_in_v or can_remove_brackets_in_k)
                if not can_remove_brackets:
                    continue

                if can_remove_brackets_in_k:
                    k_len = len(k)
                    new_k = k[1:k_len-1]
                    print(f'candidate: k[{k}] => new_k[{new_k}]')
                    changed = True

                if can_remove_brackets_in_v:
                    v_len = len(v)
                    new_v = v[1:v_len-1]
                    print(f'candidate: v[{v}] => new_v[{new_v}]')
                    changed = True

                entry={new_k: new_v}
                new_dict.update(entry)
        if changed:
            print(f'Write changes to: {dict_path}')
            # writeJSON(dict_path, new_dict)

    def poCatToDic(self, po_cat):
        po_cat_dic = OrderedDict()
        for index, m in enumerate(po_cat):
            is_first_entry = (index == 0)
            if is_first_entry:
                continue

            k = m.id
            v = m.string
            entry = {k: v}
            po_cat_dic.update(entry)
        return po_cat_dic

    def diffPOTFile(self):
        home = self.getHome()
        from_pot = 'po/blender.pot'
        to_pot = 'po/po/blender.pot'
        from_pot_path = os.path.join(home, from_pot)
        to_pot_path = os.path.join(home, to_pot)

        from_pot_cat = c.load_po(from_pot_path)
        to_pot_cat = c.load_po(to_pot_path)
        from_pot_dict = self.poCatToDic(from_pot_cat)
        to_pot_dict = self.poCatToDic(from_pot_cat)

        len_from_pot_dict = len(from_pot_dict)
        len_to_pot_dict = len(to_pot_dict)
        is_diff = (len_from_pot_dict != len_to_pot_dict)
        print(f'SIZE DIFFERENT: len_from_pot_dict:{len_from_pot_dict}; len_to_pot_dict:{len_to_pot_dict}; diff:{len_from_pot_dict - len_to_pot_dict}')

        diff_list = []
        for k, v in to_pot_dict.items():
            if not k:
                continue

            is_debug = ('Shader AOV' in k)
            if is_debug:
                print('debug')


            if not k in from_pot_dict:
                entry=('NEW/MODI', k)
                diff_list.append(entry)

        for k, v in from_pot_dict.items():
            if not k:
                continue

            is_debug = ('Shader AOV' in k)
            if is_debug:
                print('debug')

            if not k in to_pot_dict:
                entry=('REMOVED', k)
                diff_list.append(entry)

        for status, k in diff_list:
            print(f'{status} => [{k}]')

    def test_0071(self):
        from fuzzywuzzy import fuzz
        t1 = 'this and that'
        t2 = 'this and those'
        rat = fuzz.partial_token_sort_ratio(t1, t2)
        print(f't1:{t1}; t2:{t2}; rat:{rat}')

    def locRemain(self, original_word: str, new_word: str) -> list:
        '''
        locRemain:
            Find where the remainder starts, ends, excluding alphanumeric characters, so can decide
            if remainder can be removed or not and how far
        :param original_word: word where new_word is extracted from
        :param new_word: word from which dictionary has found from original word
        :return:
            list of locations (start, end) within the original where original word including
            but not containing any alpha-numerical characters, which can be removed (ie. remainder
            parts of the word in the original_word)
        '''
        try:
            try:
                p = re.compile(new_word, flags=re.I)
            except Exception as e:
                new_word_esc = re.escape(new_word)
                p = re.compile(new_word_esc, flags=re.I)

            list_of_occurences = patternMatchAllToDict(p, original_word)
            # entry = {loc: orig}
            list_of_places = []
            max_len = len(original_word)
            list_of_found_locations = list_of_occurences.keys()
            for loc in list_of_found_locations:
                s, e = loc
                while s-1 >= 0 and original_word[s-1].isalnum():
                    s -= 1

                while e+1 < max_len and original_word[e+1].isalnum():
                    e += 1

                s = max(0, s)
                e = min(e, max_len)
                loc = (s, e)
                list_of_places.append(loc)
            return list_of_places
        except Exception as e:
            print(f'original_word:{original_word}, new_word:{new_word}')
            print(e)
            raise e

    def compareExpressContruct(self, item, k, is_fuzz=False):
        i_left, i_right, k_left, k_right = cm.splitExpVar(item, k)
        is_left_match = is_right_match = True
        has_left = bool(i_left and k_left)
        if has_left:
            left_ratio = fuzz.ratio(i_left, k_left)
            is_left_match = (left_ratio >= df.FUZZY_LOW_ACCEPTABLE_RATIO)

        has_right = bool(i_right and k_right)
        if has_right:
            right_ratio = fuzz.ratio(i_right, k_right)
            is_right_match = (right_ratio >= df.FUZZY_ACCEPTABLE_RATIO)

        is_equal = (has_left or has_right) and (is_left_match and is_right_match)
        if is_equal:
            return 0, i_left, i_right, k_left, k_right
        elif item < k:
            return -1, None, None, None, None
        else:
            return 1, None, None, None, None

    def test_loc_remain(self):
        item = 'take up $$$'
        k = 'taking up courage'

        item = 'this is the $$$'
        item = 'this is the'
        k = 'This is the command you will always use when building the docs'
        is_matched, i_left, i_right, k_left, k_right = self.compareExpressContruct(item, k)
        print(f'is_matched:[{is_matched}], i_left:[{i_left}], i_right:[{i_right}], k_left:[{k_left}], k_right:[{k_right}]')
        # ratio = fuzz.ratio(item, k)
        # print(f'item:[{item}], k:[{k}], ratio:[{ratio}]')



    def plistToText(self):
        home = self.getHome()
        plist_file_path = os.path.join(home, 'Documents/Text Substitutions.plist')
        data = None
        with open(plist_file_path) as fd:
            data = fd.read()        
        # print(data)
        entry_list = re.findall(r'<string>(.*?)<\/string>', data)
        dict_list = {}
        key = expand = None
        for index, entry in enumerate(entry_list):
            is_even = (index % 2 == 0)
            if is_even:
                expand = entry                
                # print(f'even:{entry}')
            else:
                key = entry
                dict_entry = {key: expand}
                dict_list.update(dict_entry)
                # print(f'entry: {entry}')
        json_file_path = os.path.join(home, 'plist.json')
        writeJSON(json_file_path, dict_list)

        # print(entry_list)

        # doc = xmltodict.parse(data)
        # print(f'{type(doc)}')
        # for k, v in doc.items():
        #     print(f'k:{type(k)}')
        #     print(f'v:{type(v)}')
        #     i=0
        #     for kk, vv in v.items():
        #         print(f'kk:{kk}')
        #         print(f'vv:{vv}')
        #         print('*' * 30)
        #         i += 1
        #         if i > 1:
        #             exit(0)
        # for dct in doc:
        #     print(dct)
            # for k, v in dct.items():
            #     print(f'{k}=>{v}')
        # for entry in doc:
        #     pprint(entry)
        # json_data = json.dumps(doc)
        # print(json_data)

        # url = pathlib.Path(plist_file_path).as_uri()
        # print(url)
        # data = requests.get(url)
        # print(data)

    def binary_match(self, loc_from, loc_to):
        is_same_empty = not (loc_from or loc_to)
        if is_same_empty:
            return 0

        if not loc_from and loc_to:
            return -len(loc_to)

        if loc_from and not loc_to:
            return -len(loc_from)

        same_count = 0

        f_len = len(loc_from)
        f_len_mid = (f_len // 2)
        f_list_0 = loc_from[:f_len_mid].lower()
        t_list_0 = loc_to[:f_len_mid].lower()
        is_same = (bool(f_list_0) and bool(t_list_0)) and (t_list_0 == f_list_0)
        if not is_same:
            t_len = len(t_list_0)
            for i, f_char in f_list_0:
                valid = (i < t_len)
                if not valid:
                    break

                t_char = t_list_0[i]
                is_equal = (t_char == f_char)
                if not is_equal:
                    break

                same_count += 1

            return same_count
        else:
            same_count += f_len_mid


        f_list_1 = loc_from[f_len_mid+1:]
        t_list_1 = loc_to[f_len_mid+1:]
        is_same = (f_list_1.lower() == t_list_1.lower())
        if is_same:
            return same_count + len(f_list_1)
        else:
            return same_count + self.binary_match(f_list_1, t_list_1)

    def test_binary_search(self):
        t1= 'this one location'
        t2 = 'this one location is a test'
        l_t1 = len(t1)
        matched_count = self.binary_match(t1, t2)
        print(f'is_found:[{matched_count}]')

    def test_0072(self):
        t = '``-o /project/renders/frame_#####``'
        leading=r'([\`\<]+)?'
        ending=r'([\`\>]+)?'
        word = r'([\w\d\#]+)'
        sep = r'([<>\\\/\-\_\.{}:]+)'
        pat = r'(%s((%s?(%s%s)+)*%s?)%s)|(%s%s%s)' % (leading, word, sep, word, sep, ending, sep, word, sep)
        only_sep = r'^%s$' % (sep)
        only_sep_pat = re.compile(only_sep)
        # p1 = re.compile(r'(([\w\d]+)?[\\\/\-\_\.]+([\w\d]+))+')
        p = re.compile(pat)
        # m = p.search(t)
        iter = p.finditer(t)
        for m in iter:
            f = m.group(0)
            s = m.start()
            e = m.end()
            is_only_sep = (only_sep_pat.search(t) is not None)
            if f and not is_only_sep:
                print(f'{(s,e)}; [{f}]')

    def test_0073(self):
        def pat_search(local_en_txt):
            for pat, tran in numerical_pat_list:
                m = pat.search(local_en_txt)
                is_matching = (m is not None)
                if is_matching:
                    return tran
            return None

        def find_tran(en_txt):
            try:
                tran = pat_search(en_txt)
                iter = numerical_abbrev_pat.finditer(tran)
                for m in iter:
                    abbrev_txt = m.group(0)
                    try:
                        abbrev_tran_txt = numeral_dict[abbrev_txt]
                        tran = tran.replace(abbrev_txt, abbrev_tran_txt)
                    except Exception as e:
                        pass
                return tran
            except Exception as e:
                return None


        numeric_prefix = 'hằng/lần thứ/bộ/bậc'
        numeric_postfix = 'mươi/lần/bậc'
        numeral_dict = {
            '@{1t}': 'ức',
            '@{1b}': 'tỉ',
            '@{1m}': 'triệu',
            '@{1k}': 'nghìn',
            '@{1h}': 'trăm',
            '@{10}': 'chục/mươi/mười',
            '@{0}': 'không/vô/mươi',
            '@{1}': 'một/nhất/đầu tiên',
            '@{2}': 'hai/nhì/nhị/phó/thứ/giây đồng hồ',
            '@{3}': 'ba/tam',
            '@{4}': 'bốn/tứ/tư',
            '@{5}': 'năm/lăm/nhăm/Ngũ',
            '@{6}': 'Sáu/Lục',
            '@{7}': 'Bảy/Thất',
            '@{8}': 'Số tám/bát',
            '@{9}': 'Chín/cửu',
        }

        numeric_trans = {
            'zero|none|empty|nullary': '@{1}',
            'one|first|monuple|unary': '@{1}',
            'two|second|couple|binary': '@{2}',
            'three|third|triple|ternary': '@{3}',
            'four(th)?|quadruple|Quaternary': '@{4}',
            'five|fifth|quintuple|Quinary': '@{5}',
            'six(th)?|sextuple|Senary': '@{6}',
            'seven(th)?|septuple|Septenary': '@{7}',
            'eight(th)?|octa|octal|octet|octuple|Octonary': '@{8}',
            'nine(th)?|nonuple|Novenary|nonary': '@{9}',
            'ten(th)?|decimal|decuple|Denary': '@{10}',
            'eleven(th)?|undecuple|hendecuple': 'Mười @{1}',
            'twelve(th)?|doudecuple': 'Mười @{2}',
            'thirteen(th)?|tredecuple': 'Mười @{3}',
            'fourteen(th)?|quattuordecuple': 'Mười @{4}',
            'fifteen(th)?|quindecuple': 'Mười @{5}',
            'sixteen(th)?|sexdecuple': 'Mười @{6}',
            'seventeen(th)?|septendecuple': 'Mười @{7}',
            'eighteen(th)?|octodecuple': 'Mười @{8}',
            'nineteen(th)?|novemdecuple': 'Mười @{9}',
            '(twent(y|ie(s|th))+?)|vigintuple': '@{2} @{10}',
            '(thirt(y|ie(s|th))+?)|trigintuple': '@{3} @{10}',
            '(fort(y|ie(s|th))+?)|quadragintuple': '@{4} @{10}',
            '(fift(y|ie(s|th))+?)|quinquagintuple': '@{5} @{10}',
            '(sixt(y|ie(s|th))+?)|sexagintuple': '@{6} @{10}',
            '(sevent(y|ie(s|th))+?)|septuagintuple': '@{7} @{10}',
            '(eight(y|ie(s|th))+?)|octogintuple': '@{8} @{10}',
            '(ninet(y|ie(s|th))+?)|nongentuple': '@{9} @{10}',
            '(hundred(s|th)?)|centuple': '@{1h}',
            '(thousand(s|th)?)|milluple': '@{1k}',
            'million(s|th)?': '@{1m}',
            'billion(s|th)?': '@{1t}',
            'trillion(s|th)?': '@{1t}',
        }
        puntuations = r'[\,\.\:\;\'\"\}\-|_]'
        numerical_abbrev_pat = re.compile(r'@{\w+}?')
        numerical_pat_list = []
        for pat_txt, tran_txt in numeric_trans.items():
            pattern_text = r'\b(%s)\b' % (pat_txt)
            pat = re.compile(pattern_text, flags=re.I)
            entry=(pat, tran_txt)
            numerical_pat_list.append(entry)

        numeral = r"\b(one|first|once)|" \
                  r"(two|second|twice)|" \
                  r"(three|third|triple)|" \
                  r"(four|fourth|quadruple)|" \
                  r"(five|fifth|quintuple)|" \
                  r"(six|sixth|sextuple)|" \
                  r"(seven|)|" \
                  r"eight|nine|ten|eleven|twelve|((thir|four|fif|six|seven|eigh|nine)teen)|(twen|thir|for|four|fif|six|seven|eigh|nine)(ty|ties)|(hundred|thousand|(mil|tril)lion)))(s|th)?\b"
        n_p = re.compile(numeral, flags=re.I)
        t = 'Sixty five and fifty hundreds, For one two three years, hundreds thousands people came to see millions of them, thirty people and fourteen of them has made one trillion donations, and the man came third is the fifth is the nineteenth man forties forthcoming oneness final second'

        word_sep="()"
        for w in t.split():
            mm = n_p.search(w)
            is_number = (mm is not None)
            if is_number:
                print(f'[{w}] is numeral.')
            loc, stripped_word = cm.removingNonAlpha(w)
            translation = find_tran(stripped_word)
            if translation:
                print(f'[{stripped_word}] => [{translation}]')

    def test_translate(self):
        # import spacy
        # nlp = spacy.load('en_core_web_sm')
        WORD_SPLIT = re.compile(r'[^\W]+')
        tf = TranslationFinder()

        # t = "Style modules:"
        # sorted_list = sorted(transtable.items())
        # t="texture_blur"
        # t = "%s, not exacted since frame %i"
        # t = "would not turn every body's attention to the problem"
        # t = "underlying"
        # t = "color ramps"
        # t = 'DCT, similar algorithm to JPEG.'
        # t = '__Delete Driver(s).'
        # t = 'difference'
        # t = "Dope Sheet's;;;"
        # t = '"limit" ones'
        # t = "\"Basis\" is the rest shape. \"Key 1\", \"Key 2\", etc. will be the new shapes"
        # t = '"Bone" is "Bone.003" \'s parent. Therefore "Bone.003" \'s root is same as the tip of "Bone". Since "Bone" is still selected, its tip is selected. Thus the root of "Bone.003" remains selected'
        # t = 'aim to please'
        # t = 'tricky'
        # t = "assuming you are at the ``blender_docs`` subdirectory"
        # t = "do not remove or add vertices"
        # t = 'this is the same thing as the *Playback Range* option of the :ref:`Timeline editor header <animation-editors-timeline-headercontrols>`'
        # t = "Helps to maintain the hair volume when puffing the root."
        # t = "Hint: the color of the UI control changes when you wouldn't have located at precisely the frame number of the keyframed."
        # t = "\"limit\" ones"
        # t = "like e.g. the :doc:`\"copy\" ones </animation/constraints/transform/copy_location>`"
        # t = "If more realism is desired, the Mirror Modifier would be applied, resulting in a physical mirror and a complete head. You could then make both side physically different by editing one side and not the other. Unwrapping would produce a full set of UVs (for each side) and painting could thus be different for each side of the face, which is more realistic"
        # t = "Foreground colors of Warning icon next to Form of hair"
        # t = 'i.e. it will be "played" reversed...' # solving ' reversed...' is PATH and is ignored

        # t = '//one/two'
        # # t = 'one/two/three'
        # PATH_WORD_TRAIL = re.compile(r'(\\\\|/|\\-|_|\\.)\w+')
        # PATH_WORD_LEAD = re.compile(r'\w+(\\\\|/|\\-|_|\\.)')

        # m1 = PATH_WORD_LEAD.findall(t)
        # m2 = PATH_WORD_LEAD.findall(t)

        # t = "Load Template Factory Settings"
        t_list = [
            # "i.e. if you had a ``forearm`` bone selected when you copied the pose, the ``forearm`` bone of the current posed armature will get its pose when you paste it -- and if there is no such named bone, nothing will happen...",
            # "{BLENDER_USER_SCRIPTS}/startup/bl_app_templates_user",
            # "Face or Vertex select modes",
            # "Factor Start, End",
            # "perimeter of the object",
            # "First and Last Copies",
            # "Flip to Bottom/Top",
            # "Grease Pencil materials are linked at stroke level.",
            # "(Grease Pencil Edit)",
            # "found in the panel header",
            # "also available from the 3D header in both *Object Mode* and *Edit Mode* :menuselection:`Object --> Snap` and :menuselection:`Mesh --> Snap`",
            # "larger *Edge Kernel Radius*, like 8 / smaller *Edge Kernel Tolerance*, like 0.05",
            # "with a Radius of 100 px",
            # 'the Mirror Modifier; would be!! applied, 2.5 one.to.one, resulting in a physical mirror and a complete head. You could then make both side physically different',
            # "Helps to maintain the hair volume when puffing the root realism.",
            # "If more realism is desired, the Mirror Modifier would be applied, resulting in a physical mirror and a complete head. You could then make both side physically different by editing one side and not the other. Unwrapping would produce a full set of UVs (for each side) and painting could thus be different for each side of the face, which is more realistic",
            # "Image texturing only. Insert texts, Install from",
            # "Instancing Vertices",
            # "Learn the benefits of right-click-select",
            # "Light tab",
            # "Linux",
            # "Marker-And-Cell Grid",
            # "Material Library VX",
            # "Houdini Ocean Toolkit",
            # "NURBS spheres and specific element colors and sizes",
            # "NURBS, mesh, meta",
            # "NVidia Website",
            # "North / South",
            # "as long as",
            # "Quickening up",
            # "non-highlighted",
            # "show only collections that contain the selected objects",
            # "/render/freestyle/parameter_editor/line_style/modifiers/geometry/backbone_stretcher",
            # "C:\\blender_docs\\build\\html",
            # "Blender.app",
            # "3D Viewport --> Add --> Mesh --> Monkey"
            # "Object Mode, 60 degrees",
            # "Operators.bidirectional_chain()",
            "microfacet_ggx_aniso(N, T, ax, ay)",
            "Vector(...)",
            "object(s)", # not a function
            "Nuke(*.chan)", # not a function
            "RGBA(0.0, 0.0, 0.0, 1.0)",
            "Add/Remove object(s) to/from collection", # not a function
            "print()",
            "Need selected bone(s)", # not a function
            "principled_hair(N, absorption, roughness, radial_roughness, coat, offset, IOR)",
            "Result(s)",
            "./config/{APP_TEMPLATE_ID}/startup.blend",
            ".*rabbit.*",
        "./Blender.app/Contents/MacOS/Blender",
        "./autosave/ ...",
        "./config/ ...",
        "./config/bookmarks.txt",
        "./config/recent-files.txt",
        "./config/startup.blend",
        "./config/userpref.blend",
        "./config/{APP_TEMPLATE_ID}/startup.blend",
        "./config/{APP_TEMPLATE_ID}/userpref.blend",
        "./datafiles/ ...",
        "./datafiles/locale/{language}/",
        "./python/ ...",
        "./resources/theme/js/version_switch.js",
        "./scripts/ ...",
        "./scripts/addons/*.py",
        "./scripts/addons/modules/*.py",
        "./scripts/addons_contrib/*.py",
        "./scripts/addons_contrib/modules/*.py",
        "./scripts/modules/*.py",
        "./scripts/presets/interface_theme/",
        "./scripts/presets/{preset}/*.py",
        "./scripts/startup/*.py",
        "./scripts/templates_osl/*.osl",
        "./scripts/templates_py/*.py",
        ".001",
        ".Bk",
        ".Bot",
        ".Fr",
        ".L",
        ".MTL",
        ".R",
        ".Top",
        ".app",
        ".avi",
        ".bashrc",
        ".bat",
        ".bin",
        ".blend",
        ".blend1",
        ".blend2",
        ".bmp",
        ".btx",
        ".bvh",
        ".bw",
        ".chan",
        ".cin",
        ".dae",
        ".dpx",
        ".dv",
        ".dvd",
        ".eps",
        ".exr",
        ".fbx",
        ".flv",
        ".gif",
        ".glb",
        ".glb, .gltf",
        ".gltf",
        ".hdr",
        ".html",
        ".inc",
        ".j2c",
        ".jp2",
        ".jpeg",
        ".jpg",
        ".mdd",
        ".mkv",
        ".mov",
        ".mp4",
        ".mpeg",
        ".mpg",
        ".obj",
        ".ogg",
        ".ogv",
        ".osl",
        ".oso",
        ".pc2",
        ".pdb",
        ".ply",
        ".png",
        ".po",
        ".py",
        ".pyd",
        ".rgb",
        ".right",
        ".rst",
        ".sab",
        ".sat",
        ".sgi",
        ".sh",
        ".so",
        ".srt",
        ".stl",
        ".svg",
        ".svn",
        ".tga",
        ".tif",
        ".tiff",
        ".uni",
        ".vdb",
        ".velocities",
        ".vob",
        ".webm",
        ".xxxx",
        ".xyz",
        ".zip",
        "/EXIT",
        "/branches",
        "/copyright",
        "/fr",
        "/tmp",
        "resting..."
        ]

        # t_dict = {
        #     "./config/{APP_TEMPLATE_ID}/startup.blend": "./cấu hình/{TRÌNHỨNGDỤNG_BẢN MẪU_ID}/khởi động.blend/hòa trộn/chuyển đổi",
        # "./config/{APP_TEMPLATE_ID}/userpref.blend": "./cấu hình/{TRÌNHỨNGDỤNG_BẢN MẪU_ID}/userpref.blend/hòa trộn/chuyển đổi",
        # "./datafiles/ ...": "",
        # "./datafiles/locale/{language}/": "",
        # "./python/ ...": "",
        # "./scripts/ ...": "",
        # "./scripts/addons/*.py": "./tập lệnh/các trình bổ sung/*.py",
        # "./scripts/addons/modules/*.py": "./tập lệnh/các trình bổ sung/mô-đun/*.py",
        # "./scripts/addons_contrib/*.py": "./tập lệnh/các trình bổ sung_contrib/*.py",
        # "./scripts/addons_contrib/modules/*.py": "./tập lệnh/các trình bổ sung_contrib/mô-đun/*.py",
        # "./scripts/modules/*.py": "./tập lệnh/mô-đun/*.py",
        # "./scripts/presets/{preset}/*.py": "./tập lệnh/sắp đặt sẵn/{sắp đặt sẵn}/*.py",
        # "./scripts/startup/*.py": "./tập lệnh/khởi động/*.py",
        # "./scripts/templates_osl/*.osl": "./tập lệnh/khuôn mẫu_:abbr:`osl (open shading language: ngôn ngữ tô bóng mở)`:/*.:abbr:`osl (open shading language: ngôn ngữ tô bóng mở)`:",
        # "./scripts/templates_py/*.py": "./tập lệnh/khuôn mẫu_py/*.py",
        # "./scripts/templates_py/*.*": "./tập lệnh/khuôn mẫu_py/*.py",
        # "./w*": "./tập lệnh/khuôn mẫu_py/*.py"
        # }
        var = r'[\w\_\.\-]+'
        param = r'(%s(\,(\s+)?)?)+' % (var)
        multiple = r'^\w+\(s\)$'
        funct = r'(?!%s)^(%s\((%s)?\))$' % (multiple, var, param)
        FUNC = re.compile(funct)

        word = r'(\w+)'
        path_sep = r'([\~\\\\////\\\/\_\-\.\:\*\{\}]{1,2})'
        leading_hyphens = r'(^[-]+)'
        ref_tag = r'(^:%s:$)' % (word)
        single_hyphen = r'(^%s[-:*_\/]%s$)' % (word, word)
        number_format = r'(\d+[.]\d+)'
        hour_format = r'(%s:%s(:%s)?([.]%s)?)' % (word, word, word, word)
        whatever = r'(%s?)[*]{1}(%s?)' % (word, word)
        file_extension = r'^([.]%s)$' % (word)
        return_linefeed = r'^(\\[nr])$'
        bold_word = r'^(\*%s\*)$' % (word)
        digits = r'(\d+)'
        real_number = r'^(%s([,\.]{1}(%s))?)$' % (digits, digits)
        parameters = r'^([\-]{2,})'
        not_allowed = r'(?!(%s|%s|%s|%s|%s|%s|%s|%s|%s))' % (parameters, real_number, bold_word, leading_hyphens, single_hyphen, ref_tag, hour_format, number_format, return_linefeed)
        path = r'(%s|%s)?((%s(%s)?%s)+)+' % (word, path_sep, path_sep, path_sep, word)
        variable = r'[\w_-]+'
        api_path = r'((%s\.%s)+)+' % (variable, variable)
        blender_api = r'^(blender_api\:%s)$' % (api_path)

        extension_0001 = r'(%s\.%s)' % (word, word)
        extension_0002 = r'(%s\.%s)' % (whatever, word)
        extension_0003 = r'(%s\.%s)' % (word, whatever)
        extension_0004 = r'(%s\.%s)' % (whatever, whatever)

        ending_extension = r'(%s|%s|%s|%s)' \
                                        % ( \
                                            extension_0001, \
                                            extension_0002, \
                                            extension_0003, \
                                            extension_0004,
                                           )
        path_def = r'^(%s)%s?(%s)?$' % (path, path_sep, ending_extension)
        # path_def = r'^%s(%s)%s?$' % (not_allowed, path, path_sep)
        path_pattern = r'%s(%s|%s|%s)' % (not_allowed, path_def, file_extension, blender_api)
        PATH_CHECKER = re.compile(path_pattern)

        t_list = [
            # "(E.g. depending on the rest position of your elbow, it may be from (0 to 160) or from (-45 to 135));.",
            # "Cycles, Workbench",
            # "Object and Edit Mode Pivot",
            # "~/.blender/|BLENDER_VERSION|/config/startup.blend",
            # "~/blender_docs",
            # "~/blender_docs/build/html",
            # "~/blender_docs/toos_maintenance",
            # "F-Curves",
            # "2.71",
            # "--debug-xr-time",
            # "prefs-menu",
            # "https://www.youtube.com/watch?v=Ge2Kwy5EGE0",
            # "further information: `File:Manual-2.6-Render-Freestyle-PrincetownLinestyle.pdf <https://wiki.blender.org/wiki/File:Manual-2.6-Render-Freestyle-PrincetownLinestyle.pdf>`__",
            # "Mesh Primitives",
            # "~/.blender/|BLENDER_VERSION|/config/startup.blend",
            "--addons",
            "--app-template",
        "--background",
        "--debug",
        "--debug-all",
        "--debug-cycles",
        "--debug-depsgraph",
        "--debug-events",
        "--debug-ffmpeg",
        "--debug-fpe",
        "--debug-freestyle",
        "--debug-ghost",
        "--debug-gpu",
        "--debug-handlers",
        "--debug-io",
        "--debug-jobs",
        "--debug-libmv",
        "--debug-memory",
        "--debug-python",
        "--debug-value",
        "--debug-wm",
        "--debug-xr",
        "--disable-autoexec",
        "--enable-autoexec",
        "--engine",
        "--factory-startup",
        "--frame-end",
        "--frame-jump",
        "--frame-start",
        "--help",
        "--log",
        "--log \"*,^wm.operator.*\"",
        "--log \"wm.*\"",
        "--log-file",
        "--log-level",
        "--python",
        "--python-console",
        "--python-expr",
        "--python-text",
        "--render-anim",
        "--render-format",
        "--render-frame",
        "--render-frame 1",
        "--render-output",
        "--scene",
        "--start-console",
        "--threads",
        "--use-extension",
        "--verbose",
        "--version",
        "--window-border",
        "--window-fullscreen",
        "--window-geometry",
        "--window-maximized",
        "BLENDER_SYSTEM_DATAFILES",
        "BLENDER_SYSTEM_PYTHON",
        "BLENDER_SYSTEM_SCRIPTS",
        "CYCLES_CUDA_EXTRA_CFLAGS",
        "KHR_draco_mesh_compression",
        "KHR_lights_punctual",
        "KHR_materials_clearcoat",
        "KHR_materials_pbrSpecularGlossiness",
        "KHR_materials_transmission",
        "KHR_materials_unlit",
        "KHR_mesh_quantization",
        "KHR_texture_transform",
        "Keep_Transform",
        "LAYER_frozen",
        "LAYER_locked",
        "LAYER_on",
        ]
        t_list = [
            "Parent Objects",
        ]
        # for t, _ in t_dict.items():
        # output_list = {}
        for t in t_list:
            # # iter = df.pattern MENU_SEP.finditer(t)
            # matched_list = df.findInvert(df.MENU_SEP, t)
            # for loc, mtxt in matched_list.items():
            #     entry = (loc, mtxt)
            #     print(entry)
            #
            # exit(0)
            # o = url(t)
            # try:
            #     valid = all([result.scheme, result.netloc, result.path])
            # except Exception as e:
            #     valid = False
            # print(f'[{t}] [{valid}]')

            # function = FUNC.search(t)
            # is_func = (function is not None)
            # if is_func:
            #     print(f'FUNCTION: [{t}]')
            # else:
            #     print(f'NOT FUNCTION: [{t}]')
            #
            # urlx = URLX()
            # urls = urlx.find_urls(t)
            # if urls:
            #     print(f'URL: [{t}]')
            # is_path = PATH_CHECKER.search(t)
            # is_path = cm.isLinkPath(t)
            # if is_path:
            #     print(f'PATH: [{t}]')
            # else:
            #     print(f'NOT PATH: [{t}]')
            # continue
            # new_t = re.sub('[-_]', ' ', t)
            # ref_list = RefList(msg=new_t, keep_orig=False, tf=tf)
            ref_list = RefList(msg=t, keep_orig=False, tf=tf)
            ref_list.parseMessage()
            ref_list.translateRefList()
            trans = ref_list.getTranslation()
            print(f't:[{t}] => trans:[{trans}]')

        #     # tran_txt = ":abbr:`%s (%s)`" % (t, trans)
        #     # entry = {t: tran_txt}
        #     # output_list.update(entry)
        #     is_ignore = (ref_list.isIgnore())
        #     is_fuzzy = (ref_list.isFuzzy())
        #
        #     # trans, is_fuzzy, is_ignore = tf.translate(t)
        #
        #     # trans = self.binSearch(sorted_list, word_to_find)
        #     # print(f't:[{t}] => trans:[{trans}]')
        # for k, v in output_list.items():
        #     print(f"\"{k}\": \"{v.strip()}\",")

        # print(f't:[{t}]')
        # m_list = df.COMMON_SENTENCE_BREAKS.findall(t)
        # pprint(m_list)
        #
        # doc = nlp(t)
        # sen = []
        # for token in doc:
        #     is_punct = (token.pos_ == 'PUNCT')
        #     if is_punct:
        #         if not sen:
        #             continue
        #
        #         sen_text = ' '.join(sen)
        #         print(f'[{sen_text}]')
        #         sen = []
        #     else:
        #         txt = token.text
        #         s_txt = txt.strip()
        #         is_valid = (len(s_txt) > 0)
        #         if is_valid:
        #             sen.append(token.text)

            # print(f'token.text[{token.text}]; token.lemma_[{token.lemma_}]; token.pos_[{token.pos_}]; token.tag_[{token.tag_}]; token.dep_[{token.dep_}]; token.shape_[{token.shape_}]; token.is_alpha[{token.is_alpha}]; token.is_stop[{token.is_stop}];')
            # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            #       token.shape_, token.is_alpha, token.is_stop)

    def translatePO(self):
        input_po_file=self.get29xViPoPath()
        output_po_file= os.path.join(self.getHome(), 'msgmerge_out_0008.po')
        changed = False
        ignore_list = [
            ('Volume', 'Sound')
        ]
        tf = TranslationFinder()

        input_data = c.load_po(input_po_file)
        for index, m in enumerate(input_data):
            is_first_record = (index == 0)
            if is_first_record:
                continue

            ctx = m.context
            is_keyboard = (ctx == "UI_Events_KeyMaps")
            if is_keyboard:
                continue

            msgid = m.id
            msgstr = m.string

            is_fuzzy = m.fuzzy
            msg_context = m.context
            ig_entry = (msgstr, msg_context)
            is_ignore = (ig_entry in ignore_list)
            is_empty = (not bool(msgstr))
            if is_ignore:
                continue

            is_translate = (is_fuzzy or is_empty)
            if not is_translate:
                continue

            ref_list = RefList(msg=msgid, keep_orig=False, tf=tf)
            ref_list.parseMessage()
            ref_list.translateRefList()
            trans = ref_list.getTranslation()

            if not trans:
                print(f'msgid:[{msgid}] No translation found')
                continue

            tran_state = ref_list.getTranslationState()
            is_ignore = (tran_state == TranslationState.IGNORED)
            if is_ignore:
                print(f'msgid:[{msgid}] IGNORED')
                continue

            is_tran_same = (msgstr == trans)
            if is_tran_same:
                print(f'msgid:[{msgid}] same translation:[{msgstr}] IGNORED')
                continue
            
            print(f'msgid:[{msgid}]')
            print(f'msgstr:[{trans}]')
            if not is_fuzzy:
                m.flags |= {u'fuzzy'}
                # m.flags.remove(u'fuzzy')
            m.string = trans
            changed = True

        if changed:
            print(f'Writing changes to: [{output_po_file}]')
            c.dump_po(output_po_file, input_data)

    def mergeVIPOFiles(self):
        git_hub = os.environ['BLENDER_GITHUB']
        blender_pot_path = f'{git_hub}/../po/blender.pot'
        input_po_file=blender_pot_path
        tran_file = os.path.join(self.getHome(), 'msgmerge_out_0004.po')
        output_po_file=os.path.join(self.getHome(), 'msgmerge_out_0005.po')

        changed = False
        ignore_list = [
            ('Volume', 'Sound')
        ]

        tran_dict = {}
        # tf = TranslationFinder()
        tran_data = c.load_po(tran_file)
        for index, m in enumerate(tran_data):
            if index == 0:
                continue
            k = m.id
            v = m
            entry = {k: v}
            tran_dict.update(entry)

        changed = False
        input_data = c.load_po(input_po_file)
        for index, m in enumerate(input_data):
            if index == 0:
                continue

            k = m.id
            has_tran = (k in tran_dict)
            if has_tran:
                v = tran_dict[k]                # translated entry
                msgstr = v.string
                flags = v.flags
                print_flag = (flags if flags else "")
                print(f'[{k}], [{msgstr}], flags:[{print_flag}]')
                m.string = msgstr
                m.flags = flags
                changed = True
            else:
                print(f'entry [{k}] in blender.pot is NOT FOUND in the tran_file (msgmerge_out_0004.po) file')

        if changed:
            print(f'Writing changes to: [{output_po_file}]')
            c.dump_po(output_po_file, input_data)

    def test_0074(self):
        t1 = 'will'
        t2 = 'willing'
        l1 = len(t1)
        l2 = len(t2)

        match_percent = 0.0
        lx = max(l1, l2)
        lc = 100 / lx
        try:
            for i, c1 in enumerate(t1):
                c2 = t2[i]
                is_matched = (c1 == c2)
                if not is_matched:
                    print(f'stopped at [{i}], c1:[{c1}], c2:[{c2}]')
                    break
                match_percent += lc
        except Exception as e:
            pass
        print(f'match_percent:[{match_percent}]')

    def vipotoJSON(self):
        input_po_file=self.get29xViPoPath()
        input_data = c.load_po(input_po_file)
        output_po_file=os.path.join(self.getHome(), 'vipo.json')
        po_dict = {}
        for index, m in enumerate(input_data):
            is_first_record = (index == 0)
            if is_first_record:
                continue

            msgid = m.id
            msgstr = m.string
            entry={msgid: msgstr}
            po_dict.update(entry)

        po_list = list(po_dict.items())
        po_list.sort()
        po_dict = OrderedDict(po_list)

        writeJSON(output_po_file, po_dict)

    def matchingVIPOChangesToDict(self):
        output_po_file=os.path.join(self.getHome(), 'vipo.json')

        input_po_file=self.get29xViPoPath()
        input_po_data = c.load_po(input_po_file)

        home_dir = os.environ['BLENDER_GITHUB']
        input_dict = os.path.join(home_dir, 'ref_dict_0006_0001.json')

        to_dic = readJSON(input_dict)

        diff_dict = {}
        for m in input_po_data:            
            msgid = m.id
            msgstr = m.string
            is_id_empty = (not msgid)
            if is_id_empty:
                continue
            
            is_in_dict = (msgid in to_dic)
            if not is_in_dict:
                diff_entry = {msgid: msgstr}
                to_dic.update(diff_entry)
                continue
            
            dict_tran = (to_dic[msgid])
            is_tran_same = (msgstr.lower() == dict_tran.lower())
            if is_tran_same:
                continue
            
            msgid = msgid + '&U'
            diff_entry = {msgid: msgstr}
            to_dic.update(diff_entry)
        
        diff_list = list(to_dic.items())
        diff_list.sort()
        diff_dict = OrderedDict(diff_list)
        
        if diff_dict:
            writeJSON(output_po_file, diff_dict)

    def cleanWorkingTextFile(self):
        home = os.environ['BLENDER_GITHUB']
        output_po_file=os.path.join(home, 'working_txt.json')
        input_po_file=os.path.join(home, "working_txt.txt")
        
        input_po_data =readJSON(input_po_file)        
        # dict_path = os.path.join(home_dir, 'ref_dict_0006_0002.json')

        tf = TranslationFinder()
        input_dict = tf.getDict()

        changed = False
        output_data = {}
        for msgid, msgstr in input_po_data.items():
            is_in_dict = (msgid in input_dict)
            if is_in_dict:
                continue

            ref_list = RefList(msg=msgid, keep_orig=False, tf=tf)
            ref_list.parseMessage()
            ref_list.translateRefList()
            trans = ref_list.getTranslation()
            if not trans:
                trans = ""
            entry = {msgid: trans}
            output_data.update(entry)
            changed = True

        if changed:
            writeJSON(output_po_file, output_data)

    def grep_line(self, p, txt_line, file_name):
        found_dict = cm.patternMatchAll(p, txt_line)

        if found_dict:            
            # if not self.is_file_name_printed:
            #     print(f'[{file_name}]')
            #     print('=' * 80)
            #     self.is_file_name_printed = True
            
            return_list = found_dict.values()
            # return_list = [txt_line]
            return return_list
        else:
            return None
        
    def grepPOT(self, pattern, is_sub_group=False, separator=None, is_translate=False, is_considering_side_words=False):
        def isRemove(txt: str):
            remove_list=[
                '\'',
                '"',
                '`',
                '(',
                '*',
                ':',
                '/',
            ]
            for s in remove_list:
                is_remove = (txt.startswith(s) or txt.endswith(s))
                if is_remove:
                    return True
            return False

        def insertFoundItem(f_item):
            if is_translate:
                tran, is_fuzzy, is_ignore = tf.translate(f_item)
                if is_ignore:
                    return
                if tran:
                    f_item = f'[{f_item}] : [{tran}]'
            text_list.append(f_item)
            count_dict[f_item] += 1
            loc_found.append(f_item)

        home_dir = os.environ['DEV_TRAN']
        from_path = os.path.join(home_dir, 'blender_docs/build/gettext')
        po_cach = POCache(from_path, ".pot")
        # po_cach.getFileList()
        # po_cach.loadPOFiles()
        # po_cach.save()

        po_cach.load()
        count_dict = defaultdict(int)

        pats = []
        is_compile_required = isinstance(pattern, str)
        if is_compile_required:
            if is_considering_side_words:
                word = r'(\w+)'
                possible_word = r'(\s?(%s)\s?)?' % (word)
                pats = []
                pat_txt = r'%s' % (pattern)
                p = re.compile(pat_txt)
                pats.append(p)

                pat_txt = r'%s\b%s\b' % (possible_word, pattern)
                p = re.compile(pat_txt)
                pats.append(p)

                pat_txt = r'%s\b%s\b%s' % (possible_word, pattern, possible_word)
                p = re.compile(pat_txt)
                pats.append(p)

                pat_txt = r'%s\b%s\b%s%s' % (possible_word, pattern, possible_word, possible_word)
                p = re.compile(pat_txt)
                pats.append(p)

                pat_txt = r'(\s?(%s)\s?)?' % (pattern)
                p = re.compile(pat_txt)
                pats.append(p)
            else:
                pat_txt = r'%s' % (pattern)
                p = re.compile(pat_txt)
                pats.append(p)
        else:
            pats.append(pattern)

        tf = None
        if is_translate:
            tf = (TranslationFinder() if is_translate else None)

        file_found=[]
        entry_found=[]
        loc_found=[]
        entry_count = 0
        text_list = []
        mm: MatcherRecord = None
        for f, po_rec in po_cach.items():
            loc_found=[]
            for msgid, msgstr in po_rec.items():
                loc_found=[]
                for p in pats:
                    found_list = cm.patternMatchAll(p, msgid)
                    if not found_list:
                        continue

                    if f not in file_found:
                        file_found.append(f)

                    entry = (f, msgid)
                    if not entry in entry_found:
                        entry_found.append(entry)

                    for loc, mm in found_list.items():
                        if is_sub_group:
                            p_loc, p_txt = mm.getSubEntryByIndex(2)
                        else:
                            p_loc, p_txt = mm.getSubEntryByIndex(0)

                        if p_loc in loc_found:
                            continue

                        # if isRemove(p_txt):
                        #     continue

                        if separator:
                            is_sep = bool(separator)
                            is_sep_text = (is_sep and isinstance(separator, str))
                            is_sep_pattern = (is_sep and isinstance(separator, re.Pattern))

                            if is_sep_text:
                                item_list = p_txt.split(separator)
                            elif is_sep_pattern:
                                item_list = separator.split(p_txt)
                            else:
                                item_list = [p_txt]

                            for item in item_list:
                                insertFoundItem(item)
                        else:
                            insertFoundItem(p_txt)
                            if is_sub_group:
                                p_loc, p_txt = mm.getSubEntryByIndex(0)
                                insertFoundItem(p_txt)

        r_list = list(count_dict.items())
        r_list.sort(key=lambda x: x[1])
        pprint(entry_found)
        pprint(file_found)
        pprint(r_list)
        print(f'[{len(entry_found)}] lines in [{len(file_found)}] files.')
        return text_list

    def test_globals(self):
        class test_var():
            def __init__(self):
                self.var_1 = 'One'
                self.var_2 = 'Two'

            def __repr__(self):
                sl = [
                    self.var_1,
                    self.var_2
                ]
                string = '; '.join(sl)
                return string

        x = test_var()
        # k = locals().keys()
        print(x)
        # print(k)

    def test_abbr(self):
        abbr_txt = ":abbr:`SSAO (Screen Space Ambient Occlusion)` and this :abbr:`NDOF (N-Degrees of Freedom)`"
        all_matches = cm.patternMatchAll(df.ABBR_TEXT, abbr_txt)
        all_match_list = list(all_matches.items())
        first_match = all_match_list[0]
        s, mm = first_match
        (ss, ee), orig = mm.getOriginAsTuple()
        (sub_ss, sub_ee), txt = mm.getSubEntryByIndex(0)
        print(f'typeof[{type(all_matches)}]')
        exit(0)
        m = cm.patternMatchAllAsDictNoDelay(df.ABBREV_PATTERN_PARSER, abbr_txt)
        if not m:
            return None

        print(f'typeof[{type(m)}]')
        mm: MatcherRecord = None

        for s, mm in m.items():
            o_loc, o_txt = mm.getOriginAsTuple()
            print(f'orig:[{o_loc}] [{o_txt}]')
            l = mm.getSubEntriesAsList()
            for loc, txt in l:
                print(loc, txt)
                found_texts = cm.ABBR_TEXT_ALL.findall(txt)
                first_entry = found_texts[0]
                abbrev, explanation = first_entry
                print(f'abbrev:{abbrev}')
                print(f'explanation:{explanation}')

            # for loc, txt in orig.items():
            #     print_=(f'loc: [{loc}]; txt:[{txt}]')

    def test_bracket(self):
        # tt = "Use the Operator Search menu: \"Cell fracture selected mesh\" (search \"cell\" will find the list item) and (this is another one)."
        # m = cm.getTextWithinBrackets('(', ')', tt)
        # print(f'[{m}]')

        txt = ' this  '
        lead_c, trail_c, new_txt = cm.stripSpaces(txt)
        print(f'lead_c:{lead_c}; trail_c:{trail_c}; old_txt:[{txt}]; new_txt:[{new_txt}]')

    def test_ref_link(self):
        mm1: MatcherRecord = None
        mm2: MatcherRecord = None
        k = "reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>"
        k = "blender-chat"
        has_html = (cm.URL_LEADING_PATTERN.search(k) is not None)
        ref_link_find_pattern = (cm.REF_WITH_HTML_LINK if has_html else cm.REF_WITH_LINK)
        found_dict = cm.patternMatchAll(ref_link_find_pattern, k)
        mm_list = list(found_dict.items())
        actual_loc = (-1, -1)
        txt = None
        try:
            mm1_entry = mm_list[0]
            actual_loc, mm1 = mm1_entry
            (s1, e1), txt = mm1.getOriginAsTuple()

            mm2_entry = mm_list[1]
            loc2, mm2 = mm2_entry
            (s2, e2), lnk = mm2.getOriginAsTuple()
        except Exception as e:
            pass
        print(f'found_dict')

    def test_remove_blank(self):
        t = 'this two ¶¶¶¶¶¶¶¶¶ this one ¶¶¶'
        found_list = cm.findInvert(cm.FILLER_CHAR_PATTERN, t)
        count=len(found_list)
        print(f'count:{count}')
        pp(found_list)


    def test_ref_link(self):
        # t = "``D. -3.0000 (3.0000) Global``"
        # t = "scene settings <data-scenes-audio>"
        # m = cm.patternMatchAll(cm.REF_WITH_LINK, t)
        t = ":ref:`data-block menus <ui-data-block>`"
        return_dict = cm.patternMatchAll(cm.GA_REF, t)
        for loc, mm in return_dict.items():
            # (s, e), msg = mm.getOriginAsTuple()
            for index, entry in enumerate(mm.items()):
                print(f'{index}: {entry}')
                if index == 1:
                    (s, e), msg = entry
                    found_list = cm.findInvert(cm.REF_LINK, msg)
                    print(found_list)
                print('-' * 80)
        print('*' * 80)
        pp(return_dict)

    def test_parsing_link(self):
        pattern_list = [
            (cm.ARCH_BRAKET_SINGLE_FULL, RefType.ARCH_BRACKET),
            (cm.PYTHON_FORMAT, RefType.PYTHON_FORMAT),
            (cm.FUNCTION, RefType.FUNCTION),
            (cm.AST_QUOTE, RefType.AST_QUOTE),
            (cm.DBL_QUOTE, RefType.DBL_QUOTE),
            (cm.SNG_QUOTE, RefType.SNG_QUOTE),
            (cm.GA_REF, RefType.GA),
        ]

        t_list = [
            "(bracket (within bracket) and without) 'single' \"double\" :doc:`Editing </about/contribute/editing>` " \
            "``master`` ``:term:`Manifold``` **you should always** and *Usage Information*",
            "Camera: ``POINT`` or ``VIEW`` or ``VPORT`` or (wip: ``INSERT(ATTRIB+XDATA)``)",
            "(also :kbd:`Shift-W` :menuselection:`--> (Deform, ...)`).",
            ":ref:`ui-undo-redo-adjust-last-operation`",
            ":ref:`roll rotation <armature-bone-roll>`",
            ":doc:`pose library </animation/armatures/properties/pose_library>`",
        ]
        pattern_list.reverse()
        for t in t_list:
            print(t)
            print('-' * 80)
            blank_msg = str(t)
            for p, reftype in pattern_list:
                is_bracket = (reftype == RefType.ARCH_BRACKET)
                if is_bracket:
                    found_dict = cm.getTextWithinBrackets('(', ')', blank_msg, is_include_bracket=True)
                else:
                    found_dict = cm.patternMatchAll(p, blank_msg)
                mm_list = list(found_dict.items())
                for loc, mm in mm_list:
                    mm_item_list = list(mm.items())
                    for index, mm_entry in enumerate(mm_item_list):
                        print(f'{index} => {mm_entry}')
                        (s, e), txt = mm_entry
                        blank = (cm.FILLER_CHAR * (e - s))
                        blank_msg = blank_msg[:s] + blank + blank_msg[e:]
                    print('-' * 3)
            print('-' * 80)


    def test_find_invert(self):
        # t = 'begin (testing string)'
        # f = cm.findInvert(' ', t, to_matcher_record=True)
        # f = cm.findInvert(cm.SPACES, t, to_matcher_record=True)
        t = "(bracket (within bracket) and without) ¶¶¶¶¶¶¶¶ ¶¶¶¶¶¶¶¶ ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ¶¶¶¶¶¶¶¶¶¶ ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ and ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ Camera: ¶¶¶¶¶¶¶¶¶ or ¶¶¶¶¶¶¶¶ or ¶¶¶¶¶¶¶¶¶ or (wip: ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶) (also ¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶). ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶ (bracket another (within bracket another) and without another)"
        # t = "(bracket (within bracket) and without)  'single' \"double\" :doc:`Editing </about/contribute/editing>` " \
        #     "``master`` ``:term:`Manifold``` **you should always** and *Usage Information* " \
        #     "Camera: ``POINT`` or ``VIEW`` or ``VPORT`` or (wip: ``INSERT(ATTRIB+XDATA)``) " \
        #     "(also :kbd:`Shift-W` :menuselection:`--> (Deform, ...)`). " \
        #     ":ref:`ui-undo-redo-adjust-last-operation` " \
        #     ":ref:`roll rotation <armature-bone-roll>` " \
        #     ":doc:`pose library </animation/armatures/properties/pose_library>` (another bracket (another within bracket) and without another)"
        # f = cm.findInvert('\(|\)', t, to_matcher_record=True, is_removing_surrounding_none_alphas=False)
        f = cm.findInvert(cm.FILLER_PARTS, t)
        print(f)
        # pattern = '\(|\)'
        # pat_string = r'(%s)(\w[^%s]+\w)(%s)' % (pattern, pattern, pattern)
        # pat = re.compile(pat_string)
        # found_dict = cm.patternMatchAll(pat, t)
        # print(found_dict)

    def test_forward_slashes(self):
        t = "Front/Camera Mapping"
        p = re.compile(r'[\w\s]?([\/]+)[\w\s]?')
        l = cm.patternMatchAll(p, t)
        print(l)

    def test_translate_json_file(self):
        git_hub = os.environ['BLENDER_GITHUB']
        home = f'{git_hub}/..'
        input_file= os.path.join(home, "blender_manual/test_txt.json")
        output_file = os.path.join(home, "blender_manual/test_tran_txt.json")
        input_data = readJSON(input_file)

        tf = TranslationFinder()
        output_data={}
        error=False
        for msgid, msgstr in input_data.items():
            try:
                ref_list = RefList(msg=msgid, keep_orig=False, tf=tf)
                ref_list.parseMessage()
                ref_list_to_list = list(ref_list.items())
                ref_list_to_list.sort()
                ref_list.translate()
                trans = ref_list.getTranslation()
                entry={msgid: trans}
                output_data.update(entry)
            except Exception as ee:
                error=True
                print(ee)
                raise ee
        if not error:
            writeJSON(output_file, output_data)

    def test_re(self):
        from sentence import StructRecogniser as SR
        # class StructRecogniser():
        #     '''
        #         paragraph.StructRecogniser
        #         ~~~~~~~~~~~~~~~~~~~~~~~~~~
        #         This class recognise an entry of dictionary as a sentence structure which will be in the form:
        #             dict_sl = "chang\\w+ $$$ to $$$"
        #             dict_tl = "chuyển đổi từ $$$ sang thành $$$",
        #
        #         This structure will help to recognise and translate commonly know structures, such as:
        #             src_sl_txt = "changes the structure from CONSTRUCTIVE to DECONSTRUCTIVE"
        #
        #         - the class will set flag 'is_sent_struct' to True if the 'dict_sl' containing '$$$' to help identifying
        #         a dictionary entry is a sentence structure or not
        #         - the structure 'something $$$...' will be converted to a pattern (dict_sl) to recognise the
        #         sentences like 'src_sl_txt'. This pattern can be used to store in the 'sent_struct_dictionary' to help
        #         parsing text parts during translation.
        #         - once found, and parsed, the class can automatically generate the correct MatchRecord structure,
        #             self.sent_tl_rec
        #         ready to be used, translated. It also output the text that needed to be further translated, parsed etc,
        #         like reflist, for instance.
        #     '''
        #     def __init__(self, dict_sl_txt=None, dict_tl_txt=None, tran_sl_txt=None, translation_engine=None):
        #         self.is_sent_struct=False
        #         # key in dictionary, in the form 'chang\\w+ $$$ to $$$'
        #         self.dict_sl_txt: str = dict_sl_txt
        #
        #         # translation of key in dictionary, in the form 'đổi  $$$ sang thành $$$'
        #         self.dict_tl_txt: str = None
        #         if dict_tl_txt:
        #             self.dict_tl_txt: str = u'%s' % (dict_tl_txt)
        #
        #         # text in found in source language which matched the sentence structure pattern
        #         self.tran_sl_txt: str = None
        #         if tran_sl_txt:
        #             self.tran_sl_txt = tran_sl_txt
        #
        #         # text that is the result of structure translation
        #         self.tran_tl_txt: str = None
        #
        #         # pattern to recognise the sentence structure in the source language text, which will use
        #         # the preset translation
        #         self.recog_pattern: re.Pattern = None
        #
        #         self.dict_sl_rec: MatcherRecord = None
        #         self.dict_tl_rec: MatcherRecord = None
        #         self.sent_sl_rec: MatcherRecord = None
        #         self.sent_tl_rec: MatcherRecord = None
        #         self.tf = translation_engine
        #
        #         self.setupRecords()
        #
        #     def __repr__(self):
        #         string = "\n{!r}".format(self.__dict__)
        #         return string
        #
        #     def isSentenceStructure(self):
        #         return self.is_sent_struct
        #
        #     def setUpOneRecord(self, the_txt):
        #         the_txt_word_list = cm.creatSentRecogniserPattern(the_txt)
        #         mm = MatcherRecord(txt=the_txt)
        #         mm.initUsingList(the_txt_word_list)
        #         return mm, the_txt_word_list
        #
        #     def setupRecords(self):
        #         try:
        #             # self.dict_sl_rec, dict_sl_txt_word_list = self.setUpOneRecord(self.dict_sl_txt)
        #             # self.recog_pattern = cm.formPattern(dict_sl_txt_word_list)
        #             #
        #             # self.dict_tl_rec, dict_tl_txt_word_list = self.setUpOneRecord(self.dict_tl_txt)
        #
        #             dict_tl_list = self.dict_tl_rec.getSubEntriesAsList()
        #             sent_tl_list = CP.deepcopy(dict_tl_list)
        #
        #             self.sent_tl_rec = CP.copy(self.dict_tl_rec)
        #             self.sent_tl_rec.clear()
        #             self.sent_tl_rec.update(sent_tl_list)
        #
        #
        #             self.is_sent_struct = True
        #         except Exception as e:
        #             # print(f'setupDictRecord() [{self}] ERROR:{e}')
        #             self.is_sent_struct = False
        #         self.setupSentSLRecord()
        #
        #     def setupSentSLRecord(self):
        #         sl_rec: MatcherRecord = None
        #         try:
        #             sl_rec = cm.patternMatch(self.recog_pattern, self.tran_sl_txt)
        #             list_of_words = sl_rec.getSubEntriesAsList()
        #             interested_part = list_of_words[1:]
        #             sl_rec.clear()
        #             sl_rec.update(interested_part)
        #         except Exception as e:
        #             if not self.tran_sl_txt:
        #                 return
        #             sl_rec = MatcherRecord(txt=self.tran_sl_txt)
        #         self.sent_sl_rec = sl_rec
        #
        #     def getListOfTextsNeededToTranslate(self):
        #         '''
        #             using the index for $$$ in the 'sent_sl_rec' to identify the text
        #             required (unknown) to be translated
        #             tran_list hold the tuple (loc, txt), this will be held in the 'sent_tl_rec'
        #             eventually
        #         '''
        #
        #         def getListOfAnythingPosition(mm_record: MatcherRecord):
        #             '''
        #                 Find list of indexes where $$$ is mentioned in the parsed external text
        #             '''
        #             post=[]
        #             try:
        #                 mm_record_word_list = mm_record.getSubEntriesAsList()
        #                 for index, entry in enumerate(mm_record_word_list):
        #                     (loc, txt) = entry
        #                     is_filler = (df.SENT_STRUCT_PAT.search(txt) is not None)
        #                     if not is_filler:
        #                         continue
        #
        #                     post.append(index)
        #             except Exception as e:
        #                 pass
        #                 # print(f'getListOfTextNeededToTranslate(); mm_record:[{mm_record}]; ERROR:[{e}]')
        #             return post
        #
        #         def getInitialListOfTextsToBeTranslated():
        #             # run through the dictionary's source language indexes, where $$$ was
        #             # note: we are not in the loop where location and length of strings for each element is relevant
        #             # these should be dealt with later
        #             for index, from_index in enumerate(dict_sl_any_index_list):
        #                 # to target index of $$$ in the dictionary target language, where $$$ was
        #                 to_index = dict_tl_any_index_list[index]
        #
        #                 # extract untranslated text out of external sentence where $$$ supposedly occupied
        #                 # this will give you texts supposedly to be translated:
        #                 # such as:
        #                 #           the structure from CONSTRUCTIVE
        #                 #           DECONSTRUCTIVE
        #                 untran_loc, untran_txt = sent_sl_list_of_txt[from_index]
        #
        #                 # location and text where $$$ was in the external sentence, this will help us to identify start
        #                 # location. The END location, however, will be the length of text (any_s + txt_length)
        #                 any_loc, any_txt = sent_tl_list[to_index]
        #                 txt_length = len(untran_txt)
        #                 (any_s, any_e) = any_loc
        #                 new_loc = (any_s, any_s + txt_length)
        #                 new_entry = (new_loc, untran_txt)
        #
        #                 # insert into the correct position, but offsets of next text items will be out of sync
        #                 new_sent_tl_list.pop(to_index)
        #                 new_sent_tl_list.insert(to_index, new_entry)
        #
        #         def correctTextsOffsets():
        #             # now correct offsets for subsequent texts
        #             corrected_sent_tl_list=[]
        #             correct_sent_tl_txt_list=[]
        #             ls = le = 0
        #             test_dict = OrderedDict(new_sent_tl_list)
        #             txt_list = test_dict.values()
        #             test_full_txt = ''.join(txt_list)
        #             for index, (loc, txt) in enumerate(new_sent_tl_list):
        #                 ts, te = loc
        #                 txt_length = len(txt)
        #                 le = (ls + txt_length)
        #                 new_loc = (ls, le)
        #                 new_entry = (new_loc, txt)
        #                 test_txt = test_full_txt[ls: le]
        #                 corrected_sent_tl_list.append(new_entry)
        #                 is_entry_untranslated = (index in dict_tl_any_index_list)
        #                 if is_entry_untranslated:
        #                     text_to_translate_list.append(new_entry)
        #                 correct_sent_tl_txt_list.append(txt)
        #                 ls = le
        #
        #             ntxt = "".join(correct_sent_tl_txt_list)
        #             ns = 0
        #             ne = len(ntxt)
        #             # Note, the s, e here is a temporal value, this will have to matched up with the originally parsed location
        #             n_mm = MatcherRecord(s=ns, e=ne, txt=ntxt)
        #             n_mm.appendSubRecords(corrected_sent_tl_list)
        #             self.sent_tl_rec = n_mm
        #
        #         text_to_translate_list=[]
        #         dict_sl_any_index_list = None
        #         dict_tl_any_index_list = None
        #         sent_sl_list_of_txt = None
        #         sent_tl_list = None
        #         try:
        #             dict_sl_any_index_list = getListOfAnythingPosition(self.dict_sl_rec)
        #             # indexes of $$$ in the dictionary's target language entry in the form of [int, int...]
        #             dict_tl_any_index_list = getListOfAnythingPosition(self.dict_tl_rec)
        #
        #             # list of text in the external source language sentence, with untranslated text
        #             sent_sl_list_of_txt = self.sent_sl_rec.getSubEntriesAsList()
        #             # list of texts in external source language sentence, with untranslated text, but will be
        #             # replaced with translated parts from the dictionary target language ie. text on both sides of $$$
        #             sent_tl_list = self.sent_tl_rec.getSubEntriesAsList()
        #
        #             # make a copy here for easy observation during debugging
        #             new_sent_tl_list = CP.copy(sent_tl_list)
        #
        #             getInitialListOfTextsToBeTranslated()
        #             correctTextsOffsets()
        #             print('')
        #         except Exception as e:
        #             try:
        #                 loc = self.sent_sl_rec.getMainLoc()
        #                 txt = self.sent_sl_rec.getMainText()
        #                 entry=(loc, txt)
        #                 text_to_translate_list.append(entry)
        #             except Exception as ee:
        #                 pass
        #         return text_to_translate_list
        #
        #     def setTlTranslation(self, trans_list: list):
        #         tl_txt = self.sent_tl_rec.txt
        #         trans_list.sort(reverse=True)
        #         for loc, tran_txt in trans_list:
        #             tl_txt = cm.jointText(tl_txt, tran_txt, loc)
        #         self.sent_tl_rec.txt = tl_txt
        #
        #     def getTranslation(self):
        #         try:
        #             return self.sent_tl_rec.txt
        #         except Exception as e:
        #             return ""
        #
        #     def translate(self):
        #         try:
        #             if self.is_sent_struct:
        #                 list_of_text_to_be_translated = self.getListOfTextsNeededToTranslate()
        #             else:
        #                 main_entry = self.sent_sl_rec.getMainEntry()
        #                 list_of_text_to_be_translated=[main_entry]
        #
        #             tran_list=[]
        #             for loc, txt in list_of_text_to_be_translated:
        #                 tran = self.translateText(txt)
        #                 if tran:
        #                     entry=(loc, tran)
        #                     tran_list.append(entry)
        #             self.setTlTranslation(tran_list)
        #         except Exception as e:
        #             pass
        #
        #     def translateText(self, txt):
        #         try:
        #             ref_list = RefList(msg=txt, keep_orig=False, tf=self.tf)
        #             ref_list.parseMessage()
        #             ref_list_to_list = list(ref_list.items())
        #             ref_list_to_list.sort()
        #             ref_list.translate()
        #             trans = ref_list.getTranslation()
        #             return trans
        #         except Exception as e:
        #             print(f'translateText(): {e}')
        #             return None


        # t = "(bracket (within bracket) and without) 'single' \"double\" :doc:`Editing </about/contribute/editing>` ``master`` ``:term:`Manifold``` **you should always** and *Usage Information* Camera: ``POINT`` or ``VIEW`` or ``VPORT`` or (wip: ``INSERT(ATTRIB+XDATA)``) (also :kbd:`Shift-W` :menuselection:`--> (Deform, ...)`). :ref:`ui-undo-redo-adjust-last-operation` :ref:`roll rotation <armature-bone-roll>` :doc:`pose library </animation/armatures/properties/pose_library>` (bracket another (within bracket another) and without another)"
        # dict_sl = "chang\\w+ $$$ to $$$"
        # dict_tl = "đổi từ $$$ sang thành $$$",
        # src_sl_txt = "changes the structure from CONSTRUCTIVE to DECONSTRUCTIVE"
        #
        # dict_sl = "e.g: $$$"
        # dict_tl = "ví dụ: $$$ chẳng hạn",
        # src_sl_txt = "e.g: modeling and not modelling, color and not colour"
        #
        # dict_sl = "turn\\w+? $$$ attention\\w+? to"
        # dict_tl = "dồn sự tập trung/quan/chú tâm $$$ đến/tới/vào",
        # src_sl_txt = "It is recommended to pay attention to image resolution and color depth when mixing and matching images."
        #
        # # "turn\\w+? $$$ attention\\w+? to": "dồn sự tập trung/quan/chú tâm $$$ đến/tới/vào",
        # # "turn\\w+? not $$$ attention\\w? to": "không nên/chớ dồn sự tập trung/quan/chú tâm $$$ đến/tới/vào",
        #
        # # "e.g. $$$": "ví dụ $$$ chẳng hạn",
        # # v_txt = u'%s' % (v)
        #
        # dict_sl = "e.g. $$$"
        # dict_tl = "ví dụ $$$ chẳng hạn",
        # src_sl_txt = "e.g. modeling and :abbr:`NMDL (not modelling)`, color and not colour"

        dict_sl = "turn\\w+? not $$$ attention\\w+? to $$$"
        dict_tl = "ngừng việc/đừng/chớ dồn sự tập trung/quan/chú tâm $$$ đến/tới/vào $$$",
        src_sl_txt = "turning not our attentions to the ear."
        tf = TranslationFinder()

        # s_recog = StructRecogniser(dict_sl_txt=dict_sl,
        #                            dict_tl_txt=dict_tl,
        #                            tran_sl_txt=src_sl_txt,
        #                            translation_engine=tf)
        # s_recog.translate()
        # tran = s_recog.getTranslation()
        # print(f'from: {src_sl_txt}')
        # print(f'to: {tran}')

        s_recog = SR(tran_sl_txt=src_sl_txt,
                    translation_engine=tf)
        # s_recog.setupRecords()
        s_recog.translate()
        tran = s_recog.getTranslation()
        print(f'tran:{tran}')
        # list_of_text_to_be_translated = s_recog.getListOfTextsNeededToTranslate()

        # found_list = s_recog.recog_pattern.findall(src_sl_txt)
        # s_recog.tran_sl_txt = src_sl_txt

        # if s_recog.sent_tl_rec:
        #     final_txt = s_recog.sent_tl_rec.txt
        #     for loc, txt in list_of_text_to_be_translated:
        #         (ss, se) = loc
        #         actual_txt = final_txt[ss: se]
        #         print(actual_txt)
        #
        #     print(f'sentence: [{final_txt}]')
        #
        # print('to be translated:')
        # print(list_of_text_to_be_translated)

        # mm_rec_dict = cm.patternMatchAll(df.SENT_STRUCT_PAT, struct_pat)
        # # print(f'[{mm_rec_dict}]')
        #
        # k_list = cm.findInvert(df.SENT_STRUCT_PAT, struct_pat)
        # # v_list = cm.findInvert(df.SENT_STRUCT_PAT, v_txt)
        # #
        # # k_pat_list = []
        # # k_list = list(k_list.items())
        # # k_list.sort()
        # # for k_loc, k_mm in k_list:
        # #     k_txt = k_mm.getMainText()
        # #     k_pat_list.append(f'({k_txt})')
        # tp_txt = df.SENT_STRUCT_PAT.sub('(.*)', struct_pat)
        # tp_txt = f'({tp_txt})'
        # tp_txt = r'%s' % (tp_txt)
        # tp = re.compile(tp_txt)
        # # tp = re.compile(r'(change)(.*)(to)(.*)')
        # tp_word_list = patStructToListOfWords(struct_pat)
        # tp = formPattern(tp_word_list)
        # tp_mm = MatcherRecord()
        # tp_mm.initUsingList(tp_word_list, original_text=struct_pat, pattern=tp)
        # tfound_dict = cm.patternMatchAll(tp, t)
        # print(tfound_dict)

        # v_pat_list = []
        # v_list = list(v_list.items())
        # v_list.sort()
        # for v_loc, v_mm in v_list:
        #     v_txt = v_mm.getMainText()
        #     v_pat_list.append(f'({v_txt})')
        #
        # v_pat_list.sort(reverse=False)
        # vp = re.compile(u'(.*)'.join(v_pat_list))
        # vp = re.compile(u'(đổi từ)(.*)(sang thành)(.*)')
        # vtxt = u'%s' % (v)
        # vp_word_list = patStructToListOfWords(vtxt)
        # vp_mm = MatcherRecord()
        # vp_mm.initUsingList(vp_word_list)
        # print(vp_word_list)

    def test_translate_0001(self, text_list=None):
        from paragraph import Paragraph as PR
        tf = TranslationFinder()
        if not text_list:
            t_list = [
                # "``sin(x)/x``",
                # "``singing``",
                # "``cosy``",
                # "particularly those used in :abbr:`CAD (Computer-Aided Design)`",
                # "Continue with the next step: :doc:`Editing </about/contribute/editing>`.",
                # "``:menuselection:`3D Viewport --> Add --> Mesh --> Monkey``` -- menus.",
                # "Zoom out eight zoom levels (:kbd:`NumpadMinus` -- eight times).",
                # "(:abbr:`POV (Point Of View)` and camera) locations.Avoid `weasel words <https://en.wikipedia.org/wiki/Weasel_word>`__ and **bold text** with \"some quoted\" and \'single quoted\'",
                # "Sorting ``Operators.sort()``",
                # "RGB(0.6, 0.6, 1.0)",
                # "%s Diffuse, %s Glossy, %s Transmission",
                # "Couldn't open file %r (%s)",
                # "``D. -3.0000 (3.0000) Global``",
                # "``0 + (cos(frame / 8) * 4)``",
                # ":ref:`curve-bezier`",
                # ":ref:`curve-nurbs`",
                # "Curve NURBS: ``curved-POLYLINE``",
                # "These :ref:`data-block menus <ui-data-block>` are used",
                # "See :term:`Alpha Channel`.",
                # "``:term:`Manifold``` -- Links to an entry in the :doc:`Glossary </glossary/index>`."
                # "especially :ref:`NURBS <curve-nurbs>` ones"
                # ":doc:`NLA </editors/nla/introduction>`.",
                # "`Radiosity (computer graphics) <https://en.wikipedia.org/wiki/Radiosity_%28computer_graphics%29>`__"
                # "`MPEG-4(DivX) <https://en.wikipedia.org/wiki/MPEG-4>`__",
                # "like the :doc:`\"limit\" ones </animation/constraints/transform/limit_location>`",
                # "like e.g. the :doc:`\"copy\" ones </animation/constraints/transform/copy_location>`).",
                # "What is here `previous section <Write the Add-on (Simple)>`_. But as this...",
                # "Generally, **you should always translate exactly what is in the text**,",
                # "Otherwise you will get a warning: ``'locale' is not under version control as present situation``",
                # "'locale' is this word"
                # "``:abbr:`SSAO (Screen Space Ambient Occlusion)``` (bracket (within bracket) and without) 'single' \"double\" :doc:`Editing </about/contribute/editing>` " \
                # "``master`` ``:term:`Manifold``` **you should always** and *Usage Information* " \
                # "Camera: ``POINT`` or ``VIEW`` or ``VPORT`` or (wip: ``INSERT(ATTRIB+XDATA)``) " \
                # "``:menuselection:`3D Viewport --> Add --> Mesh --> Monkey``` " \
                # "(also :kbd:`Shift-W` :kbd:`Ctrl-0`, :kbd:`Shift-Ctrl-=`, :kbd:`Ctrl-Minus`, :kbd:`Shift-Ctrl-8`, :kbd:`Ctrl-Slash`, :kbd:`Shift-Ctrl-Comma`, :kbd:`Shift-Ctrl-Period` :menuselection:`--> (Deform, ...)`), :menuselection:`--> Ambient Occlusion`" \
                # ":ref:`ui-undo-redo-adjust-last-operation` " \
                # ":ref:`roll rotation <armature-bone-roll>` " \
                # ":doc:`pose library </animation/armatures/properties/pose_library>` (bracket another (within bracket another) and without another) with some free text",
                # "(bracket (within bracket) and without) and  (bracket another (within bracket another) and without another) with some free text",
                # "depending on the particle system's render settings, see :doc:`Visualization </physics/particles/emitter/render>`",
                # "Generally, ",
                # "depending on the particle system's render settings, see :doc:`Visualization </physics/particles/emitter/render>`",
                # "``diffuse_ramp(N, colors[8])``",
                # "``ambient_occlusion()``",
                # "Result(s)",
                # "down/right arrow icon",
                # "down/up arrow peak icon",
                # "e.g. \".R\"/\".L\", or \"_right\"/\"_left\" ...",
                # "e.g. \"handL\"/ \"handR\" will not work!",
                # "quadruple",
                # "e.g. 50 frames"
                # "e.g. Sky Texture node",
                # "e.g. Linear, Bézier, Quadratic, etc.",
                # "e.g. Turing and above",
                # "e.g. ``*-0001.jpg``, ``*-0002.jpg``, ``*-0003.jpg``, etc, of any image format",
                # "e.g. ``.png`` will list all PNG files",
                # "e.g. all hydrogen atoms form one instancing vertices structure",
                # "e.g. an Armature modifier or any deformation modifier",
                # "e.g. an edge",
                # "e.g. an empty or camera",
                # "e.g. anger or surprise",
                # "e.g. any non-parallel vector",
                # "e.g. arms, legs, spines, fingers...",
                # "e.g. at points where edges make an acute turn",
                # "e.g. because the library file was moved or renamed after linking from it",
                # "e.g. changing ``file_01.blend`` to ``file_02.blend``",
                # "changing ``file_01.blend`` to ``file_02.blend``",
                # "e.g. changing ``file_01.blend`` to ``file_02.blend``",
                # "her object",
                # "e.g. circles",
                "e.g. diffuse color",
            ]

        else:
            t_list = text_list

        try:
            for t in t_list:
                pr = PR(txt=t, translation_engine=tf)
                tran = pr.translate()
                print(tran)

        except Exception as e:
            print(e)

        # # p = re.compile(r'(?:\s|^)(%\w)(?:\W|$)')
        # result_list=[]
        # try:
        #     for t in t_list:
        #         # test_txt = t[185:190]
        #         # is_function = cm.FUNCTION.findall(t)
        #         # print(f'is_function:[{is_function}]')
        #         # exit(0)
        #         try:
        #             ref_list = RefList(msg=t, keep_orig=False, tf=tf)
        #             ref_list.parseMessage()
        #             ref_list_to_list = list(ref_list.items())
        #             ref_list_to_list.sort()
        #             ref_list.translate()
        #             trans = ref_list.getTranslation()
        #             entry=(t, trans)
        #             result_list.append(entry)
        #         except Exception as ee:
        #             print(ee)
        #             print('*' * 30)
        #         # print(f't:[{t}] => trans:[{trans}]')
        # except Exception as e:
        #     pass
        # print(f'-' * 80)
        # for t, tran in result_list:
        #     msg = t.replace('"', '\\"')
        #     sent_translation = tran.replace('"', '\\"')
        #     output = f'"{msg}": "{sent_translation}",'
        #     print(output)

    def run(self):
        # self.test_forward_slashes()
        # self.test_find_invert()
        # self.test_re()
        # self.test_parsing_link()
        # self.test_ref_link()
        # self.test_remove_blank()
        # self.test_ref_link()
        # self.test_bracket()
        # self.test_abbr()
        # self.test_globals()
        # self.matchingVIPOChangesToDict()
        # self.vipotoJSON()
        # self.test_0074()
        # self.test_0073()
        # self.plistToText()
        # self.test_binary_search()
        # self.sorting_temp_05()
        self.resort_dictionary()
        # self.test_translate_json_file()
        self.test_translate_0001()
        # t_list = self.grepPOT(re.compile(r'[^\w\s\-\_\;]+(\w)[\w\s\-\_\.\,\;]+(\w)[^\w\s\-\_\.\,\;]+'))
        # self.test_translate_0001(text_list=t_list)
        # mnu_p = re.compile(r':menuselection:[`]([^`]+)[`]')
        # sep_pat = re.compile(r'\s?(-->)\s?')
        # self.grepPOT(mnu_p, is_sub_group=True, separator=sep_pat, is_translate=True)
        # p = re.compile(r'(?!(\w[\.\,]\w))(\w[^\.\,]+\S)[\.\,](\s|$)')
        # self.grepPOT(p, is_sub_group=True)
        # self.grepPOT(df.GA_REF, is_sub_group=True)
        # simple_bracket = re.compile(r'\s?\([^\(\)]+\)\s?')
        # self.grepPOT(simple_bracket, is_sub_group=False)
        # self.grepPOT(df.FUNCTION, is_sub_group=False)
        # self.grepPOT('have more', is_considering_side_words=True)
        # self.cleanWorkingTextFile()
        # self.translatePO()
        # self.test_0063()
        # print(self.recur(4))
        # self.parseSVG()
        # self.translate_po_file()
        # self.test_pattern_0001()
        # self.test_insert_abbr()
        # self.test_capt_0001()
        # self.test_refs_0001()
        # self.test_0064()
        # self.test_0066()
        # self.test_0067()
        # self.test_0068()
        # self.test_0069()
        # self.test_0070()
        # self.test_0072()
        # self.test_0071()
        # self.cleanDictionary()
        # self.diffPOTFile()
        # self.test_loc_remain()
        # self.mergeVIPOFiles()


# # trans_finder = TranslationFinder()
# def tranRef(msg, is_keep_original):
#     ref_list = RefList(msg=msg, keep_orig=is_keep_original, tf=trans_finder)
#     ref_list.parseMessage()
#     ref_list.translateRefList()
#     tran = ref_list.getTranslation()
#     trans_finder.addDictEntry((msg, tran))
#     print("Got translation from REF_LIST")
#     return tran

x = test()
x.run()


