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
    if file.suffix != ".mp4":
        new_name += '.mp4'
    else:
        new_name += '.mkv'

    bash_command = [
        "HandBrakeCLI",
        "-O",
        "-e", "x265",
        "--preset=HQ 1080p30 Surround",
        "--optimize",
        "-i", str(path),
        "-o", new_name
    ]

    print("Running command:", " ".join(bash_command))
    result = subprocess.run(bash_command)

    if result.returncode == 0:
        print(f"Successfully encoded. Removing original file: {path}")
        os.remove(path)
    else:
        print(f"Encoding failed with exit code {result.returncode}. Original file kept.")


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
