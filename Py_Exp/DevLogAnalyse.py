import re


RE_BODY_PREFIX = re.compile(
    r"\[(?P<time>\d{1,2}:\d{1,2}:\d{1,2})\]\D?:(?P<ue4log>.*)")

# log category congfig: will become json string from client
LOG_CATEGORIES = [
    {
        "cat": "platform",
        "menu": "平台",
        "keys": ["LogTargetPlatformManager:"]
    },
    {
        "cat": "asset",
        "menu": "资源",
        "keys": ["LogUObjectGlobals:", "LogClass:", "LogAutomationTest:", "LogCook:"]
    },
    {
        "cat": "blueprint",
        "menu": "蓝图",
        "keys": ["LogBlueprint:", "LogEnum:"]
    },
    {
        "cat": "material",
        "menu": "材质",
        "keys": ["LogMaterial:", "LogShaderLibrary:"]
    },
    {
        "cat": "audio",
        "menu": "音频",
        "keys": ["LogAudioDebug:"]
    },
]

cat_reg_list = []
for iter in LOG_CATEGORIES:
    reg_str = "|".join(iter["keys"])
    cat_reg_list.append("(?P<{cat}>{key_str})".format(cat=iter["cat"],
                                                      key_str=reg_str))

# Log Analyse Key Regex string
RE_UE4_LOG_CATEGORIES = re.compile("(" + "|".join(cat_reg_list) +
                                   r")\D?(?P<content>.*)")
# filter include warning and error message
RE_WARN_ERROR_FILTER = re.compile(r"[wW]arn(ing)?|[eE]rror")

# extract UE4 link info
RE_UE4_PATH_OR_CLASS = re.compile(r"((?:[\/|\\]Game|[\/|\\]Content)(?:[\/|\\][^”\'\"“:]*)+)")


def analyse_UE4logline(line, ana_obj):
    if RE_WARN_ERROR_FILTER.search(line):
        match = RE_UE4_LOG_CATEGORIES.search(line)
        if match:
            for iter in LOG_CATEGORIES:
                if match[iter["cat"]]:
                    # print(match.groupdict())
                    ana_obj["catagory"] = iter["cat"]
                    ana_obj["key"] = match[iter["cat"]]
                    ana_obj["text"] = match["content"]
                    ana_obj["paths"] = RE_UE4_PATH_OR_CLASS.findall(ana_obj["text"])
        else:
            ana_obj["text"] = line


def analyse_teamcity_buildlog(log_text):
    lines = log_text.splitlines()

    state = 0
    log_obj = {'head': {"text": ""}, 'body': [], 'foot': {"text": ""}}
    for line in lines:
        match = RE_BODY_PREFIX.match(line)
        if state == 0:
            if match:
                state = 1
            else:
                log_obj['head']['text'] = log_obj['head']['text'] + \
                    '\r\n' + line

        if state == 1:
            if match:
                line_log = match.groupdict()
                line_obj = {
                    "time": line_log["time"],
                    "text": "",
                    "catagory": "",
                    "key": ""
                }
                analyse_UE4logline(line_log["ue4log"], line_obj)
                log_obj["body"].append(line_obj)
            else:
                state = 2

        if state == 2:
            log_obj['foot']['text'] = log_obj['foot']['text'] + \
                '\r\n' + line
    return log_obj


# testlog_path = "D:/Users/feng.yan/Documents/testlog.txt"
# with open(testlog_path, 'r', encoding='utf-8') as file:
#     text = file.read()

# analyse_teamcity_buildlog(text)

#result = RE_UE4_PATH_OR_CLASS.findall("[16:01:31] :	 [Step 1/1]   LogMaterial: Warning: D:\TeamCity\buildAgent\work\86314017ea15d70\Project_Rox\Rox_Demo_0\Content\Environment\DungePart_A\Material\Master\MM_Rooftops_Concrete.uasset: Failed to compile Material for platform PCD3D_SM5, Default Material will be used in game.")
result = RE_UE4_PATH_OR_CLASS.findall("[16:03:53] :	 [Step 1/1]   LogUObjectGlobals: Warning: 加载“D:/TeamCity/buildAgent/work/86314017ea15d70/Project_Rox/Rox_Demo_0/Content/Blueprints/NPC/AI/EQSQuery/TargetInRange.uasset”时未能加载“/Script/EnvironmentQueryEditor”：无法找到文件。")
print(result)

# lines = text.splitlines()
# df = pd.DataFrame(lines)
# lines = df.drop_duplicates()
# print(lines)
