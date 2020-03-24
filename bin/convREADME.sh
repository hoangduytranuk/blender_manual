cd $BLENDER_GITHUB
rm -f ../README.html
pandoc README.md -f markdown -t html -s -o ../README.html
firefox ../README.html
