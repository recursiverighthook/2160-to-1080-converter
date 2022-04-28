import argparse
import os
import glob
from pathlib import Path


def find_movies(path):
    files = glob.glob(path + "/**/*", recursive=True)
    files_to_reduce = []
    for f in files:
        size = os.path.getsize(f)
        if size >= 10000000000:
            files_to_reduce.append(f)
    return files_to_reduce


def optimize_movies(path):
    file = Path(path)
    parent_folder = file.parent
    new_name = os.path.splitext(os.path.join(parent_folder, file.name))[0]
    if os.path.splitext(file)[1] != ".mp4":
        new_name += '.mp4'
    else:
        new_name += '.mkv'

    bashCommand = 'HandBrakeCLI -O -e x264 --preset=\"Super HQ 1080p30 Surround\" -i \'%s\' -o \'%s\'' % (
    path, new_name)
    print(bashCommand)
    os.system(bashCommand)
    os.system('rm \'%s\'' % path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert movies over a certain size to the proper format')
    parser.add_argument('--path', nargs='?', help='root document path')
    args = parser.parse_args()
    movies = find_movies(args.path)
    for movie in movies:
        try:
            print("Beginning conversion of " + movie)
            optimize_movies(movie)
        except Exception:
            print("Unable to convert " + movie)
            print('' + Exception)
