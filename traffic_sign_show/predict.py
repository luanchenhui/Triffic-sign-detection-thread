# import the necessary packages
from keras.preprocessing.image import img_to_array
import numpy as np
# import imutils
import cv2

from keras.models import load_model

norm_size = 32

"""
    Note:
   .h5 it include net_model and weights. 
"""
model = load_model("traffic_sign.model")


def predict(image_path, is_show, model=model):
    print('神经网预测')

    model = load_model("traffic_sign.model")
    print('load model')
    #load the image

    image = cv2.imread(image_path)

    orig = image.copy()
    print('read image')
     
    # pre-process the image for classification
    image = cv2.resize(image, (norm_size, norm_size))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    print('process image')

    # classify the input image
    result = model.predict(image)[0]
    print('get result')
    #print (result.shape)
    proba = np.max(result)
    label = str(np.where(result==proba)[0])
    label = "{}: {:.2f}%".format(label, proba * 100)
    print(label)
    
    if is_show:
        # draw the label on the image
        # output = imutils.resize(orig, width=400)
        cv2.putText(output, label, (10, 25),cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (0, 255, 0), 2)
        # save the output image
        cv2.imwrite("image/save.png", output)

    return label


# change the init_parameter
# if __name__ == '__main__':
#     model_path, image_path, is_show = init_parameter()
#     predict(model_path, image_path, is_show)
