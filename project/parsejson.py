import json


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
                if time >= parse("20191023000000") and time <= parse("20191023080000"):
                    data = dict_data["data"]
                    for res in data:
                        assetId = res["assetId"]
                        webGroupId = res["webGroupId"]
                        industryDynamic = res['industryDynamic']
                        assetInIndustrys = res["assetInIndustrys"]
                        assetInIndustrysSecondlevel = res["assetInIndustrysSecondlevel"]
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


if __name__ == "__main__":
    inFilePath = r"C:\Users\dell\Desktop\20191023.txt"
    outFilePath = "./4_count.txt"
    count_id(inFilePath, outFilePath)
