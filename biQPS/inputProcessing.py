import csv
import logging
import math
import numpy as np
import warnings

class  inputProcessing(): 
    ## preProcessing component
    def __init__(self):
        self.csvFileList       = [];
    
    
    def _extractCSVFile(self,files):
        for filename in files: 
            if filename.endswith(".txt"): # List of csv. files
                try:
                    f = open(filename, 'r+')
                except OSError:
                    print('Cannot open', filename)
                else:
                    self.csvFileList = self.csvFileList + f.read().splitlines()
                    #print(self.csvFileList)
                    f.close()
            elif filename.endswith(".csv"): # csv. file
                self.csvFileList = self.csvFileList + [filename]
            else:
                warnings.warn("Wrong input format (%s). Please use .csv or .txt files."%filename)
        #print(self.csvFileList)
        return self.csvFileList