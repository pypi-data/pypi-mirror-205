# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keras_data_format_converter',
 'keras_data_format_converter.layers',
 'keras_data_format_converter.layers.confighandlers']

package_data = \
{'': ['*']}

install_requires = \
['libclang==14.0.1', 'protobuf>=3.20.3,<4.0.0', 'tensorflow==2.12.0']

extras_require = \
{':platform_machine == "arm64"': ['tensorflow-macos>=2.11.0,<3.0.0'],
 ':platform_machine == "x86_64"': ['tensorflow-addons>=0.19.0,<0.20.0']}

setup_kwargs = {
    'name': 'keras-data-format-converter',
    'version': '0.1.15.dev1',
    'description': 'Generates equal keras models with the desired data format',
    'long_description': '# Keras data format converter\n\nGenerates equal keras models with the desired data format  \n\n\n## Requirements\ntensorflow >= 2.0\n\n\n## API\n`convert_channels_first_to_last(model: keras.Model, inputs_to_transpose: List[str] = None, verbose: bool = False) -> keras.Model`\n\n`convert_channels_last_to_first(model: tf.keras.Model, inputs_to_transpose: List[str] = None, verbose: bool = False) \\\n        -> tf.keras.Model`\n\n`model`: Keras model to convert\n\n`inputs_to_transpose`: list of input names that need to be transposed due tothe data foramt changing  \n\n`verbose`: detailed output\n\n## Getting started\n\n```python\nfrom tensorflow import keras\nfrom keras_data_format_converter import convert_channels_last_to_first\n\n# Load Keras model\nkeras_model = keras.models.load_model("my_image_model")\n\n# Call the converter (image_input is an input that needs to be transposed, can be different for your model)\nconverted_model = convert_channels_last_to_first(keras_model, ["image_input"])\n```\n\n## Supported Layers with Special handling\n- [X] Normalization layers\n- [x] Permute\n- [x] Reshape\n- [x] Concatenate\n- [ ] Dot\n- [ ] MultiHeadAttention\n- [ ] TFOpLambda (Inserted by the Functional API construction whenever users call\n  a supported TF symbol on KerasTensors, see [here](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/keras/layers/core.py#L1284) at Tensorflow repo for more info)\n\n## Unsupported Layers due to lack of data_format property\n- Cropping1D\n- Upsampling1D\n- Zeropadding1D\n- All layers in tensorflow.keras.preprocessing\n\n## How to deploy\n- Create a new release version on GitHub\n- Update parameters in setup.py (usually `version` and `download_url`)\n- Run `python setup.py sdist` in root directory\n- Run `pip install twine`\n- Run `twine upload dist/*`\n \n\n\n## License\nThis software is covered by MIT License.\n',
    'author': 'dorhar',
    'author_email': 'doron.harnoy@tensorleap.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
