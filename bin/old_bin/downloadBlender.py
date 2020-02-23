#!/usr/bin/python3
import urllib as UL
import os
from argparse import ArgumentParser

class MakingVIDocuments:
    def __init__(self):
        self.input_file = None
        self.use_local_file = False

    def setVars(self, input_file):
        self.input_file = input_file
        self.use_local_file = (path.exists(self.input_file))

    def downloadFile(self, file_name):
        url = file_name
        base_name = os.
    def run(self):
        #os.environ.update({'LC_ALL':'C.UTF-8'})
        #os.environ.update({'LANG':'C.UTF-8'})


        os.chdir(self.make_dir)
        if (self.is_clean):
            os.system("make clean")
            os.system("find locale/vi/LC_MESSAGES -type f -name \"*.mo\" -exec rm -f {} {} \;")
            os.system("make update_po")

        cmd = "make -d --trace -w -B -e SPHINXOPTS=\"-D language='vi'\" 2>&1"
        print("Performing: %s" % cmd)
        os.system(cmd)
        #from_dir="/home/htran/blender_documentations/blender_docs/build/html/"
        #to_dir="/home/htran/blender_documentations/new_blender_manual/blender_docs/build/html/"
        from_dir="/home/htran/blender_documentations/blender_docs/"
        to_dir="/home/htran/blender_documentations/new_blender_manual/blender_docs/"
        cmd = "rsync -arP --delete {} {}".format(from_dir, to_dir)
        print("Performing: %s" % cmd)
        os.system(cmd)

parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_true')
#parser.add_argument("-d", "--dir", dest="make_dir", help="Directory where MAKE is performed")
parser.add_argument("-f", "--file", dest="input_file", help="Locally downloaded input file")
args = parser.parse_args()

print("args: {}".format(args))

x = MakingVIDocuments()
x.setVars(args.input_file)
x.run()
