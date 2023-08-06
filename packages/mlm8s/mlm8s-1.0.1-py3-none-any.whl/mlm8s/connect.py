import tensorflow as tf

def connect(units=128):
    """
    Keras_Layer generator that:
                                1. concatenates multiple inputs
                                2. feeds outcome into new layer e.g. Dense
                                3. normalizes output batches

    Example:                    x4 = connect('dense')([x1, x2, x3])
    """

    concat = tf.keras.layers.Concatenate(axis=-1)
    normalize = tf.keras.layers.BatchNormalization()
    last_layer = tf.keras.layers.Dense(units, activation='relu')

    block = lambda x: last_layer(normalize(concat(x)))

    return block
