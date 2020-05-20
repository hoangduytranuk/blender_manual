��    0      �                V        t  '   �     �     �     �  �        �     �       �     �   �     Z  �   ^     2  z   9     �     �     �     �     �     �  
             "     )     6  �   G  [   �    9	     H
  
   f
  	   q
  �   {
  D  T     �  �   �  q   K  �   �  u   C  �   �  @   ~  |  �  �   <     �  �   �  h   �  �  )  V   �     .  '   H     p     �     �  �   �     �     �     �  �   �  �   �  "   +  �   N     "  z   8  
   �     �     �     �               1     L     `     x     �  �   �  [   Y    �     �     �     �  �     D  �  '   &  �   N  q   �  �   Z   u   �   �   V!  @   "  |  \"  �   �#     ]$  �   q$  h   l%   Absolute quantity of pigment. Range :math:`[0, 1]` equivalent to :math:`[0\%, 100\%]`. Absorption coefficient Attenuation coefficient :math:`\sigma`. Black (Melanin :math:`1`) Blonde (Melanin :math:`0.25`) Brown (Melanin :math:`0.75`) Chiang, M. J. , Bitterli, B. , Tappan, C. and Burley, B. (2016), A Practical and Controllable Hair and Fur Model for Production Path Tracing. Computer Graphics Forum, 35: 275-283. `doi:10.1111/cgf.12830 <https://doi.org/10.1111/cgf.12830>`__ Coat Color Direct coloring For each strand, vary both Roughness values by :math:`RandomFactor`. Range :math:`[0, 1]` equivalent to :math:`[0\%, 100\%]` of the initial roughness values. For each strand, vary the melanin concentration by :math:`RandomFactor`. Range :math:`[0, 1]` equivalent to :math:`[0\%, 100\%]` of the initial melanin concentration. IOR Index of refraction (:term:`IOR`) defining how much the ray changes direction. At 1.0 rays pass straight through like in a transparent material; higher values give more refraction. Default value is :math:`1.55`. Inputs Mathematically, this parameter is mapped to the logistic distribution's scale factor :math:`s` (section 4.1 of [CBTB16]_). Melanin Melanin Redness Melanin concentration Offset Outputs Principled Hair BSDF Properties Radial Roughness Random Random Color Random Roughness Random number source. If no node is connected here, it is automatically instanced with the value obtained from :menuselection:`Hair Info --> Random`. Ratio of pheomelanin to eumelanin. Range :math:`[0, 1]` equivalent to :math:`[0\%, 100\%]`. Realistic hair should have a minimum of variance between each strand. The shader allows for this by specifying two values, *Random Color* and *Random Roughness*, which remap the specified Melanin/Roughness values to the range :math:`Color/Roughness \pm Randomization\%`. Reddish (Melanin :math:`0.5`) References Roughness Simulate a shiny coat of fur, by reducing the Roughness to the given factor only for the first light bounce (diffuse). Range :math:`[0, 1]` equivalent to a reduction of :math:`[0\%, 100\%]` of the original Roughness. Specifies the attenuation coefficient :math:`\sigma_{a}`, as applied by the `Beer-Lambert law <https://en.wikipedia.org/wiki/Beer%E2%80%93Lambert_law#Expression_with_attenuation_coefficient>`__. This mode is intended mainly for technical users who want to use coefficients from the literature without any sort of conversion. Standard shader output. The *Principled Hair* :abbr:`BSDF (Bidirectional scattering distribution function)` is a physically-based, easy-to-use shader for rendering hair and fur. The chosen color is converted to an absorption coefficient with the following formula (section 4.2 of [CBTB16]_): The melanin concentration is multiplied by :math:`randomFactor`, where :math:`randomFactor = 1.0 + 2.0*(Random - 0.5) * RandomColor`. The ratio formula is: :math:`eumelanin = Melanin*(1.0-MelaninRedness)`, :math:`pheomelanin = Melanin*MelaninRedness`. The resulting quantities are converted (after randomization, if specified) to absorption concentration via the following formula (section 6.1 of [EFHLA11]_, adjusted for the range :math:`[0, 1]`): This is a linear mapping to the underlying exponential function: This mode defines the color as the quantity and ratio of the pigments which are commonly found in hair and fur, *eumelanin* (prevalent in brown-black hair) and *pheomelanin* (red hair). The quantity is specified in the *Melanin* input, and the ratio between them in *Melanin Redness*. Increasing concentrations darken the hair (the following are with *Melanin Redness* :math:`1`): This shader is an implementation of the paper by Chiang et al. [CBTB16]_, which was used in the Disney film, "Zootopia"\ :sup:`®`. Tint d'Eon, E. , Francois, G. , Hill, M. , Letteri, J. and Aubry, J. (2011), An Energy‐Conserving Hair Reflectance Model. Computer Graphics Forum, 30: 1181-1187. `doi:10.1111/j.1467-8659.2011.01976.x <https://doi.org/10.1111/j.1467-8659.2011.01976.x>`__ where :math:`\beta_{N}` is the radial roughness of the hair after applying randomization (if specified). Project-Id-Version: Blender 2.79 Manual 2.79
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2020-05-08 17:07+1000
PO-Revision-Date: 2020-02-26 21:13+0000
Last-Translator: Hoang Duy Tran <hoangduytran1960@gmail.com>
Language: vi
Language-Team: London, UK <hoangduytran1960@gmail.com>
Plural-Forms: nplurals=1; plural=0
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.8.0
 Absolute quantity of pigment. Range :math:`[0, 1]` equivalent to :math:`[0\%, 100\%]`. -- Absorption coefficient Attenuation coefficient :math:`\sigma`. Black (Melanin :math:`1`) Blonde (Melanin :math:`0.25`) Brown (Melanin :math:`0.75`) Chiang, M. J. , Bitterli, B. , Tappan, C. and Burley, B. (2016), A Practical and Controllable Hair and Fur Model for Production Path Tracing. Computer Graphics Forum, 35: 275-283. `doi:10.1111/cgf.12830 <https://doi.org/10.1111/cgf.12830>`__ -- Coat Màu Sắc -- Color -- Direct coloring For each strand, vary both Roughness values by :math:`RandomFactor`. Range :math:`[0, 1]` equivalent to :math:`[0\%, 100\%]` of the initial roughness values. For each strand, vary the melanin concentration by :math:`RandomFactor`. Range :math:`[0, 1]` equivalent to :math:`[0\%, 100\%]` of the initial melanin concentration. Chỉ Số Khúc Xạ (IOR) -- IOR Index of refraction (:term:`IOR`) defining how much the ray changes direction. At 1.0 rays pass straight through like in a transparent material; higher values give more refraction. Default value is :math:`1.55`. Đầu Vào -- Inputs Mathematically, this parameter is mapped to the logistic distribution's scale factor :math:`s` (section 4.1 of [CBTB16]_). -- Melanin -- Melanin Redness -- Melanin concentration Dịch Chuyển -- Offset Đầu Ra -- Outputs -- Principled Hair BSDF Tính Chất -- Properties -- Radial Roughness Ngẫu Nhiên -- Random -- Random Color -- Random Roughness Random number source. If no node is connected here, it is automatically instanced with the value obtained from :menuselection:`Thông Tin về Tóc (Hair Info) --> Ngẫu Nhiên (Random)`. Ratio of pheomelanin to eumelanin. Range :math:`[0, 1]` equivalent to :math:`[0\%, 100\%]`. Realistic hair should have a minimum of variance between each strand. The shader allows for this by specifying two values, *Random Color* and *Random Roughness*, which remap the specified Melanin/Roughness values to the range :math:`Color/Roughness \pm Randomization\%`. Reddish (Melanin :math:`0.5`) -- References Độ Ráp -- Roughness Simulate a shiny coat of fur, by reducing the Roughness to the given factor only for the first light bounce (diffuse). Range :math:`[0, 1]` equivalent to a reduction of :math:`[0\%, 100\%]` of the original Roughness. Specifies the attenuation coefficient :math:`\sigma_{a}`, as applied by the `Beer-Lambert law <https://en.wikipedia.org/wiki/Beer%E2%80%93Lambert_law#Expression_with_attenuation_coefficient>`__. This mode is intended mainly for technical users who want to use coefficients from the literature without any sort of conversion. Đầu ra chuẩn của bộ tô bóng. The *Principled Hair* :abbr:`BSDF (Bidirectional scattering distribution function)` is a physically-based, easy-to-use shader for rendering hair and fur. The chosen color is converted to an absorption coefficient with the following formula (section 4.2 of [CBTB16]_): The melanin concentration is multiplied by :math:`randomFactor`, where :math:`randomFactor = 1.0 + 2.0*(Random - 0.5) * RandomColor`. The ratio formula is: :math:`eumelanin = Melanin*(1.0-MelaninRedness)`, :math:`pheomelanin = Melanin*MelaninRedness`. The resulting quantities are converted (after randomization, if specified) to absorption concentration via the following formula (section 6.1 of [EFHLA11]_, adjusted for the range :math:`[0, 1]`): This is a linear mapping to the underlying exponential function: This mode defines the color as the quantity and ratio of the pigments which are commonly found in hair and fur, *eumelanin* (prevalent in brown-black hair) and *pheomelanin* (red hair). The quantity is specified in the *Melanin* input, and the ratio between them in *Melanin Redness*. Increasing concentrations darken the hair (the following are with *Melanin Redness* :math:`1`): This shader is an implementation of the paper by Chiang et al. [CBTB16]_, which was used in the Disney film, "Zootopia"\ :sup:`®`. Sắc Thái -- Tint d'Eon, E. , Francois, G. , Hill, M. , Letteri, J. and Aubry, J. (2011), An Energy‐Conserving Hair Reflectance Model. Computer Graphics Forum, 30: 1181-1187. `doi:10.1111/j.1467-8659.2011.01976.x <https://doi.org/10.1111/j.1467-8659.2011.01976.x>`__ where :math:`\beta_{N}` is the radial roughness of the hair after applying randomization (if specified). 