'''
Created on 31 Jan 2017

@author: Hoang Duy Tran <hoangduytran1960@googlemail.com>
'''
import abc
from abc import ABCMeta

class PluginBase(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def load (self, input_src):
        '''Retrieve data from the input source and return an object'''
        return
    
    @abc.abstractmethod
    def save (self, output_src, data):
        '''Save the data object to the output'''
        return
    