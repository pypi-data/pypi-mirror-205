import tensorflow as tf


def get_sampling_matrix(shape = tf.TensorShape([10, 100])):
    """
    returns sub-gaussian sampling-matrix
    """
    sampling_matrix = tf.random.uniform(shape)
    sampling_matrix = sampling_matrix / tf.expand_dims(tf.norm(sampling_matrix, axis=1), axis=1)
    return sampling_matrix

@tf.function
def lipschitz_grad_lasso(A):
    """
    calculates the smallest Lipschitz constant of grad(f(x)).
    With f(x) = l2(y - Ax) + l1(x); aka: LASSO.
    """
    At = tf.einsum('...ij -> ...ji', A)
    AtA = tf.einsum('...ji, ...ab -> ...jb', At, A)
    eig = tf.linalg.eig(AtA)[0]
    eig = tf.math.real(eig)
    eig_max = tf.math.reduce_max(eig, axis=-1)
    lipschitz = 2*eig_max
    return lipschitz


def soft_threshold(x, offset):
    '''
    prox for l1-norm
    '''
    thd = tf.abs(x) - offset
    gtr = tf.greater(thd, 0)
    gtr = tf.cast(gtr, dtype=tf.float32)
    thd = thd * gtr * tf.sign(x)
    return thd

def deadzone_l1_loss(y_true, y_pred, error_min=0.01):
    '''
    mean of l1 - losses with loss = 0 if |error| < error_min
    '''
    error = tf.abs(y_true - y_pred)
    loss = tf.math.maximum(error - error_min, 0)
    return tf.reduce_mean(loss, axis=-1)

def nesterov_momentum(t):
    '''
    momentum term defined by the increasing t sequence
    note: in order to increase performance of fista,
          it is best practise to reset the momentum
    '''
    t_new = (1+tf.sqrt(1+4*tf.square(t)))*0.5
    momentum = (t - 1)/t_new
    return momentum, t_new

@tf.function
def ista_prox_lasso(ground_truth, dictionary, estimation, rate=1):
    print('retrace')
    y = ground_truth
    A = dictionary
    x = estimation
    At = tf.einsum('...ij -> ...ji', A)
    Ax = tf.einsum('...ij, ...jo -> ...io', A, x)
    offset = 1 / lipschitz_grad_lasso(A)
    residual = Ax - y
    grad_l2 = 2 * tf.einsum('...ji, ...io -> ...jo', At, residual)
    arg = x - tf.einsum('j, jmn -> mn', offset, grad_l2)
    estimation = soft_threshold(arg, offset * rate)
    return estimation

@tf.function
def fista(y, A, x, t, rate=1):
    x_new = ista_prox_lasso(y, A, x, rate)
    m, t_new = nesterov_momentum(t)
    y = x_new + m * (x_new - x)
    return y, t_new

def lasso_l1(sigma=1e-2, cardinality=16):
    '''
    simga      :     Noise Level
    cardinaltiy:     of Dictionary
    '''
    sigma = tf.cast(sigma, dtype=tf.float32)
    cardinality = tf.cast(cardinality, dtype=tf.float32)
    rate = sigma * tf.sqrt(2. * tf.math.log(cardinality))
    rate = tf.cast(rate, dtype=tf.float32)
    l1_reg = tf.keras.regularizers.L1(float(rate))
    return l1_reg

def norm_l0(x, axis=None):
    l0 = tf.greater(tf.abs(x), 0)
    l0 = tf.cast(l0, dtype=tf.float32)
    l0 = tf.reduce_sum(l0, axis)
    return l0

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
