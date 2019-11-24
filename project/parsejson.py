import json
import os

"""数据校验：文件一致性校验
"""


def count_id(filePath, outPath):
    with open(filePath, mode='r') as file:
        try:
            out_file = open(outPath, mode="a+", encoding="utf-8")  # 保存文件
            openNum = 1
            s = set()
            lines = file.readlines()
            print(len(lines))
            for line in lines:
                dict_data = json.loads(line)
                taskId = dict_data['taskId']
                data = dict_data["data"]
                for res in data:
                    assetId = res["assetId"]
                    webGroupId = res["webGroupId"]
                    industryDynamic = res['industryDynamic']
                    if webGroupId == "1" or industryDynamic != "0":
                        s.add(taskId)
                        result = {"taskId": taskId, "assetId": assetId, "webGroupId": webGroupId,
                                  "industryDynamic": industryDynamic, "count": len(s)}
                        result = json.dumps(result)
                        out_file.write(result)
                        out_file.write("\n")

                if openNum % 1000 == 0:
                    out_file.flush()
                    print(openNum, "写入文件" + outPath)
                openNum += 1

            out_file.close()
        except Exception as e:
            print(e)


from dateutil.parser import parse
import traceback


def count_id(filePath, outPath):
    '''
    统计webgroupID
    :param filePath:
    :param outPath:
    :return:
    '''
    with open(filePath, mode='r') as file:
        try:
            out_file = open(outPath, mode="a+", encoding="utf-8")  # 保存文件
            openNum = 1
            s = set()
            lines = file.readlines()
            out_file.write(",".join(["id", "taskId", "assetId", "webGroupId", "industryDynamic", "assetInIndustrys",
                                     "assetInIndustrysSecondlevel"]))
            out_file.write("\n")
            for line in lines:
                dict_data = json.loads(line)
                taskId = dict_data['taskId']
                time_seg = taskId.split(":")[1]
                time = parse(time_seg)
                if time >= parse("20191023060000") and time <= parse("20191023150000"):
                    data = dict_data["data"]
                    for res in data:
                        assetId = res["assetId"]
                        webGroupId = res["webGroupId"]
                        industryDynamic = res['industryDynamic']
                        assetInIndustrys = res["assetInIndustrys"]
                        assetInIndustrysSecondlevel = res["assetInIndustrysSecondlevel"]
                        # if webGroupId == "1":
                        # if industryDynamic != "0":
                        if assetInIndustrys == 1:
                            result = []
                            s.add(taskId)
                            result.append(str(len(s)))
                            result.append(taskId)
                            result.append(assetId)
                            result.append(webGroupId)
                            result.append(industryDynamic)
                            result.append(str(assetInIndustrys))
                            result.append(assetInIndustrysSecondlevel)
                            out_file.write(",".join(result))
                            out_file.write("\n")

                if openNum % 1000 == 0:
                    out_file.flush()
                    print(openNum, "写入文件" + outPath)
                openNum += 1

            out_file.close()
        except Exception as e:
            traceback.print_exception(e)


import pandas as pd
import numpy as np
import os


def count_all(filePath):
    '''
    统计webgroupID
    :param filePath:
    :param outPath:
    :return:
    '''
    with open(filePath, mode='r') as file:
        try:

            s = set()
            ases = []
            lines = file.readlines()
            taskIds = []
            for line in lines:
                dict_data = json.loads(line)
                taskId = dict_data['taskId']
                time_seg = taskId.split(":")[1]
                time = parse(time_seg)
                if time >= parse("20191023060000") and time <= parse("20191023150000"):
                    taskIds.append(taskId)
                    data = dict_data["data"]
                    for res in data:
                        assetId = res["assetId"]
                        webGroupId = res["webGroupId"]
                        industryDynamic = res['industryDynamic']
                        assetInIndustrys = res["assetInIndustrys"]
                        assetInIndustrysSecondlevel = res["assetInIndustrysSecondlevel"]
                        ases.append(1)
                        # if webGroupId == "1":
                        # if industryDynamic != "0":
                        if assetInIndustrys == 1:
                            result = []
                            s.add(taskId)
                            result.append(str(len(s)))
                            result.append(taskId)
                            result.append(assetId)
                            result.append(webGroupId)
                            result.append(industryDynamic)
                            result.append(str(assetInIndustrys))
                            result.append(assetInIndustrysSecondlevel)

            print(len(ases))
        except Exception as e:
            traceback.print_exception(e)


