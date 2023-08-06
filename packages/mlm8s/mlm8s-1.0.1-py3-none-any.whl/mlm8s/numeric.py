import tensorflow as tf

def rapson_newton(fun, funprime, start, numinterations):
    """
    fun:          function that is monotone and zero at poit of interest
                           eg: lambda x:  x^3 - 5
    funprime:     first derivative of function.   eg: lambda x: 3x^2

    """
    estimate = start
    for n in range(numinterations):
        print(estimate)
        estimate = estimate - fun(estimate) / funprime(estimate)
    return estimate

@tf.function
def fun4n(fun, n, initial_state, external_force, const_param):
    states = tf.TensorArray(tf.float32, size=n, clear_after_read=False)
    state = initial_state

    for i in tf.range(n):
        state = fun(state, external_force[i], const_param)
        states = states.write(i, state)

    return states.stack()