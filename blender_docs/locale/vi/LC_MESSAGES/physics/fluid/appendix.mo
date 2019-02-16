��          �               l  �   m  f  �    V  �   Y  �  �  
  �  �   �       X  +    �	       �   
  �   �  �   o       A      �   b  4   V    �  �   �  �  Y  �     f  �    �  �   �  �  �  
  0  �   ;     �  X  �    ,     �  �   �  �   c  �   #     �  A   �  �      4   !    C!  �   X"   Before running a high resolution simulation that might take hours, check the overall timing first by doing lower resolution runs. Blender crashes after clicking *bake* -- this can happen if the resolution is really high and more than 2GB are allocated, causing Blender to crash. Reducing the resolution should help in this case. Many operating systems limit the total amount of memory that can be allocated by a *process*, such as Blender, even if the *machine* has more memory installed. Blender freezes after clicking *bake*. Pressing :kbd:`Esc` makes it work again after a while -- this can happen if the resolution is too high and memory is swapped to a drive, making everything horribly slow. Reducing the resolution should help in this case. Currently there is a problem with zero gravity simulation. It could be avoided by simply selecting a very small gravity until this is fixed. Currently these files will not be automatically deleted, so it is a good idea to e.g. create a dedicated directory to keep simulation results. Doing a fluid simulation is similar to clicking the *animation* button. Currently you have to take care of organizing the fluid surface meshes in some directory by yourself. If you want to stop using the fluid simulation, you can simply delete all the ``*fluid*.bobj.gz`` files. Do not be surprised, but you will get whole bunch of mesh (.bobj.gz) files after a simulation. One set for preview, and another for final. Each set has a ``.gz`` file for each frame of the animation. Each file contains the simulation result -- so you will need them. Do not try to do a complicated scene all at once. Blender has a powerful compositor that you can use to combine multiple animations. Fluid Appendix Fluid objects must be completely inside the bounding box of the domain object. If not, baking may not work correctly or at all. Fluid and obstacle objects can be meshes with complex geometries. Very thin objects might not appear in the simulation, if the chosen resolution is too coarse to resolve them (increasing it might solve this problem). For example, to produce an animation showing two separate fluid flows while keeping your domain small, render one ``.avi`` using the one flow. Then move the domain and render another ``.avi`` with the other flow using an alpha channel (in a separate B&W .avi?). Then, composite both ``.avi``\ 's using the compositor's Add node. A third ``.avi`` is usually the smoke and mist and it is laid on top of everything as well. Add a rain sheet on top of the mist and spray and you will have quite a storm brewing! And then lightning flashes, trash blowing around, all as separate animations, compositing the total for a truly spectacular result. Hints If an object is initialized as *Volume*, it has to be closed and have an inner side (a plane will not work). To use planes, switch to *Shell*, or extrude the plane. If the fluid simulation exits with an error message (stating e.g. that the "init has failed"), make sure you have valid settings for the domain object, e.g. by resetting them to the defaults. If the setup seems to go wrong, make sure all the normals are correct (hence, enter *Edit Mode*, select all, and recalculate normals once in a while). Limitations & Workarounds Memory used doubles when you set surface subdivision from 1 to 2. Note that first frame may well take only a few hundred MBs of ram-memory, but latter ones go over one GB, which may be why your bake fails after awhile. If so, try to bake one frame at the middle or end at full res so you will see if it works. Some useful hints about fluid simulation in Blender: The meshes should be closed, so if some parts of e.g. a fluid object are not initialized as fluid in the simulation, check that all parts of connected vertices are closed meshes. Unfortunately, the Suzanne (monkey) mesh in Blender is not a closed mesh (the eyes are separate). Using "generate particles" will also add memory requirements, as they increase surface area and complexity. Ordinary fluid simulations generated particles probably consume less memory. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-04 21:09+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 Before running a high resolution simulation that might take hours, check the overall timing first by doing lower resolution runs. Blender crashes after clicking *bake* -- this can happen if the resolution is really high and more than 2GB are allocated, causing Blender to crash. Reducing the resolution should help in this case. Many operating systems limit the total amount of memory that can be allocated by a *process*, such as Blender, even if the *machine* has more memory installed. Blender freezes after clicking *bake*. Pressing :kbd:`Esc` makes it work again after a while -- this can happen if the resolution is too high and memory is swapped to a drive, making everything horribly slow. Reducing the resolution should help in this case. Currently there is a problem with zero gravity simulation. It could be avoided by simply selecting a very small gravity until this is fixed. Currently these files will not be automatically deleted, so it is a good idea to e.g. create a dedicated directory to keep simulation results. Doing a fluid simulation is similar to clicking the *animation* button. Currently you have to take care of organizing the fluid surface meshes in some directory by yourself. If you want to stop using the fluid simulation, you can simply delete all the ``*fluid*.bobj.gz`` files. Do not be surprised, but you will get whole bunch of mesh (.bobj.gz) files after a simulation. One set for preview, and another for final. Each set has a ``.gz`` file for each frame of the animation. Each file contains the simulation result -- so you will need them. Do not try to do a complicated scene all at once. Blender has a powerful compositor that you can use to combine multiple animations.  -- Fluid Appendix Fluid objects must be completely inside the bounding box of the domain object. If not, baking may not work correctly or at all. Fluid and obstacle objects can be meshes with complex geometries. Very thin objects might not appear in the simulation, if the chosen resolution is too coarse to resolve them (increasing it might solve this problem). For example, to produce an animation showing two separate fluid flows while keeping your domain small, render one ``.avi`` using the one flow. Then move the domain and render another ``.avi`` with the other flow using an alpha channel (in a separate B&W .avi?). Then, composite both ``.avi``\ 's using the compositor's Add node. A third ``.avi`` is usually the smoke and mist and it is laid on top of everything as well. Add a rain sheet on top of the mist and spray and you will have quite a storm brewing! And then lightning flashes, trash blowing around, all as separate animations, compositing the total for a truly spectacular result. Gợi ý -- Hints If an object is initialized as *Volume*, it has to be closed and have an inner side (a plane will not work). To use planes, switch to *Shell*, or extrude the plane. If the fluid simulation exits with an error message (stating e.g. that the "init has failed"), make sure you have valid settings for the domain object, e.g. by resetting them to the defaults. If the setup seems to go wrong, make sure all the normals are correct (hence, enter *Edit Mode*, select all, and recalculate normals once in a while).  -- Limitations & Workarounds Memory used doubles when you set surface subdivision from 1 to 2. Note that first frame may well take only a few hundred MBs of ram-memory, but latter ones go over one GB, which may be why your bake fails after awhile. If so, try to bake one frame at the middle or end at full res so you will see if it works. Some useful hints about fluid simulation in Blender: The meshes should be closed, so if some parts of e.g. a fluid object are not initialized as fluid in the simulation, check that all parts of connected vertices are closed meshes. Unfortunately, the Suzanne (monkey) mesh in Blender is not a closed mesh (the eyes are separate). Using "generate particles" will also add memory requirements, as they increase surface area and complexity. Ordinary fluid simulations generated particles probably consume less memory. 