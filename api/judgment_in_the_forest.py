from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import numpy as np
import tensorflow as tf
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
# tf.disable_resource_variables()

# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3
# tf.logging.set_verbosity(tf.logging.WARN)

# import warnings
# warnings.filterwarnings('ignore')

import os
# import tensorflow as tf
import logging
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=Warning)
tf.get_logger().setLevel('INFO')
tf.autograph.set_verbosity(0)
tf.get_logger().setLevel(logging.ERROR)


def load_graph(model_file):
  graph = tf.Graph()
  graph_def = tf.GraphDef()

  with open(model_file, "rb") as f:
    graph_def.ParseFromString(f.read())
  with graph.as_default():
    tf.import_graph_def(graph_def)

  return graph


def read_tensor_from_image_file(file_name,
                                input_height=299,
                                input_width=299,
                                input_mean=0,
                                input_std=255):
  input_name = "file_reader"
  output_name = "normalized"
  file_reader = tf.read_file(file_name, input_name)
  if file_name.endswith(".png"):
    image_reader = tf.image.decode_png(file_reader, channels=3, name="png_reader")
  elif file_name.endswith(".gif"):
    image_reader = tf.squeeze(tf.image.decode_gif(file_reader, name="gif_reader"))
  elif file_name.endswith(".bmp"):
    image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
  else:
    image_reader = tf.image.decode_jpeg(file_reader, channels=3, name="jpeg_reader")
  float_caster = tf.cast(image_reader, tf.float32)
  dims_expander = tf.expand_dims(float_caster, 0)
  resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
  normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
  # sess = tf.compat.v1.Session()
  
  sess = tf.Session()
  result = sess.run(normalized)

  return result


def load_labels(label_file):
  label = []
  proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
  for l in proto_as_ascii_lines:
    label.append(l.rstrip())
  return label


def label_image(model_file, file_name, label_file,input_height, input_width,input_mean, input_std, input_layer, output_layer):
  graph = load_graph(model_file)
  t = read_tensor_from_image_file(
      file_name,
      input_height=input_height,
      input_width=input_width,
      input_mean=input_mean,
      input_std=input_std)

  input_name = "import/" + input_layer
  output_name = "import/" + output_layer
  input_operation = graph.get_operation_by_name(input_name)
  output_operation = graph.get_operation_by_name(output_name)

  with tf.Session(graph=graph) as sess:
    results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: t
    })
  results = np.squeeze(results)
  top_k = results.argsort()[-5:][::-1]
  labels = load_labels(label_file)

  max_ratio = 0
  max_label = ''
  for i in top_k:
    if max_ratio <= results[i]:
      max_ratio = results[i]
      max_label = labels[i]
  return {"max_label": max_label, "max_ratio": max_ratio}

def judgment_in_the_forest(file_name):
  model_file = "model/output_graph.pb"
  label_file = "model/output_labels.txt"
  input_layer = "Placeholder"
  output_layer = "final_result"
  input_height = 299
  input_width = 299
  input_mean = 0
  input_std = 255

  result = label_image(
    model_file,
    file_name,
    label_file,
    input_height,
    input_width,
    input_mean,
    input_std,
    input_layer,
    output_layer)
  return result


if __name__ == "__main__":
  file_name = "/root/img/not_forest/45-1859073_141-1391882_20.png"
  parser = argparse.ArgumentParser()
  parser.add_argument("--image", help="image to be processed")
  args = parser.parse_args()
  if args.image:
    file_name = args.image
  
  result = judgment_in_the_forest(file_name)
  print(result)
