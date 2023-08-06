import numpy as np
import tensorflow as tf

@tf.function
def standardize(x):
    x = (x-np.mean(x))/np.std(x)
    return x

@tf.function
def normalize(x):
    x = (x-np.min(x))/(np.max(x)-np.min(x))
    return x

@tf.function
def stretch(x, s):
    return x*[s, 1/s]

@tf.function
def rotate_deg(x, alpha_deg=45.):
    alpha = -alpha_deg/90.*tf.asin(1.)
    cos = tf.math.cos(alpha)
    sin = tf.math.sin(alpha)
    rot_matrix = [[cos, -sin], [sin, cos]]
    rotated_x = tf.linalg.matmul(x, rot_matrix)
    return rotated_x

@tf.function
def flatten(x):
    hm_ins = x.shape[0]
    x = np.reshape(x, [hm_ins, -1])
    return x

def correlate(inputs, outputs, input_lag):
    lag = input_lag
    outputs = np.pad(outputs[:,lag:], pad_width=[[0,0], [0, lag]])
    coefs = np.corrcoef(inputs, outputs)
    return coefs[-1, :-1]

def group_unique(array, axis=0):
    a = array
    a = a[a[:, axis].argsort()]
    groups = np.split(a, np.unique(a[:, axis], return_index=True)[1][1:])
    return groups


@tf.function
def span_polar_basis(x, y):
    print("Traced")
    phi = tf.math.atan2(y, x)
    e_r = tf.stack([
                    tf.math.cos(phi),
                    tf.math.sin(phi)
                   ])
    e_phi = tf.stack([
                      tf.math.sin(phi) * -1,
                      tf.math.cos(phi)
                     ])

    e_r = tf.cast(e_r, dtype=tf.float32)
    e_phi = tf.cast(e_phi, dtype=tf.float32)
    return e_r, e_phi

@tf.function
def create_meshgrid(shape = tf.constant([10, 10, 10]), indexing = 'ij'):
    ranges = tf.map_fn(tf.range, shape, fn_output_signature = tf.RaggedTensorSpec(shape=[None],dtype=tf.int32))
    grid = tf.meshgrid(*ranges, indexing = indexing)
    grid = tf.stack(grid, axis=-1)
    return grid
