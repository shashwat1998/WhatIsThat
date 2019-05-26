
import numpy as np
from keras.applications import vgg16, inception_v3, resnet50, mobilenet
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import decode_predictions
import matplotlib.pyplot as plt

#vgg_model = vgg16.VGG16(weights='imagenet')
print("ready")


def classify(file_name):
    filename = 'images/'+file_name
    # load an image in PIL format
    original = load_img(filename, target_size=(224, 224))
    print('PIL image size', original.size)
    plt.imshow(original)
    plt.show()

    # convert the PIL image to a numpy array
    # IN PIL - image is in (width, height, channel)
    # In Numpy - image is in (height, width, channel)
    numpy_image = img_to_array(original)
    plt.imshow(np.uint8(numpy_image))
    plt.show()
    print('numpy array size', numpy_image.shape)

    # Convert the image / images into batch format
    # expand_dims will add an extra dimension to the data at a particular axis
    # We want the input matrix to the network to be of the form (batchsize, height, width, channels)
    # Thus we add the extra dimension to the axis 0.
    image_batch = np.expand_dims(numpy_image, axis=0)
    print('image batch size', image_batch.shape)
    plt.imshow(np.uint8(image_batch[0]))

    # prepare the image for the VGG model
    processed_image = vgg16.preprocess_input(image_batch.copy())

    # get the predicted probabilities for each class
    # predictions = vgg_model.predict(processed_image)
    # print predictions

    # convert the probabilities to class labels
    # We will get top 5 predictions which is the default
    # label = decode_predictions(predictions)
    l = [[('n02124075', 'Egyptian_cat', 0.84743756), ('n02441942', 'weasel', 0.035382476),
          ('n02123045', 'tabby', 0.031043062), ('n02123159', 'tiger_cat', 0.017164368),
          ('n02443484', 'black-footed_ferret', 0.015669418)]]
    list_result = l[0]
    return list_result


if __name__ == '__main__':

    classify()