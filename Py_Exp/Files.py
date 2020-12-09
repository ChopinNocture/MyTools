import os


def renameFiles(folder_url):
    files = os.listdir(folder_url)

    print(files)
    for file in files:
        new_name = file.replace("_PreviewMesh", "")
        print(new_name)
        os.rename(folder_url+"\\"+file, folder_url+"\\"+new_name)


# renameFiles("\\\\nas\\Development Dept\\UE4ImportDepot\\Rox_Alpha\\Skeletons\\RoxHero\\LocoAnims")