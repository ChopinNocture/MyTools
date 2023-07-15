import os
import argparse
import random
from PIL import Image



def add_arguments(parser):
    parser.add_argument(
        '-path', '-p',
        action='store',
        dest='path',
        help='where to store',
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="TGA to PNG with Alpha")
    add_arguments(parser)
    args = parser.parse_args()

    destPath = "./"
    if args.path is not None and os.path.exists(args.path):
        fullPath = os.path.abspath(args.path)
        destPath = os.path.dirname(fullPath)
        
    img = Image.new("RGB", (64, 64))
    #imgResized = img.resize((512, 512)).reduce(512)
    # rgba = img.convert("RGBA")
    datas = img.getdata()
    # rgba.putdata(datas)

    newData = []
    for i in datas:    
        list = [0,0,1,0,0,0,0,0,0,0,0,0]
        #list = [0,0,1,1,1,1,1,0]
        r = random.randint(min, max) * random.choice(list)
        g = random.randint(min, max) * random.choice(list)
        b = random.randint(min, max) * random.choice(list)
        #a = random.randint(min, max) * random.choice(list)
        newData.append((r,g,b))
        #print(i)
    
    img.putdata(newData)
    #img.show()

    destfile = os.path.join(destPath, "44x22" + ".png")
    #print(destfile)
    img.save(destfile, "PNG")
    
    