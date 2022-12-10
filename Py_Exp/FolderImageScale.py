from PIL import Image
import os.path

path = "F:/Dev/P4/7up_Home/depot/UETechSupport/TelecomHome/Content/Animations/XiaoMai/Textures/Emoji"
subdirs = os.listdir(path)

for folder in subdirs:
    subpath = os.path.join(path, folder)
    if os.path.isdir(subpath):
        save_path = subpath + "_2"
        file_list = os.listdir(subpath)
        for file in file_list:
            if not (('jpg' in file) or ('png' in file)):
                continue
            else:
                img = Image.open(os.path.join(subpath, file))
                img_resized = img.resize((img.width>>1, img.height>>1), Image.ANTIALIAS)
                if not os.path.exists(save_path):
                    os.mkdir(save_path)
                img_resized.save(os.path.join(save_path, file))