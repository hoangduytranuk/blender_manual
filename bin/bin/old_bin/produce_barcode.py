#!/usr/bin/python3
import os
import re
from argparse import ArgumentParser

class ProduceBarCodeGeneration:
    def __init__(self):
        self.produce_code_table=[
            ["244101000006","Braeburn Apples","KG"],
            ["244210000003","Bramley Apples", "KG"],
            ["244060000000","Broccoli","KG"],
            ["244550000008","Brussels Sprouts","KG"],
            ["244759000007","Butternut Squash","KG"],
            ["244562000003","Carrots","KG"],
            ["244016000009","Cassava","KG"],
            ["244075000002","Chayote Loose","KG"],
            ["243017000001","Conference Pears","KG"],
            ["244067000003","Courgettes","KG"],
            ["244105000002","Cox Apples","KG"],
            ["244019000006","Dudhi","KG"],
            ["244449000003","Elviva Potatoes","KG"],
            ["247535000000","Fairtrade Bannanas","KG"],
            ["244410000001","Forelle Pears","KG"],
            ["244021000001","Golden Delicious Apples","KG"],
            ["244139000009","Granny Smith Apples","KG"],
            ["244710000015","Green Peppers","EACH"],
            ["243173000006","Jersey Potatoes","KG"],
            ["244729000006","Large Potatoes","KG"],
            ["244629000007","Leeks","KG"],
            ["244053000000","Lemons","EACH"],
            ["244048000008","Limes","EACH"],
            ["244018000007","Mooli","KG"],
            ["244085000009","Mushrooms","KG"],
            ["244093000008","Onions","KG"],
            ["244712000006","Orange Peppers","EACH"],
            ["244390000008","Oranges","EACH"],
            ["244672000009","Parsnips","KG"],
            ["244128000003","Pink Lady Apples","KG"],
            ["244017000008","Plantain","KG"],
            ["244446000006","Pomegranates","EACH"],
            ["244554000004","Red Cabbage","KG"],
            ["244288000004","Red Grapefruit","EACH"],
            ["244082000002","Red Onions","KG"],
            ["244711000007","Red Peppers","EACH"],
            ["244023000009","Red Seedless","KG"],
            ["244173000003","Royal Gala Apples","KG"],
            ["243029000006","Satsumas","KG"],
            ["244238000009","Snacking Bannanas","KG"],
            ["244450000009","Sweet Clementines","KG"],
            ["244091000000","Sweet Potatoes","KG"],
            ["244063000007","Tomatoes","KG"],
            ["244813000004","Turnips","KG"],
            ["243050000006","White Cabbage","KG"],
            ["244291000008","White Grapefruit","EACH"],
            ["244713000005","Yellow Peppers","EACH"],
            #Assorted Items
            ["240635000000","Fairtrade Cotton Bag","EACH"],
            ["240633000002","Co-op Handy Shopper Bag","EACH"],
            ["5000404186442","Bags For Life","EACH"]
            ]
        self.is_clean : bool = False
        self.make_dir : str = None

    def setVars(self, is_clean : bool, make_dir: str):
        self.is_clean = (True if (is_clean) else False)
        self.make_dir = (os.environ['BLENDER_MAN_EN'] if (make_dir == None) else make_dir)

    def run(self):
        pwd = "/home/htran/Documents/jobs/orridge/produce_barcode"
        os.chdir(pwd)

        PS=".eps"
        PNG=".png"
        width=180
        height=50
        mode="EAN-13"
        astrisk="*"
        for index,item in enumerate(self.produce_code_table):
            code_string, item_name, quantization=item
            if (mode == "EAN-13"):
                code_string = "{}{}{}".format(astrisk, code_string, astrisk)
            item_name = "{} {}".format(item_name, quantization)
            output_file=re.sub(" ", "_", item_name)

            cmd = "barcode -b \"{}\" -c -e {} -g{}x{} -o {}{}".format(code_string, mode, width, height, output_file, PS)
            print("Performing: %s" % cmd)
            os.system(cmd)

            cmd = "inkscape -D -z {}{} -e {}{}".format(output_file, PS, output_file, PNG)
            #cmd = "convert {}{} {}{}".format(output_file, PS, output_file, PNG)
            print("Performing: %s" % cmd)
            os.system(cmd)

#parser = ArgumentParser()
##parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_const', const=True)
#parser.add_argument("-c", "--clean", dest="clean_action", help="Clean before MAKE.", action='store_true')
#parser.add_argument("-d", "--dir", dest="make_dir", help="Directory where MAKE is performed")
#args = parser.parse_args()

#print("args: {}".format(args))

x = ProduceBarCodeGeneration()
#x.setVars(args.clean_action, args.make_dir)
x.run()
