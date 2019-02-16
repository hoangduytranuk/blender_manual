��          �               �   /   �   0   -  3   ^  �   �  )   W  �   �  !   $     F  <   Z  =   �  0   �  �       �  �    /   �  0   �  3   (  �   \  }   !	  �   �	  W   B
  1   �
  <   �
  =   	  0   G  �  x  %   q   An Auto-execution warning in the Drivers panel. An Auto-run warning in the Info editor's header. By default Blender will not autorun Python scripts. If using a *Scripted Expression* Driver Type, you will have to open the file as *Trusted Source*, or set *Auto Run Python Scripts* in :menuselection:`User Preferences --> File --> Auto Execution`. Intra-armature Bone Drivers can Misbehave Parts of the User Interface may use different units of measurements for angles, rotation. In the Graph Editor, while working with Drivers, all angles are Radians. Rotational Properties are Radians Scripted Expression Some common problems people may run into when using drivers. The Auto Run Python Scripts checkbox in the User Preferences. The Trusted Source checkbox in the File Browser. There is a `well-known limitation <https://developer.blender.org/T40301>`__ with drivers on bones that refer to another bone in the same armature. Their values can be incorrectly calculated based on the position of the other bone as it was *before* you adjust the current frame. This can lead to obvious shape glitches when the rendering of frames has a jump in the frame number (either because the blend-file is currently on a different frame number or because you are skipping already rendered frames). Troubleshooting Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-12-05 19:50+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 An Auto-execution warning in the Drivers panel. An Auto-run warning in the Info editor's header. By default Blender will not autorun Python scripts. If using a *Scripted Expression* Driver Type, you will have to open the file as *Trusted Source*, or set *Auto Run Python Scripts* in :menuselection:`User Preferences --> File --> Auto Execution`. Bộ Điều Vận Xương Nội Bộ Cốt có thể Xử Hành Bất Thường -- Intra-armature Bone Drivers can Misbehave Parts of the User Interface may use different units of measurements for angles, rotation. In the Graph Editor, while working with Drivers, all angles are Radians. Các Tính Chất về Xoay Chiều đều là Rad -- Rotational Properties are Radians Biểu Thức Tập Lệnh -- Scripted Expression Some common problems people may run into when using drivers. The Auto Run Python Scripts checkbox in the User Preferences. The Trusted Source checkbox in the File Browser. There is a `well-known limitation <https://developer.blender.org/T40301>`__ with drivers on bones that refer to another bone in the same armature. Their values can be incorrectly calculated based on the position of the other bone as it was *before* you adjust the current frame. This can lead to obvious shape glitches when the rendering of frames has a jump in the frame number (either because the blend-file is currently on a different frame number or because you are skipping already rendered frames). Xử Lý Sự Cố -- Troubleshooting 