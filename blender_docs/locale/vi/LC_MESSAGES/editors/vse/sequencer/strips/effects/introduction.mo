��    	      d               �   �   �   }   a     �  �   �  �   �  G  �  �     '  �  �    �   �	  }   �
       �      �     G  �  �   G  '  #   Blender offers a set of effects that can be added to your sequence. Each effect is explained in the next pages individually, but they all are added and controlled in the same way. If you picked the wrong effect from the menu, you can always exchange it with :ref:`Change <sequencer-edit-change>` operator. Introduction Since most Effects strips depend on one or two source strips, their frame location and duration depends on their source strips. Thus, you may not be able to move it; you have to move the source strips in order to affect the effect strip. The only exception is the :doc:`Color Generator </editors/vse/sequencer/strips/effects/color>` effect. It does not depend on a base strip; you can add and position it independent of any other strip. Change the length as you would any strip. To add an effect strip, select one base strip (image, movie, or scene) by :kbd:`RMB` clicking on it. For some effects, like the Cross transition effect, you will need to :kbd:`Shift-RMB` a second overlapping strip (it depends on the effect you want). Then select :menuselection:`Add --> Effect` and pick the effect you want from the pop-up menu. When you do, the Effect strip will be shown above the source strips. If it is an independent effect, like the :doc:`Color Generator </editors/vse/sequencer/strips/effects/color>`, it will be placed at the position of the frame indicator. To use an effect that combines or makes a transitions select two strips, When you add the effect strip, it will be placed in a channel above the two. Its duration will be the overlap between the two strips as a maximum. With some effects, like the :doc:`Alpha Over </editors/vse/sequencer/strips/effects/alpha_over_under_overdrop>`, the order in which you select the strips is important. You can also use one effect strip as the input or source strip with another strip, thus layering effects on top of one another. Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-11-01 19:20+0000
PO-Revision-Date: 2018-11-14 21:46+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@googlemail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@googlemail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.6.0
 Blender offers a set of effects that can be added to your sequence. Each effect is explained in the next pages individually, but they all are added and controlled in the same way. If you picked the wrong effect from the menu, you can always exchange it with :ref:`Change <sequencer-edit-change>` operator. Giới Thiệu -- Introduction Since most Effects strips depend on one or two source strips, their frame location and duration depends on their source strips. Thus, you may not be able to move it; you have to move the source strips in order to affect the effect strip. The only exception is the :doc:`Color Generator </editors/vse/sequencer/strips/effects/color>` effect. It does not depend on a base strip; you can add and position it independent of any other strip. Change the length as you would any strip. To add an effect strip, select one base strip (image, movie, or scene) by :kbd:`RMB` clicking on it. For some effects, like the Cross transition effect, you will need to :kbd:`Shift-RMB` a second overlapping strip (it depends on the effect you want). Then select :menuselection:`Add --> Effect` and pick the effect you want from the pop-up menu. When you do, the Effect strip will be shown above the source strips. If it is an independent effect, like the :doc:`Color Generator </editors/vse/sequencer/strips/effects/color>`, it will be placed at the position of the frame indicator. To use an effect that combines or makes a transitions select two strips, When you add the effect strip, it will be placed in a channel above the two. Its duration will be the overlap between the two strips as a maximum. With some effects, like the :doc:`Alpha Over </editors/vse/sequencer/strips/effects/alpha_over_under_overdrop>`, the order in which you select the strips is important. You can also use one effect strip as the input or source strip with another strip, thus layering effects on top of one another. 