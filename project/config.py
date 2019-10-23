
fasttext_model_1 = "/data/appRun/CarClassifyService/model/car_classify_model_1.bin"
fasttext_model_2 = "/data/appRun/CarClassifyService/model/car_classify_model_2.bin"

#实时预测-配置各个路径的位置
result_path = "/data/appRun/CarClassifyService/data/result/" #预测结果
log_path = "/data/appRun/CarClassifyService/data/log/" #log文件；格式或数据错误的新闻消息记录-error.txt,预测正常的新闻消息记录-result.txt
threshold_1labelsPro = 0.60 #一级分类（是汽车）隶属概率
threshold_mlabelsPro = 0.15 #多标签分类隶属概率
threshold_contentSize = 10 #有效文本（title+content）字数阈值，字数过少的默认为“非汽车”

#停用词
stopWords_path = "/data/appRun/CarClassifyService/data/StopWords.txt"
stopwords = {}.fromkeys([line.rstrip() for line in open(stopWords_path,'rb')])

#汽车品牌
carBrands_path = "/data/appRun/CarClassifyService/data/CarBrands.txt" #汽车品牌文件-（329个）
carBrands = {}.fromkeys([line.rstrip() for line in open(carBrands_path,'rb')])

#hdfs监控目录
hdfs_dir = "hdfs://amend/classify/taskDir"

#spark资源配置
monitoring_cycle_time = 1   #spark 监控hdfs周期
standalone = 'spark://10.121.17.198:7077'
spark_cores_max = 24
spark_executor_cores = 8
spark_executor_memory = "8g"
spark_default_parallelism = 100
spark_shuffle_consolidateFiles = "true"
spark_shuffle_file_buffer = "128k"
spark_shuffle_memoryFraction = 0.7
appName = "news_classify_spark"

#kafka配置
conf = {
    'host':['10.121.17.193:9092','10.121.17.194:9092','10.121.17.195:9092'],
    'topic':'LabelTopic',
    'groupid':'car-group',
    'max_request_size':52428800 #50M
}