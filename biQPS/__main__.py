import argparse
import csv
import logging
import math
from .preProcessing import preProcessing
from .localComputation import calLocalComp
import numpy as np
from statistics import median as med

def main():
    parser              = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, nargs="+",help=".csv input files")
    parser.add_argument('--K', type=int, default='50',help="interval length (default: 20); only valid for gcMode=1 and gcMode=2")
    parser.add_argument('--lcMode', type=str,choices=['SQM'], default='SQM',help="local computation mode (default:'SQM')")
    parser.add_argument('--gcMode', type=int, choices=[1, 2,3], default=3,help="global computation mode (default:3)")
    parser.add_argument('-o', type=str, default='output.txt',help=".txt output file")
    args  = parser.parse_args()
    prePC = preProcessing()
    
    f= open(args.o,"w+")
    f.write("inputFiles\tpredictedValues\n")
    ## Computation
    Qo = []
    if args.lcMode == 'SQM':
        localComp = calLocalComp()
        localComp._loadModel(1500,181)
        if args.gcMode == 3:
            K1 = 60
            K2 = 50
            for cntSess in range(0,len(args.i)):
                #print('Session: %s'%(args.i[cntSess]))
                noSegment = prePC._loadData(file=args.i[cntSess])
                miQsi = 100
                maQsi = 0
                laQsi = 0
                avQsi = 0
                Kmin = min(K1,K2)
                if noSegment<=Kmin: # Not enough a interval
                    sI=(prePC._divideInterval(0,noSegment))
                    Qo = localComp._predict(sI,np.array([0]).reshape(-1,1))
                    f.write("%s\t%f\n"%(args.i[cntSess],Qo[cntSess]))
                else:
                    for cntSeg in range(Kmin-1,noSegment):
                        cntSI_K1=cntSeg-K1+1  #from 0 to  noSegment-K+1
                        cntSI_K2=cntSeg-K2+1
                        
                        ## Dividing into intervals
                        sI_K1=(prePC._divideInterval(cntSI_K1,K1))
                        sI_K2=(prePC._divideInterval(cntSI_K2,K2))
                        
                        ## Local computation
                        try:
                            Qsi_K1 = localComp._predict(sI_K1,np.array([0]).reshape(-1,1))
                            Qsi_K2 = localComp._predict(sI_K2,np.array([0]).reshape(-1,1))
                        except Exception as e:
                            logging.exception("Error in calculating local localComputation!")
                        
                        ## Global computation
                        if cntSI_K1>= 0:
                            avQsi  =  (avQsi*(cntSI_K1)+Qsi_K1)/(cntSI_K1+1)
                        else:
                            avQsi  =  Qsi_K1
                        if cntSI_K2>= 0:
                            miQsi  = min(Qsi_K2,miQsi)
                            maQsi  = max(Qsi_K2,maQsi)
                            laQsi  = Qsi_K2
                        else:
                            miQsi  = Qsi_K2
                            maQsi  = Qsi_K2
                            laQsi  = Qsi_K2
                    Qo.append(float(miQsi*0.28+laQsi*0.28+avQsi*0.426+maQsi*0.014))
                    f.write("%s\t%f\n"%(args.i[cntSess],Qo[cntSess]))
        else:
            K=args.K
            for cntSess in range(0,len(args.i)):
                #print('Session: %s'%(args.i[cntSess]))
                noSegment = prePC._loadData(file=args.i[cntSess])
                if noSegment<=K: # Not enough a interval
                    sI=(prePC._divideInterval(0,noSegment))
                    Qo = localComp._predict(sI,np.array([0]).reshape(-1,1))
                else:
                    QsiArr = []
                    for cntSeg in range(K-1,noSegment):
                        cntSI =cntSeg-K+1  #from 0 to  noSegment-K+1
                        
                        ## Dividing into intervals
                        sI=(prePC._divideInterval(cntSI,K))
                        
                        ## Local computation
                        try:
                            Qsi = localComp._predict(sI,np.array([0]).reshape(-1,1))
                        except Exception as e:
                            logging.exception("Error in calculating local localComputation!")
                        
                        ## Global computation
                        QsiArr.append(Qsi)
                    if args.gcMode == 1:
                        Qo.append(float(np.mean(np.array(QsiArr))))
                    else:
                        Qo.append(float(med(np.array(QsiArr))))
                f.write("%s\t%f\n"%(args.i[cntSess],Qo[cntSess]))
        #print('Qo:')
        #print(Qo)
    else:
        logging.exception("Invalid lcMode: %s!"%args.lcMode)
    f.close()

    





