import os
import datetime

mediaList = ['jpg', 'jpeg', 'png', 'mp4', 'mov', 'mp3', 'wav']
imageList = ['jpg', 'jpeg', 'png']
videoList = ['mp4', 'mov']
audioList = ['mp3', 'wav']
basePath = os.getcwd()

def MoveFileToDestination(fileName) :
    ext = fileName.split('.')[-1]
    extWithDot = '.' + ext
    newFileName = fileName.replace(extWithDot, extWithDot.lower())
    ext = newFileName.split('.')[-1]

    seconds = os.path.getctime(fileName)
    dateStr = datetime.datetime.fromtimestamp(seconds).strftime('%Y-%m')
    yearStr = dateStr.split('-')[0]
    monthStr = dateStr.split('-')[1]

    newPath = os.path.join(yearStr, monthStr)

    typeStr = ''
    if ext in imageList :
        typeStr = 'image'
    elif ext in videoList :
        typeStr = 'video'
    elif ext in audioList :
        typeStr = 'audio'

    typePath = os.path.join(newPath, typeStr)
    if not os.path.isdir(typePath) :
        os.makedirs(typePath)

    newFilePath = os.path.join(typePath, newFileName)

    srcPath = os.path.join(basePath, fileName)
    dstPath = os.path.join(basePath, newFilePath)

    print(srcPath + ' to ' + dstPath)

    if not os.path.isfile(dstPath) :
        os.rename(srcPath, dstPath)
        print('File moved: \"' + dstPath + '\"')

for name in os.listdir() :
    if os.path.isfile(name) :
        ext = name.split('.')[-1]
        if ext.lower() in mediaList :
            MoveFileToDestination(name)
