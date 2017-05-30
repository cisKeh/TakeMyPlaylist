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
    if not os.path.exists(dest):
        os.makedirs(dest)
    titleList = []
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
        except IOError:
            print("ERROR:\t" + title + " not found\n(path \"" + path + "\" doesn't exist)")

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
