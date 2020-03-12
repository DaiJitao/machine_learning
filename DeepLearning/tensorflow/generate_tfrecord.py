import glob
import io
import os
import tensorflow as tf

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

