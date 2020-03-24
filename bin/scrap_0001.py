import requests
from argparse import ArgumentParser
from bs4 import BeautifulSoup, Tag

class ParseRST:
    def __init__(self):
        self.input_file = None
        self.term_list = []

    def setVars(self, input_file : str):
        self.input_file = input_file

    def writeFile(self, data):
        with open(self.input_file, 'w') as f:
            f.write(data)

    def parse_title(self, elem):
        self.term_list.append(elem.text)

    def parse_field_list(self, elem):
        for field in elem.find_all('field'):
            l.append(field.field_name.text)

    def parse_literal(self, elem):
        for kbd in elem.find_all('literal', {'classes': 'kbd'}):
            kbd.replaceWith(":kbd:`{}`".format(kbd.text))

    def run(self):

        #data = requests.get('file://home/htran/blender_documentations/blender_docs/build/rstdoc/index.rst')
        #file="/home/htran/blender_documentations/blender_docs/build/rstdoc/modeling/meshes/editing/vertices.rst"
        with open(self.input_file) as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        kw = ['title', 'field_list', 'term', 'strong', 'rubric']

        for k in kw:
            for elem in soup.find_all(k):
                self.parse_title(elem)

        print(self.term_list)

        #find_all('tip' | 'note') == do not work always
        #first instance of 'paragraph'
        # literal_list=term.find_all('literal', {'classes': 'kbd'})
        #
        # has_literal = (literal_list != None) and (len(literal_list) > 0)
        # if (has_literal):
        #     print(term.text, literal_list)
        #     #text_line="{}".format(term.text)
        #     #print("{} :kbd:`{}`".format(literal_list))
        #     # for literal in term.find_all('literal', {'class': 'kbd'}):
        #     #     text = "{} :kbd:`{}`".format(term.text, literal.text)
        #     #print(text_line)
        # else:
        #     print(term.text)

parser = ArgumentParser()
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
#parser.add_argument("-i", "--inplace", dest="write_inplace", \
                    #help="Write out the changes to the original file. \
                    #NOTE: Not Recommended! DANGEROUS: Use it at your own peril.", \
                    #action='store_true')
parser.add_argument("-f", "--file", dest="input_file", help="Input rst file.")
args = parser.parse_args()

x = ParseRST()
x.setVars(args.input_file)
x.run()
