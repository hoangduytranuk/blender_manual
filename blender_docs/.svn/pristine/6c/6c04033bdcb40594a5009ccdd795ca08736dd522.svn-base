# Apache License, Version 2.0

# This script is to reduce tedious steps involved when updating PO files.
# It looks more complex then it really is, since we do multi-processing
# to update the PO files, to save some time.

# Subversion Checkout Location
# ============================
#
# Note: this script supports subversion repositories at these locations:
#
# ./local/(.svn)          All languages in one checkout.
# ./local/{LANG}/(.svn)   Each language in it's own checkout.
#
# All commands run from the project root, passing in paths
# without changing directories.
#
# This works since subversion will detect the parent directories ".svn"
# path without us having to change directories.

import os
from subprocess import Popen, PIPE

def find_vcs_root(test, dirs=(".git", ".svn"), default=None):
    prev, test = None, os.path.abspath(test)
    while prev != test:
        if any(os.path.isdir(os.path.join(test, d)) for d in dirs):
            return test
        prev, test = test, os.path.abspath(os.path.join(test, os.pardir))
    return default

def dir_list_folder(head_dir, dir_name):
    outputList = []
    for root, dirs, files in os.walk(head_dir):
        for d in dirs:
            if d.upper() == dir_name.upper():
                outputList.append(os.path.join(os.path.join(root, d), os.pardir))
    return outputList

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = find_vcs_root(CURRENT_DIR)
LOCALDIR = os.path.abspath(os.path.join(BASE_DIR, 'locale'))
PO_LANG = [dir for dir in os.listdir(LOCALDIR) if dir not in {'.svn'}]
SVN_DIRS_ALL = dir_list_folder(LOCALDIR, '.svn')

for SVN_DIR in SVN_DIRS_ALL:
    os.system('svn cleanup %s' % SVN_DIR)
    os.system('svn up %s' % SVN_DIR)

#
# # Create PO files:
# make clean
# make gettext
#
#
# # Update PO files
# #
# # note, this can be slow so (multi-process)
for lang in PO_LANG:
    #sphinx-intl --config=manual/conf.py update --pot-dir=build/locale --language="$PO_LANG"

for SVN_DIR in SVN_DIRS_ALL:
    os.system('svn --force --depth infinity add %s .' % SVN_DIR)

#
# # Notify on redundant PO files
# python3 tools_rst/rst_check_locale.py
#
# # Print Commit message:
# REVISION=$(svn info "$ROOTDIR" | grep '^Revision:' | sed -e 's/^Revision: //')
# for SVNDIR in "$SVN_DIRS_ALL"; do
#   echo " svn ci \"$SVNDIR\" -m \"Update r"$REVISION\"""
# done
