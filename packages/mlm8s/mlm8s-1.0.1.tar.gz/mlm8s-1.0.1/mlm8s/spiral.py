import tensorflow as tf


class Spiral1D(tf.keras.layers.Layer):
    def __init__(self, units=32):
        super(Spiral1D, self).__init__()
        self.units = units
        self.koordinates = None
        self.size = None
        self.phi2 = None
        self.PI = tf.constant(3.1415926535897932)

    def build(self, input_shape):
        signal_length = tf.reduce_prod(input_shape[1:])
        signal_length_flt = tf.cast(signal_length, dtype=tf.float32)

        size = tf.sqrt(signal_length_flt / ((self.PI / 4.) * 0.70))
        size = tf.round(size / 2.)
        size = size * 2 + 1
        self.size = size

        r, phi = self.__create_circular_grid()

        phi2 = tf.round(r) * 2 * self.PI + phi
        self.phi2 = tf.cast(phi2, dtype=tf.float32)

        spiral = r / phi2
        spiral = tf.where(tf.math.is_nan(spiral), 0., spiral)

        koordinates = tf.reshape(phi2, shape=[-1])
        koordinates = tf.argsort(koordinates)

        koordinates = tf.expand_dims(koordinates, axis=1)
        koordinates = tf.cast(koordinates, dtype=tf.int64)

        self.koordinates = koordinates

    def call(self, inputs):
        signal = tf.reshape(inputs, shape=[-1])
        koordinates = self.koordinates[:signal.shape[0]]
        size = self.size

        size = tf.cast(size, dtype=tf.int32)
        size2 = tf.cast(size * size, dtype=tf.int32)

        spiral = tf.sparse.SparseTensor(indices=koordinates, values=signal, dense_shape=[size2])
        spiral = tf.sparse.reorder(spiral)
        spiral = tf.sparse.to_dense(spiral, default_value=None, validate_indices=True)
        spiral = tf.reshape(spiral, shape=[size, size])
        spiral = tf.stack([spiral, self.phi2], axis=-1)
        spiral = tf.expand_dims(spiral, axis=0)
        return spiral

    def __create_grid2d(self):
        size = tf.cast(self.size, dtype=tf.float32)
        rnge = tf.range(self.size)
        rnge = rnge - size / 2. + 0.5
        x1, x2 = tf.meshgrid(rnge, rnge)
        grid = tf.stack([x1, x2])
        return grid

    def __create_circular_grid(self):
        x1, x2 = self.__create_grid2d()
        r = tf.abs(x1 * x1 + x2 * x2)
        r = tf.sqrt(r)
        phi = x1 / r
        phi = tf.acos(phi)
        phi = tf.where(tf.math.is_nan(phi), 0., phi)
        phi = phi * tf.sign(x2)  # +PI
        mask1 = x2 == 0
        mask2 = x1 < 0
        is_pi = tf.math.logical_and(mask1, mask2)
        is_pi = tf.cast(is_pi, dtype=tf.float32) * self.PI
        phi = phi + is_pi
        return r, phi


class Spiral(tf.keras.layers.Layer):

    def __init__(self):
        super(Spiral, self).__init__()
        # self.units = units
        self.koordinates = None
        self.size = None
        self.phi2 = None
        self.PI = tf.math.acos(0.) * 2

    def build(self, input_shape):
        batch_size = tf.cast(input_shape[0], dtype=tf.float32)
        signal_length = tf.cast(input_shape[1], dtype=tf.float32)
        channel_dims = tf.cast(input_shape[-1], dtype=tf.float32)
        self.batch_size = batch_size
        self.signal_length = signal_length
        self.channel_dims = channel_dims

        size = tf.sqrt(signal_length / ((self.PI / 4.) * 0.70))
        size = tf.round(size / 2.)
        size = size * 2 + 1
        self.size = size
        size2 = tf.cast(size * size, dtype=tf.int32)
        self.size2 = size2

        indices_signal = self.__calc_signal_indices()
        indices = self.__combine_indices(indices_signal)
        indices = indices[:, :input_shape[1], :]
        indices = tf.reshape(indices, shape=[-1, 3])
        self.indices = indices

    def call(self, inputs):
        signal = tf.reshape(inputs, shape=[-1])
        spiral = tf.sparse.SparseTensor(indices=self.indices,
                                        values=signal,
                                        dense_shape=[inputs.shape[0],
                                                     self.size2,
                                                     inputs.shape[2]])
        spiral = tf.sparse.reorder(spiral)
        spiral = tf.sparse.to_dense(spiral, default_value=None, validate_indices=True)
        spiral = tf.reshape(spiral, shape=[inputs.shape[0], self.size, self.size, inputs.shape[2]])
        return spiral

    def get_embd(self):
        return tf.stack([self.phi2, self.r], axis=-1)

    def __create_grid2d(self):
        size = tf.cast(self.size, dtype=tf.float32)
        rnge = tf.range(self.size)
        rnge = rnge - size / 2. + 0.5
        x1, x2 = tf.meshgrid(rnge, rnge)
        grid = tf.stack([x1, x2])
        return grid

    def __create_circular_grid(self):
        x1, x2 = self.__create_grid2d()
        r = tf.abs(x1 * x1 + x2 * x2)
        r = tf.sqrt(r)
        phi = x1 / r
        phi = tf.acos(phi)
        phi = tf.where(tf.math.is_nan(phi), 0., phi)
        phi = phi * tf.sign(x2)  # +PI
        mask1 = x2 == 0
        mask2 = x1 < 0
        is_pi = tf.math.logical_and(mask1, mask2)
        is_pi = tf.cast(is_pi, dtype=tf.float32) * self.PI
        phi = phi + is_pi
        return r, phi

    def __calc_signal_indices(self):
        r, phi = self.__create_circular_grid()
        self.r = r

        phi2 = tf.round(r) * 2 * self.PI + phi
        self.phi2 = tf.cast(phi2, dtype=tf.float32)

        spiral = r / phi2
        spiral = tf.where(tf.math.is_nan(spiral), 0., spiral)

        indices_signal = tf.reshape(phi2, shape=[-1])
        indices_signal = tf.argsort(indices_signal)

        indices_signal = tf.expand_dims(indices_signal, axis=1)
        indices_signal = tf.cast(indices_signal, dtype=tf.int64)
        return indices_signal

    def __combine_indices(self, indices_signal):
        rnge_batch_size = tf.reshape(tf.range(self.batch_size, dtype=tf.int64),
                                     shape=[-1, 1, 1])

        indices_signal = tf.reshape(indices_signal,
                                    shape=[1, -1, 1])

        rnge_channel = tf.reshape(tf.range(self.channel_dims, dtype=tf.int64),
                                  shape=[1, 1, -1])

        ones = tf.ones([self.batch_size, indices_signal.shape[1], self.channel_dims], dtype=tf.int64)

        indices_batch = tf.einsum('bsc, boo->bsc', ones, rnge_batch_size)
        indices_signal = tf.einsum('bsc, oso->bsc', ones, indices_signal)
        indices_channel = tf.einsum('bsc, ooc->bsc', ones, rnge_channel)
        indices = tf.stack([indices_batch, indices_signal, indices_channel], axis=-1)
        return indices