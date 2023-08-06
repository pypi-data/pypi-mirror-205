import tensorflow as tf


def huber_loss(y_true, y_pred, grad_max=1):
    """
    Robust Least-squares aka. Huber-penalty from
    Peter J. Huber. "Robust Estimation of a Location Parameter" - 1964

    inputs:
            y_true:     ground truth
            y_pred:     prediction
            grad_max:   maximum absolut gradient of loss

    outputs:
            mean of losses along last axis s.t.
            if |y_true - y_pred| <= threshold -> l2-penalty
            if |y_true - y_pred| > threshold -> l1-penalty
    """
    error = y_true - y_pred
    linear_loss = (2 * tf.abs(error) - grad_max) * grad_max
    linear_loss = tf.math.maximum(linear_loss, grad_max * grad_max)
    quadratic_loss = tf.square(error)
    loss = tf.math.minimum(linear_loss, quadratic_loss)
    return tf.reduce_mean(loss, axis=-1)


def deadzone_l1_loss(y_true, y_pred, error_min=0.01):
    """
    mean of l1 - losses with loss = 0 if |error| < error_min
    """
    error = tf.abs(y_true - y_pred)
    loss = tf.math.maximum(error - error_min, 0)
    return tf.reduce_mean(loss, axis=-1)


def complementary_distance(sample, batch, grad=100):
    """
    costfunction similar to interior point method
    data must encode boolean values via float
    eg: arg1 * arg2:  [1,0,1,1] * [[1,0,0,1]] -> low since arg2 does not complement 2. value of arg1
        arg2 * arg1:  [1,0,0,1] * [[1,0,1,1]] -> higher since arg1 complements 3. value of arg2

                                              -> Order matters!!!!!

    input:      sample of shape:[depth]
                batch of shape: [batchsize, depth]
    """
    batch = tf.cast(batch, dtype=tf.float32)
    grad = tf.cast(grad, dtype=tf.float32)
    order = 1./(tf.sqrt(1./grad))
    depth = batch.shape[-1]
    offset = tf.pow(order, 1/depth)
    offset = tf.exp(-offset)                               # TODO !!!!
    sample = tf.equal(sample, 0)
    cost = tf.boolean_mask(batch, sample, axis=1)
    cost = 1./(cost+(1./order))
    cost = cost/order
    cost = tf.reduce_sum(cost, axis=1) / cost.shape[-1]
    cost = tf.clip_by_value(cost, clip_value_min=0, clip_value_max=1)
    cost = tf.round(cost*grad)/grad
    return cost