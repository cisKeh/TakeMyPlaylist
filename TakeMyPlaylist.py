# -*- coding: utf-8 -*-
#!/usr/bin/python
import getopt
import os
import shutil
import sys
from urllib.parse import unquote
import platform
from html.parser import unescape


#TODO: resolve unicode problem
def parsingXml(xmlPath):
    pathList = []
    f = open(xmlPath, 'r')
    for line in f:
        if('<key>Location</key><string>' in line):
            if(platform.system() == 'Linux'):
                print(unescape(unquote(line[30:-10]).replace("file://","")))
                pathList.append(unescape(unquote(line[30:-10]).replace("file://","")))

            elif(platform.system() == 'Windows'):
                pathList.append(unescape(unquote(line[30:-10]).replace("file://localhost","")))

    return pathList



def findMusic(xml,dest):
    pathList = parsingXml(xml)
    pathList.insert(0,'/rolo')
    if not os.path.exists(dest):
        os.makedirs(dest)
    titleList = []
    pathNbr = 0
    for path in pathList:
        title = ''
        character = ''
        index = 1
        try:
            while (character != '/'):
                character = path[-index]
                if (character != '/'):
                    title = character + title
                index += 1
            titleList.append(title)
            shutil.copy2(path,dest)
            pathNbr += 1
            print(title + " was copied " + u"\033[92m \u2714\033[0m\t" + str(pathNbr) + "/" + str(len(pathList)))
        except IOError:
            print(u"\033[91mERROR\033[0m: " + title + " not found\t--->\t(path \"" + path + "\" doesn't exist)")
    print("TOTAL MUSIC COPIED: " + str(pathNbr) + "/" + str(len(pathList)))


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "x:d:", ["xml=", "dest="])
        xml = ""
        destPath = ""
        for opt, arg in opts:
            if opt in ("-x", "--xml"):
                xml = arg
            if opt in ("-d", "--dest"):
                destPath = arg
        if (xml[0] != "/"):
            xml = os.path.join(os.getcwd(),xml)
        if (destPath[0] != "/"):
            destPath = os.path.join(os.getcwd(),destPath)
    except:
        print("command: "+ sys.argv[0] + "-x <xmlfile> -d <destination path>")
        sys.exit(2)
    finally:
        findMusic(xml, destPath)




#print(u"\033[1;32;49m \u2714\033[1;32;0m")
