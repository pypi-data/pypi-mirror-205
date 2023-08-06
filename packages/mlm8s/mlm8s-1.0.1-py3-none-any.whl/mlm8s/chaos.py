import tensorflow as tf

@tf.function
def saddle(x, radius=1., mode=1., mass=0.5, sensitivity=1.):
    """
    saddle-node bifurcation
    inputs: x            state
            radius(+/-)  defines the bistable positions for modes(+/-)
            mode         switches the stable radius according to sign(mode)
            mass         defines the acceleration to/from modes
                         for high mass: the absolute speed between modes
                         is almost constant!!!
            sensitivity  scales mode

    output: x_dot        speed between modes
                               is normed s.t.: max(speed) = 1!
    """
    print("Traced")
    mass = tf.abs(mass) + 1.
    speed = tf.pow(tf.abs(radius), mass)
    x = tf.pow(tf.abs(x), mass)
    radius = tf.pow(radius, mass)
    mode = tf.tanh(mode * 3. * tf.abs(sensitivity))

    x_dot = (radius - x) * mode / speed
    return x_dot


@tf.function
def lorenz(state, force, parameters):
    """
    https://en.wikipedia.org/wiki/Lorenz_system
    """
    print('Traced')
    s = parameters[0]
    r = parameters[1]
    b = parameters[2]

    step = parameters[3]

    x = state[0]
    y = state[1]
    z = state[2]

    x_dot = s * (y - x)
    y_dot = r * x - y - x * z
    z_dot = x * y - b * z

    x = step * x_dot + x
    y = step * y_dot + y
    z = step * z_dot + z
    return tf.stack([x, y, z])