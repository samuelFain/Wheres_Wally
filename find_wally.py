import tkinter as tk
from tkinter import font, messagebox
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["AUTOGRAPH_VERBOSITY"] = "0"
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pygame import mixer
from matplotlib import pyplot as plt
import numpy as np
import sys
import tensorflow as tf
import matplotlib
from PIL import Image
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import argparse

matplotlib.use("TkAgg")
tf.get_logger().setLevel("WARNING")

from object_detection.utils import ops as utils_ops

utils_ops.tf = tf.compat.v1
tf.gfile = tf.io.gfile

mixer.init()
model_path = './trained_model/frozen_inference_graph.pb'

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.compat.v2.io.gfile.GFile(model_path, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


label_map = label_map_util.load_labelmap('./trained_model/labels.txt')
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=1, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

with detection_graph.as_default():
    with tf.compat.v1.Session(graph=detection_graph) as sess:
        parser = argparse.ArgumentParser()
        parser.add_argument('image_path')
        args = parser.parse_args()
        image_np = load_image_into_numpy_array(Image.open(args.image_path))
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        scores = detection_graph.get_tensor_by_name('detection_scores:0')
        classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        # Actual detection.
        (boxes, scores, classes, num_detections) = sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: np.expand_dims(image_np, axis=0)})

        if scores[0][0] < 0.1:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Not found", "Wally not found :(")
            sys.exit()

        print('Wally found')
        mixer.music.load('sounds/found_wally_yay.mp3')
        mixer.music.play()

        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8)


        def close_window():
            sys.exit()


        window = tk.Tk()
        window.title("Result")
        window.geometry("1400x1200")
        window.configure(background="white")
        figure = plt.figure(figsize=(14, 11))
        plt.imshow(image_np, aspect='auto')
        canvas = FigureCanvasTkAgg(figure, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        plt.margins(0, 0)
        plt.gca().set_axis_off()
        myFont = font.Font(family="Helvatica")
        button = tk.Button(text='Close Window', bg="#FA8072", width="10", height="1", command=close_window)
        button['font'] = myFont
        button.pack()
        window.mainloop()
        plt.show()
        sys.exit()
