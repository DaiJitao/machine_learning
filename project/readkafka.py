
from kafka import KafkaConsumer

#kafka配置
conf = {
    'host':['10.121.17.193:9092','10.121.17.194:9092','10.121.17.195:9092'],
    'topic': 'LabelTopic', # "PosNegTopic", #'LabelTopic',
    'groupid':'car-group',
    'max_request_size':52428800 #50M
}

def readKafka():
    print('consumer start to consuming...')
    consumer = KafkaConsumer( bootstrap_servers=conf['host'],  group_id=conf['groupid'], auto_offset_reset='earliest')#earliest ,auto_offset_reset='latest'
    consumer.subscribe((conf['topic'], ))
    for message in consumer:
        print(message)
        if None == message.key:
            message_key = "No key"
            print(message.topic,message_key,message.value.decode('utf-8'))
        else:
            print(message.topic,message.key.decode('utf-8'),message.value.decode('utf-8'))

#Testing for monitor kafka messages
if __name__ == '__main__':
    readKafka()