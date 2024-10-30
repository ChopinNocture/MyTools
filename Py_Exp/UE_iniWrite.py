import re
import os.path

TEXT_FILE = "中奖概率.txt"
TEXT_FILE_PATH = "E:/Development/Packages" #"C:/Users/Administrator/Desktop/"
INI_FILE = "Game.ini"
INI_FILE_PATH = "E:/Development/Packages" #"C:/Projects/Football/Football/Saved/Config/Windows/"

KEYWORDS = ["围巾数量", "衣服数量", "钥匙数量", "预估玩家基数" , "预估连续三次破门率"]
# "[/Game/BP/Game/BP_Controller.BP_Controller_C]"


def update_value_in_file(filename, target_filename, keywords):
    keyword_pattern = '|'.join(re.escape(keyword) for keyword in keywords)
    pattern = re.compile(rf'^{keyword_pattern}\s*=\s*([-+]?[0-9]*\.?[0-9]+)\s*$')

    # 正则表达式：匹配格式为 "关键字 = 数字" 的行
    #pattern = re.compile(rf'^{re.escape(keyword)}\s*=\s*([-+]?[0-9]*\.?[0-9]+)\s*$')
    keylines = {}

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            match = pattern.match(line.strip())
            if match:
                keylines[match.group(0).split('=')[0].strip()] = line
    print(keylines)

    #updated = False
    with open(target_filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(target_filename, 'w', encoding='utf-8') as file:
        for line in lines:
            left = line.split('=')[0].strip()
            if left in keylines:
                # 如果存在匹配的关键字，则覆盖
                line = keylines[left]
                #updated = True
            file.write(line)

        # 检查是否需要添加新的行
        for key in keylines:
            if not any(line.startswith(key) for line in lines):
                # 如果没有找到该关键字，则添加
                file.write(keylines[key])



fileA = os.path.join(TEXT_FILE_PATH, TEXT_FILE)
fileB = os.path.join(INI_FILE_PATH, INI_FILE)

update_value_in_file(fileA, fileB, KEYWORDS)
