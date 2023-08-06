# mlm8s

###### miscellaneous for machine-learning in TensorFlow

```
pip install keras_tuner
pip install mlm8s
```

#### Imports:
```
from mlm8s import ListedPaths, paths2labels, strings2onehot, paths2label_dicts, map_via_dict
from mlm8s import GeneratorDataset, HyperModel, connect
from mlm8s import standardize, normalize, stretch, rotate_deg, flatten, correlate
from mlm8s import create_meshgrid, span_polar_basis
from mlm8s import group_unique
from mlm8s import print_plot_play
from mlm8s import get_sampling_matrix, soft_threshold, deadzone_l1_loss, lasso_l1, norm_l0, huber_loss
from mlm8s import lipschitz_grad_lasso, nesterov_momentum, ista_prox_lasso, fista
```
<br>

#### Labels from Paths:

```
from mlm8s import ListedPaths, paths2label_dicts, map_via_dict

### read PATH2DATA and (onehot-)encode by file-containing folder:

paths = ListedPaths(PATH2DATA)*'ogg'
label_dict = paths2label_dicts(paths(), seperators=['/', '.'], indices=[-2, 0])
labels = map_via_dict(paths2labels(paths()), label_dict)
```
<br>

#### Class - GeneratorDataset:

Enables alternating results of tf.random* -calls, from within
the generator of tf.data.Dataset.from_generator*.

```
kwargs = dict()
kwargs['paths'] = paths
kwargs['seperators'] = ['/', '.']
kwargs['indices'] = [-2, 0]

### Feature-Engineering with generator, that can use random variables!!
def engineer_features(paths):
    # use data in path to engineer features
    features = tf.random.uniform(shape=[32, 256, 256, 4])
    return features

kwargs['engineer_features'] = engineer_features

### Creating Features & Labels:
def generate_from_paths(batch_size=1024, **kwargs):
    paths = kwargs['paths']
    seperators = kwargs['seperators']
    indices = kwargs['indices']
    engineer_features = kwargs['engineer_features']
    rdm_paths = paths.get_rdm(batch_size)
    features = engineer_features(rdm_paths)
    labels = paths2labels(rdm_paths, seperators, indices)
    labels = map_via_dict(labels, label_dict)
    return features, labels

### Creating tf.data.Dataset, that can generate an infinite number of random batches
###                           from 'generate_from_paths'.
ds = GeneratorDataset(generate_from_paths, batch_size=128, epochs=16, **kwargs)()

for batch in ds.take(1):
    x, y = batch
    print(x.shape, y.shape)
```
