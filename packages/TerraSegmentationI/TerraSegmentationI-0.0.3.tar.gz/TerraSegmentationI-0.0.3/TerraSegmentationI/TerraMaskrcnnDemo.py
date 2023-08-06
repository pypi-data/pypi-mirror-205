import os
from os.path import exists, join, basename
import sys
import random
import math
import numpy as np
import skimage.io
import matplotlib
import matplotlib.pyplot as plt
import gdown
import json
from PIL import Image, ImageDraw
import cv2
import warnings
warnings.filterwarnings('ignore')

ROOT_DIR = os.path.abspath('Mask_RCNN')

sys.path.append(ROOT_DIR)
import mrcnn
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize

sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))

import coco


# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
# IMAGE_DIR = os.path.join(ROOT_DIR, "images")
class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
# config.display()
from keras.backend import manual_variable_initialization 
manual_variable_initialization(True)

# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO


import tensorflow.compat.v1 as tf
tf.keras.Model.load_weights(model.keras_model, COCO_MODEL_PATH, by_name=True)

class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']

# Загрузка и тестирование картинок
def load_detect_image(path):
  
  image = None
  if(path.startswith('http')):
    image_file = basename(path)
    gdown.download(path)
   
    image = skimage.io.imread(image_file)
   
  else:
    image = skimage.io.imread(path)
  results = model.detect([image], verbose=1)

# Visualize results
  r = results[0]
  visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                            class_names, r['scores'])
# для дообучения на своем датасете  
def get_classes_info(train_json_path):
  '''Получение информации о количестве классов
   и наименованиях категорий из файлов аннотаций
    '''
  json_file = open(train_json_path)
  coco_json = json.load(json_file)
  json_file.close()

  class_names = []
  class_ids = []
  
  for cat in coco_json['categories']:
    class_name = cat['name']
    if class_name not in class_names:
      class_names.append(class_name)
    class_id = cat['id']
    if class_id not in class_ids:
      class_ids.append(class_id)
  num_classes = len(class_ids)

  # Добавляем категорию "фон" на нулевую позицию
  class_names.insert(0,'BG')

  return class_names, num_classes

def get_custom_config(num_classes):
  class CustomConfig(coco.CocoConfig):
        """Configuration for training on the custom dataset.
        Derives from the base Config class and overrides values specific
        to the custom dataset.
        """
        # Give the configuration a recognizable name
        NAME = 'my_config'

        # Train on 1 GPU and 1 image per GPU. Batch size is 1 (GPUs * images/GPU).
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

        # Number of classes (including background)
        NUM_CLASSES = num_classes + 1 #  num_classes + background 

        # All of our training images are 512x512
        IMAGE_MIN_DIM = 512
      
        IMAGE_MAX_DIM = 512

      

        # You can experiment with this number to see if it improves training
        STEPS_PER_EPOCH = 100

        # This is how often validation is run. If you are using too much hard drive space
        # on saved models (in the MODEL_DIR), try making this value larger.
        VALIDATION_STEPS = 5
        
        # Matterport originally used resnet101
        BACKBONE = 'resnet50'

        # To be honest, I haven't taken the time to figure out what these do
        RPN_ANCHOR_SCALES = (8, 16, 32, 64, 128)
        TRAIN_ROIS_PER_IMAGE = 32
        MAX_GT_INSTANCES = 50 
        POST_NMS_ROIS_INFERENCE = 500 
        POST_NMS_ROIS_TRAINING = 1000 
  
  class TrainedConfig(CustomConfig):
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
        IMAGE_MIN_DIM = 512
        IMAGE_MAX_DIM = 512
        DETECTION_MIN_CONFIDENCE = 0.85
    

  inference_config = TrainedConfig()           
  custom_config = CustomConfig()
  # custom_config.display()
  
  return custom_config, inference_config 
  
    
  
