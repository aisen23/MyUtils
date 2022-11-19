import os
import datetime
import sys


imageList = ['jpg', 'jpeg', 'png']
videoList = ['mp4', 'mov', 'mkv']
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


def MakeUniquePath(path):
    returnValue = [False, 'StringValue']

    if not os.path.isfile(path):
        return returnValue

    print('File: \"' + path + '\" is exist. Trying to make unique!!!')
    ext = '.' + path.split('.')[-1]
    path = path[0 : len(path) - len(ext)]

    index = 0
    newPath = path + '_' + str(index)
    while os.path.isfile(newPath + ext):
        index += 1
        newPath = path + '_' + str(index)

    newPath += ext
    print('newPath: ' + newPath)

    returnValue[0] = True
    returnValue[1] = newPath

    return returnValue


def MoveFileToDestination(fileName, filePath, destination):
    ext = fileName.split('.')[-1]
    extWithDot = '.' + ext
    ext = ext.lower()

    seconds = os.path.getmtime(filePath)
    dateStr = datetime.datetime.fromtimestamp(seconds).strftime('%Y-%m-%d-%H-%M-%S')
    dateStrArray = dateStr.split('-')
    yearStr = dateStrArray[0]
    monthStr = dateStrArray[1]
    dayStr = dateStrArray[2]
    hourStr = dateStrArray[3]
    minuteStr = dateStrArray[4]
    secondStr = dateStrArray[5]

    newFileName = yearStr + monthStr + dayStr + '_' + hourStr + minuteStr + secondStr + extWithDot.lower()

    dstPath = os.path.join(destination, yearStr, monthStr)

    typeStr = ''
    if IsImage(ext):
        typeStr = 'image'
    elif IsVideo(ext):
        typeStr = 'video'
    elif IsAudio(ext):
        typeStr = 'audio'

    dstPath = os.path.join(dstPath, typeStr)
    if not os.path.isdir(dstPath):
        os.makedirs(dstPath)
    dstPath = os.path.join(dstPath, newFileName)

    moved = False
    while not moved:
        if not os.path.isfile(dstPath):
            print(filePath + ' to ' + dstPath)
            os.rename(filePath, dstPath)
            moved = True
        else:
            pair = MakeUniquePath(dstPath)
            if len(pair) == 2 and pair[0]:
                dstPath = pair[1]
            else:
                print('Error: can\'t make unique name.')
                return



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