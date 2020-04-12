import tensorflow as tf
from tensorflow.keras import models


def convert_model(source='', target=''):
    converter = tf.lite.TFLiteConverter.from_keras_model(models.load_model(source))
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    quantized_model = converter.convert()
    open(target + '.tflite', 'wb').write(quantized_model)


if __name__ == '__main__':
    # import sys
    # sys.argv
    from tkinter import filedialog

    classifier = None
    default_dir = 'deep_learning\\Saved Models'
    model_filename = filedialog.askopenfilename(title='Open file', initialdir=default_dir)

    if model_filename != '':
        msg = 'Selected: ' + model_filename[model_filename.rfind('/') + 1:]
        # r"..\Saved Models\Categorical\Loss - 0.052453 - 14 inputs_SMVNeuralNet.h5"
        target = model_filename[model_filename.rfind('\\') + 1:].rstrip('.h5')
        convert_model(source=model_filename, target=target)
