import re


RE_BODY_PREFIX = re.compile(
    r"\[(?P<time>\d{1,2}:\d{1,2}:\d{1,2})\]\D?:(?P<ue4log>.*)")

# log category congfig: will become json string from client
LOG_CATEGORIES = [
    {
        "cat": "other",
        "menu": "其它",
        "keys": ["LogTargetPlatformManager:", "LogSavePackage:"]
    },
    {
        "cat": "asset",
        "menu": "资源",
        "keys": ["LogUObjectGlobals:", "LogClass:", "LogAutomationTest:", "LogCook:"]
    },
    {
        "cat": "blueprint",
        "menu": "蓝图",
        "keys": ["LogBlueprint:", "LogEnum:", "LogLinker:"]
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


def analyse_UE4logline(line, time):
    if RE_WARN_ERROR_FILTER.search(line):
        ana_obj = {
            "time": time,
            "text": "",
            "catagory": "",
            "key": ""
        }
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
            ana_obj["catagory"] = "none"
        return ana_obj
    return None


def analyse_teamcity_buildlog(log_text):
    lines = log_text.splitlines()
    lines = list(set(lines))

    log_obj = {'info': {"text": ""}, 'body': []}
    for line in lines:
        match = RE_BODY_PREFIX.match(line)
        if match:
            line_log = match.groupdict()
            line_obj = analyse_UE4logline(line_log["ue4log"], line_log["time"])
            if line_obj:
                log_obj["body"].append(line_obj)
        else:
            log_obj['info']['text'] = log_obj['info']['text'] + \
                '\r\n' + line
    return log_obj



testlog_path = "D:/Users/feng.yan/Documents/Rox_Alpha_Daily_Build_24.log"
with open(testlog_path, 'r', encoding='utf-8') as file:
    text = file.read()

result = analyse_teamcity_buildlog(text)

#result = RE_UE4_PATH_OR_CLASS.findall("[16:01:31] :	 [Step 1/1]   LogMaterial: Warning: D:\TeamCity\buildAgent\work\86314017ea15d70\Project_Rox\Rox_Demo_0\Content\Environment\DungePart_A\Material\Master\MM_Rooftops_Concrete.uasset: Failed to compile Material for platform PCD3D_SM5, Default Material will be used in game.")
#result = RE_UE4_PATH_OR_CLASS.findall("[16:03:53] :	 [Step 1/1]   LogUObjectGlobals: Warning: 加载“D:/TeamCity/buildAgent/work/86314017ea15d70/Project_Rox/Rox_Demo_0/Content/Blueprints/NPC/AI/EQSQuery/TargetInRange.uasset”时未能加载“/Script/EnvironmentQueryEditor”：无法找到文件。")
#result = analyse_UE4logline("[11:47:37] :	 [Step 1/1]   LogInit: Display: LogAutomationTest: Warning: FGridFlowItem::ItemId is not initialized properly. Module:DungeonArchitectRuntime File:Public/Frameworks/GridFlow/AbstractGraph/GridFlowAbstractItem.h", "1")

print(result)

# lines = text.splitlines()
# df = pd.DataFrame(lines)
# lines = df.drop_duplicates()
# print(lines)
