from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import font, messagebox
from playsound import playsound
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import numpy as np
import sys
import tensorflow as tf
import matplotlib
from PIL import Image
import matplotlib.patches as patches
import argparse

matplotlib.use("TkAgg")

model_path = './trained_model/frozen_inference_graph.pb'


def draw_box(box, image_np):
    # expand the box by 50%
    box += np.array([-(box[2] - box[0]) / 2, -(box[3] - box[1]) / 2, (box[2] - box[0]) / 2, (box[3] - box[1]) / 2])

    fig = plt.figure(figsize=(10, 10))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    fig.add_axes(ax)

    # draw blurred boxes around box
    ax.add_patch(patches.Rectangle((0, 0), box[1] * image_np.shape[1], image_np.shape[0], linewidth=0, edgecolor='none',
                                   facecolor='w', alpha=0.8))
    ax.add_patch(patches.Rectangle((box[3] * image_np.shape[1], 0), image_np.shape[1], image_np.shape[0], linewidth=0,
                                   edgecolor='none', facecolor='w', alpha=0.8))
    ax.add_patch(patches.Rectangle((box[1] * image_np.shape[1], 0), (box[3] - box[1]) * image_np.shape[1],
                                   box[0] * image_np.shape[0], linewidth=0, edgecolor='none', facecolor='w', alpha=0.8))
    ax.add_patch(patches.Rectangle((box[1] * image_np.shape[1], box[2] * image_np.shape[0]),
                                   (box[3] - box[1]) * image_np.shape[1], image_np.shape[0], linewidth=0,
                                   edgecolor='none', facecolor='w', alpha=0.8))

    return fig, ax


detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with tf.io.gfile.GFile(model_path, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


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
            sys.exit('Wally not found :(')


        def close_window():
            sys.exit()


        print('Wally found')
        playsound('sounds/found_wally_yay.mp3', False)
        window = tk.Tk()
        window.title("Result")
        window.geometry("1000x1100")
        window.configure(background="white")

        fig, ax = draw_box(boxes[0][0], image_np)
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        plt.gca().set_axis_off()
        myFont = font.Font(family="Helvatica")
        button = tk.Button(text='Close Window', bg="#FA8072", width="10", height="1", command=close_window)
        button['font'] = myFont
        button.pack()
        ax.imshow(image_np)
        window.mainloop()
        plt.show()
