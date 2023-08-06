import tensorflow as tf

class Rounding_Loss(tf.keras.layers.Layer):

    """
    Regulizer that forces results to a linear grid
    """

    def __init__(self, resulution=1., rate=1e-2, power=1.):
        super(Rounding_Loss, self).__init__()
        self.rate = rate
        self.resulution = resulution
        self.power = power
        self.PI = tf.acos(0.) * 2

    def calc_round_loss(self, inputs):

        x = tf.tensordot(self.resulution, inputs, axes=0)
        loss = tf.cos(x * 2 * self.PI)
        loss = (loss + 1) / 2
        loss = 1 - tf.pow(loss, self.power)
        loss = tf.reduce_sum(loss, axis=-1)
        loss = loss / tf.cast(loss.shape[-1], dtype=tf.float32)
        loss = tf.reduce_mean(loss)

        return loss

    def call(self, inputs):
        self.add_loss(self.rate * self.calc_round_loss(inputs))
        return inputs

    def get_config(self):
        return {'resulution': self.resulution, 'rate': self.rate, 'power': self.power}