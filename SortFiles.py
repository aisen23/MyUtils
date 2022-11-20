import os
import datetime
import sys


__image_list__ = ['jpg', 'jpeg', 'png']
_video_list__ = ['mp4', 'mov', 'mkv']
__audio_list__ = ['mp3', 'wav']
__media_list__ = __image_list__ + _video_list__ + __audio_list__
__base_path__ = os.getcwd()
__destination_path__ = os.getcwd()


def is_image(ext):
    return ext in __image_list__


def is_video(ext):
    return ext in _video_list__


def is_audio(ext):
    return ext in __audio_list__


def make_unique_path(path):
    return_value = [False, 'StringValue']

    if not os.path.isfile(path):
        return return_value

    print('File: \"' + path + '\" is exist. Trying to make unique!!!')
    ext = '.' + path.split('.')[-1]
    path = path[0: len(path) - len(ext)]

    index = 0
    new_path = path + '_' + str(index)
    while os.path.isfile(new_path + ext):
        index += 1
        new_path = path + '_' + str(index)

    new_path += ext
    print('newPath: ' + new_path)

    return_value[0] = True
    return_value[1] = new_path

    return return_value


def move_file(file_path, destination):
    ext = file_path.split('.')[-1]
    ext_with_dot = '.' + ext
    ext = ext.lower()

    seconds = os.path.getmtime(file_path)
    date_str = datetime.datetime.fromtimestamp(seconds).strftime('%Y-%m-%d-%H-%M-%S')
    date_str_array = date_str.split('-')
    year_str = date_str_array[0]
    month_str = date_str_array[1]
    day_str = date_str_array[2]
    hour_str = date_str_array[3]
    minute_str = date_str_array[4]
    second_str = date_str_array[5]

    new_file_name = year_str + month_str + day_str + '_' + hour_str + minute_str + second_str + ext_with_dot.lower()

    dst_path = os.path.join(destination, year_str, month_str)

    type_str = ''
    if is_image(ext):
        type_str = 'image'
    elif is_video(ext):
        type_str = 'video'
    elif is_audio(ext):
        type_str = 'audio'

    dst_path = os.path.join(dst_path, type_str)
    if not os.path.isdir(dst_path):
        os.makedirs(dst_path)
    dst_path = os.path.join(dst_path, new_file_name)

    moved = False
    while not moved:
        if not os.path.isfile(dst_path):
            print(file_path + ' to ' + dst_path)
            os.rename(file_path, dst_path)
            moved = True
        else:
            pair = make_unique_path(dst_path)
            if len(pair) == 2 and pair[0]:
                dst_path = pair[1]
            else:
                print('Error: can\'t make unique path.')
                return


def remove_empty_directories(src_path):
    for path, sub_directories, files in os.walk(src_path, topdown=False):
        if not sub_directories and not files:
            os.rmdir(path)
            print('Remove empty directory: ' + path)


def main(argv):
    source = __base_path__
    destination = __destination_path__
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

    for root, directories, files in os.walk(source):
        for name in files:
            file_path = os.path.join(root, name)
            if os.path.isfile(file_path):
                ext = name.split('.')[-1]
                if ext.lower() in __media_list__:
                    move_file(file_path, destination)

    remove_empty_directories(source)


if __name__ == "__main__":
    main(sys.argv[1:])
