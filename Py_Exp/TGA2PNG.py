import os
import argparse
from PIL import Image



def add_arguments(parser):
    parser.add_argument(
        '-file', '-f',
        action='store',
        dest='file',
        help='movie of youtube url',
        required=True
    )
    parser.add_argument(
        '-dir',
        action='store',
        dest='dir',
        help='where to store, default is ./',
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="TGA to PNG with Alpha")
    add_arguments(parser)
    args = parser.parse_args()

    if os.path.exists(args.file):
        fullName = os.path.abspath(args.file)
        fileName = os.path.basename(fullName)
        destPath = os.path.dirname(fullName)
        if args.dir is not None:
            destPath = args.dir
        
        sts = fileName.split(".")

        if sts[1].lower() == "tga":
            pureName = sts[0]
            img = Image.open(fullName)
            rgba = img.convert("RGBA")
            destfile = os.path.join(destPath, pureName + ".png")
            rgba.save(destfile, "PNG")
        elif sts[1].lower() == "png":
            pureName = sts[0]
            img = Image.open(fullName)
            rgba = img.convert("RGBA")
            destfile = os.path.join(destPath, pureName + ".tga")
            rgba.save(destfile, "TGA")
       
        