��    4      �              \  &   ]  8   �  q   �     /     B     U  I   ]  $   �  �   �  �   �  `   7  R   �  
   �  G   �  M   >  |   �     	       	   4  �   >  I   �     ;	  h   B	     �	  3   �	     �	  �   
  j   �
  9   1     k  .   |  l   �       [         |  j   �  	     b        n  �   ~  �   )  t   �     t  �  �  �   x  �   *  ^     e   f  \   �  K   )  R   u  �  �  &   �  8   �  q   �     R  7   h     �  I   �  $     �   +  �     `   �  R   �     J  G   f  M   �  |   �     y     �     �  �   �  I   g     �  h   �     0  3   I     }  �   �  j   R  9   �  5   �  .   -  l   \     �  [   �     B   j   \      �   b   �   #   7!  �   [!  �   "  t   �"     Q#  �  j#  �   U%  �   &  ^   �&  e   C'  \   �'  K   (  R   R(   A quick introduction to Blender's API. A quick tutorial on the essentials of writing an add-on. Add a subdirectory under ``my_scripts`` called ``addons`` (it *must* have this name for Blender to recognize it). Add-on Information Add-on Preferences Add-ons Add-ons are divided into categories by what areas of Blender they affect. Add-ons tab in the User Preferences. Add-ons that activate or change multiple hotkeys now have a special system of activation. For example, with the "UI: Pie Menu Official" add-on for each menu there's a selection box to activate the menu and its hotkey. Blender comes with some useful Add-ons already, ready to be enabled. But you can also add your own, or any interesting ones you find on the web. Blender will copy newly installed add-ons under the directory selected in your User Preferences. Blender's add-ons are split into two groups depending on who writes/supports them: Categories Community: Add-ons that are written by people in the Blender community. Create an empty directory in a location of your choice (e.g. ``my_scripts``). Enable and disable an add-on by checking or unchecking the box on the right of the add-on you chose, as shown in the figure. Enabling an add-on. Enabling and Disabling Filtering For add-ons that you found on the web or your own to show on the list, you have to install them first by clicking *Install from File...* and providing a ``.zip`` or ``.py`` file. Guidelines on writing new add-on that you might want to get into Blender. Header If you want an Add-on to be enabled every time you start Blender, you will need to *Save User Settings*. Individual Activation Information on how to get your add-on into Blender. Install from File Now the add-on will be installed, not automatically enabled. The search field will be set to the add-on's name (to avoid having to look for it). Enable the add-on by turning on the checkbox. Now when you install add-ons you can select the *Target Path* option to *User Pref* (from the *File* tab). Official: Add-ons that are written by Blender developers. Online Resources Open the *File* tab of the *User Preferences*. Provides an index of Add-ons that are included with Blender as well as listing a number of external Add-ons. Refresh Save the User Preferences and restart Blender for it to recognize the new add-ons location. Saving Add-on Preferences Scans the :doc:`Add-on Directory </getting_started/installing/configuration/directories>` for new add-ons. Searching Set the *Scripts* in the User Preferences to point to your script directory (e.g. ``my_scripts``). Supported Level The Add-ons tab lets you manage secondary scripts, called "Add-ons" that extends Blender's functionality. In this tab you can search, install, enable and disable Add-ons. The add-on functionality should be immediately available. If the Add-on does not activate when enabled, check the :doc:`Console window </advanced/command_line/introduction>` for any errors, that may have occurred. This menu contains a list of helpful links for both users and people who are interested in writing their own add-on. User-Defined Add-on Path With Pie menus, First you activate the add-on. This activates the "Add-ons Preferences Submodule Activation". You then need to expand the Add-ons Preferences, then you will see the list of Pie Menu types you can choose from. From here you can individually activate the menus you like to use. If the menu conflicts with another favorite, there's no need to activate it. You can activate any combination and save as user settings so your activations are available next time you start Blender. You can also create a personal directory containing new add-ons and configure your files path in the *File* tab of the *User Preferences*. To create a personal script directory: You can click the arrow at the left of the add-on box to see more information, such as its location, a description and a link to the documentation. Here you can also find a button to report a bug specific of this add-on. `API Concepts <https://www.blender.org/api/blender_python_api_current/info_quickstart.html>`__ `Add-on Tutorial <https://www.blender.org/api/blender_python_api_current/info_tutorial_addon.html>`__ `Add-ons development guidelines <https://wiki.blender.org/wiki/Process/Addons/Guidelines>`__ `How to share your add-on <https://wiki.blender.org/wiki/Process/Addons>`__ `Scripts Catalog <https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts>`__ Project-Id-Version: Blender 2.79 Manual 2.79
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
 A quick introduction to Blender's API. A quick tutorial on the essentials of writing an add-on. Add a subdirectory under ``my_scripts`` called ``addons`` (it *must* have this name for Blender to recognize it). -- Add-on Information Tùy chọn về Trình Bổ Sung -- Add-on Preferences Trình Bổ Sung -- Add-ons Add-ons are divided into categories by what areas of Blender they affect. Add-ons tab in the User Preferences. Add-ons that activate or change multiple hotkeys now have a special system of activation. For example, with the "UI: Pie Menu Official" add-on for each menu there's a selection box to activate the menu and its hotkey. Blender comes with some useful Add-ons already, ready to be enabled. But you can also add your own, or any interesting ones you find on the web. Blender will copy newly installed add-ons under the directory selected in your User Preferences. Blender's add-ons are split into two groups depending on who writes/supports them: Phân Loại: -- Categories Community: Add-ons that are written by people in the Blender community. Create an empty directory in a location of your choice (e.g. ``my_scripts``). Enable and disable an add-on by checking or unchecking the box on the right of the add-on you chose, as shown in the figure. Enabling an add-on. -- Enabling and Disabling -- Filtering For add-ons that you found on the web or your own to show on the list, you have to install them first by clicking *Install from File...* and providing a ``.zip`` or ``.py`` file. Guidelines on writing new add-on that you might want to get into Blender. Tiêu Đề -- Header If you want an Add-on to be enabled every time you start Blender, you will need to *Save User Settings*. -- Individual Activation Information on how to get your add-on into Blender.  -- Install from File Now the add-on will be installed, not automatically enabled. The search field will be set to the add-on's name (to avoid having to look for it). Enable the add-on by turning on the checkbox. Now when you install add-ons you can select the *Target Path* option to *User Pref* (from the *File* tab). Official: Add-ons that are written by Blender developers. Nguồn Tài Nguyên Trên Mạng -- Online Resources Open the *File* tab of the *User Preferences*. Provides an index of Add-ons that are included with Blender as well as listing a number of external Add-ons. Làm Tươi Lại -- Refresh Save the User Preferences and restart Blender for it to recognize the new add-ons location. Saving Add-on Preferences Scans the :doc:`Add-on Directory </getting_started/installing/configuration/directories>` for new add-ons. -- Searching Set the *Scripts* in the User Preferences to point to your script directory (e.g. ``my_scripts``). Mức Hỗ Trợ -- Supported Level The Add-ons tab lets you manage secondary scripts, called "Add-ons" that extends Blender's functionality. In this tab you can search, install, enable and disable Add-ons. The add-on functionality should be immediately available. If the Add-on does not activate when enabled, check the :doc:`Console window </advanced/command_line/introduction>` for any errors, that may have occurred. This menu contains a list of helpful links for both users and people who are interested in writing their own add-on. User-Defined Add-on Path With Pie menus, First you activate the add-on. This activates the "Add-ons Preferences Submodule Activation". You then need to expand the Add-ons Preferences, then you will see the list of Pie Menu types you can choose from. From here you can individually activate the menus you like to use. If the menu conflicts with another favorite, there's no need to activate it. You can activate any combination and save as user settings so your activations are available next time you start Blender. You can also create a personal directory containing new add-ons and configure your files path in the *File* tab of the *User Preferences*. To create a personal script directory: You can click the arrow at the left of the add-on box to see more information, such as its location, a description and a link to the documentation. Here you can also find a button to report a bug specific of this add-on. `API Concepts <https://www.blender.org/api/blender_python_api_current/info_quickstart.html>`__ `Add-on Tutorial <https://www.blender.org/api/blender_python_api_current/info_tutorial_addon.html>`__ `Add-ons development guidelines <https://wiki.blender.org/wiki/Process/Addons/Guidelines>`__ `How to share your add-on <https://wiki.blender.org/wiki/Process/Addons>`__ `Scripts Catalog <https://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts>`__ 