import tensorflow as tf
import keras_tuner as keras_tuner

class HyperModel(keras_tuner.HyperModel):

    """
    HyperModel-Factory for KerasTuner with ADAM and early-stopping
    """

    def __init__(self, models, in_shape, out_shape, loss=['mse'], metrics=['mse'], *args, **kwargs):
        """
        models:     List of functions that generate keras-models with hyperparameters
                    [model_1, model_2, ...] each with args: (hyperparameters, in_shape, out_shape)
        """
        self.models = models
        self.model_choices = tf.range(len(models))
        self.in_shape = in_shape
        self.out_shape = out_shape
        self.loss = loss
        self.metrics = metrics
        self.seed = None
        self.batch_size = None
        super(HyperModel, self).__init__(*args, **kwargs)

    def fit(self, model, *args, **kwargs):
        stop_early = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=2, restore_best_weights=True)
        callbacks = kwargs['callbacks'] + [stop_early]
        epochs = kwargs['epochs']

        history = model.fit(
                            batch_size=self.batch_size,
                            callbacks=callbacks,
                            epochs=epochs,
                            *args,
                            )
        return history

    def compile_model(self, model, hp):
        self.seed = hp.Choice("seed", [27, 42, 123])
        tf.random.set_seed(self.seed)
        self.batch_size = hp.Choice("batch_size", [16, 128, 512, 1024])

        learning_rate = hp.Float("lr", min_value=1e-5, max_value=1e-1, sampling="log")
        beta_1 = hp.Float("beta_1", min_value=0.5, max_value=0.999, sampling="log")
        beta_2 = hp.Float("beta_2", min_value=0.7, max_value=0.9999, sampling="log")
        epsilon = hp.Choice("epsilon", [1e-7, 1e-5, 1e-3, .1, 1.])

        adam = tf.keras.optimizers.Adam(learning_rate=learning_rate,
                                        beta_1=beta_1,
                                        beta_2=beta_2,
                                        epsilon=epsilon,
                                        )

        model.compile(steps_per_execution=1,
                      optimizer=adam,
                      loss=self.loss,
                      metrics=self.metrics
                      )
        model._name = self.name + '_' + str(self.seed) + '_lr_' + str(learning_rate)
        return model

    def build(self, hp, name='myModel'):
        self.name = name
        model_type = hp.Choice("model_type", [0])
        model = self.models[model_type](hp, self.in_shape, self.out_shape)
        model = self.compile_model(model, hp)
        return model
