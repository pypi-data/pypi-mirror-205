"""
Lattice that maps inputs to best-matching-units (BMU) of kernel.
             enables Kohonen-Layers aka Self-Organizing-Maps
                     also: non-parametric UMAP.
             is capable of high-dimensional Donut-topologies for cyclic data like angles.

Example 6-dimensional input mapped to 3-dimensional lattice:

        ltc = Lattice(output_shape=tf.constant([100, 100, 100]), isCyclic=[False, False, True])
        ltc.build(input_shape=[None, 6])
"""

import tensorflow as tf

class Lattice(tf.keras.layers.Layer):

    def __init__(self, output_shape, isCyclic):
        super(Lattice, self).__init__()
        self.grid_shape = output_shape
        self.grid = None
        self.mask_cyclic = None
        self.set_topology(isCyclic)
        pass

    def build(self, input_shape):
        self._init_meshgrid(self.grid_shape, indexing='ij')
        grid_flattened = tf.reshape(self.grid, shape=[1, -1, self.grid_shape.shape[0]])
        grid_flattened = tf.cast(grid_flattened, dtype=tf.float32)  # + tf.random.uniform(shape=grid_flattened.shape)/3.
        grid_flattened = (grid_flattened - tf.reduce_mean(grid_flattened, axis=1)) / tf.math.reduce_std(grid_flattened,
                                                                                                        axis=1)
        self.grid_flattened = tf.Variable(initial_value=grid_flattened, trainable=True)
        self.w = tf.Variable(initial_value=tf.random.normal(shape=[1,
                                                                   tf.math.reduce_prod(self.grid_shape),
                                                                   input_shape[1]
                                                                   ],
                                                            stddev=1),
                             trainable=False)
        super(Lattice, self).build(input_shape)
        pass

    def set_topology(self, isCyclic):
        isCyclic = tf.cast(isCyclic, dtype=tf.float32)
        # self.isCyclic = tf.reshape(tf.cast(isCyclic, dtype=tf.int32), shape=[1,-1])
        self.mask_cyclic = tf.reshape(isCyclic, shape=[1, -1])
        pass

    def _init_meshgrid(self, shape, indexing='ij'):
        ranges = tf.map_fn(tf.range, shape, fn_output_signature=tf.RaggedTensorSpec(shape=[None], dtype=tf.int32))
        grid = tf.meshgrid(*ranges, indexing=indexing)
        self.grid = tf.stack(grid, axis=-1)
        pass

    def _get_linear_grid_distance(self, x, y):
        distance = tf.abs(x - y)
        distance = distance * (1. - self.mask_cyclic)
        distance_linear = tf.reshape(distance, shape=[x.shape[0], -1, self.grid_shape.shape[0]])
        return distance_linear

    def _get_cyclic_grid_distance(self, x, y):
        maxi = tf.cast(self.grid_shape, dtype=tf.float32)
        centre = maxi / 2
        distance = tf.math.floormod(tf.abs(x - y) - centre, maxi) - centre
        distance = tf.abs(distance) * self.mask_cyclic
        distance_cyclic = tf.reshape(distance, shape=[x.shape[0], -1, self.grid_shape.shape[0]])
        return distance_cyclic

    def _get_index_distance(self, x, y, norm=2):
        distance = self._get_linear_grid_distance(x, y) + self._get_cyclic_grid_distance(x, y)
        distance = tf.norm(distance, ord=norm, axis=-1)
        return distance

    def _get_BMUs(self, x, hm_neighbors=1):
        # get best matching unit (BMU) of lattice
        k = hm_neighbors
        grid = self.grid_flattened
        x = tf.expand_dims(x, axis=1)

        activation_distance = tf.abs(x - self.w)
        activation_distance = tf.square(activation_distance)  # via l2-norm
        activation_distance = tf.reduce_sum(activation_distance, axis=-1)
        values_neg, indices = tf.math.top_k(-tf.abs(activation_distance), k)
        neighbors_distance = -1 * values_neg

        bmu = tf.gather(grid[0], indices[:, 0])

        return bmu, neighbors_distance

    def call(self, x):
        bmu, neighbors_distance = self._get_BMUs(x)
        return bmu

    def compute_output_shape(self, input_shape):
        return tf.constant(1).shape  # self.grid_shape