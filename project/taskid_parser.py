import json

if __name__ == "__main__":
    file = r"G:\新华网项目\新华网前端设计思路\praise\dev_80_201909090000_201909222359_20190925151049_1.txt"
    docs = open(file, mode="r", encoding='utf-8').readlines()
    result_docs = []
    for doc in docs[:1000]:
        t = json.loads(doc.strip())
        assetId = t["assetId"]
        content = t["content"]
        assetId = assetId.strip().replace(" ", "")
        content = content.strip().replace(" ", "")
        temp = {"assetId": assetId, "content": content}
        result_docs.append(temp)

    data = {
        "taskId": "test9_789_201912020000_201912152359_20191216003210_1",
        "kafkaTopicName": "CarKBTopicTest",
        "sendCount": "1",
        "docs": result_docs
    }
    outfile = r"G:\新华网项目\新华网前端设计思路\praise\test_data_clean.txt"
    t = json.dumps(data, ensure_ascii=False)

    with open(outfile, mode="w", encoding='utf-8') as f:
        f.write(t)
