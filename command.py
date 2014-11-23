import os 
import os.path 
import shutil 
import time, datetime

def DA_baksmali():
    cmd="java -jar tools/baksmali-2.0.3.jar workspace/test/classes.dex -o workspace/smali"
    os.system(cmd)

def DA_unzip():
    cmd="unzip -qq workspace/test.apk -d workspace/test"
    os.system(cmd)
    
def DA_move_file(source,  target): 
    shutil.copy(source,  target)

def DA_clean():
    cmd="rm -rf workspace/*"
    os.system(cmd)
    
