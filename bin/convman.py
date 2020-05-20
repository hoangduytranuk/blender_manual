#!/usr/bin/python3
import os
from argparse import ArgumentParser

class MakingVIDocuments:
    def __init__(self):
        self.is_clean : bool = False
        self.make_dir : str = None
        self.home_dir = os.environ['HOME']

    def setVars(self, is_clean : bool, make_dir: str):
        self.is_clean = (True if (is_clean) else False)
        self.make_dir = (os.environ['BLENDER_MAN_EN'] if (make_dir == None) else make_dir)

    def run(self):
        os.environ.update({'LC_ALL':'C.UTF-8'})
        os.environ.update({'LANG':'C.UTF-8'})

        os.chdir(self.make_dir)
        if (self.is_clean):
            os.system("make clean")
            os.system("find locale/vi/LC_MESSAGES -type f -name \"*.mo\" -exec rm -f {} {} \;")
            os.system("make update_po")

        # cmd = "make -d --trace -w -B -e SPHINXOPTS=\"-D language='vi'\" 2>&1"
        cmd = 'sphinx-build -b html -D language="vi" ./manual "build/html"'
        print("Performing: %s" % cmd)
        os.system(cmd)

        cmd = 'sphinx-build -b html -D language="en" ./manual "build/en/html"'
        print("Performing: %s" % cmd)
        os.system(cmd)

        #from_dir="/home/htran/blender_documentations/blender_docs/build/html/"
        #to_dir="/home/htran/blender_documentations/new_blender_manual/blender_docs/build/html/"
        HOME_DIR=
        from_dir= self.home_dir + "blender_docs/"
        to_dir = self.home_dir + "blender_docs/"
        github_dir="/home/htran/blender_documentations/github/blender_manual/blender_docs"

        exclude_list=["exts/process_doctree.py", "exts/TranslatePO.py", "exts/__pycache__"]

        ex_list=[]
        for ex in exclude_list:
            entry="--exclude {}".format(ex)
            ex_list.append(entry)
        ex_files = " ".join(ex_list)

        cmd = "rsync -arP --delete {} {} {}".format(ex_files, from_dir, to_dir)
        print("Performing: %s" % cmd)
        os.system(cmd)

        cmd = "rsync -arP --delete {} {} {}".format(ex_files, from_dir, github_dir)
        print("Performing: %s" % cmd)
        os.system(cmd)

parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_true')
parser.add_argument("-d", "--dir", dest="make_dir", help="Directory where MAKE is performed")
args = parser.parse_args()

print("args: {}".format(args))

x = MakingVIDocuments()
x.setVars(args.clean_action, args.make_dir)
x.run()
