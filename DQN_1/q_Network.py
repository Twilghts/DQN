import tensorflow as tf


class QFunc(tf.keras.Model):
    def __init__(self, name):
        super(QFunc, self).__init__(name=name)
        self.conv1 = tf.keras.layers.Conv2D(
            32, kernel_size=(8, 8), strides=(4, 4),
            padding="valid", activation='relu'
        )
        self.conv2 = tf.keras.layers.Conv2D(
            64, kernel_size=(4, 4), strides=(2, 2),
            padding="valid", activation='relu'
        )
        self.conv3 = tf.keras.layers.Conv2D(
            64, kernel_size=(3, 3), strides=(1, 1),
            padding="valid", activation='relu'
        )
        self.flat = tf.keras.layers.Flatten()
        self.fc1 = tf.keras.layers.Dense(512, activation='relu')
        self.fc2 = tf.keras.layers.Dense(512, activation='linear')

    def call(self, pixels, **kwargs):
        pixels = tf.divide(tf.cast(pixels, tf.float32), tf.constant(255.0))
        features = self.flat(self.conv3(self.conv2(self.conv1(pixels))))
        qvalue = self.fc2(self.fc1(features))

        return qvalue