def count_file_nums(file_path=r"C:\Users\dell\Desktop\taskDir", start_time=None, end_time=None):
    names = os.listdir(file_path)
    count = 0
    taskIDs = []
    taskId_times = []
    for name in names:
        file_time = name.split("_")[1]
        time = parse(file_time)
        if time >= parse("20191123060000") and time <= parse("20191123070000"):
            count += 1
            taskIDs.append(name[:-4])
            taskId_times.append(file_time)

    return count, taskIDs, taskId_times


def get_title(file):
    res = {}
    try:
        with open(file, mode="r", encoding="utf-8") as values:
            lines = values.readlines()
            for line in lines:
                data = json.loads(line)
                title = data["title"]
                assetId = data['assetId']
                res.update({assetId:title})
        return res
    except:
        print("文件读取异常" + file)
        return ""


def combine(values_file, src_path, out_file):
    with open(values_file, mode="r", encoding="utf-8") as values:
        lines = values.readlines()
        taskIds = []
        assetIds = []
        webGroupIds = []
        industryDynamics = []
        assetInIndustryses = []
        secondlevels = []
        titles = []
        file_names = []
        try:
            i = 0
            for line in lines:
                data = json.loads(line)
                taskId = data["taskId"]
                # 获取路径
                src_file = taskId.replace(":", "_") + ".txt"
                print(src_path + src_file)
                result = get_title(src_path + src_file)
                data_list = data["data"]
                for res in data_list:
                    assetId = res["assetId"]
                    webGroupId = res["webGroupId"]
                    industryDynamic = res['industryDynamic']
                    assetInIndustrys = res["assetInIndustrys"]
                    secondlevel = res["assetInIndustrysSecondlevel"]
                    taskIds.append(taskId)
                    assetIds.append(assetId)
                    webGroupIds.append(webGroupId)
                    industryDynamics.append(industryDynamic)
                    assetInIndustryses.append(assetInIndustrys)
                    secondlevels.append(secondlevel)
                    title = result[assetId] if result[assetId] != None else ""
                    titles.append(title)
                    file_names.append(src_file)
                    i += 1
                    if i % 1000 == 0:
                        print("次数", i)
        except Exception as e:
            print(e)

    writer = pd.ExcelWriter(out_file, engine="xlsxwriter", options={'strings_to_urls': False})
    data = pd.DataFrame(
        {"taskID": taskIds, "assetId": assetIds, "title": titles, "webGroupId": webGroupIds,
         "industryDynamic": industryDynamics,
         "assetInIndustrys": assetInIndustryses, "Secondlevel": secondlevels,
         "文件名字": file_names})
    # data.to_csv("./count/all_values1.csv", index=False, header=True, quoting=0)
    print("文件开始写入")
    data.to_excel(writer, index=False)
    writer.save()
    print(out_file, "文件已经保存")


if __name__ == "__main__":
    filePath = r"C:\Users\dell\Desktop\taskDir"
    values_file = "./count/all_values2.txt"
    src_path = "C:/Users/dell/Desktop/taskDir1/"
    out_file = "./count/stat_res3.xls"
    combine(values_file, src_path, out_file)
    e = get_title("C:/Users/dell/Desktop/taskDir1/fd-L_20191123061252_2503_xhwnews-consumer-group.txt")
    print(e)
    print(e['-6181288884544622998'])

    # count, taskIDs, taskId_times = count_file_nums(filePath, None, None)
    # print(get_title(r"C:\Users\dell\Desktop\taskDir1\fd-L_20191123061252_2503_xhwnews-consumer-group.txt"))

    # t = "assetInIndustrys"
    # outFilePath = "./" + t + "_count.csv"
    # count_id(inFilePath, outFilePath)
    # d = pd.read_csv(outFilePath, dtype=np.str)
    # d.to_excel("./count/" + t + "_count.xls")
    # os.remove(outFilePath)
    # count_all(inFilePath)
