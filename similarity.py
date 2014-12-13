import os 
import os.path 
import shutil 
import time, datetime
import md5
import operator


app_info_list=[]

class app_info:
    def __init__(self):
        self.packagename=""
        self.classSignatures=[]

def DA_init_data(filePath):
    inputFile = open(filePath, 'r')
    lines = inputFile.readlines()
    i = 0
    while i<len(lines) and lines != "":
        app_info_tmp = app_info()
        app_info_tmp.packagename = lines[i].strip()
        i += 1
        while i < len(lines) and lines[i].find("########")==-1:
            classSignature=lines[i].split(" ")
            #print classSignature[0]
            app_info_tmp.classSignatures.append(classSignature[0])
            i += 1        
        app_info_list.append(app_info_tmp)
        i += 1
        
#    for i in range(len(app_info_list)):
#        print app_info_list[i].packagename
#        for j in range(10):
#            print app_info_list[i].classSignatures[j]
#        print " "
                
def DA_compare_class(classListA, classListB):
    pointA = 0
    pointB = 0
    score = 0
    while pointA < len(classListA) and pointB < len(classListB):
        if  cmp(classListA[pointA], classListB[pointB]) == 0:
            score += 1
            pointA += 1
            pointB += 1
        elif cmp(classListA[pointA], classListB[pointB]) < 0:
            pointA += 1
        else:
            pointB += 1
    return score

if __name__=="__main__":
    DA_init_data('./result/result.txt')
    print DA_compare_class(app_info_list[0].classSignatures, app_info_list[1].classSignatures)
    
    
