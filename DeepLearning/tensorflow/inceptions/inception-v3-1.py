import os
import tarfile # unzip tar file lib
import tensorflow as tf


'''图结构保存'''
def save_graph_structure():
    # model dir
    model_dir = r"F:\data\inception_model"
    # model structure dir
    model_log = "F:/data/inception_v3/log"

    if not os.path.exists(model_log):
        os.makedirs(model_log)

    if model_dir.endswith("/"):
        model = model_dir + 'classify_image_graph_def.pb'
    else:
        model = model_dir + '/classify_image_graph_def.pb'

    with tf.Session() as sess:
        # 创建一个图来存放google训练好的模型
        with tf.gfile.FastGFile(model, "rb") as f:
            graph_def = tf.GraphDef() # # 生成图
            graph_def.ParseFromString(f.read()) # # 图加载模型
            tf.import_graph_def(graph_def, name='') #将图从graph_def导入到当前默认图中. (即将舍弃的参数)
        # 保存图结构
        writer = tf.summary.FileWriter(model_log, sess.graph)
        writer.close()

    print("图结构已经保存!" + model_log)

if __name__ == '__main__':
    file = tf.gfile.FastGFile(r"G:\douyin_tb.sql", "r")
    # print(file.read())
    print(file.readlines())