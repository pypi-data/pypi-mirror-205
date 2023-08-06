import tensorflow as tf


class Polynom(tf.keras.layers.Layer):
    '''
    Polynom:      of order n is spanned for each channel:
                  x, x^2 ... , x^n

    Note:         This layer does not learn anything!
                  It only maps the input to a polynomial basis.

    input_shape:  [batch_size, sequence_length, channels]
    output_shape: [batch_size, sequence_length, channels, n]


    '''

    def __init__(self, units=32, eps=0.01, **kwargs):
        '''
        units:  order of Polynom
        eps:    max relative error for 99.98 % of Data,
                given that Data is ~ N(1, 0)
        '''
        super(Polynom, self).__init__(**kwargs)
        self.units = units
        self.eps = eps
        self.xpnt = None
        self.norm = None
        self.sig = None

    def build(self, input_shape):
        rnge = tf.range(self.units, dtype=tf.float32) + 1.
        self.xpnt = tf.reshape(rnge, shape=[1, 1, 1, -1])
        self.norm = 1. / self.integrate_xn(rnge)
        quantil = 3.719  # 0.9999 Quantil for N(0,1)
        self.sig = quantil / tf.sqrt(-2. * tf.math.log(1 - self.eps))

    @tf.function
    def factorial(self, n):
        fac = tf.exp(tf.math.lgamma(n + 1.))
        return fac

    @tf.function
    def integrate_xn(self, n):
        '''
        itegrates f(x, n, a) dx from 0 to inf
        with f(x, n, a) = x^n * exp(-0.5(x)^2)
        '''
        pwr = tf.pow(2., (n - 1) / 2)
        gma = self.factorial((n + 1) / 2 - 1)
        return pwr * gma

    @tf.function
    def window(self, inputs):
        """
        Gaußian ~ N(0, sig)
        """
        window = tf.exp(-0.5 * tf.square(inputs / self.sig))
        return window

    @tf.function
    def span(self, inputs):
        """
        spans a basis of x^n from n=[1, units] (without constant!)

        inputs_shape: [batch_size, sequence_length, channels]
        output_shape: [batch_size, sequence_length, channels, n]

        inputs:       is expected to be ~ N(0,1)

        output:       is normed s.t.: the expected amplitude
                      of its elements are equal.
                      is windowed via a Gaußian ~ N(0, sig[n]) in order to avoid extreme values
                      s.t.: the relative error to x^n is upperbounded to 'eps'
                      for 99.98 % of the inputs. Given that 'w' did converge!
        """
        inputs = tf.expand_dims(inputs, axis=-1)
        pwr = tf.pow(inputs, self.xpnt)
        window = self.window(inputs)
        inputs = pwr * window
        output = tf.einsum('bsck, k ->bsck', inputs, self.norm)
        return output

    @tf.function
    def call(self, inputs):
        output = self.span(inputs)
        return output

    def get_config(self):
        config = super().get_config()
        config.update({"units": self.units})
        return config


class Polynom_Dense(tf.keras.layers.Layer):
    '''
    Polynom:     is learned for each channel:
                 w1*x + w2*x^2 ... + wn*x^n + b

    input_shape: [batch_size, sequence_length, channels]
    '''

    def __init__(self, units=32, eps=0.01, **kwargs):
        '''
        units:  order of Polynom
        eps:    max relative error for 99.98 % of Data,
                given that Data is ~ N(1, 0)
        '''
        super(Polynom, self).__init__(**kwargs)
        self.units = units
        self.eps = eps
        self.xpnt = None
        self.norm = None
        self.sig = None

    def build(self, input_shape):
        rnge = tf.range(self.units, dtype=tf.float32) + 1.
        self.xpnt = tf.reshape(rnge, shape=[1, 1, 1, -1])
        self.norm = 1. / self.integrate_xn(rnge)
        quantil = 3.719  # 0.9999 Quantil for N(0,1)
        self.sig = quantil / tf.sqrt(-2. * tf.math.log(1 - self.eps))

        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer="random_normal",
            trainable=True,
        )

        self.b = self.add_weight(
            shape=(1, 1, input_shape[-1]),
            initializer="random_normal",
            trainable=True,
        )

    @tf.function
    def factorial(self, n):
        fac = tf.exp(tf.math.lgamma(n + 1.))
        return fac

    @tf.function
    def integrate_xn(self, n):
        '''
        itegrates f(x, n, a) dx from 0 to inf
        with f(x, n, a) = x^n * exp(-0.5(x)^2)
        '''
        pwr = tf.pow(2., (n - 1) / 2)
        gma = self.factorial((n + 1) / 2 - 1)
        return pwr * gma

    @tf.function
    def window(self, inputs):
        """
        Gaußian ~ N(0, sig)
        """
        window = tf.exp(-0.5 * tf.square(inputs / self.sig))
        return window

    @tf.function
    def span(self, inputs):
        """
        spans a basis of x^n from n=[1, units] (without constant!)

        inputs_shape: [batch_size, sequence_length, channels]
        output_shape: [batch_size, sequence_length, channels, n]

        inputs:       is expected to be ~ N(0,1)

        output:       is normed s.t.: the expected amplitude
                      of its elements are equal.
                      is windowed via a Gaußian ~ N(0, sig[n]) in order to avoid extreme values
                      s.t.: the relative error to x^n is upperbounded to 'eps'
                      for 99.98 % of the inputs. Given that 'w' did converge!
        """
        inputs = tf.expand_dims(inputs, axis=-1)
        pwr = tf.pow(inputs, self.xpnt)
        window = self.window(inputs)
        inputs = pwr * window
        output = tf.einsum('bsck, k ->bsck', inputs, self.norm)
        return output

    @tf.function
    def call(self, inputs):
        inputs = self.span(inputs)
        output = tf.einsum('bsck, ck->bsck', inputs, self.w)
        output = tf.reduce_sum(output, axis=-1) + self.b
        return output

    def get_config(self):
        config = super().get_config()
        config.update({"units": self.units})
        return config
