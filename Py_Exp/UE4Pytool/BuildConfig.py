from os import path
import os.path as Path
import unreal


TEMP_FILE = "c:/temp/maplist.txt"

CONTENT_CONFIG_NAME = "\Game"
LEVEL_ROOT_PATH = "Levels"

INI_MAPCOOK_STR = "+MapsToCook=(FilePath=\"DIR_STRING\")"

pack_level_folders = [
    "AutoDungeon",
    # "Tower/Tower02",
    # "Tower/Tower03",
    # "Tower/Tower04",
    # "Tower/Tower05",
    # "Village/Village02",
    "Theme/Theme01/Theme_CustRoom",
    "Theme/ThemeBlackTower"
]

unreal.log("--Python build config maplist:")
#help(unreal.BlueprintFileUtilsBPLibrary)
contentPath = unreal.SystemLibrary.get_project_content_directory()

lines = []

for iter in pack_level_folders:
    level_path = Path.join(contentPath, LEVEL_ROOT_PATH, iter)
    unreal.log(level_path)
    found_paths = unreal.BlueprintFileUtilsBPLibrary.find_recursive(
        level_path, "*.umap", True, False)
    if found_paths:
        for it_fp in found_paths:
            filename = it_fp.strip(contentPath).strip(".umap")
            filename = Path.normpath(Path.join(CONTENT_CONFIG_NAME, filename))
            #unreal.log(" - - " + Path.normpath(filename))
            filename = INI_MAPCOOK_STR.replace("DIR_STRING", filename)
            lines.append(filename+"\n")
            unreal.log(" :" + filename)

file = open(TEMP_FILE, 'w')
file.writelines(lines)
file.close()
#INI_MAPCOOK_STR.
#contentPath
