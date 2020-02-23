#!/usr/bin/python3
from argparse import ArgumentParser
from bs4 import BeautifulSoup, Tag
class BeautifyHTML:
    def __init__(self):
        self.input_file = None
        self.is_inplace = False

    def setVars(self, input_file : str, write_inplace : bool):
        self.input_file = input_file
        self.is_inplace = (True if (write_inplace) else False)

    def writeFile(self, data):
        with open(self.input_file, 'w') as f:
            f.write(data)

    def run(self):
        with open(self.input_file) as f:
            soup = BeautifulSoup(f, 'html.parser')
        data_output = soup.prettify()
        if (self.is_inplace):
            #print("should be writing into the file:{}".format(self.input_file))
            self.writeFile(data_output)
            print("wrote changes into the file:{}".format(self.input_file))
        else:
            print(data_output)


parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
parser.add_argument("-i", "--inplace", dest="write_inplace", \
                    help="Write out the changes to the original file. \
                    NOTE: Not Recommended! DANGEROUS: Use it at your own peril.", \
                    action='store_true')
parser.add_argument("-f", "--file", dest="input_file", help="Input HTML file to be beautify.")
args = parser.parse_args()

x = BeautifyHTML()
x.setVars(args.input_file, args.write_inplace)
x.run()
