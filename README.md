# Where's Wally 
## _solving Where's Wally puzzles with Tensorflow Object Detection_

This is a Tensorflow project that includes a model for solving Where's Wally puzzles. It uses Faster RCNN Inception v2 model initially trained on COCO dataset and retrained for finding Wally using transfer learning with Tensorflow Object Detection API.

## Project Description
Using Tensorflow Object Detection API and using a Python script built around it we will be able to find Wally in a photo. It consists of the following steps:

- Preparing the Dataset by creating a set of labelled training images where labels represent x y locations of Wally in an image.
- Fetching and configuring the model to use with Tensorflow Object Detection API.
- Training the model on our dataset.
- Testing the model on evaluation images using an exported graph.

## Project Output

