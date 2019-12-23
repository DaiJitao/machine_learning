import pandas as pd
from kafka import KafkaConsumer
from project.parsejson import count_file_nums

# kafka配置
conf = {
    'host': ['10.121.17.193:9092', '10.121.17.194:9092', '10.121.17.195:9092'],
    'topic': 'LabelTopic_v1',  # 'LabelTopic', # "PosNegTopic", #'LabelTopic',
    'groupid': "1",  # 'car-group',
    'max_request_size': 52428800  # 50M
}


def readKafka(save, out_file, out_txt, taskID_times):
    print('consumer start to consuming...')
    consumer = KafkaConsumer(bootstrap_servers=conf['host'], group_id=conf['groupid'],
                             auto_offset_reset='earliest')  # earliest ,auto_offset_reset='latest'
    consumer.subscribe((conf['topic'],))
    taskIds = []
    values = []
    count = 0
    out_data = open(out_txt, mode="w+", encoding="utf-8")
    for message in consumer:
        # print(message)
        if None == message.key:
            message_key = "No key"
            print(message.topic, message_key, message.value.decode('utf-8'))
        else:
            # topic = message.topic
            key = message.key.decode('utf-8')
            value = message.value.decode('utf-8')
            key_time = key.split(":")[1]
            # print(value)
            if "20191123" in key_time:
                # 遍历指定的taskIDs
                for temp in taskID_times:
                    if key_time == temp:
                        print(key)
                        taskIds.append(key)
                        values.append(value)
            count += 1
            if count % 200 == 0:
                print("计算次数", count)

            if (len(taskIds) >= len(taskID_times)):
                print("退出遍历msg")
                break

    if save:
        out_data.write("\n".join(values))
        out_data.close()
        writer = pd.ExcelWriter(out_file, engine="xlsxwriter", options={'strings_to_urls': False})
        data = pd.DataFrame({"时间段6-7": taskIds, "计算结果": values})
        data.to_csv("./count/all_values1.csv", index=False, header=True, quoting=0)
        print("文件开始写入")
        data.to_excel(writer, index=False)
        writer.save()
        print(out_file, "文件已经保存")


def readKafka2():
    print('consumer start to consuming...')
    consumer = KafkaConsumer(bootstrap_servers=conf['host'], group_id="3",
                             auto_offset_reset='earliest')  # earliest ,auto_offset_reset='latest'
    consumer.subscribe((conf['topic'],))
    count = 0

    for message in consumer:
        # print(message)
        if None == message.key:
            message_key = "No key"
            print(message.topic, message_key, message.value.decode('utf-8'))
        else:
            # topic = message.topic
            key = message.key.decode('utf-8')
            value = message.value.decode('utf-8')
            if "20191203111316" in key:
                print(value)
            if key == "fd-L:20191203111316:500050-21:ceshi62yq-consumer-group":
                print(value)
            count += 1
            if count % 200 == 0:
                print("计算次数", count)


# Testing for monitor kafka messages
def main():
    filePath = r"C:\Users\dell\Desktop\taskDir"
    out_file = "./count/taskID5.xls"
    out_txt = "./count/all_values1.txt"
    count, taskIDs, taskId_times = count_file_nums(filePath, None, None)
    readKafka(True, out_file, out_txt, taskId_times)

if __name__ == '__main__':
    readKafka2()
