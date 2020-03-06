#!/usr/bin/python3
import os
from argparse import ArgumentParser

class PeformCommand:
    def __init__(self):
        self.is_clean : bool = False
        self.source_dir : str = None

    def setVars(self, is_clean : bool, source_dir: str):
        self.is_clean = (True if (is_clean) else False)
        self.source_dir = (os.environ['BLENDER_GIT'] if (source_dir == None) else source_dir)

    def run(self):
        is_new = False
        self.source_dir = os.environ['BLENDER_GIT']
        #print(self.source_dir)
        #exit(1)
        home_dir = os.environ['HOME']
        git_dir="blender-git"
        blender_dir="blender"
        is_new = (not os.path.isdir(self.source_dir))
        if (is_new):
            base_dir=os.path.join(home_dir, git_dir)
            if (not os.path.isdir(base_dir)):
                os.makedirs(base_dir)

            os.chdir(base_dir)
            os.system("sudo apt install git, build-essential")
            os.system("git clone https://git.blender.org/blender.git")
            os.system("./blender/build_files/build_environment/install_deps.sh")
            os.chdir(blender_dir)
        else:
            os.chdir(self.source_dir)

        os.system("git submodule update --init --recursive")
        os.system("git submodule foreach git checkout master")
        os.system("git submodule foreach git pull --rebase origin master")
        os.system("make update")

#parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_true')
#parser.add_argument("-d", "--dir", dest="source_dir", help="Directory where MAKE is performed")
#args = parser.parse_args()

#print("args: {}".format(args))

x = PeformCommand()
#x.setVars(args.clean_action, args.source_dir)
x.run()
