��    4      �              \    ]     s  �  �  �   -  d   	  k   n  #   �  :   �     9  a   I     �     �     �     �  �   	  8   �	     6
  �  <
  N   �  �     �   �  �   ;  =     p   D  J   �  p      x   q  N  �  �   9  >   �  �        �  �   �     �  L   �  /        H    ]  �  w      o    �   �     ;  �   W  �   #  �   �  t  �     $  &  -  w   T  K   �  �       �!     �"  �  �"  �   �$  d   �%  k   �%  #   Q&  :   u&     �&  a   �&     "'     @'     O'     g'  �   �'  8   w(     �(  �  �(  N   L*  �   �*  �   :+  �   �+  =   �,  p   �,  J   ;-  p   �-  x   �-  N  p.  �   �/  >   a0  �   �0     S1  �   k1     >2  L   T2  /   �2     �2    �2  �   4    �5  o  �6  �   8     �8  �   �8  �   �9  �   S:  t  8;  "   �<  &  �<  w   �=  O   o>   After rendering the frames, you may need to edit the clips, or first use the Compositor to do green-screen masking, matting, color correction, DOF, and so on to the images. That result is then fed to the Sequencer where the strips are cut and mixed and a final overlay is done. Animation Preview Blender creates a file for each frame of the animation. You can then use Blender's compositor to perform any frame manipulation (post-processing). You can then use Blender's VSE to load that final image sequence, add an audio track to the animation, and render out to an MPEG format to complete your movie. The Frame Sequence approach is a little more complicated and takes more drive space, but gives you more flexibility. Choose *Add Image* from the add menu. Select all the frames from your output folder that you want to include in your animation (press :kbd:`A` to Select All easily). They will be added as a strip to the Sequence editor. Choose the output path and file type in the Output panel as well, for example ``//render/my-anim-``. Click the *Animation* render button and Blender will render out the Sequence editor output into your movie. Computer not needed for other uses. Confirm the range of your animation (frame Start and End). Direct Approach Finally you can render out from the Sequencer and compress the frames into a playable movie clip. First prepare your animation. Frame Sequence Frame Sequence Approach Frame Sequence Workflow Generally, you do a lot of intermediate renders of different frames in your animation to check for timing, lighting, placement, materials, and so on. At some point, you are ready to make a final render of the complete animation for publication. Here are some guidelines to help you choose an approach. Hints If the total render time is an hour or more, you want to use the "Frame Sequence" approach. For example, if you are rendering a one-minute video clip for film, there will be (60 seconds per minute) X (24 frames per second) or 1440 frames per minute. If each frame takes 30 seconds to render, then you will be able to render two frames per minute, or need 720 minutes (12 hours) of render time. In Blender, now go into the :doc:`Video Sequence editor </editors/vse/index>`. In the *Dimensions* panel, choose the render size, Pixel Aspect Ratio, and the Range of Frames to use, as well as the frame rate, which should already be set. In the Output panel set up your animation to be rendered out as images, generally using a format that does not compromise any quality. In the Output panel, choose the container and codec you want (e.g. ``MPEG H.264``) and configure them. The video codecs are described on the previous page: :doc:`Output Options </render/output/output>`. Intermediate frames/adjustments needed for compression/codec. It can be useful to render a subset of the animated sequence, since only part of an animation may have an error. Just disable the *Overwrite* option to start rendering where you left off. May need to interrupt rendering to use the computer, and want to be able to resume rendering where you left off. Now you can edit the strip and add effects or simply leave it like it is. You can add other strips, like an audio strip. Once the animation is finished, use your OS file explorer to navigate into the output folder (``render`` in this example). You will see lots of images (``.png`` or ``.exr``, etc. depending on the format you chose to render) that have a sequence number attached to them ranging from 0000 to a max of 9999. These are your single frames. Post-production work needed: - Color/lighting adjustment - Green screen/matte replacement - Layering/compositing - Multiple formats and sizes of ultimate product Precise timing (e.g. lip-sync to audio track) needed in parts. Press the big *Animation* button. Do a long task (like sleeping, playing a video game, or cleaning your driveway) while you wait for your computer to finish rendering the frames. Rendering Animations Rendering takes all available CPU time; you should render overnight, when the computer is not needed, or set Blender to a low priority while rendering, and work on other things (be careful with the RAM space!). Save your blend-file. Scrub through the animation, checking that you have included all the frames. Short segments with total render time < 1 hour. Stable power supply. The :doc:`VSE </editors/vse/index>` does not support multi-layer EXR files. To render to a video format you will have to skip the next three steps and instead use an :doc:`Image Input node </compositing/types/input/image>` in the :doc:`compositor </compositing/types/input/image>`. The Direct Approach, which is highly **not** recommended and not a standard practice, is where you set your output format to an AVI or MOV format, and click *Animation* to render your scene directly out to a movie file. Blender creates one file that holds all the frames of your animation. You can then use Blender's VSE to add an audio track to the animation and render out to an MPEG format to complete your movie. The Frame Sequence is a much more stable approach, where you set your output format to a still format (such as JPG, PNG or a multi-layer format), and click *Animation* to render your scene out to a set of images, where each image is a frame in the sequence. There are two approaches you can use when making a movie, or animation, with or without sound. The approach you should use depends on the amount of CPU time you will need to render the movie. You can render a "typical" frame at the desired resolution, and then multiply by the number of frames that will ultimately go into the movie, to arrive at a total render time. This allows you an easy recovery if there is a problem and you have to re-start the rendering, since the frames you have already rendered will still be in the output directory. Total render time > 1 hour. Unless your animation renders in a few minutes, it is best to render the animation as separate image files. Instead of rendering directly to a compressed movie file, use a lossless format (e.g. ``PNG``). Using an image format for output, you can use the *Frame Step* option to render every *N'th* frame. Then disable *Overwrite* and re-render with *Frame Step* set to 1. While rendering stills will allow you to view and save the image from the render buffer when it is complete, animations are a series of images, or frames, and are automatically saved directly out to a drive after being rendered. Why go through all this hassle? Well, first of all, if you render out single frames, you can stop the render at any time by pressing :kbd:`Esc` in the render window or UV/Image editor. You will not lose the frames you have already rendered, since they have been written out to individual files. You can always adjust the range you want to continue from where you left off. Workflow You can edit the frames afterwards and post-process them. You can add neat effects in the Sequence editor. You can render the same sequence into different resolutions (640×480, 320×240, etc.) and use different codecs (to get different file sizes and quality) with almost no effort whatsoever. You can then make a movie out of the separate frames with Blender's Sequence editor or use 3rd party encoding software. Your computer accidentally turns off in the middle of rendering your movie! Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-07 01:52+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 After rendering the frames, you may need to edit the clips, or first use the Compositor to do green-screen masking, matting, color correction, DOF, and so on to the images. That result is then fed to the Sequencer where the strips are cut and mixed and a final overlay is done.  -- Animation Preview Blender creates a file for each frame of the animation. You can then use Blender's compositor to perform any frame manipulation (post-processing). You can then use Blender's VSE to load that final image sequence, add an audio track to the animation, and render out to an MPEG format to complete your movie. The Frame Sequence approach is a little more complicated and takes more drive space, but gives you more flexibility. Choose *Add Image* from the add menu. Select all the frames from your output folder that you want to include in your animation (press :kbd:`A` to Select All easily). They will be added as a strip to the Sequence editor. Choose the output path and file type in the Output panel as well, for example ``//render/my-anim-``. Click the *Animation* render button and Blender will render out the Sequence editor output into your movie. Computer not needed for other uses. Confirm the range of your animation (frame Start and End). Direct Approach Finally you can render out from the Sequencer and compress the frames into a playable movie clip. First prepare your animation. Frame Sequence Frame Sequence Approach -- Frame Sequence Workflow Generally, you do a lot of intermediate renders of different frames in your animation to check for timing, lighting, placement, materials, and so on. At some point, you are ready to make a final render of the complete animation for publication. Here are some guidelines to help you choose an approach. Gợi ý -- Hints If the total render time is an hour or more, you want to use the "Frame Sequence" approach. For example, if you are rendering a one-minute video clip for film, there will be (60 seconds per minute) X (24 frames per second) or 1440 frames per minute. If each frame takes 30 seconds to render, then you will be able to render two frames per minute, or need 720 minutes (12 hours) of render time. In Blender, now go into the :doc:`Video Sequence editor </editors/vse/index>`. In the *Dimensions* panel, choose the render size, Pixel Aspect Ratio, and the Range of Frames to use, as well as the frame rate, which should already be set. In the Output panel set up your animation to be rendered out as images, generally using a format that does not compromise any quality. In the Output panel, choose the container and codec you want (e.g. ``MPEG H.264``) and configure them. The video codecs are described on the previous page: :doc:`Output Options </render/output/output>`. Intermediate frames/adjustments needed for compression/codec. It can be useful to render a subset of the animated sequence, since only part of an animation may have an error. Just disable the *Overwrite* option to start rendering where you left off. May need to interrupt rendering to use the computer, and want to be able to resume rendering where you left off. Now you can edit the strip and add effects or simply leave it like it is. You can add other strips, like an audio strip. Once the animation is finished, use your OS file explorer to navigate into the output folder (``render`` in this example). You will see lots of images (``.png`` or ``.exr``, etc. depending on the format you chose to render) that have a sequence number attached to them ranging from 0000 to a max of 9999. These are your single frames. Post-production work needed: - Color/lighting adjustment - Green screen/matte replacement - Layering/compositing - Multiple formats and sizes of ultimate product Precise timing (e.g. lip-sync to audio track) needed in parts. Press the big *Animation* button. Do a long task (like sleeping, playing a video game, or cleaning your driveway) while you wait for your computer to finish rendering the frames. -- Rendering Animations Rendering takes all available CPU time; you should render overnight, when the computer is not needed, or set Blender to a low priority while rendering, and work on other things (be careful with the RAM space!). Save your blend-file. Scrub through the animation, checking that you have included all the frames. Short segments with total render time < 1 hour. Stable power supply. The :doc:`VSE </editors/vse/index>` does not support multi-layer EXR files. To render to a video format you will have to skip the next three steps and instead use an :doc:`Image Input node </compositing/types/input/image>` in the :doc:`compositor </compositing/types/input/image>`. The Direct Approach, which is highly **not** recommended and not a standard practice, is where you set your output format to an AVI or MOV format, and click *Animation* to render your scene directly out to a movie file. Blender creates one file that holds all the frames of your animation. You can then use Blender's VSE to add an audio track to the animation and render out to an MPEG format to complete your movie. The Frame Sequence is a much more stable approach, where you set your output format to a still format (such as JPG, PNG or a multi-layer format), and click *Animation* to render your scene out to a set of images, where each image is a frame in the sequence. There are two approaches you can use when making a movie, or animation, with or without sound. The approach you should use depends on the amount of CPU time you will need to render the movie. You can render a "typical" frame at the desired resolution, and then multiply by the number of frames that will ultimately go into the movie, to arrive at a total render time. This allows you an easy recovery if there is a problem and you have to re-start the rendering, since the frames you have already rendered will still be in the output directory. Total render time > 1 hour. Unless your animation renders in a few minutes, it is best to render the animation as separate image files. Instead of rendering directly to a compressed movie file, use a lossless format (e.g. ``PNG``). Using an image format for output, you can use the *Frame Step* option to render every *N'th* frame. Then disable *Overwrite* and re-render with *Frame Step* set to 1. While rendering stills will allow you to view and save the image from the render buffer when it is complete, animations are a series of images, or frames, and are automatically saved directly out to a drive after being rendered. Why go through all this hassle? Well, first of all, if you render out single frames, you can stop the render at any time by pressing :kbd:`Esc` in the render window or UV/Image editor. You will not lose the frames you have already rendered, since they have been written out to individual files. You can always adjust the range you want to continue from where you left off. Quy Trình Làm Việc -- Workflow You can edit the frames afterwards and post-process them. You can add neat effects in the Sequence editor. You can render the same sequence into different resolutions (640×480, 320×240, etc.) and use different codecs (to get different file sizes and quality) with almost no effort whatsoever. You can then make a movie out of the separate frames with Blender's Sequence editor or use 3rd party encoding software.  -- Your computer accidentally turns off in the middle of rendering your movie! 