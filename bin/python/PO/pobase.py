import sys
import os

from basefileio import BaseFileIO
from basefileio import findFileByExtension, findFileByExtensionRelative
from podocument import Document

class POBasic(BaseFileIO):
    
    def __init__(self, input_dir, direction):
        self.input_dir = input_dir
        self.direction = direction

    def getSortedFileList(self, extension : str):
        find_by_extension = findFileByExtension(extension)
        self.listDir(self.input_dir, find_by_extension)
        sorted_files = find_by_extension.result
        #sorted_files=sorted(files, key=os.path.getctime, reverse=direction)
        sorted_files.sort(key=str.lower, reverse=self.direction)
        #sorted_files=sorted(files, reverse=self.direction)
        return sorted_files

    def getSortedFileListRelative(self, extension : str):
        find_by_extension = findFileByExtensionRelative(self.input_dir, extension)
        self.listDir(self.input_dir, find_by_extension)
        sorted_files = find_by_extension.result
        #sorted_files=sorted(files, key=os.path.getctime, reverse=direction)
        sorted_files.sort(key=str.lower, reverse=self.direction)
        return sorted_files

    def getSortedPOFileList(self):
        return self.getSortedFileList(".po")

    def getSortedPOFileListRelative(self):
        return self.getSortedFileListRelative(".po")

    def getSortedRSTFileList(self):
        return self.getSortedFileList(".rst")

    def getSortedRSTFileListRelative(self):
        return self.getSortedFileListRelative(".rst")
