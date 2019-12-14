#!/usr/bin/python3
# Image Recognition Using Tensorflow Exmaple.
# Code based on example at:
# https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/examples/label_image/label_image.py
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import numpy as np
import threading
import queue
import time
import sys
import pdb

# sudo apt install python3-pip
# sudo python3 -m pip install --upgrade pip
# sudo python3 -m pip install --upgrade setuptools
# sudo python3 -m pip install --upgrade tensorflow==1.15

def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label

def predict_image(q, sess, graph, image_bytes, uuid, labels, input_operation, output_operation):
    image = read_tensor_from_image_bytes(image_bytes)
    results = sess.run(output_operation.outputs[0], {
        input_operation.outputs[0]: image
    })
    results = np.squeeze(results)
    prediction = results.argsort()[-5:][::-1][0]
    q.put( {'uuid':uuid, 'prediction':labels[prediction].title(), 'percent':results[prediction]} )

def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()
    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)
    return graph

def read_tensor_from_image_bytes(imagebytes, input_height=299, input_width=299, input_mean=0, input_std=255):
    image_reader = tf.image.decode_png( imagebytes, channels=3, name="png_reader")
    float_caster = tf.cast(image_reader, tf.float32)
    dims_expander = tf.expand_dims(float_caster, 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    sess = tf.compat.v1.Session()
    result = sess.run(normalized)
    return result

def main(image_list):
    # Loading the Trained Machine Learning Model created from running retrain.py on the training_images directory
    graph = load_graph('./output/output_graph.pb')
    labels = load_labels("./output/output_labels.txt")

    # Load up our session
    input_operation = graph.get_operation_by_name("import/Placeholder")
    output_operation = graph.get_operation_by_name("import/final_result")
    sess = tf.compat.v1.Session(graph=graph)

    # Can use queues and threading to spead up the processing
    q = queue.Queue()
    #unknown_images_dir = 'test_images'
    #unknown_images = os.listdir(unknown_images_dir)
    
    one = time.time()
    #Going to interate over each of our images.
    #for image in unknown_images:
    for uuid,image in image_list:
        #img_full_path = '{}/{}'.format(unknown_images_dir, image)
        
        #print('Processing Image {}'.format(img_full_path))
        # We don't want to process too many images at once. 10 threads max
        # while len(threading.enumerate()) > 10:
        #    time.sleep(0.0001)

        #predict_image function is expecting png image bytes so we read image as 'rb' to get a bytes object
        #image_bytes = open(img_full_path,'rb').read()
        #threading.Thread(target=predict_image, args=(q, sess, graph, image_bytes, img_full_path, labels, input_operation, output_operation)).start()
        threading.Thread(target=predict_image, args=(q, sess, graph, image, uuid, labels, input_operation, output_operation)).start()

    two = time.time()
    print(f"Loaded all threads, took {two - one} seconds..")
    print('Waiting For Threads to Finish...')
    while q.qsize() < len(image_list):
        time.sleep(0.0001)
    three = time.time()
    print(f"Thread finished, took {three - two} more seconds..")
    #getting a list of all threads returned results
    prediction_results = [q.get() for x in range(q.qsize())]
    #pdb.set_trace()
    print(f"Giving results to interact.py after {time.time() - three} more seconds")
    return prediction_results

if __name__ == "__main__":
    print("Intented to run as module!")
    sys.exit(1)