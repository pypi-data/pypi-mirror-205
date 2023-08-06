import tensorflow as tf


class Triangle(tf.keras.layers.Layer):

    def __init__(self, units=32, prime=3.):
        super(Triangle, self).__init__()
        self.units = units
        self.prime = prime

    def build(self, input_shape):
        w_init = tf.keras.initializers.HeUniform()
        self.w = tf.Variable(initial_value=w_init(shape=(input_shape[-1], self.units),
                                                  dtype='float32'), trainable=True)
        self.b = tf.Variable(initial_value=tf.zeros([self.units]), trainable=True)

    def call(self, inputs):
        inputs = inputs
        mapped = tf.matmul(inputs, self.w) + self.b
        result = tf.math.floormod(mapped, 4) - 2
        result = tf.abs(result) - 1
        return result
