import argparse
import os
import glob
import subprocess
from pathlib import Path


def find_movies(path):
    return glob.glob(path + '/**/' + '*2160p*', recursive=True)

def create_new_movie(path):
    file = Path(path)
    parent_folder = file.parent
    new_name = os.path.join(parent_folder, file.name.replace("2160p", "1080p").replace("Remux-", ""))
    bashCommand = 'HandBrakeCLI --preset=\"Super HQ 1080p30 Surround\" -i \'%s\' -o \'%s\'' % (path, new_name)
    print(bashCommand)
    os.system(bashCommand)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Retrieve documents from docman machine')
    parser.add_argument('--path', nargs='?', help='root document path')
    args = parser.parse_args()
    movies = find_movies(args.path)
    for movie in movies:
        try :
            print("Beginning conversion of " + movie)
            create_new_movie(movie)
        except Exception:
            print("Unable to convert " + movie)
            print('' + Exception)
