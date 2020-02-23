'''
Created on 31 Jan 2017

@author: Hoang Duy Tran <hoangduytran1960@googlemail.com>
'''
import abc
from pluginbase import PluginBase

class SubclassImplementation(PluginBase):
    
    def load(self, input_src):
        return input_src.read()
    
    def save(self, output_src, data):
        return output_src.write(data)

    
if __name__ == '__main__':
    print('Subclass:', issubclass(SubclassImplementation, PluginBase))
    print('Instance:', isinstance(SubclassImplementation(), PluginBase))