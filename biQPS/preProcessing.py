import csv
import logging
import math
import numpy as np

class  preProcessing(): 
    ## preProcessing component
    def __init__(self):
        self.feaNames       = ['QP','BR','RS','FR','SD']
        self.noFea          = len(self.feaNames)+1 # Add padding status feature for each segment
        self._MAX_          = {'SD': [20], 'QP': [52],'BR': [15000],'RS': [2073600],'FR': [30],'HE': [1080],'WI': [1920]}
        self.I              = [] #I
        self.noSegment 		= 0
    
    def _loadData(self,file): 
        ## Extract data from .csv files
        self.I              = [] #I
        self.noSegment      = 0
        try: 
            self.extractFromCSVFile(file)
            #print(self.inputArray)
        except Exception as e:
            logging.exception("Error in extracting data from CVS file: %s!"%file)
        return self.noSegment

    def _divideInterval(self,idxInterval,K): 
        ## Divide each session into short intervals
        try:
            lb   = idxInterval if idxInterval >0 else 0
            ub   = lb+K
            sI= np.array(self.I)[:,lb:ub].transpose().reshape(1,-1,self.noFea)
        except Exception as e:
            #print(idxInterval)
            #print(K)
            #print(lb)
            #print(ub)
            logging.exception("Error in dividing input array!")
        return sI


    def extractFromCSVFile(self,filename):
        with open(filename, 'r') as csvFile:
            reader      = csv.reader(csvFile)
            headers    = next(reader,None) # Extract headers
            iArray      = {}
            for feaN in headers:
                iArray[feaN] = []
            for segment in reader: #each row
                for feaN,feaV in zip(headers,segment):
                    try:
                        norFeaV = float(feaV)/float(self._MAX_[feaN][0]) #normalize
                        if feaN == 'RS':
                            norFeaV = math.sqrt(float(feaV)/float(self._MAX_[feaN][0]))
                    except Exception as e:
                        logging.exception("Error in normalizing feature: %s %d!"%feaN,self._MAX_[feaN][0])
                    iArray[feaN].append(norFeaV)
            for cntFea in range(0,len(self.feaNames)):
                self.I.append(iArray[self.feaNames[cntFea]])
            self.noSegment = len(self.I[0])
            paddStatus = [1] * self.noSegment
            self.I.append(paddStatus)
            #print(self.I)
            #print(self.noSegment)