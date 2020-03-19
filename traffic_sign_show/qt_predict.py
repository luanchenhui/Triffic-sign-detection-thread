from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
import time

from keras.models import load_model
import cv2
from keras.preprocessing.image import img_to_array
import numpy as np
# import imutils
import cv2
from SiaCNN_brightness import build_model
from keras import Model
# from keras.models import Input
from keras.layers import Input, GlobalMaxPooling2D

# from predict import predict
"""
    Note:
        in the emit message, can't having ':'.
        
"""


class Predicter(QThread):
    sinOut = pyqtSignal(str) # 自定义信号，执行run()函数时，从相关线程发射此信号
    # model, branch_model = build_model(64e-5, 0)
    # model.load_weights(setting.model_path)
    # model.load_weights(setting.model_path_brightness)
    model, branch_model = build_model(64e-5, 0)
    # 定义特征提取网络模型
    feature_detection_model = Model(model.layers[2].layers[0].input,
                                    model.layers[2].layers[-2].output)
    # 定义最大池化模型
    input = Input(shape=(None, None, 32))
    GlobalMaxPooling = GlobalMaxPooling2D()(input)
    GlobalMaxPooling_model = Model(input, GlobalMaxPooling)

    # 定义距离计算模型
    distance_model = Model(model.layers[3].layers[0].input,
                           model.layers[3].layers[-1].output)

    def __init__(self, parent=None):
        super(Predicter, self).__init__(parent)
        self.image_path = ""
        self.working = True
        self.norm_size = 32

        # load the trained convolutional neural network
        # print("[INFO] loading network...")
        # self.model = load_model("ckpt/traffic_sign.model")

        self.num = 0

    def __del__(self):
        self.working = False
        self.wait()

    # def send_image_path(self, image_path):
    #     self.image_path = image_path

    def run(self):
        print('调用线程')
        self.sinOut.emit("R:正在分析中\n请稍后。。。\n")
        print('分析中')
        print(self.image_path)
        # response = self.predict(self.image_path, True)
        # response = self.predict(True)
        image = cv2.imread(self.image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        orig = image.copy()
        # pre-process the image for classification
        image = cv2.resize(image, (self.norm_size, self.norm_size))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print('图像处理完了，到这里没问题')

        # classify the input image
        # model = load_model("traffic_sign.model")
        model, branch_model = build_model(64e-5, 0)
        # 定义特征提取网络模型
        feature_detection_model = Model(model.layers[2].layers[0].input,
                                        model.layers[2].layers[-2].output)
        # 定义最大池化模型
        input = Input(shape=(None, None, 32))
        GlobalMaxPooling = GlobalMaxPooling2D()(input)
        GlobalMaxPooling_model = Model(input, GlobalMaxPooling)

        # 定义距离计算模型
        distance_model = Model(model.layers[3].layers[0].input,
                               model.layers[3].layers[-1].output)
        template_feature_maps = feature_detection_model.predict(image)
        template_fea = GlobalMaxPooling_model.predict(template_feature_maps)
        fea1 = distance_model.predict(template_fea)
        # #

        print('模型加载玩了，到这里没问题')
        result = distance_model.predict(template_fea)
        print('模型处理完了')
        print('get result')
        # print (result.shape)
        proba = np.max(result)
        label = str(np.where(result == proba)[0])
        label = "{}: {:.2f}%".format(label, proba * 100)
        print(label)

        if True:
            # draw the label on the image
            # output = imutils.resize(orig, width=400)
            cv2.putText(orig, label, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2)
            # save the output image
            cv2.imwrite("image/save.png", orig)

        response = label
        print('response:'+str(response))
        self.sinOut.emit("P:类型\t{}\n当前时间\t{}\n".format(response, time.localtime()))
        self.sinOut.emit("I:image/save.png")

    def predict(self, is_show):
        print('神经网预测')
        # model = load_model("traffic_sign.model")
        print('load model')
        # load the image

        image = cv2.imread(self.image_path)

        orig = image.copy()
        print('read image')

        # pre-process the image for classification
        image = cv2.resize(image, (self.norm_size, self.norm_size))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        print('process image')

        # classify the input image
        result = self.model.predict(image)[0]
        print('get result')
        # print (result.shape)
        proba = np.max(result)
        label = str(np.where(result == proba)[0])
        label = "{}: {:.2f}%".format(label, proba * 100)
        print(label)


        return label
