import os 
import os.path 
import shutil 
import time, datetime
import md5
import operator
import sys
from command import *

api_call_list = {}
out_put_file = "result/result.txt"
out_put_file_point = file(out_put_file ,'w+')
count_number = 0

class class_info:
    def __init__(self):
        self.md5=""
        self.path=""
        self.weight= 0


def DA_get_api_call_list():
    inputFile = open('methodstable.txt', 'r')
    lines = inputFile.readlines()
    for i in range(0,len(lines)-1,2):
        api_call_list[lines[i+1].strip()]=lines[i].strip()
    
#    for k in api_call_list.iterkeys():
#        print k,api_call_list[k]

def DA_get_class_signature(classPath):
    inputFile=open(classPath, 'r')
    lines=inputFile.readlines()
    methodFlag=0
    methodList=[]
    methodSignature=""
    classWeight=0
    for i in range(len(lines)):
        if lines[i].find(".method")!=-1:
            methodFlag=1
        if lines[i].find(".end method")!=-1:
            methodFlag=0
            if len(methodSignature)>4:
                classWeight += len(methodSignature)/4
                m = md5.new()
                m.update(methodSignature)
                methodSignatureMd5 = m.hexdigest()
                methodList.append(methodSignatureMd5)
#                print methodSignatureMd5, methodSignature
                methodSignature = ""
                
        if methodFlag == 1:
            if lines[i].find("invoke-")!=-1:
                startPos = lines[i].find("}, L")
                methodName = lines[i][startPos+4:lines[i].find("(",startPos+4)]
                if api_call_list.has_key(methodName):
                    methodSignature += api_call_list[methodName]
#                    print api_call_list[methodName],methodName
#   end for    

    methodList.sort()
    classSignature=""
    for i in range(len(methodList)):
        classSignature += methodList[i]
    
    if len(classSignature)!= 0:
        m = md5.new()
        m.update(classSignature)
        classSignatureMd5 = m.hexdigest()
        class_info_tmp = class_info()
        if (len(classPath)>16):
            class_info_tmp.path = classPath[16:]
        else:
            class_info_tmp.path = classPath
        class_info_tmp.md5 = classSignatureMd5
        class_info_tmp.weight = classWeight
        return class_info_tmp
    return ""




def DA_generate_signature(rootdir):
    DA_class_info_list = []
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
 #           print "parent is:" + parent
 #           print "filename is:" + filename
            classPath=os.path.join(parent,filename)
            class_info_tmp = DA_get_class_signature(classPath)
            if class_info_tmp != "":
                print class_info_tmp.md5,  str(class_info_tmp.weight), class_info_tmp.path
                DA_class_info_list.append(class_info_tmp)
#                print classSignatureMd5 , classPath
#end for

    DA_class_info_list.sort(key=operator.attrgetter('md5'))
    for i in range(len(DA_class_info_list)):
        print DA_class_info_list[i].md5, DA_class_info_list[i].weight, DA_class_info_list[i].path
        out_put_file_point.write(DA_class_info_list[i].md5 + " " + str(DA_class_info_list[i].weight) + " " + DA_class_info_list[i].path + "\n") 

def DA_get_package_info():
    cmd="tools/aapt d badging workspace/test.apk"
    rlt=os.popen(cmd,'r').read()
    lines = rlt.split("\n")
    line0Split = lines[0].split("'")
    if len(line0Split)>2:
        packageName = line0Split[1]
        print packageName
        out_put_file_point.write(packageName+"\n")
        return 1
    else:
        return 0

def DA_get_package_md5():
    m = md5.new()  
    f = open('workspace/test.apk','rb')  
    maxbuf = 8192  
    while 1:  
        buf = f.read(maxbuf)  
        if not buf:  
            break  
        m.update(buf)
    f.close()
    print m.hexdigest()
    out_put_file_point.write(m.hexdigest()+"\n")
    return 1

def DA_analysis():
 #   try:
    DA_unzip()
    DA_baksmali()
    if DA_get_package_info() == 0:
        return 0
    else:
        DA_get_package_md5()
        DA_generate_signature("workspace/smali")
        out_put_file_point.write("####################################################\n") 
        return 1
#    finally:
#        return 0    
    

def DA_analysis_folder(rootdir):
    for parent,dirnames,filenames in os.walk(rootdir):
        for filename in filenames:
            apkPath = os.path.join(parent, filename) 
            print apkPath
            DA_clean()
            DA_move_file(apkPath,"workspace/test.apk")
            DA_analysis()
    
def DA_init():
    DA_get_api_call_list()
#    DA_clean()
   # out_put_file_point = file(out_put_file ,'w+')

def DA_end():
    out_put_file_point.close()
    DA_clean()




def DA_menu():
    print "          DroidAnalytics 0.2 beta"
    print "             Designed by mzheng"
    print "          -a: analysis the apk files in the \"apk\" folder"
    print "          -c: clean workspace"

if __name__=="__main__":
    if len(sys.argv)==1:
        DA_menu()
    elif (len(sys.argv)==2 and sys.argv[1]=="-a"):
        DA_init()
        DA_analysis_folder("apk/")
        DA_end()
    elif (len(sys.argv)==2 and sys.argv[1]=="-c"):
        DA_cleanWorkSpace()


















