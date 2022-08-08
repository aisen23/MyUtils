import os
import datetime
import sys


imageList = ['jpg', 'jpeg', 'png']
videoList = ['mp4', 'mov']
audioList = ['mp3', 'wav']
mediaList = imageList + videoList + audioList
basePath = os.getcwd()
destPath = os.getcwd()


def IsImage(ext):
    if ext in imageList:
        return True

    return False


def IsVideo(ext):
    if ext in videoList:
        return True

    return False


def IsAudio(ext):
    if ext in audioList:
        return True

    return False


def TryChangeRegistratorVideoName(fileName):
    newFileName = fileName
    eventPrefix = 'EV'
    normalPrefix = 'NO'
    if fileName.startswith(eventPrefix):
        newFileName = fileName.replace(eventPrefix, '')
    elif fileName.startswith(normalPrefix):
        newFileName = fileName.replace(normalPrefix, '')

    return newFileName


def MoveFileToDestination(fileName, filePath, destination):
    ext = fileName.split('.')[-1]
    extWithDot = '.' + ext
    newFileName = fileName.replace(extWithDot, extWithDot.lower())
    ext = newFileName.split('.')[-1]

    seconds = os.path.getmtime(filePath)
    dateStr = datetime.datetime.fromtimestamp(seconds).strftime('%Y-%m')
    yearStr = dateStr.split('-')[0]
    monthStr = dateStr.split('-')[1]

    dstPath = os.path.join(destination, yearStr, monthStr)

    typeStr = ''
    if IsImage(ext):
        typeStr = 'image'
    elif IsVideo(ext):
        typeStr = 'video'
        newFileName = TryChangeRegistratorVideoName(newFileName)
    elif IsAudio(ext):
        typeStr = 'audio'

    dstPath = os.path.join(dstPath, typeStr)
    if not os.path.isdir(dstPath) :
        os.makedirs(dstPath)
    dstPath = os.path.join(dstPath, newFileName)


    if not os.path.isfile(dstPath):
        print(filePath + ' to ' + dstPath)
        os.rename(filePath, dstPath)


def RemoveEmptyDirs(srcPath):
    for path, subDirs, files in os.walk(srcPath, topdown=False):
        if not subDirs and not files:
            os.rmdir(path)
            print('Remove empty directory: ' + path)


def main(argv):
    source = basePath
    destination = destPath
    if len(argv) >= 1:
        path = argv[0]
        if os.path.isdir(path):
            source = destination = path
    if len(argv) >= 2:
        path = argv[1]
        if os.path.isdir(path):
            destination = path

    print('source: ' + source)
    print('destination: ' + destination)

    for root, dirs, files in os.walk(source):
        for name in files:
            filePath = os.path.join(root, name)
            if os.path.isfile(filePath):
                ext = name.split('.')[-1]
                if ext.lower() in mediaList:
                    MoveFileToDestination(name, filePath, destination)

    RemoveEmptyDirs(source)


if __name__ == "__main__":
    main(sys.argv[1:])