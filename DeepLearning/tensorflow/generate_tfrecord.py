import glob
import io
import os
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image

flags = tf.app.flags
flags.DEFINE_string('images_path', None, 'Path to images (directory).')
flags.DEFINE_string('output_path', None, 'Path to output tfrecord file.')
FLAGS = flags.FLAGS


def int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def int64_list_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def bytes_list_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))


def float_list_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

'''demo2'''

def write_test1(input, output):
    writer = tf.python_io.TFRecordWriter(output)
    # read picture and encode it
    image = tf.read_file(input)
    image = tf.image.decode_jpeg(image)

    with tf.Session() as sess:
        image = sess.run(image)
        shape = image.shape
        print("image shape: ", shape)
        # convert iamge to string
        image_data = image.tostring()
        print("image to String: ", len(image_data), type(image_data))
        name = bytes("cat", encoding='utf-8')
        print(type(name))
        feature = {
            'name': tf.train.Feature(bytes_list=tf.train.BytesList(value=[name])),
            'shape': tf.train.Feature(int64_list=tf.train.Int64List(value=[shape[0], shape[1], shape[2]])),
            'data': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_data]))
        }
        example = tf.train.Example(
            features=tf.train.Features(feature=feature)
        )
        # 将example序列化成string 类型，然后写入。
        writer.write(example.SerializeToString())
    writer.close()

def _parse_record(example_proto):
    features = {
        'name':tf.FixedLenFeature((), tf.string),
        'shape':tf.FixedLenFeature([3], tf.int64),
        'data': tf.FixedLenFeature((), tf.string)
    }
    parsed_features = tf.parse_single_example(example_proto, features=features)
    return parsed_features

def read_test1(input_file):
    # tf versions >= 1.4.0
    # dataset = tf.data.TFRecordDataset(input_file)
    # tf version=1.3.0
    dataset = tf.contrib.data.TFRecordDataset(input_file)
    dataset = dataset.map(_parse_record)
    iterator = dataset.make_one_shot_iterator()

    with tf.Session() as sess:
        features = sess.run(iterator.get_next())
        name = features['name']
        name = name.decode()
        img_data = features['data']
        shape = features['shape']
        print("==============")
        print(type(shape))
        print(len(img_data))

        # 从bytes数组中加载图片原始数据，并重新reshape，它的结果是 ndarray 数组
        img_data = np.fromstring(img_data, dtype=np.uint8)

        image_data = np.reshape(img_data, shape)
        for i in range(738):
            for j in range(500):
                image_data[i][j][1]=243
        print(image_data)
        print(shape)

        plt.figure()
        # 显示图片
        plt.imshow(image_data)
        plt.show()

        # 将数据重新编码成jpg图片并保存
        img = tf.image.encode_jpeg(image_data)
        tf.gfile.GFile('cat_encode.jpg', 'wb').write(img.eval())



def demo1():
    input_photo = r'F:\data\zhang.jpg'
    out_file = r"F:\data\zhang.tfrecord"
    # write_test1(input=input_photo, output=out_file)
    read_test1(input_file=out_file)


'''end demo2'''

if __name__ == '__main__':
    demo1()