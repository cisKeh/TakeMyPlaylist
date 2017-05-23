#!/usr/bin/python
import getopt
import os
import shutil
import sys


def parseXml(xmlPath):
    """
    Extract every artist from xml (xml come from itunes) and return it into a list
    :param xmlPath: path of xml
    :return: list of artist from Itunes playlist
    """
    resultPlaylist =[]
    try:
        f = open(xmlPath, 'r')
        playlist = []
        for line in f:
            if ('<key>Artist</key><string>' in line):
                result = line[28:-10]

                if (result not in playlist):
                    playlist.append(result)

        resultPlaylist = [w.replace('&#38;', '&') for w in playlist]
        print("###########################################")
        print("ARTIST FOUND IN PLAYLIST:")
        print(resultPlaylist)
        print("###########################################\n")

    except IOError:
        print("ERROR: File doesn't exist or incorrect path")
    finally:
        return resultPlaylist


def findMusic(xml, src, dest):
    """
    Call parseXml() for creating a playlist with Artist Name inside.
    Then create the destination path and copy every existing artist(in playlist) from source to destination
    :param xml:path of xml file 
    :param src: path of source
    :param dest: path of destination
    :return: nothing
    """
    # playlist = ["juan"]
    playlist = parseXml(xml)
    os.chdir(src)
    if not os.path.exists(dest):
        os.makedirs(dest)
    for elem in os.listdir("."):
        if elem in playlist:
            srcPath = os.path.join(src, elem)
            destPath = os.path.join(dest, elem)
            # print("srcPath: "+srcPath)
            # print("destPath:"+destPath)
            if not os.path.exists(destPath):
                if os.path.isdir(srcPath):
                    shutil.copytree(srcPath, destPath)
                else:
                    shutil.copy2(srcPath, destPath)
                print(elem + " has been copied\t"+u"\033[1;32;49m \u2714\033[1;32;0m")
            else:
                print(elem + " already exist")


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "x:s:d:", ["xml=", "source=", "dest="])
        xml = ""
        sourcePath = ""
        destPath = ""
        for opt, arg in opts:
            if opt in ("-x", "--xml"):
                xml = arg
            if opt in ("-s", "--source"):
                sourcePath = arg
            if opt in ("-d", "--dest"):
                destPath = arg
        if (xml[0] != "/"):
            xml = os.path.join(os.path.getcwd(),xml)
        if (sourcePath[0] != "/"):
            sourcePath = os.path.join(os.path.getcwd(),sourcePath)
        if (destPath[0] != "/"):
            destPath = os.path.join(os.path.getcwd(),destPath)

    except:
        print(sys.argv[0] + "-x <xmlfile> -s <source path> -d <destination path>")
        sys.exit(2)
    finally:
        findMusic(xml, sourcePath, destPath)
