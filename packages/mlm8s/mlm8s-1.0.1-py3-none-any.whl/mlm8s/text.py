import tensorflow as tf


def build_re_pattern(liste):
  """
  creates regular-expression pattern-string
  for a list of words.
  """
  pattern = ''.join([' '+w+r'\b|' for w in liste])[:-1]
  return pattern

def custom_standardization(input_data):
  """
  standadizes text strings
  eg: for text-vectorization via keras
  """
  stripped = tf.strings.regex_replace(input_data, names_pattern, ' ')
  stripped = tf.strings.lower(stripped)
  stripped = tf.strings.regex_replace(stripped, stopword_pattern, ' ')
  stripped = tf.strings.regex_replace(stripped, '<br />', ' ')
  stripped = tf.strings.regex_replace(stripped,
                                      '[%s]' % re.escape(string.punctuation),
  
                                      '')
  # clean newline and words that are split by newline
  # also kills digits
  stripped = tf.strings.regex_replace(stripped, r'\n|'+r'-\n|'+r'\t', '')
  # clean single letters
  stripped = tf.strings.regex_replace(stripped, '(^| ).(( ).)*( |$)', ' ')
  # replace numbers that are not part of a word
  # Note: needs to run 2x
  stripped = tf.strings.regex_replace(stripped, r'(\A|[. ,])\d+([. ,]|$)', '  ')
  stripped = tf.strings.regex_replace(stripped, r'(\A|[. ,])\d+([. ,]|$)', '  ')
  return stripped

def build_vocab(dataset_train, standardization, batchsize=128, max_tokens=130_000):
  """
  builds vocabulary from dataset with custom_standardization
  """
  vectorize = tf.keras.layers.TextVectorization(
    max_tokens=max_tokens,
    standardize=standardization,
    split='whitespace',
    output_mode='int')
  # create vocabulary from train_ds
  text_only_ds = ds_train.map(lambda x, y: x).batch(batchsize)
  vectorize.adapt(text_only_ds)
  vocab = vectorize.get_vocabulary()
  return vocab

def stemm(vocab):
  """
  stemm via nltk.snowball
  """
  stemmed = [nltk.stem.SnowballStemmer("english").stem(word) for word in vocab]
  return stemmed

def plot_stemming_efficiency(stemmed, min_vocab_size = 3000):
  """
  helps with choosing the right min_vocab_size
  by plotting relative stemming efficiency.

  args:
        stemmed - list of stemmed vocabulary that is far to long 
        min_vocab_size - integer of current estimation that gets
                         marked in the plot
  """
  min_vocab_k = tf.cast(min_vocab_size/1000, dtype=tf.int32)
  stemming_efficiency = lambda i: ((i-len(set(stemmed[:i]))) / len(set(stemmed[:i])))
  stemming_efficiency = [stemming_efficiency(i) for i in range(1, len(vocab), 1000)]
  plt.figure(figsize=(10, 3))
  plt.title('relative stemming efficiency:')
  plt.xlabel('size of vocabulary in 1000s')
  plt.ylabel('efficiency')
  plt.plot(stemming_efficiency)
  plt.plot(stemming_efficiency[:min_vocab_k])
  return min_vocab_size

def build_lookup(keys, values, min_keys=3000, verbose=False):
  """
  build lookup-dict from unique but non-bijective key-value pairs
  note: <keys> and <values>   should correspond to eachother and
                                     be ordered according to frequency

  args:
        keys           - list of keys that is far to long 
        values         - list of values that is far to long
        min_keys       - integer that describes the number of 
                         unique lookup values. Defaults to 3000,
                         wich is the average number of words an
                         educated not-native english-speaker knows

  returns: lookup-dict with at least <min_keys> key-value pairs
  
  """
  table = [list(z) for z in zip(keys, values) if z[1] in stemmed[:min_keys]]
  table = dict(table)
  if verbose:
    print(str(len(table.keys())) + ' different words will be mapped to ' + 
          str(len(set(table.values()))) + ' unique tokens')
  return table

def custom_split(text):
  """
  spitter that can be used within tf.keras.layers.TextVectorization

  """
  split = tf.strings.regex_replace(text, ' +', ' ')
  split = tf.strings.split(split, sep=' ')
  return split


class LookUp(tf.keras.layers.Layer):

   def __init__(self, standardize, split, lookup):
     super(LookUp, self).__init__()
     self.standardize = standardize
     self.split = split
     keys = list(lookup.keys())
     values = list(lookup.values())
     values = tf.strings.to_hash_bucket_strong(values, len(values), [2, 42])
     lookup =  tf.lookup.KeyValueTensorInitializer(keys, values)
     self.lookup = tf.lookup.StaticVocabularyTable(lookup, num_oov_buckets = 1)
     self._name = 'lookup'
     
   def call(self, inputs):
     text = self.standardize(inputs)
     words = self.split(text)
     words = tf.ragged.map_flat_values(self.lookup.lookup, words)
     return words

def build_text_input(standardize,
                     split,
                     lookup_dict,
                     embedding_dims):
  
  vocab_size = len(table.values()) + 1
  input_layer = tf.keras.Input(shape=(1,), dtype=tf.string)
  lookup_layer = LookUp(standardize, split, lookup_dict)
  embedding_layer = tf.keras.layers.Embedding(vocab_size,
                                              embedding_dims,
                                              name='embedding')
  reshape_layer = tf.keras.layers.Lambda(lambda x: tf.squeeze(x, axis=1))
  model = tf.keras.models.Sequential([input_layer,
                                      lookup_layer,
                                      embedding_layer,
                                      reshape_layer,
                                     ])
  return model
