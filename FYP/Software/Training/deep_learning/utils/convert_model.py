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
    source = r"C:\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\deep_learning\Saved Models\MSE\Loss - 0.001872 - 720 inputs_ConvNeuralNet.h5"
        # r"C:\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\deep_learning\Saved Models\Categorical\Loss - 0.052453 - 14 inputs_SMVNeuralNet.h5"
    target = source[source.rfind('\\') + 1:].rstrip('.h5')
    convert_model(source=source, target=target)
