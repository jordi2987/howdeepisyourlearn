import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D

def build_unet(input_size=(256,256,3)):
    inputs = Input(input_size)
    # Encoder
    conv1 = Conv2D(64, 3, activation='relu', padding='same')(inputs)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    # Decoder
    up1 = UpSampling2D(size=(2, 2))(pool1)
    # Customize for Singapore food textures
    outputs = Conv2D(1, 1, activation='sigmoid')(up1)
    return tf.keras.Model(inputs=inputs, outputs=outputs)
