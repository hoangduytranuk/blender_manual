cd $BLENDER_MAN_EN/locale/vi
svn cleanup
svn update
cd $BLENDER_MAN_EN
rm -fr build/locale
make gettext
sphinx-intl --config=manual/conf.py update --pot-dir=build/locale --language="vi"
python3 tools_rst/rst_check_locale.py