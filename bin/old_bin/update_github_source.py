#!/usr/bin/python3
import os
from argparse import ArgumentParser

class TransferChanges:
    exclude_list=[
        ".svn",
        "build",
        "*.pyc",
        "*.mo"
        #"",
        ]
    #rsync -a -v --progress --modify-window=1 -c -b -i -s -m --del -vv --ignore-errors --chmod=ugo=rwx --delete --delete-excluded  --exclude='*~'  --exclude='.*' --backup-dir=.rsync_bakupd
    normal_option = "-aruhvm --progress "
    dry_run_option = "n"
    from_dir = "blender_documentations/blender_docs/"
    to_dir="blender_documentations/github/blender_manual/blender_docs/"
    log_file_name="rsync_run.txt"
    def __init__(self):
        self.is_dry_run : bool = False
        self.make_dir : str = None

    def setVars(self, is_dry_run : bool):
        self.is_dry_run = (True if (is_dry_run) else False)
        self.home_dir = os.environ['HOME']
        self.from_dir = os.path.join(self.home_dir, TransferChanges.from_dir)
        self.to_dir=os.path.join(self.home_dir, TransferChanges.to_dir)
        self.log_file_path = os.path.join(self.home_dir, TransferChanges.log_file_name)

    def run(self):

        option = TransferChanges.normal_option
        if (self.is_dry_run):
            option += (TransferChanges.dry_run_option)

        command = "rsync {} --delete ".format(option)
        for x in self.exclude_list:
            command += "--exclude {} ".format(x)

        command += "{} {} > {}; cat {}".format(self.from_dir, self.to_dir, self.log_file_path, self.log_file_path)

        #os.system("rsync -arhvmn --delete --exclude '.svn' --exclude 'build' --exclude '*.pyc' --exclude '*.mo' $source_dir $target_dir > $log_file")
        os.system(command)
        print("Command executed:\n{}".format(command))

        command = "cd {}; \
        make clean; \
        make -d --trace -w -b html -B -e SPHINXOPTS=\"-D language='vi'\" 2>&1; \
        cd build; \
        zip -r9 blender_vietnamese_html.zip html/; \
        cd ..; \
        make -d --trace -w -b singlehtml -B -e SPHINXOPTS=\"-D language='vi'\" 2>&1; \
        cd build; zip -r9 blender_vietnamese_single.zip singlehtml/; \
        cd ../..;".format(self.to_dir)

        command = "convpo; \
        change_placeholders.sh $PWD"

        os.system(command)
        print("Command executed:\n{}".format(command))

parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
parser.add_argument("-t", "--test", dest="test_action", help="Perform dry run only.", action='store_true')
#parser.add_argument("-d", "--dir", dest="make_dir", help="Directory where MAKE is performed")
args = parser.parse_args()

print("args: {}".format(args))

x = TransferChanges()
x.setVars(args.test_action)
x.run()
