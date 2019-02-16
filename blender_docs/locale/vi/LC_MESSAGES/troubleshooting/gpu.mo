��    $      <              \  �   ]     �              !  �  5  �        �  q   �     3  �   ?       �   	     �  <  �  =  �	  �   /  @   &  �   g       y     _   �  o   �  {   Y  �   �  �   �  T   �  �   �  M   _  !   �  )   �  �   �     |     �     �  �  �  �   a     �          #    A  �  U  �   1     �  q   �     V  �   e     '  �   /     �  <  �  =    �   U  @   L  �   �     '  y   8  _   �  o      {   �   �   �   �   �!  T   �"  �   #  M   �#  $   �#  )   �#  �   %$     �$  !   �$  	   �$   Blender uses of OpenGL for the 3D viewport and user interface. The graphics card (GPU) and driver have a big impact on Blender's behavior and performance. Common Problems Crash on Startup Drivers For AMD the drivers are open source, except for the OpenCL support which is available as part of Pro drivers. Installing packages through your Linux distribution is usually best. AMD also provides graphics drivers for download on their website if you need the latest version. For NVIDIA there are open source (Nouveau) and closed source (by NVIDIA) graphics drivers. Blender functions best with the closed source drivers as they are more optimized and complete. Linux graphics drivers can be downloaded from NVIDIA's website, however in most cases the ones from your Linux distribution are fine and make things easier. Manually downloading drivers is mostly useful to get the very latest version, for example for a GPU that was only recently released. For best performance the dedicated GPU should be used for Blender. Which GPU to use for which application can be configured in your graphics driver settings. Graphics Hardware If there is a graphics glitch specific to the onboard GPU, then using the dedicated GPU can also help avoid that. Information Installing the latest driver can help upgrade the OpenGL version, though some graphics cards are simply too old to run the latest Blender. Using Blender 2.79 or earlier is the only option then. Laptops Laptops often have two GPUs for power saving purposes. One slower onboard GPU (typically Intel) and one faster dedicated GPU for better performance (AMD or NVIDIA). Linux On Linux, graphics drivers are usually installed as a package by your Linux distribution. Installing the latest drivers is typically done by upgrading packages or the distribution as a whole. Some distributions provide multiple packages for multiple drivers versions, giving you the choice to install newer versions. On Windows drivers are provided by the graphics card manufacturer (Intel, AMD and NVIDIA). Windows update automatically installs graphics drivers, or your computer manufacturer may provide its own version of the graphics drivers. However these are not always the latest version or may have been corrupted in some way. On Windows, graphics drivers can sometimes get corrupted. In this case it can help to uninstall all graphics drivers (there may be multiple from Intel, AMD and NVIDIA) and perform a clean installation with drivers from the manufacturer's website. On laptops, make sure you are using a dedicated GPU (see above). On macOS graphics drivers are built into the operating system and the only way to get newer drivers is to upgrade macOS as a whole to the latest version. Render Errors See :doc:`Eevee </render/eevee/limitations>` and :doc:`Cycles </render/cycles/gpu_rendering>` documentation respectively. See :ref:`Invalid Selection, Disable Anti-Aliasing <troubleshooting-3dview-invalid-selection>`. This means your graphics card and driver do not have the minimum required OpenGL 3.3 version needed by Blender. This pages lists possible solutions for graphics glitches, problems with Eevee and Cycles, and crashes related to your GPU. To ensure you have the latest version, go to the graphics card manufacturer's website and download the latest drivers from there. It can help to uninstall the previous drivers first and perform a clean installation. To find out which graphics card and driver Blender is using, use :menuselection:`Help --> Save System Info` inside Blender. The OpenGL section will have information about your graphics card, vendor and driver version. Try lowering quality settings in :menuselection:`Preferences --> System --> OpenGL`. Try running Blender from the :doc:`command line </advanced/command_line/index>`, to see if any helpful error messages are printed. Try undoing settings in your graphics drivers, if you made any changes there. Unsupported Graphics Driver Error Update your graphics drivers (see above). Upgrading to the latest graphics drivers often solves problems. Newer drivers have bug fixes that help Blender function correctly. Windows Wrong Selection in 3D Viewport macOS Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2019-02-04 12:38+0000
PO-Revision-Date: 2019-02-05 02:07+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 Blender uses of OpenGL for the 3D viewport and user interface. The graphics card (GPU) and driver have a big impact on Blender's behavior and performance. -- Common Problems -- Crash on Startup Bộ Điều Vận -- Drivers For AMD the drivers are open source, except for the OpenCL support which is available as part of Pro drivers. Installing packages through your Linux distribution is usually best. AMD also provides graphics drivers for download on their website if you need the latest version. For NVIDIA there are open source (Nouveau) and closed source (by NVIDIA) graphics drivers. Blender functions best with the closed source drivers as they are more optimized and complete. Linux graphics drivers can be downloaded from NVIDIA's website, however in most cases the ones from your Linux distribution are fine and make things easier. Manually downloading drivers is mostly useful to get the very latest version, for example for a GPU that was only recently released. For best performance the dedicated GPU should be used for Blender. Which GPU to use for which application can be configured in your graphics driver settings. -- Graphics Hardware If there is a graphics glitch specific to the onboard GPU, then using the dedicated GPU can also help avoid that. -- Information Installing the latest driver can help upgrade the OpenGL version, though some graphics cards are simply too old to run the latest Blender. Using Blender 2.79 or earlier is the only option then. Laptops Laptops often have two GPUs for power saving purposes. One slower onboard GPU (typically Intel) and one faster dedicated GPU for better performance (AMD or NVIDIA). Linux On Linux, graphics drivers are usually installed as a package by your Linux distribution. Installing the latest drivers is typically done by upgrading packages or the distribution as a whole. Some distributions provide multiple packages for multiple drivers versions, giving you the choice to install newer versions. On Windows drivers are provided by the graphics card manufacturer (Intel, AMD and NVIDIA). Windows update automatically installs graphics drivers, or your computer manufacturer may provide its own version of the graphics drivers. However these are not always the latest version or may have been corrupted in some way. On Windows, graphics drivers can sometimes get corrupted. In this case it can help to uninstall all graphics drivers (there may be multiple from Intel, AMD and NVIDIA) and perform a clean installation with drivers from the manufacturer's website. On laptops, make sure you are using a dedicated GPU (see above). On macOS graphics drivers are built into the operating system and the only way to get newer drivers is to upgrade macOS as a whole to the latest version. -- Render Errors See :doc:`Eevee </render/eevee/limitations>` and :doc:`Cycles </render/cycles/gpu_rendering>` documentation respectively. See :ref:`Invalid Selection, Disable Anti-Aliasing <troubleshooting-3dview-invalid-selection>`. This means your graphics card and driver do not have the minimum required OpenGL 3.3 version needed by Blender. This pages lists possible solutions for graphics glitches, problems with Eevee and Cycles, and crashes related to your GPU. To ensure you have the latest version, go to the graphics card manufacturer's website and download the latest drivers from there. It can help to uninstall the previous drivers first and perform a clean installation. To find out which graphics card and driver Blender is using, use :menuselection:`Help --> Save System Info` inside Blender. The OpenGL section will have information about your graphics card, vendor and driver version. Try lowering quality settings in :menuselection:`Preferences --> System --> OpenGL`. Try running Blender from the :doc:`command line </advanced/command_line/index>`, to see if any helpful error messages are printed. Try undoing settings in your graphics drivers, if you made any changes there. -- Unsupported Graphics Driver Error Update your graphics drivers (see above). Upgrading to the latest graphics drivers often solves problems. Newer drivers have bug fixes that help Blender function correctly. Windows -- Wrong Selection in 3D Viewport  -- macOS 