#!/usr/bin/env python3
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

import os, sys, shutil
import subprocess
sys.path.append('../tools_rst')
import rst_check_locale

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

def svn_up(directory):
    cmd = (
        "sphinx-intl %s" % directory,
        "svn up %s" % directory,
    )
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        shell=True,
    )
    print(p.stdout.read().strip().decode('utf-8'))

def build_gettext(input, output):
    import multiprocessing
    threads = multiprocessing.cpu_count()
    cmd = (
        "sphinx-build -j %s -t builder_html -b gettext %s %s" % (threads, input, output)
    )
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        shell=True,
    )
    print(p.stdout.read().strip().decode('utf-8'))

def update_po(config, build_dir, lang):
    cmd = (
        "sphinx-intl --config=%s update --pot-dir=%s --language=%s" % (config, build_dir, lang)
    )
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        shell=True,
    )
    print(p.stdout.read().strip().decode('utf-8'))

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = find_vcs_root(CURRENT_DIR)
LOCALDIR = os.path.abspath(os.path.join(BASE_DIR, 'locale'))
PO_LANG = [dir for dir in os.listdir(LOCALDIR) if dir not in {'.svn'}]
SVN_DIRS_ALL = dir_list_folder(LOCALDIR, '.svn')

for SVN_DIR in SVN_DIRS_ALL:
    svn_up(SVN_DIR)

# make clean
if os.path.exists(os.path.join(BASE_DIR, 'build')):
    shutil.rmtree(os.path.join(BASE_DIR, 'build'))

build_gettext(
    os.path.join(BASE_DIR, 'manual'),
    os.path.join(BASE_DIR, 'build/locale'),
)

for lang in PO_LANG:
    update_po(
        os.path.join(BASE_DIR, 'manual/conf.py'),
        os.path.join(BASE_DIR, 'build/locale'),
        lang
    )

for SVN_DIR in SVN_DIRS_ALL:
    os.system('svn --force --depth infinity add %s .' % SVN_DIR)

# Notify on redundant PO files
# not working
#warn_locale()

def svnversion():
    p = subprocess.Popen("svnversion", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    return stdout

for SVN_DIR in SVN_DIRS_ALL:
    revision = svnversion()
    print("svn ci " + SVN_DIR + " -m \"Update Po-files r"  + revision + "\"")
