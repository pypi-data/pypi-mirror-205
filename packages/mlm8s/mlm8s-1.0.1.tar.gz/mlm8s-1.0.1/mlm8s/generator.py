import tensorflow as tf

class GeneratorDataset():
    """
    
    Class that - enables tf.data.Dataset from generator that utilize random variables that are unique
               - is a work-around and might get obsolete with future versions of TensorFlow
    
    __call__:  returns a tf.data.Dataset with non-deterministic order of generated data.
    
    """
    @tf.autograph.experimental.do_not_convert()
    def __init__(self, generator, batch_size=1024, epochs=16, autotune=tf.data.AUTOTUNE, **kwargs):
        
        """
        
        'generator' is function like:
        
        def generator(batch_size, **kwargs):
        
            ...generate some random batch...
            
            return x, y
            
        'epochs' = maximum possible number of epochs 
        
        """
        
        self.generator = generator
        self.batch_size = batch_size
        self.epochs = epochs
        self.autotune = autotune
        
        dummy_generator = lambda: tf.range(self.epochs*self.batch_size, dtype=tf.int32)
        dataset = tf.data.Dataset.from_generator(dummy_generator, tf.int32)
        dataset = dataset.map(lambda dummy: self.__wrap(dummy, self.generator, **kwargs), num_parallel_calls=self.autotune)
        dataset = dataset.batch(batch_size, drop_remainder=True, num_parallel_calls=self.autotune, deterministic=None,)
        self.dataset = dataset.prefetch(self.autotune)
        pass
    
    def __wrap(self, dummy, core, **kwargs):
        x, y = core(batch_size=1, **kwargs)
        return (x[0], y[0])
    
    def __call__(self):
        return self.dataset
    
