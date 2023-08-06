import tensorflow as tf

class Voltera(tf.keras.layers.Layer):
    """
    input_shape:  [batch_size, sequence_length, channels]
    output_shape: [batch_size, sequence_length]

    Voltera:      1. For each channel a polynomial-basis is spanned:
                     1, x, x^2 ... , x^n
                  2. Every single x^i basis (channels * (n+1))
                     are combined via an outerproduct
                  3. Every product gets weighted
                  4. All weighted products are summed

    """

    def __init__(self, units=16, outputs=1, eps=0.001, kernel_regularizer=None, **kwargs):
        '''
        units:  defines order of Polynom: (units 16 -> order=15 -> 16^channels weights)
        eps:    max relative error for 99.98 % of Data,
                given that Data is ~ N(1, 0)
        '''
        super(Voltera, self).__init__(**kwargs)
        self.units = units
        self.order = units - 1
        self.outputs = outputs
        self.eps = eps
        self.xpnt = None
        self.norm = None
        self.sig = None
        self.equation = None
        self.nr_weights = None
        self.kernel_regularizer = tf.keras.regularizers.get(kernel_regularizer)

    def build(self, input_shape):

        self._input_shape = input_shape
        rnge = tf.range(self.order, dtype=tf.float32) + 1
        self.xpnt = tf.reshape(rnge, shape=[1, 1, 1, -1])
        self.norm = 1. / self.integrate_xn(rnge)
        # 0.9999 Quantil for N(0,1)
        quantil = 3.719
        self.sig = quantil / tf.sqrt(-2. * tf.math.log(1 - self.eps))
        self.equation = self.einsum_equation(input_shape[-1])

        nr_weights = tf.pow(self.units, input_shape[-1])
        self.nr_weights = tf.cast(nr_weights, dtype=tf.int32)
        self.w = self.add_weight(shape=[self.nr_weights, self.outputs],
                                 initializer=tf.keras.initializers.RandomUniform(minval=-1e-6, maxval=1e-6),
                                 regularizer=self.kernel_regularizer,
                                 trainable=True
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

    def einsum_equation(self, order):
        '''
        generates string for einsum notation for outerproduct of last dimensions
        eg.: '...x, ...y, ...z->...xyz'
        '''
        xyz = 'xyzuvwijklmnopqrstfghabcde' + 'ABSCDEFGHIJKLMNOPQRSTUVWXYZ'
        equation = ''
        for i in range(order):
            equation = equation + '...' + xyz[i]
            if i == order - 1:
                break
            equation = equation + ', '
        equation = equation + '->...'
        for i in range(order):
            equation = equation + xyz[i]
        return equation

    @tf.function
    def outer_product(self, inputs):
        '''
        calculates batch-wise outer-product of last dimension
        input_shape: [batch_size, sequence, channels, order]

        '''
        xyz = tf.unstack(inputs, axis=-2)
        output = tf.einsum(self.equation, *xyz)
        output = tf.reshape(output, shape=[-1, self._input_shape[1], self.nr_weights])
        return output

    @tf.function
    def window(self, inputs):
        '''
        Gaußian ~ N(0, sig)
        '''
        window = tf.exp(-0.5 * tf.square(inputs / self.sig))
        return window

    @tf.function
    def span_polynoms(self, inputs):
        '''
        spans a basis of x^n from n=[0, units]

        inputs_shape: [batch_size, sequence_length, channels]
        output_shape: [batch_size, sequence_length, channels, n]

        inputs:       is expected to be ~ N(0,1)

        output:       is normed s.t.: the expected amplitude
                      of its elements are equal.
                      is windowed via a Gaußian ~ N(0, sig[n]) in order to avoid extreme values
                      s.t.: the relative error to x^n is upperbounded to 'eps'
                      for 99.98 % of the inputs. Given that 'w' did converge!
        '''
        inputs = tf.expand_dims(inputs, axis=-1)
        pwr = tf.pow(inputs, self.xpnt)
        window = self.window(inputs)
        inputs = pwr * window
        output = tf.einsum('bsck, k ->bsck', inputs, self.norm)
        # Adding a constant to the Polynom for every channel
        ones = 1. + 0 * output[:, :, :, 0]
        ones = tf.expand_dims(ones, axis=-1)
        output = tf.concat([ones, output], axis=-1)
        return output

    @tf.function
    def span(self, inputs):
        inputs = self.span_polynoms(inputs)
        outputs = self.outer_product(inputs)
        return outputs

    @tf.function
    def call(self, inputs):
        inputs = self.span(inputs)
        inputs = tf.einsum('bsk, ko ->bso', inputs, self.w)
        return inputs

    def get_config(self):
        config = super().get_config()
        config.update({"units": self.units})
        return config