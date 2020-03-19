# loss function
import keras.backend as K

def contrastive_loss(y_true, y_pred):
    '''Contrastive loss from Hadsell-et-al.'06
    http://yann.lecun.com/exdb/publis/pdf/hadsell-chopra-lecun-06.pdf
    '''
    margin = 2
    sqaure_pred = K.square(y_pred)
    margin_square = K.square(K.maximum(margin - y_pred, 0))
    return K.mean((1-y_true) * sqaure_pred + (y_true) * margin_square)


from keras import regularizers
from keras.optimizers import Adam, RMSprop
from keras.engine.topology import Input
from keras.layers import Activation, Add, BatchNormalization, Concatenate, \
    Conv2D, Dense, Flatten, GlobalMaxPooling2D, Lambda, MaxPooling2D, Reshape, Dropout
from keras.models import Model, Sequential
import keras.backend as K

# from contrastiveLoss import *
'''
更改模型，在scnn1网络基础上，更改头网络，更改为论文中使用的相似度度量l2范数；
'''
img_shape = (None, None, 1)
kernel_size = (3, 3)
pool_size = (2, 2)
epochs = 20
batch_size = 256
nb_filters = 32
img_rows, img_cols = 100, 100
if K.image_data_format() == 'channels_first':
    shape_ord = (1, img_rows, img_cols)
else:
    shape_ord = (img_rows, img_cols, 1)


def euclidean_distance(vects):
    x, y = vects
    sum_square = K.sum(K.square(x - y), axis=1, keepdims=True)
    return K.sqrt(K.maximum(sum_square, K.epsilon()))


def eucl_dist_output_shape(shapes):
    shape1, shape2 = shapes
    return (shape1[0], 1)


def accuracy(y_true, y_pred):
    '''Compute classification accuracy with a fixed threshold on distances.
    '''
    return K.mean(K.equal(y_true, K.cast(y_pred > 0.5, y_true.dtype)))


def subblock(x, filter, **kwargs):
    # x = BatchNormalization()(x)
    y = x
    # reduce the number of features to 'filter'
    y = Conv2D(filter, (1, 1), activation='relu', **kwargs)(y)
    # y = BatchNormalization()(y)
    # extend the feature field
    y = Conv2D(filter, (3, 3), activation='relu', **kwargs)(y)
    # y = BatchNormalization()(y)
    # no activation # restore the number of original features
    y = Conv2D(K.int_shape(x)[-1], (1, 1), **kwargs)(y)
    # add the bypass connection
    y = Add()([x, y])
    y = Activation('relu')(y)
    return y


def build_model(lr, l2, activation='sigmoid'):
    ############
    # Branch Model
    ############
    regul = regularizers.l2(l2)
    optim = Adam(lr=lr)
    kwargs = {'padding': 'same', 'kernel_regularizer': regul}

    inp = Input(shape=img_shape)  # (64, 64, 3)
    x = Conv2D(32, (3, 3), strides=1, activation='relu', **kwargs)(inp)
    for _ in range(2):
        # x = BatchNormalization()(x)
        x = Conv2D(16, (3, 3), activation='relu', **kwargs)(x)

    x = MaxPooling2D((2, 2), strides=(2, 2))(x)  # 48x48x64
    # x = BatchNormalization()(x)

    for _ in range(2):
        x = Conv2D(32, (3, 3), activation='relu', **kwargs)(x)  # 48x48x128
        x = subblock(x, 32, **kwargs)

    # x = MaxPooling2D((2, 2), strides=(2, 2))(x)  # 24x24x128
    # x = BatchNormalization()(x)
    # x = Conv2D(256, (1, 1), activation='relu', **kwargs)(x)  # 24x24x256
    # for _ in range(4): x = subblock(x, 64, **kwargs)

    x = GlobalMaxPooling2D()(x)  # 512
    # x = Flatten(name='Flatten')(x)

    branch_model = Model(inp, x)

    ########################
    # HEAD MODEL
    ########################

    inp_h = Input(shape=branch_model.output_shape[1:])
    x = Dropout(0.5, name='Drop1')(inp_h)
    x = Dense(128, name='Dense1')(x)
    x = Dropout(0.5, name='Drop2')(x)
    x = Dense(32, name='Dense2')(x)
    head_model = Model(inp_h, x)

    ########################
    # SIAMESE NEURAL NETWORK
    ########################

    # Complete model is constructed by calling the branch model on each input image,
    # and then the head model on the resulting 512-vectors.
    img_a = Input(shape=img_shape)
    img_b = Input(shape=img_shape)
    xa = branch_model(img_a)
    xb = branch_model(img_b)
    ha = head_model(xa)
    hb = head_model(xb)
    distance = Lambda(euclidean_distance,
                      output_shape=eucl_dist_output_shape)([ha, hb])

    model = Model([img_a, img_b], distance)
    model.compile(loss=contrastive_loss, optimizer=optim, metrics=[accuracy, 'mae'])
    return model, branch_model

if __name__ == '__main__':
    model, branch_model = build_model(64e-5, 0)

