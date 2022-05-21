# Where's Wally 
## _solving Where's Wally puzzles with Tensorflow Object Detection_

![wally-gif](https://github.com/samuelFain/Wheres_Wally/blob/master/wally-cut.gif)

This is a Tensorflow project that includes a model for solving Where's Wally puzzles. It uses Faster RCNN Inception v2 model initially trained on COCO dataset and retrained for finding Wally using transfer learning with Tensorflow Object Detection API.

## Project Description
Using Tensorflow Object Detection API and using a Python script built around it we will be able to find Wally in a photo. It consists of the following steps:

- Preparing the Dataset by creating a set of labelled training images where labels represent x y locations of Wally in an image.
- Fetching and configuring the model to use with Tensorflow Object Detection API.
- Training the model on our dataset.
- Testing the model on evaluation images using an exported graph.

## Plan VS Execution
### Preparing the Dataset
Plan:
Create a training set containing labeled images, with specified locations of Wally in them
![Picture1](https://user-images.githubusercontent.com/65926551/149316646-06f64a85-5bbf-4467-bb98-2251e8f45d38.png)

Execution:
Instead of solving Wally puzzles by hand (which would take a very long time), we used an already solved training set of Where’s Wally puzzles. 
(can be found in ‘Tools’ slide)

### Preparing the Model
Plan:
Use pre-trained TensorFlow model, and configure it for our Dataset


Execution:
TensorFlow provides a set of pre trained models with different performances.
For this project we used a ‘transfer learning’ technique.It involves taking a model usually trained to solve some general problem and retraining it to solve ours. We used the knowledge obtained in the pre trained model and transferred it out to a new one. 

We used the Faster RCNN with Inception v2 model trained on the COCO dataset along with it’s pipeline configuration file. Target labels & Target data refer to the dataset we prepared in the previous step.The result will be a Target model that would be ready to be retrained in the next step.


![Picture1](https://user-images.githubusercontent.com/65926551/149317530-31e934e5-e4ae-46bb-a1a4-06f6597f47f1.png)


### Training
Plane:
Tensorflow Object Detection API provides a simple-to-use Python script to retrain our model locally.

Execution:
Using ‘train.py’ script from Tensorflow object detection API (located in models/research/object_detection) with parameters from our pipeline configuration file into a newly created directory where our new checkpoints and retrained model will be stored.
We stopped the training when the loss on our evaluation stopped decreasing (below 0.01).
Input (Linux terminal):
python train.py --logtostderr --pipeline_config_path= PATH_TO_PIPELINE_CONFIG 
--train_dir=PATH_TO_TRAIN_DIR

![Picture1](https://user-images.githubusercontent.com/65926551/149317328-4b555600-fd6e-4317-b7d9-a31c37a82ad2.png)




## Project Output
Using Python script (based on Tensorflow Object Detection API) we performed object detection on our photos using the re-trained model.

![Picture1](https://user-images.githubusercontent.com/65926551/149313527-cd03014e-2540-41d7-a311-f2b17653d409.png)

## Conclusions
- Overall, the model managed to find Wally in the evaluation images in a few seconds and in good accuracy (above 85%).
- Overfitting: the model failed to find Wally where he was really large, which by intuition should be even easier to solve as opposed to finding him where his really small. This indicates that our model probably overfit our training data mostly as a result of using a small and not diverse number of training images.
- Increasing number of epochs will not improve the model accuracy – from the point where the loss was under 0.01 extra epochs did not make a significant difference in accuracy.
- Opposed to using google collab, using a local machine with a GPU has its benefits when it comes to reliability and convenience. Working with files and Linux terminal was simpler and we were able to leave the machine running for a few hours while training the model without dependency on internet connection.

## Possible Improvements
- Training the network on more examples – expose the model to large verity of puzzles, including different sizes of Wally in both complex and simple puzzles.
- Change the network complexity by changing the network parameters (values of weights). The parameters (weights) will remain small because they ensure a more stable model that is less sensitive to statistical fluctuations in the input data (Large weighs tend to cause sharp transitions in the activation functions and thus large changes in output for small changes in inputs).
- One possible interesting improvement would be to train the model to find Wally in grayscale puzzles as well. This would be possible by changing the dataset to grayscale and retrain the model again.

## Tools
- TensorFlow Object Detection API  
https://github.com/tensorflow/models/tree/master/research/object_detection
- “Hey Waldo” – git repo of Wally images  
https://github.com/vc1492a/Hey-Waldo
- PyCharm – python IDE
- Python version –  3.7
- Machine System – Ubuntu 20.4  (Linux)  
- Pipenv – package & virtual environment manager

## Libraries
- matplotlib
- numpy
- TensorFlow – TensorFlow API
- object_detection - TensorFlow Object Detection API (Tensorflow 2.x)
- PIL - Python Imaging Library
- Tkinter – Python GUI library

## Bibliography

- “How to Find Wally with a Neural Network"  
https://towardsdatascience.com/how-to-find-wally-neural-network-eddbb20b0b90
- TensorFlow Object Detection API Documentation  
https://www.tensorflow.org/api_docs 
- TensorFlow installation with pip  
https://www.tensorflow.org/install/pip
- Transfer learning and fine-tuning  
https://www.tensorflow.org/tutorials/images/transfer_learning
- Graphical User Interfaces with Tk  
https://docs.python.org/3/library/tk.html








