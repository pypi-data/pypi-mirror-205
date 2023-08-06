import tensorflow as tf
import matplotlib.pyplot as plt


def get_learning_rate(step=0, max_lr=0.1, max_step=1_000_000., resets=7, t1=1.5, t2=3., p1=2., p2=1.5, verbose=False):
    """
    Creates a learning-rate that diminishes over 'step' in a saw-like fashion.
                            for callbacks.
    Note: Use 'verbose=True' to get accustomed to the parameterization of its shape!
    """
    if verbose:
        step = tf.range(max_step)

    step = tf.cast(step + 1, dtype=tf.float32) / max_step
    saw = tf.pow(step, p1)
    saw = tf.math.floormod(-saw, 1 / (resets + 1))
    saw = saw / (1. / (resets + 1.))  # saw gets normalized
    saw = tf.exp(saw * t2)
    saw = saw / tf.exp(t2)  # saw gets normalized (again!)
    saw = saw * tf.pow(1 - step, p2)
    lr = max_lr * (tf.exp(-step * t1) + saw) / 2

    if verbose:
        plt.plot(lr)

    return lr