class CocoLikeDataset(utils.Dataset):
    """ Generates a COCO-like dataset, i.e. an image dataset annotated in the style of the COCO dataset.
        See http://cocodataset.org/#home for more information.
    """
    def load_data(self, annotation_json, images_dir):
        """ Load the coco-like dataset from json
        Args:
            annotation_json: The path to the coco annotations json file
            images_dir: The directory holding the images referred to by the json file
        """
        # Load json from file
        json_file = open(annotation_json)
        coco_json = json.load(json_file)
        json_file.close()
        
        # Add the class names using the base method from utils.Dataset
        source_name = "coco_like"
        for category in coco_json['categories']:
            class_id = category['id']
            class_name = category['name']
            # if class_id < 1:
                # print('Error: Class id for "{}" cannot be less than one. (0 is reserved for the background)'.format(class_name))
                # return
            
            self.add_class(source_name, class_id, class_name)
        
        # Get all annotations
        annotations = {}
        for annotation in coco_json['annotations']:
            image_id = annotation['image_id']
            if image_id not in annotations:
                annotations[image_id] = []
            annotations[image_id].append(annotation)
        
        # Get all images and add them to the dataset
        seen_images = {}
        for image in coco_json['images']:
            image_id = image['id']
            if image_id in seen_images:
                print("Warning: Skipping duplicate image id: {}".format(image))
            else:
                seen_images[image_id] = image
                try:
                    image_file_name = image['file_name']
                    image_width = image['width']
                    image_height = image['height']
                except KeyError as key:
                    print("Warning: Skipping image (id: {}) with missing key: {}".format(image_id, key))
                
                image_path = os.path.abspath(os.path.join(images_dir, image_file_name))
                image_annotations = annotations[image_id]

                # Add the image using the base method from utils.Dataset
                self.add_image(
                    source=source_name,
                    image_id=image_id,
                    path=image_path,
                    width=image_width,
                    height=image_height,
                    annotations=image_annotations
                )
                
    def load_mask(self, image_id):
        """ Load instance masks for the given image.
        MaskRCNN expects masks in the form of a bitmap [height, width, instances].
        Args:
            image_id: The id of the image to load masks for
        Returns:
            masks: A bool array of shape [height, width, instance count] with
                one mask per instance.
            class_ids: a 1D array of class IDs of the instance masks.
        """
        image_info = self.image_info[image_id]
        annotations = image_info['annotations']
        instance_masks = []
        class_ids = []
        
        for annotation in annotations:
            class_id = annotation['category_id']
            mask = Image.new('1', (image_info['width'], image_info['height']))
            mask_draw = ImageDraw.ImageDraw(mask, '1')
            for segmentation in annotation['segmentation']:
                mask_draw.polygon(segmentation, fill=1)
                bool_array = np.array(mask) > 0
                instance_masks.append(bool_array)
                class_ids.append(class_id)

        mask = np.dstack(instance_masks)
        class_ids = np.array(class_ids, dtype=np.int32)
        
        return mask, class_ids

def create_dataset(train_path, train_json_path, val_path, val_json_path):
  ''' Получение тренировочной и 
  валидационной выборки для обучения 
  '''
  dataset_train = CocoLikeDataset()
  dataset_train.load_data(train_json_path, train_path)
  dataset_train.prepare()

  dataset_val = CocoLikeDataset()
  dataset_val.load_data(val_json_path, val_path)
  dataset_val.prepare()
  
  return dataset_train, dataset_val

def visualize_samples(dataset):
  ''' Визуализация случайных изображений 
  и масок
  '''
  image_ids = np.random.choice(dataset.image_ids, 4)
  for image_id in image_ids:
    image = dataset.load_image(image_id)
    mask, class_ids = dataset.load_mask(image_id)
    visualize.display_top_masks(image, mask, class_ids, dataset.class_names)

def get_model_for_train(custom_config):
  '''построение модели для обучения
  и загрузка весов '''

  from keras.backend import manual_variable_initialization 
  manual_variable_initialization(False)
  model = mrcnn.model.MaskRCNN(mode='training', 
                              model_dir=MODEL_DIR, 
                              config=custom_config)



  import tensorflow.compat.v1 as tf
  tf.keras.Model.load_weights(model.keras_model, filepath=COCO_MODEL_PATH, 
                    by_name=True, skip_mismatch=True)
  return model

def get_trained_model(custom_config,dataset_train, dataset_val, epochs=1, layers='heads'):
  '''обучение модели '''

  trained_model = get_model_for_train(custom_config)
  trained_model.train(dataset_train, dataset_val, learning_rate=config.LEARNING_RATE, epochs=epochs, layers=layers)
  return trained_model

def model_for_test(model_dir, weights_dir, inference_config):
  
  from keras.backend import manual_variable_initialization 
  manual_variable_initialization(True)
  model = mrcnn.model.MaskRCNN(mode='inference', model_dir=model_dir, config= inference_config)
  

  # Load the weights into the model.
  import tensorflow.compat.v1 as tf
  tf.keras.Model.load_weights(model.keras_model, filepath=weights_dir, 
                    by_name=True)
  return model

def test_image(trained_model,path, inference_config, CLASS_NAMES):
  model = model_for_test(COCO_MODEL_PATH, trained_model.find_last(), inference_config)
  image = None
  if(path.startswith('http')):
    image_file = basename(path)
    gdown.download(path)
   
    image = skimage.io.imread(image_file)
   
  else:
    image = skimage.io.imread(path)
  results = model.detect([image], verbose=1)

# Visualize results
  r = results[0]
  visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                            CLASS_NAMES, r['scores'])
   
  
