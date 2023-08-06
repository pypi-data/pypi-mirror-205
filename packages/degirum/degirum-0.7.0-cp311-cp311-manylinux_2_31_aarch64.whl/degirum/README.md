# PySDK - DeGirum AI Inference Software Development Kit

***Version 0.7.0***

*Copyright DeGirum Corp. 2022-2023*


The DeGirum AI Inference Software Development Kit, **PySDK**, is a Python package which
provides APIs to perform inference on ML models.

PySDK consists of the following components:
1. PySDK library, which includes the following essential modules:
    - `degirum.zoo_manager` - AI model zoo management classes
    - `degirum.model` module - AI model management classes
    - `degirum.postprocessor` module - AI inference result handling classes
2. The `CoreClient` extension module implementing APIs to work with DeGirum AI accelerator cards installed locally
3. The `aiclient` extension module implementing APIs to work with DeGirium AI servers running on remote systems
4. The `degirum.server` module - helper module that allows launching AI server on a local AI hardware to be used by
remote clients.
5. The `degirum` console script implementing command-line interface to various PySDK management facilities.


The PySDK package provides the necessary tools to support the following use cases:
- **Local Inference**: perform AI inferences on the local system using DeGirum AI accelerator hardware installed
on the same system
- **AI Server Hosting**: deploy the system with installed DeGirum AI accelerator hardware as AI server
- **AI Server Inference**: connect to one or several AI servers and perform AI inferences on those servers remotely
- **Cloud Inference**: connect to DeGirum Cloud Platform and perform AI inferences in the cloud

# Installation

## Basic Installation of PySDK Python Package

It is recommended to install PySDK in a virtual environment. Please see
[PySDK Supported Configurations](https://cs.degirum.com/pysdk_main_doc) page for a list of supported system configurations.

To install DeGirum PySDK from the DeGirum index server use the following command:

```sh
python -m pip install degirum --extra-index-url https://degirum.github.io/simple
```

To force reinstall the most recent PySDK version without reinstalling all dependencies use the following command:

```sh
python -m pip install degirum --upgrade --no-deps --force-reinstall --extra-index-url https://degirum.github.io/simple
```

## Kernel Driver Installation

### Linux Kernel Driver Installation

Hosts that have DeGirum Orca card installed need a driver to enable its functionality. The driver is distributed
as a source package via a DeGirum aptitude repository. It can be built automatically after download.

1. Add the following line to `/etc/apt/sources.list` to register the DeGirum APT repository:

   ```sh
   deb-src https://degirum.github.io/apt-repo ORCA main
   ```

1. Download DeGirum public key by running the following command:

   ```sh
   wget -O - -q http://degirum.github.io/apt-repo/DeGirum.gpg.key | sudo apt-key add -
   ```

1. Update package information from configured sources, and download prerequisites by running the following commands:

   ```sh
   sudo apt update
   sudo apt install dpkg-dev debhelper
   ```

1. Finally, download and build DeGirum Linux driver package by running the following command:

   ```sh
   sudo apt-get --build source orca-driver
   ```

### Kernel Driver Installation for Other Operating Systems

The current version of DeGirum software package supports only Linux kernel driver.
Kernel driver support for other operating systems is under development.
This document will be updated when kernel drivers for other operating systems will be released.


# Quick Start

> *Note:* This quick start guide covers the **Local inference** use case when you run AI inferences on the local host
with DeGirum AI accelerator hardware installed on this local host as an option.
See [System Configuration for Specific Use Cases](#system-configuration-for-specific-use-cases) section for 
more use cases.

To start working with PySDK you import `degirum` package:

```python
import degirum as dg
```

The main PySDK entry point is `degirum.connect` function, which creates and returns
`degirum.zoo_manager.ZooManager` *zoo manager object*
(for detailed explanation of PySDK concepts refer to [Model Zoo Manager](#model-zoo-manager) section):

```python
zoo = dg.connect(dg.CLOUD, "https://cs.degirum.com", <your cloud API access token>")
```

When instantiated this way, zoo manager automatically connects to DeGirum Public cloud model zoo, and you have free
access to all AI models from this public model zoo. However, to access the public cloud zoo you need
a *cloud API access token*, which you can generate on DeGirum Cloud Portal site https://cs.degirum.com under
*Management | My Tokens* main menu item (see more on that in 
[Configuration for Cloud Inference](#configuration-for-cloud-inference) section).

To see the list of all AI models available for inference in the public model zoo, 
use `degirum.zoo_manager.ZooManager.list_models` method. It returns a list of strings, where each string is a 
model name:

```python
model_list = zoo.list_models()
print(model_list)
```

If you want to perform AI inference using some model, you need to *load* it using 
`degirum.zoo_manager.ZooManager.load_model` method. You provide the model name as a method argument. 
The model name should be one of model names returned by `list_models()` method, for example:

```python
model = zoo.load_model("mobilenet_v2_ssd_coco--300x300_quant_n2x_orca_1")
```

The `load_model()` method returns a `degirum.model.Model` object, which can be used to perform AI inferences.

Before performing AI inferences, you may want to adjust some model parameters. The model class has a list of
parameters which can be modified during runtime. These model parameters affect how the input data is
*pre-processed* and how the inference results are *post-processed*. All model parameters have reasonable default values,
so in the beginning you may skip this step.

Some usable model parameters are:

| Property Name | Description | Possible Values |
|---------------|-------------|-----------------|
| `degirum.model.Model.image_backend` | image processing package to be used |`"auto"`, `"pil"`, or `"opencv"`;<br>`"auto"` tries PIL first |
| `degirum.model.Model.input_pad_method` | how input image will be padded or cropped when resized |`"stretch"`, `"letterbox"`, `"crop-first"`, or `"crop-last"` |
| `degirum.model.Model.input_crop_percentage` | percentage of image dimensions to crop around if `"input_pad_method"` is set to `"crop-first"` or `"crop-last"` | Float value in [0..1] range |
| `degirum.model.Model.output_confidence_threshold` | confidence threshold to reject results with low scores | Float value in [0..1] range |
| `degirum.model.Model.output_nms_threshold` | rejection threshold for non-max suppression |  Float value in [0..1] range |
| `degirum.model.Model.overlay_color` | color to draw AI results | Tuple in (R,G,B) format or list of tuples in (R,G,B) format |
| `degirum.model.Model.overlay_font_scale` | font scale to print AI results | Float value |
| `degirum.model.Model.overlay_show_labels` | `True` to show class labels when drawing AI results | True/False |
| `degirum.model.Model.overlay_show_probabilities` | `True` to show class probabilities when drawing AI results| True/False |

For the complete list of model parameters see [Model Parameters](#model-parameters) section.

Now you are ready to perform AI inference. To do an inference you either invoke `degirum.model.Model.predict` method
or simply *call* the model, supplying the input image as an argument. The inference result is returned.

A model may accept input images in various formats:

- as a string containing the file name of the image file on the local file system:

   ```python
   result = model("./images/TwoCats.jpg")
   ```

- as a string containing URL of the image file:

   ```python
   result = model("https://degirum.github.io/images/samples/TwoCats.jpg")
   ```

- as a PIL image object:

   ```python
   from PIL import Image
   image = Image.open("./images/TwoCats.jpg")
   result = model(image)
   ```

- as a numpy array (for example, returned by OpenCV):

   ```python
   import cv2
   image = cv2.imread("./images/TwoCats.jpg")
   model.input_numpy_colorspace = "BGR" # set colorspace to match OpenCV-produced numpy array
   result = model(image)
   ```

The result object returned by the model (an object derived from `degirum.postprocessor.InferenceResults` class)
contains the following information:
- numeric inference results
- graphical inference results
- original image

Numeric results can be accessed by `degirum.postprocessor.InferenceResults.results` property. This property returns a
list of result dictionaries, one dictionary per detected object or class. The format of this dictionary is model-dependent. For example, to iterate over all classification model inference results you may do this:

```python
for r in result.results:
   print(f"Detected class: '{r['label']}' with probability {r['score']}")
```

Tip: if you just print your inference result object, all the numeric results will be pretty-printed in YAML format:

```python
print(result)
```

Graphical results can be accessed by `degirum.postprocessor.InferenceResults.image_overlay` property. This property
returns a graphical object containing an original image with all inference results draw over it. The graphical object
type depends on the graphical package specified for the model `image_backend` (if you omit it, it will be PIL, if PIL
is installed, otherwise OpenCV). Once you get this object, you may display it, print it, or save it to a file the way
you like using the graphical package of your choice. For example, for PIL:

```python
result_image = result.image_overlay
result_image.save("./images/TwoCatsResults.jpg")
result_image.show()
```

The original image can be accessed by `degirum.postprocessor.InferenceResults.image` property, which returns graphical
object, whose type again depends on the graphical package specified for the model `image_backend`.


# System Configuration for Specific Use Cases

The PySDK package can be used in the following use cases:
- **Local inference**: running AI inferences on the local host with DeGirum AI accelerator hardware installed on
this local host as an option
- **AI Server inference**: running AI inferences on remote AI server host with DeGirum AI accelerator hardware
installed on that remote host
- **Cloud Inference**: running AI inferences on DeGirum Cloud Platform, which automatically manages a set of AI
computing nodes equipped with different types of AI accelerator hardware including DeGirum Orca, Google EdgeTPU,
and Intel Myriad
- **AI Server hosting**: configuring the host with DeGirum AI accelerator hardware as AI server to be used for remote
AI inferences

The following sections provide step-by-step instructions how to setup the system for the particular use case.
For detailed explanation of PySDK concepts refer to [Model Zoo Manager](#model-zoo-manager) section.

## Configuration for Local Inference

1. Install PySDK package as described in 
[Basic Installation of PySDK Python Package](#basic-installation-of-pysdk-python-package) section.

1. If your system is equipped with DeGirum AI accelerator hardware, install the kernel driver as described in
[Kernel Driver Installation](#kernel-driver-installation) section.

   > *Note:* If your system is not equipped with any AI accelerator hardware, the set of AI models available for local
   inference will be limited only to CPU models.

1. For local inferences, you call `degirum.connect` passing `degirum.LOCAL` constant or `"@local"` string 
as a first argument.

1. If you plan to operate with DeGirum-hosted cloud model zoo, then you call `degirum.connect` providing the cloud model 
zoo URL in the `"https://cs.degirum.com[/<zoo URL>]"` format and the cloud API access token as the second and third 
arguments:

   ```python
   zoo = dg.connect(dg.LOCAL, "https://cs.degirum.com/my_organization/my_zoo", 
      token="<your cloud API access token>")
   ```

   You can obtain the model zoo URL on DeGirum Cloud Portal site https://cs.degirum.com under *Management | Models* 
   main menu item. If `<zoo URL>` suffix is not specified, then DeGirum Public cloud model zoo will be used.

   You can generate your token on DeGirum Cloud Portal site https://cs.degirum.com under *Management | My Tokens* 
   main menu item.
   
1. If you plan to operate with locally deployed model, then you call `degirum.connect` providing the 
the full path to the model JSON file as the second argument, omitting the third argument:

   ```python
   zoo = dg.connect(dg.LOCAL, "full/path/to/model.json")
   ```


## Configuration for AI Server Hosting

1. Install the kernel driver as described in [Kernel Driver Installation](#kernel-driver-installation) section.
1. Follow instructions provided in [Configuring and Launching AI Server](#configuring-and-launching-ai-server) section.


## Configuration for AI Server Inference

> Make sure your AI server host is already configured as described in the 
[Configuration for AI Server Hosting](#configuration-for-ai-server-hosting) section, and it is up and running.

1. Install PySDK package as described in 
[Basic Installation of PySDK Python Package](#basic-installation-of-pysdk-python-package) section.

1. If you plan to operate with a model zoo, locally deployed on the AI server host system, you call `degirum.connect`
providing just the hostname or IP address of the AI server host you want to use for AI inference:

   ```python
   zoo = dg.connect("192.168.0.118")
   ```

1. If you plan to operate with AI server taking models from a cloud model zoo of your choice, you call 
`degirum.connect` providing the hostname or IP address of the AI server host as the first argument, 
the cloud zoo URL as the second argument, and the cloud API access token as the third argument.
The cloud model zoo URL you specify in the `"https://cs.degirum.com[/<zoo URL>]"` format:

   ```python
   zoo = dg.connect( "192.168.0.118", "https://cs.degirum.com/my_organization/my_zoo",
      token="<your cloud API access token>")
   ```

   You can obtain the model zoo URL on DeGirum Cloud Portal site https://cs.degirum.com under *Management | Models* 
   main menu item. If `<zoo URL>` suffix is not specified, then DeGirum Public cloud model zoo will be used.

   You can generate your token on DeGirum Cloud Portal site https://cs.degirum.com under *Management | My Tokens* 
   main menu item.


## Configuration for Cloud Inference

Starting from ver. 0.3.0 the PySDK supports inferences on DeGirum Cloud Platform, 
and starting from ver. 0.5.0 the PySDK supports cloud model zoo access.

DeGirum Cloud Platform solves the Edge AI development problem by providing the toolchain to design, run, and
evaluate ML models across different hardware platforms in the cloud.

DeGirum **Cloud Platform** includes the following components:
1. DeGirum Cloud Device Farm accessible through the Cloud Application Server and PySDK
1. DeGirum Cloud Portal Management site, [cs.degirum.com](https://cs.degirum.com)
1. Cloud model zoos hosted on DeGirum Cloud Platform.

**The DeGirum Cloud Device Farm** is a set of computing nodes with various AI hardware accelerators installed in
those nodes, including: DeGirum Orca, Google Edge TPU, Intel&reg; Movidius&trade; Myriad&trade; VPU.
The farm nodes are hosted by DeGirum.

**The Cloud Application Server** provides web API to perform AI inference on the Cloud Farm devices.
Starting from ver. 0.3.0 PySDK supports Application Server web API and provides **the same level** of functionality
transparently to the end user: you may run **exactly the same code** on the Cloud Platform as it was designed for
traditional use cases such as local inference or AI server inference.

**The cloud model zoo** is a collection of AI models, stored on DeGirum Cloud Platform.
A registered DeGirum Cloud Platform user can create and maintain multiple cloud zoos with either private or 
public access. A model zoo with private access is visible to all users belonging to the same organization.
A model zoo with public access is visible to all registered users of DeGirum Cloud Platform.
DeGirum maintains the Public Model Zoo with extensive set of AI models available free of charge to all registered users.

**The DeGirum Cloud Portal Management site** provides GUI to get access to the various Cloud Platform assets such as:
- cloud API access **tokens**, which are required to access the Cloud Application Server through PySDK;
- cloud model zoos belonging to the user's organization;
- Jupiter Lab container with per-user private storage to quickly run Python scripts using pre-installed PySDK;
- PySDK documentation;
- PySDK examples;
- *Graphit AI &trade;* visual AI model design tool;
- Cloud Model Compiler and Model Parameters Wizard.


To get started with DeGirum Cloud Platform perform the following steps:

1. Contact DeGirum Customer Support at support@degirum.com or click *Request Access* button on
[cs.degirum.com](https://cs.degirum.com) main page to request an invitation. Once the invitation request gets
processed, you will receive the invitation e-mail.

1. Follow the link in the invitation e-mail to activate your DeGirum Cloud Platform account. On the activation
page you will be asked for the new password.

1. Once your account is activated, you login into the *Cloud Management Portal* by clicking the *Login* button on
[cs.degirum.com](https://cs.degirum.com) main page.
Use your e-mail as the login name.

1. Once logged in, you will see the *DeGirum Cloud Portal Management* menu. Click on the *Management | My Tokens* menu
item to open the *Tokens Management* page.

1. Generate new API token by clicking the *Generate new token* button. You need to provide the token name
(arbitrary string) and the token expiration date (or you may select *Unlimited Token* option).

1. Once the token is generated, you copy it into a clipboard by clicking the *Copy* button. Please save
the token string in some secure place: you will need this token string on later steps in order to access the
Cloud Application Server via PySDK.

1. If you develop new Python script with DeGirum PySDK or if you already have a Python script which uses
DeGirum PySDK and which you want to run on DeGirum Cloud Platform, then find the line of code, which invokes
`degirum.connect` method and change it the following way:

    ```python
    zoo = dg.connect(dg.CLOUD, "https://cs.degirum.com", token = "<your cloud API access token>" )
    ```

Here `"https://cs.degirum.com"` is the URL of the DeGirum Cloud Application Server, and 
`"<your cloud API access token>"` is the token string you generated on the previous step.

All the rest of your code does not need any modifications compared to traditional use cases: PySDK support
of the Cloud Platform is completely transparent to the end user.

If you specify just `"https://cs.degirum.com"` URL, then the DeGirum Public cloud model zoo will be used.

If you want to work with the cloud model zoo of your choice, then specify the URL in the 
`"https://cs.degirum.com/<zoo URL>"` format. Here `<zoo URL>` suffix is the name of the cloud model zoo in the form of
`<organization>/<zoo>`. You can obtain the model zoo URL suffix on DeGirum Cloud Portal site https://cs.degirum.com 
under *Management | Models* main menu item: just select the model zoo you want to access to open the model zoo 
page and click copy button near the model zoo name to copy the model zoo URL suffix into the clipboard.


# Model Zoo Manager

There are three main concepts in PySDK: the AI inference engine, the AI model zoo, and the AI model.
The AI inference engines perform inferences of AI models, while AI model zoos are places where these models are stored.

PySDK supports the following AI inference types:

1. **Local** inference: when the client application uses PySDK to directly communicate with the AI hardware accelerator
installed on the same computer where this application runs.

1. **AI Server** inference: when the AI hardware accelerator is controlled by the DeGirum AI Server software stack,
and the client application communicates with that AI Server to perform AI inferences. The client application and 
the AI server can run on two different computers connected to the same local network.

1. **Cloud** inference: when the client application communicates with the DeGirum Cloud Platform software over the 
Internet to perform AI inferences on the DeGirum Cloud Farm devices.

PySDK supports the following AI model zoo types:

1. **Local** model zoo: when the set of AI models is located in some local directory on the computer with AI hardware 
accelerator. In the case of the local inference, the local model zoo is located on the computer where you run your 
application. In the case of AI server inference the local model zoo is located on the computer where AI Server software 
is installed.

1. **Cloud** model zoo: when the set of AI models is located on the DeGirum Cloud Platform.
You create and maintain cloud model zoos using [DeGirum Cloud Platform](https://cs.degirum.com) web GUI.
There are two types of cloud model zoos: **public** and **private**. A public model zoo is visible to all registers 
cloud users, while a private model zoo is visible only the the members of your organization.

Almost all combinations of AI inference type and model zoo type are supported by the PySDK:
1. A cloud inference using a cloud model zoo
1. An AI Server inference using a cloud model zoo
1. An AI Server inference a using a local model zoo
1. A local inference using a cloud model zoo
1. A local inference using a particular model from a local model zoo

> *Note*: the combination of a cloud inference with a local model zoo is not supported.

The PySDK starting point is `degirum.connect` function, which creates and returns `degirum.zoo_manager.ZooManager` 
**model zoo manager** object. This function has the following parameters, which specify the inference type and 
the model zoo to use:

- `inference_host_address`: inference engine designator; it defines which inference engine to use.

   For AI Server-based inference it can be either the hostname or IP address of the AI Server host,
   optionally followed by the port number in the form `host:port`.

   For DeGirum Cloud Platform-based inference it is the string `"@cloud"` or `degirum.CLOUD` constant.

   For local inference it is the string `"@local"` or `degirum.LOCAL` constant.

- `zoo_url`: model zoo URL string which defines the model zoo to operate with.

   For a cloud model zoo, it is specified in the following format: `<cloud server prefix>[/<zoo suffix>]`.
   The `<cloud server prefix>` part is the cloud platform root URL, typically `https://cs.degirum.com`.
   The optional `<zoo suffix>` part is the cloud zoo URL suffix in the form `<organization>/<model zoo name>`.
   You can confirm zoo URL suffix by visiting your cloud user account and opening the model zoo management page.
   If `<zoo suffix>` is not specified, then DeGirum public model zoo `degirum/public` is used.

   For AI Server-based inferences, you may omit both `zoo_url` and `token` parameters.
   In this case locally-deployed model zoo of the AI Server will be used.

   For local AI hardware inferences, if you want to use particular AI model from your local drive, then
   you specify `zoo_url` parameter equal to the path to that model's .json configuration file.
   The `token` parameter is not needed in this case.

- `token`: cloud API access token used to access the cloud zoo. To obtain this token you need to
open a user account on [DeGirum cloud platform](https://cs.degirum.com). Please login to your account and
go to the token generation page to generate an API access token.

The function returns the model zoo manager object, which connects to the model zoo of your choice and provides 
the following functionality:
- list and search models available in the connected model zoo;
- create appropriate AI model handling objects to perform AI inferences;
- request various AI model parameters.


## Model Zoo URL Cheat Sheet

| Inference Type      | Model Zoo Type | `connect()` parameters |
|---------------------|----------------|------------|
| Cloud inference     | Cloud zoo      | `zoo = dg.connect(dg.CLOUD, "https://cs.degirum.com[/<zoo URL>]", "<token>")`|
| AI server inference | Cloud zoo      | `zoo = dg.connect("<hostname>", "https://cs.degirum.com[/<zoo URL>]", "<token>")`|
| AI server inference | Local zoo      | `zoo = dg.connect("<hostname>")`|
| Local inference     | Cloud zoo      | `zoo = dg.connect(dg.LOCAL, "https://cs.degirum.com[/<zoo URL>]", "<token>")`|
| Local inference     | Local file     | `zoo = dg.connect(dg.LOCAL, "/path/to/model.json")` |


## Cloud Model Caching

Each time you request a model for inference from a cloud model zoo on either local system or on AI server host,
it gets downloaded to a local filesystem of that inference host into a some internal cache directory.

Cache directories are maintained per each cloud zoo URL. 

If the model already exists in the cache directory, its checksum is verified against the checksum of the model in the
cloud zoo. If these checksums mismatch, the model from the cloud zoo is downloaded and replaces the model in the cache.
This mechanism guarantees that each time you request a cloud model for AI inference, you always get the most up to date
model. It greatly simplifies the model deployment on a large quantity of distributed nodes, when each node
automatically downloads the updated model from the cloud on the first model inference request.

Cache directories' root location is operating system specific:
- For Windows it is `%APPDATA%/DeGirum`
- For Linux it is `~/.local/share/DeFirum`
- For MacOS it is `Library/Application Support/DeGirum`

The cache size is limited (currently by 1GB, to avoid uncontrolled growth of model cache directory).
Once it is exceeded, the least recently used models get evicted from the cache.

## Listing and Searching AI Models

**AI model** is represented in a model zoo by a set of files stored in the model subdirectory, which
is unique for each model. Each model subdirectory contains the following model files:

| Model File | Description |
|------------|-------------|
| `<model name>.json` | JSON file containing all model parameters. The name of this file is the name of the model. This file is mandatory. |
| `<model name>.n2x` | DeGirum Orca binary file containing the model. This file is mandatory for DeGirum Orca models |
| `<model name>.tflite` | TensorFlow Lite binary file containing the model. This file is mandatory for TFLite models |
| `<model name>.blob` | OpenVINO binary file containing the model. This file is mandatory for OpenVINO models |
| `<class dictionary>.json` | JSON file containing class labels for classification, detection, or segmentation models. This file is optional. |

To obtain the list of available AI models, you may use `degirum.zoo_manager.ZooManager.list_models` method.
This method accepts arguments which specify the model filtering criteria. All the arguments are optional.
If a certain argument is omitted, then the corresponding filtering criterion is not applied.
The following filters are available:

| Argument | Description | Possible Values |
|----------|-------------|-----------------|
| `model_family` | Model family name filter. Used as a search substring in the model name | Any valid substring like `"yolo"`, `"mobilenet"` |
| `device` | Inference device filter: a string or a list of strings of device names | `"orca"`: DeGirum Orca device<br> `"cpu"` : host CPU<br> `"edgetpu"`: Google EdgeTPU device |
| `precision` | Model calculation precision filter: a string or a list of strings of model precision labels | `"quant"`: quantized model<br> `"float"`: floating point model |
| `pruned` | Model density filter: a string or a list of strings of model density labels | `"dense"`: dense model<br> `"pruned"`: sparse/pruned model |
| `runtime` | Runtime agent type filter: a string or a list of strings of runtime agent types | `"n2x"`: DeGirum N2X runtime<br> `"tflite"`: Google TFLite runtime<br> `"openvino"`: OpenVINO runtime |

The method returns a list of model name strings. These model name strings are to be used later when you load
AI models for inference.

The `degirum.zoo_manager.ZooManager.list_models` method returns the list of models, which was requested at the time
you connected to a model zoo by calling `degirum.connect`. This list of models is then stored inside the
Model Zoo manager object, so subsequent calls to `list_models` method would quickly return the model list without
connecting to a remote model zoo. If you suspect that the remote model zoo contents changed, then to update the model
list you need to create another instance of Zoo Manager object by calling `degirum.connect`.

## Loading AI Models

Once you obtained the AI model name string, you may load this model for inference by calling
`degirum.zoo_manager.ZooManager.load_model` method and supplying the model name string as its argument.
For example:

```python
model = zoo.load_model("mobilenet_v2_ssd_coco--300x300_quant_n2x_orca_1")
```

If a model with the supplied name string is found, the `load_model()` method returns model handling object of
`degirum.model.Model` class. Otherwise, it throws an exception.

### Models from Cloud Zoo

If you load the model from the *cloud* model zoo, this model will be downloaded first and stored in the cache
directory associated with that cloud model zoo. If the model already exists in the cache, it will
be loaded from that cache but only if the cached model checksum matches the model checksum in the cloud zoo.
If checksums do not match, the model from the cloud zoo will be downloaded again into the cache.

> *Note*: your inference host needs to have Internet access to work with cloud zoo models.

> *Note:* Model Zoo manager does not provide any explicit method to download a model from the cloud zoo: the model is
downloaded automatically when possible, if the model is not in the cache or the cached model checksum does not match the
model checksum in the cloud zoo. However, the PySDK provides `degirum download-zoo` command to explicitly download 
the whole or part of a cloud model zoo of your choice to the local directory (see more in 
[PySDK Command-Line Interface](#pysdk-command-line-interface) section).

### Models from AI Server Local Zoo

If you load the model from the *AI server* local model zoo, the command to load the model will be sent to the AI server:
the connected AI server will handle all model loading actions remotely.

> *Note:* The AI Server lists the models that it serves and you can only load those models: the job of managing
remote AI server model zoo is not handled by Model Zoo manager class and should be done different way. Please refer
to [Configuring and Launching AI Server](#configuring-and-launching-ai-server) section for details.

### Models from Local Drive

In order to work with locally-deployed model, you need to download that model from some model zoo in advance,
for example by using PySDK `degirum download-zoo` command (see more in 
[PySDK Command-Line Interface](#pysdk-command-line-interface) section).
This is the only option which allows you to perform AI inferences without any network connection.


# Running AI Model Inference

Once you loaded an AI model and obtained model handling object, you can start doing AI inferences on your model.
The following methods of `degirum.model.Model` class are available to perform AI inferences:
- `degirum.model.Model.predict` and `degirum.model.Model.__call__` to run prediction of a single data frame
- `degirum.model.Model.predict_batch` to run prediction of a batch of frames
- `degirum.model.Model.predict_dir` to run prediction of multiple files in a directory

The `predict()` and `__call__` methods behave exactly the same way (actually, `__call__` just calls `predict()`).
They accept single argument - input data frame, perform AI inference of that data frame, and return inference result -
an object derived from `degirum.postprocessor.InferenceResults` superclass.

The batch prediction methods, `predict_batch()` and `predict_dir()`, perform predictions of multiple frames in a
pipelined manner, which is more efficient than just calling `predict()` method in a loop.
These methods are described in details in [Batch Inferences](#batch-inferences) section.

## Cloud Server Connection Issues

For cloud inferences the connection to the cloud server is performed at the beginning of each predict-style method call, 
and disconnection is performed at the end of that call. This greatly reduces performance since the cloud server 
connection/disconnection is relatively long activities. To overcome this problem you may use the model object inside
the `with` block. When predict-style method is called inside the `with` block, the disconnection is not performed 
at the end of such call, so consecutive predict call does not perform reconnection as well, thus saving execution time.

The following code demonstrates the approach:

```python
   # here model_name variable stores the model name
   # and data_list variable stores the list of input data frames to process
   
   # wrap the load_model() call in with block to avoid disconnections
   with zoo.load_model(model_name) as model:
      # perform prediction loop
      for data in data_list:
         result = model.predict(data)
```


## Input Data Handling

PySDK model prediction methods support different types of input data. An exact input type depends on the model
to be used. The following input data types are supported:
- **image** input data
- **audio** input data
- **raw tensor** input data

The input data object you supply to model predict methods also depends on the number of inputs the model has.
If the model has single data input, then the data objects you pass to model predict methods are single objects.
IN rare cases the model may have multiple data inputs; in this case the data objects you pass to model predict methods 
are lists of objects: one object per corresponding input.

The number and the type of inputs of the model are described by the `InputType` property of the `ModelInfo` class
returned by `degirum.model.Model.model_info` property (see [Model Info](#model-info) section for details about model
info properties). The `InputType` property returns the list of input data types, one type per model input.
So the number of model inputs can be deduced by evaluating the length of the list returned by the `InputType` property.

The following sections describe details of input data handling for various model input types.

### Image Input Data Handling

When dealing with model inputs of **image** type (`InputType` is equal to `"Image"`), the PySDK model prediction
methods accept a wide variety of input data frame types:
- the input frame can be the name of a file with frame data;
- it can be the HTTP URL pointing to a file with frame data;
- it can be a numpy array with frame data;
- it can be a PIL `Image` object;
- it can by `bytes` object containing raw frame data.

An AI model requires particular input tensor dimensions and data type which, in most of the cases, does not match the
dimensions of the input frame. In this case, PySDK performs automatic conversion of the input frame to the format
compatible with AI model input tensor, performing all the necessary conversions such as resizing, padding, colorspace
conversion, and data type conversion.

PySDK performs input frame transformations using one of the two graphical packages (called **backends**): PIL or OpenCV.
The backend is selected by `degirum.model.Model.image_backend` property. By default it is set to `auto`, meaning
that PIL backend will be used first, and if it is not installed, then OpenCV backend will be used.
You may explicitly select which backend to use by assigning either `"pil"` or `"opencv"` to
`degirum.model.Model.image_backend` property.

> *Note:* In case of OpenCV backend, you cannot pass PIL Image objects to model predict methods.

If your input frame is in the file on a local filesystem, or is accessible through HTTP protocol, pass the filename
string or URL string directly to model predict methods: PySDK will (down-)load the file, decode it, and convert
to the model input tensor format. The set of supported graphical file formats is defined solely by the graphical backend
library you selected, PIL or OpenCV - PySDK does not perform any own decoding.

Sometimes, image conversion to AI model input tensor format requires image resizing. This resizing can be done in two
possible ways:
- preserving the aspect ratio;
- not preserving the aspect ratio.

In addition, the image can be cropped or not cropped.

You can control the way of image resizing by `degirum.model.Model.input_pad_method` property, which can have one of the following values: `"stretch"`, `"letterbox"`, `"crop-first"`, and `"crop-last"`. 

When you select the `"stretch"` method, the input image is resized exactly to the AI model input tensor dimensions, 
possibly changing the aspect ratio. 

When you select the `"letterbox"` method (default way), the image is resized to fit the AI model input tensor 
dimensions while preserving the aspect ratio. The voids which can appear on the image sides are filled with the color 
specified by `degirum.model.Model.input_letterbox_fill_color` property (black by default). 

When you select the `"crop-first"` method, the image is first cropped to match the AI model input tensor aspect ratio 
with respect to the `degirum.model.Model.input_crop_percentage` and then resized to match the AI model input tensor 
dimensions. For example: an input image with dimensions 640x480 going into a model with input tensor dimensions 224x224
with crop percentage of 0.875 will first be center cropped to 420x420 (*420 = `min`(640, 480) \* 0.875*) 
and then resized to 224x224. 

When you select `"crop-last"` method, if the AI model input tensor dimensions are equal (square), the image is resized 
with its smaller side equal to the model dimension with respect to `degirum.model.Model.input_crop_percentage`. 
If the AI model input tensor dimensions are not equal (rectangle), the image is resized with stretching to the input 
tensor dimensions with respect to `degirum.model.Model.input_crop_percentage`. The image is then cropped to fit the 
AI model input tensor dimensions and aspect ratio. For example: an input image with dimensions 640x480 going into a
model with input tensor dimensions of 224x224 with crop percentage of 0.875 will first be resized to 341x256 
(*256 = 224 / 0.875* and *341 = 256 \* 640 / 480*) and then center cropped to 224x224. Alternatively an input image 
with dimensions 640x480 and a model with input tensor dimensions 280x224 will be resized to 320x256 
(*320 = 280 / 0.875* and *256 = 224 / 0.875*) and then center cropped to 280x224.

You can specify the resize algorithm in the `degirum.model.Model.input_resize_method` property, which may have the
following values: `"nearest"`, `"bilinear"`, `"area"`, `"bicubic"`, or `"lanczos"`.
These values specify various interpolation algorithms used for resizing.

In case your input frames are stored in numpy arrays, you may need to tell PySDK the order of colors in those numpy
arrays: RGB or BGR. This order is called the **colorspace**. By default, PySDK treats numpy arrays as having RGB
colorspace. So if your numpy arrays as such, then no additional action is needed from your side. But if your numpy
arrays have color order opposite to default, then you need to change `degirum.model.Model.input_numpy_colorspace`
property.

*Note:* If a model has multiple image inputs, the PySDK applies the same `input_***` image properties as discussed above
for every image input of a model.


### Audio Input Data Handling

When dealing with model inputs of **audio** type (`InputType` is equal to `"Audio"`), PySDK does not perform any
conversions of the input data: it expects numpy 1-D array with audio waveform samples of proper size and with proper
sampling rate. The waveform size should be equal to `InputWaveformSize` model info property. The waveform sampling
rate should be equal to `InputSamplingRate` model info property. And finally the data element type should be equal
to the data type specified by the `InputRawDataType` model info property.
All aforementioned model info properties are the properties of the `ModelInfo` class returned by
`degirum.model.Model.model_info` property (see [Model Info](#model-info) section for details).


### Tensor Input Data Handling

When dealing with model inputs of **raw tensor** type (`InputType` is equal to `"Tensor"`),  PySDK expects that you
provide a 4-D numpy array of proper dimensions.
The dimensions of that array should match model input dimensions as specified by the following model info properties:
- `InputN` for dimension 0,
- `InputH` for dimension 1,
- `InputW` for dimension 2,
- `InputC` for dimension 3.

The data element type should be equal to the data type specified by the `InputRawDataType` model info property
(see [Model Info](#model-info) section for details).


## Inference Results

All model predict methods return result objects derived from `degirum.postprocessor.InferenceResults` class.
Particular class types of result objects depend on the AI model type: classification, object detection, pose detection, 
segmentation etc. But from the user point of view, they deliver identical functionality.

Result object contains the following data:
- `degirum.postprocessor.InferenceResults.image` property keeps original image;
- `degirum.postprocessor.InferenceResults.image_overlay` property keeps original image with inference results
drawn on a top; the type of such drawing is model-dependent:
  - for classification models, the list of class labels with probabilities is printed below the original image;
  - for object detection models, bounding boxes of detected object are drawn on the original image;
  - for hand and pose detection models, detected keypoints and keypoint connections are drawn on the original image;
  - for segmentation models, detected segments are drawn on the original image;
- `degirum.postprocessor.InferenceResults.results` property keeps a list of numeric results (follow the property link
for detailed explanation of all result formats);
- `degirum.postprocessor.InferenceResults.image_model` property keeps the binary array with image data converted to
AI model input specifications. This property is assigned only if you set `degirum.model.Model.save_model_image` model
property before performing predictions.

The `results` property is what you typically use for programmatic access to inference results. The type of `results` is
always a list of dictionaries, but the format of those dictionaries is model-dependent.
Also, if the result contains coordinates of objects, all such coordinates are recalculated from the model coordinates
back to coordinates on the original image, so you can use them directly.

The `image_overlay` property is very handy for debugging and troubleshooting. It allows you to quickly assess the 
correctness of the inference results in graphical form.

There are result properties which affect how the overlay image is drawn:
- `degirum.postprocessor.InferenceResults.overlay_alpha`: transparency value (alpha-blend weight) for all overlay
details;
- `degirum.postprocessor.InferenceResults.overlay_font_scale`: font scaling factor for overlay text;
- `degirum.postprocessor.InferenceResults.overlay_line_width`: line width in pixels for overlay lines;
- `degirum.postprocessor.InferenceResults.overlay_color`: RGB color tuple or list of RGB color tuples for drawing all 
overlay details;
- `degirum.postprocessor.InferenceResults.overlay_show_labels`: flag to enable drawing class labels of detected objects;
- `degirum.postprocessor.InferenceResults.overlay_show_probabilities`: flag to enable drawing probabilities of
detected objects;
- `degirum.postprocessor.InferenceResults.overlay_fill_color`: RGB color tuple for filling voids which appear due to 
letterboxing.

When each individual result object is created, all these overlay properties (except `overlay_fill_color`) are assigned
with values of similarly named properties taken from the model object (see 
[Model Parameters](#model-parameters) section for the list of model properties). This allows assigning overlay 
property values only once and applying them to all consecutive results. But if you want to play with individual result, 
you may reassign any of overlay properties and then re-read `image_overlay` property. Each time you read 
`image_overlay`, it returns new image object freshly drawn according to the current values of overlay properties.

The `overlay_color` property is used to define the color to draw overlay details. In the case of a single RGB tuple,
the corresponding color is used to draw all the overlay data: points, boxes, labels, segments, etc.
In the case of a list of RGB tuples the behavior depends on the model type.
- For classification models different colors from the list are used to draw labels of different classes.
- For detection models different colors are used to draw labels *and boxes* of different classes.
- For pose detection models different colors are used to draw keypoints of different persons.
- For segmentation models different colors are used to highlight segments of different classes.

If the list size is less than the number of classes of the model, then `overlay_color` values are used cyclically,
for example, for three-element list it will be `overlay_color[0]`, then `overlay_color[1]`, `overlay_color[2]`,
and again `overlay_color[0]`.

The default value of `overlay_color` is a single RBG tuple of yellow color for all model types except segmentation models.
For segmentation models it is the list of RGB tuples with the list size equal to the number of model classes.
You can use `Model.label_dictionary` property to obtain a list of model classes.
Each color is automatically assigned to look pretty and different from other colors in the list.

> *Note"* `overlay_fill_color` is assigned with `degirum.model.Model.input_letterbox_fill_color`.


## Batch Inferences

If you need to process multiple frames using the same model and the same settings, the most effective way to do it is
to use batch prediction methods of `degirum.model.Model' class:
- `degirum.model.Model.predict_batch` method to run predictions on a list of frames;
- `degirum.model.Model.predict_dir` method to run predictions on files in a directory.

Both methods perform predictions of multiple frames in a pipelined manner, which is more efficient than just calling
`predict()` method in a loop.

Both methods return the generator object, so you can iterate over inference results. This allows you to directly use
the result of batch prediction methods in for-loops, for example:

```python
for result in model.predict_batch(['image1.jpg','image2.jpg']):
   print(result)
```

> *Note:* Since batch prediction methods return generator object, simple assignment of batch prediction method result
to some variable does not start any inference. Only iterating over that generator object does.

The `predict_batch` method accepts single parameter: an iterator object, for example, a list. You populate your
iterator object with the same type of data you pass to regular `predict()`, i.e. input image path strings,
input image URL string, numpy arrays, or PIL Image objects (in case of PIL image backend).

The `predict_dir` method accepts a filepath to a directory containing graphical files for inference.
You may supply optional `extensions` parameter passing the list of file extensions to process.

The following minimal example demonstrates how to use batch predict to perform AI inference from the
video file:

```python
import degirum as dg
import cv2

# connect to cloud model zoo, load model, set model properties needed for OpenCV
zoo = dg.connect(dg.CLOUD, "https://cs.degirum.com", token="<your cloud API access token>")
model = zoo.load_model("mobilenet_v2_ssd_coco--300x300_quant_n2x_orca_1")
model.image_backend = "opencv"
model.input_numpy_colorspace = "BGR"
stream = cv2.VideoCapture("images/Traffic.mp4") # open video file

# define generator function to produce video frames
def frame_source(stream):
   while True:
   ret, frame = stream.read()
      if not ret:
         break # end of file
      yield frame

# run batch predict on stream of frames from video file
for result in model.predict_batch(frame_source(stream)):
   # show annotated frames
   cv2.imshow("Demo", res.image_overlay)   

stream.release()
```


## Model Parameters

The model behavior can be controlled with various `Model` class properties, which define model parameters.
They can be divided into the following categories:
- parameters, which control how to handle input frames;
- parameters, which control the inference;
- parameters, which control how to display inference results;
- parameters, which control model run-time behavior and provide access to model information

The following table provides complete summary of `Model` class properties arranged by categories.

| Property Name | Description | Possible Values | Default Value |
|---------------|-------------|-----------------|---------|
| *Input Handling Parameters* |
| `image_backend` | package to be used for image processing |`"auto"`, `"pil"`, or `"opencv"`<br>`"auto"` tries PIL first | `"auto"` |
| `input_letterbox_fill_color` | image fill color in case of 'letterbox' padding | 3-element tuple of RGB color | `(0,0,0)` |
| `input_numpy_colorspace` | colorspace for numpy arrays | `"RGB"` or `"BGR"` | `"RGB"` |
| `input_pad_method` | how input image will be padded when resized |`"stretch"`, `"letterbox"`, `"crop-first"`, or `"crop-last"` | `"letterbox"` |
| `input_crop_percentage` | a percentage of input image dimension to retain when `"input_pad_method"` is set to `"crop-first"` or `"crop-last"` | Float value in [0..1] range | `1.0` |
| `input_resize_method` | interpolation algorithm for image resizing | `"nearest"`, `"bilinear"`, `"area"`, `"bicubic"`, `"lanczos"` | `"bilinear"` |
| `save_model_image` | flag to enable/disable saving of model input image in inference results | Boolean value | `False` |
| *Inference Parameters* |
| `output_confidence_threshold` | confidence threshold to reject results with low scores | Float value in [0..1] range | `0.1` |
| `output_max_detections` | maximum number of objects to report for detection models | Integer value | `20` |
| `output_max_detections_per_class` | maximum number of objects to report for each class for detection models | Integer value | `100` |
| `output_max_classes_per_detection` | maximum number of classes to report for detection models | Integer value | `30` |
| `output_nms_threshold` | rejection threshold for non-max suppression |  Float value in [0..1] range | `0.6` |
| `output_pose_threshold` | rejection threshold for pose detection models |  Float value in [0..1] range | `0.8` |
| `output_postprocess_type` | inference result post-processing type. You may set it to `'None'` to bypass post-processing. | String | Model-dependent |
| `output_top_k` | Number of classes with biggest scores to report for classification models. If `0`, report all classes above confidence threshold | Integer value | `0` |
| `output_use_regular_nms` | use regular (per-class) NMS algorithm as opposed to global (class-ignoring) NMS algorithm for detection models | Boolean value | `False` |
| *Display Parameters* |
| `overlay_alpha` | transparency value (alpha-blend weight) for all overlay details | Float value in [0..1] range |`0.5` |
| `overlay_color` | color for drawing all overlay details | 3-element tuple of RGB color or list of 3-element tuples of RGB color  | `(255,255,128)` |
| `overlay_font_scale` | font scaling factor for overlay text | Positive float value | `1.0` |
| `overlay_line_width` | line width in pixels for overlay lines | `3` |
| `overlay_show_labels` | flag to enable drawing class labels of detected objects | Boolean value | `True` |
| `overlay_show_probabilities` | flag to enable drawing probabilities of detected objects | Boolean value | `False` |
| *Control and Information Parameters* |
| `devices_available` | list of inference device indices which can be used for model inference **(read-only)** | List of integer values | N/A |
| `devices_selected` | list of inference device indices selected for model inference | List of integer values | Equal to `devices_available` |
| `label_dictionary` | model class label dictionary **(read-only)** | Dictionary | N/A |
| `measure_time` | flag to enable measuring and collecting inference time statistics | Boolean value | `False` |
| `model_info` | model information object to provide read-only access to model parameters **(read-only)** | `ModelParams` object | N/A |
| `non_blocking_batch_predict` | flag to control the blocking behavior of `predict_batch()` method | Boolean value | `False` |
| `eager_batch_size` | The size of the batch to be used by device scheduler when inferencing this model. The batch is the number of consecutive frames before this model is switched to another model during batch predict. | Integer value in [1..80] range | 8 |
| `frame_queue_depth` | The depth of the model prediction queue. When the queue size reaches this value, the next prediction call will block until there will be space in the queue. | Integer value in [1..160] range | 80 for cloud inference, 8 for other cases |

> *Note:* For segmentation models default value of `overlay_color` is the list of unique colors (RGB tuples). 
The size of the list is equal to the number of model classes. Use `label_dictionary` property to get a list of models classes.

## Model Info

AI models have a lot of static attributes defining various model features and characteristics.
Unlike model properties, these attributes in most cases cannot be changed: they come with the model.

To access all model attributes, you may query read-only model property `degirum.model.Model.model_info`.

> *Note:* New deep copy of model info class is created each time you read this property, so any changes made to this copy
will not affect model behavior.

Model attributes are divided into the following categories:
- Device-related attributes
- Pre-processing-related attributes
- Inference-related attributes
- Post-processing-related attributes

The following table provides a complete summary of model attributes arranged by categories.
The *Attribute Name* column contains the name of the `ModelInfo` class member returned by the `model_info` property.

 *Note:* Each attribute in the *Pre-Processing-Related Attributes* group is a list of values, one per model input.

| Attribute Name | Description | Possible Values |
|----------------|-------------|-----------------|
| *Device-Related Attributes* |
| `DeviceType` | Device type to be used for AI inference of this model | `"ORCA"`: DeGirum Orca,<br> `"EDGETPU"`: Google EdgeTPU,<br> `"MYRIAD"`: Intel Myriad,<br> `"CPU"`: host CPU |
| `RuntimeAgent` | Type of runtime to be used for AI inference of this model | `"N2X"`: DeGirum NNExpress runtime,<br> `"TFLITE"`: Google TFLite runtime|
| `EagerBatchSize` | The size of the batch to be used by device scheduler when inferencing this model. The batch is the number of consecutive frames before this model is switched to another model during batch predict. | Integer number |
| *Pre-Processing-Related Attributes* |
| `InputType` | Model input type | List of the following strings:<br>`"Image"`: image input type,<br>`"Audio"`: audio input type,<br>`"Tensor"`: raw tensor input type |
| `InputN` | Input frame dimension size | `1`<br>Other sizes to be supported |
| `InputH` | Input height dimension size | Integer number |
| `InputW` | Input width dimension size | Integer number |
| `InputC` | Input color dimension size | Integer number |
| `InputQuantEn` | Enable input frame quantization flag (set for quantized models) | Boolean value |
| `InputRawDataType` | Data element type for audio or tensor inputs | List of the following strings:<br>`"DG_UINT8"`: 8-bit unsigned integer,<br>`"DG_INT16"`: 16-bit signed integer,<br>`"DG_FLT"`: 32-bit floating point |
| `InputTensorLayout` | Input tensor shape and layout | List of the following strings:<br>`"NHWC"`: 4-D tensor frame-height-width-color<br>More layouts to be supported |
| `InputColorSpace` | Input image colorspace (sequence of colors in C dimension) | List of the following strings:<br>`"RGB"`, `"BGR"`|
| `InputScaleEn` | Enable global scaling of input data flag | List of boolean values |
| `InputScaleCoeff` | Scaling factor for input data global scaling; applied when `InputScaleEn` is enabled | List of float values |
| `InputNormMean` | Mean value for per-channel input data normalization; applied when both `InputNormMean` and `InputNormStd` are not empty | List of 3-element arrays of float values |
| `InputNormStd` | StDev value for per-channel input data normalization; applied when both `InputNormMean` and `InputNormStd` are not empty | List of 3-element arrays of float values |
| `InputQuantOffset` | Quantization offset for input image quantization | List of float values |
| `InputQuantScale` | Quantization scale for input image quantization | List of float values |
| `InputWaveformSize` | Input waveform size in samples for audio input types | List of positive integer values |
| `InputSamplingRate` | Input waveform sampling rate in Hz for audio input types | List of positive float values |
| `InputResizeMethod` | Interpolation algorithm used for image resizing during model training | List of the following strings:<br>`"nearest"`, `"bilinear"`, `"area"`, `"bicubic"`, `"lanczos"`|
| `InputPadMethod` | How input image was padded when resized during model training | List of the following strings:<br>`"stretch"`,  `"letterbox"` |
| `InputCropPercentage` | How much input image was cropped during model training | Float value in [0..1] range |
| `ImageBackend` | Graphical package used for image processing during model training | List of the following strings:<br>`"pil"`, `"opencv"` |
| *Inference-Related Attributes* |
| `ModelPath` | Path to the model JSON file | String with filepath |
| `ModelInputN` | Model frame dimension size | `1`<br>Other sizes to be supported |
| `ModelInputH` | Model height dimension size | Integer number |
| `ModelInputW` | Model width dimension size | Integer number |
| `ModelInputC` | Model color dimension size | Integer number |
| `ModelQuantEn` | Enable input frame quantization flag (set for quantized models) | Boolean value |
| *Post-Processing-Related Attributes* |
| `OutputNumClasses` | Number of classes model detects | Integer value |
| `OutputSoftmaxEn` | Enable softmax step in post-processing flag | Boolean value |
| `OutputClassIDAdjustment` | Class ID adjustment: number subtracted from the class ID reported by the model | Integer value |
| `OutputPostprocessType` | Post-processing type | `"Classification"`, `"Detection"`, `"DetectionYolo"`, `"PoseDetection"`, `"HandDetection"`, `"FaceDetect"`, `"Segmentation"`, `"BodyPix"`, `"Python"`<br>Other types to be supported |
| `OutputConfThreshold` | Confidence threshold to reject results with low scores | Float value in [0..1] range |
| `OutputNMSThreshold` | Rejection threshold for non-max suppression |  Float value in [0..1] range |
| `OutputTopK` | Number of classes with biggest scores to report for classification models | Integer number |
| `MaxDetections` | Maximum number of objects to report for detection models | Integer number |
| `MaxDetectionsPerClass` | Maximum number of objects to report for each class for detection models | Integer number |
| `MaxClassesPerDetection` | Maximum number of classes to report for detection models | Integer number |
| `UseRegularNMS` | Use regular (per-class) NMS algorithm as opposed to global (class-ignoring) NMS algorithm for detection models | Boolean value |

## Inference Advanced Topics

### Selecting Devices for Inference

Every AI model in a model zoo is designed to work on a particular hardware, either on AI accelerator hardware
such as DeGirum Orca, or on host computer CPU. Imagine the situation when the host computer is equipped with
multiple hardware devices of a given type, and you run multiple inferences of a model designed for this device
type. In this case by default **all available** hardware devices of this type will be used for this model inferences.
This guarantees top inference performance in the case of single model running on all available devices.

To get the information about available devices you query `degirum.model.Model.devices_available` property.
It returns the list of device indices of all available devices of the type this model is designed for.
Those indices are zero-based, so if your host computer has a single device of a given type, the returned list
would contain single zero element: `[0]`. In case of two devices it will be `[0, 1]` and so on.

In certain cases you may want to limit the model inference to particular subset of available devices.
For example, you have two devices and you want to run concurrent inference of two models.
In default case both devices would be used for both model inferences causing the models to be reloaded to
devices each time you run the inference of another model. Even if the model loading for DeGirum Orca devices
is extremely fast, it still may cause performance degradation. In this case you may want to run the first model
inference only on the first device, and the second model inference only on the second device.
To do so you need to assign `degirum.model.Model.devices_selected` property of each model object to contain
the list of device indices you want your model to run on. In our example you need to assign the list `[0]` to the
`devices_selected` property of the first model object, and the list `[1]` to the second model object.

In general, the list you assign to the `devices_selected` property should contain only indices occurred in the
list returned by the `devices_available` property.

> *Note*: since the inference device assignment for cloud inferences is performed dynamically, and actual
AI farm node configuration is unknown until the inference starts, the `devices_available` property for such use case
always returns the full list of available devices.

### Handling Multiple Streams of Frames

The Model class interface has a method, `degirum.model.Model.predict_batch`, which can run multiple predictions
on a sequence of frames. In order to deliver the sequence of frames to the `predict_batch` you implement
an iterable object, which returns your frames one-by-one. One example of iterable object is a regular Python
list, another example is a function, which yields frame data using `yield` statement. Then you pass such iterable
object as an argument to the `predict_batch` method. In turn, the `predict_batch` method returns a generator object,
which yields prediction results using `yield` statement.

All the inference magic with pipelining sequential inferences, asynchronously retrieving inference results,
supporting various inference devices, and AI server vs. local operation modes happens inside the implementation
of `predict_batch` method. All you need to do is to wrap your sequence of frame data in an iterable object, pass this
object to `predict_batch`, and iterate over the generator object returned by `predict_batch` using either
`for`-loop or by repeatedly calling `next()` built-in function on this generator object.

The following example runs the inference on an infinite sequence of frames captured from the camera:

```python
import cv2 # OpenCV
stream = cv2.VideoCapture(0) # open video stream from local camera #0

def source(): # define iterator function, which returns frames from camera
   while True:
      ret, frame = stream.read()
      yield frame

for result in model.predict_batch(source()): # iterate over inference results
   cv2.imshow("AI camera", res.image_overlay) # process result
```

But what if you need to run multiple concurrent inferences of multiple asynchronous data streams with different frame
rates? The simple approach when you combine two generators in one loop either using `zip()` built-in function or by
manually calling `next()` built-in function for every generator in a loop body will not work effectively.

Non-working example 1. Using `zip()` built-in function:

```python
batch1 = model1.predict_batch(source1()) # generator object for the first model
batch2 = model2.predict_batch(source2()) # generator object for the second model
for result1, result2 in zip(batch1, batch2)
   # process result1 and result2
```

Non-working example 2. Using `next()` built-in function:

```python
batch1 = model1.predict_batch(source1()) # generator object for the first model
batch2 = model2.predict_batch(source2()) # generator object for the second model
while True:
   result1 = next(batch1)
   result2 = next(batch2)
   # process result1 and result2
```

The reason is that the Python runtime has Global Interpreter Lock (GIL), which allows running only one thread at a time
blocking the execution of other threads. So if the currently running thread is itself blocked by waiting for
the next frame or waiting for the next inference result, all other threads are blocked as well.

For example, if the frame rate of `source1()` is slower than the frame rate of `source2()` and assuming that the
model inference frame rates are higher than the corresponding source frame rates, then the code above will
spend most of the time waiting for the next frame from `source1()`, not letting frames from `source2()` to be retrieved,
so the `model2` will not get enough frames and will idle, losing performance.

Another example is when the inference latency of `model1` is higher than the inference queue depth expressed in time
(this is the product of the inference queue depth expressed in frames and the single frame inference time).
In this case when the `model1` inference queue is full, but inference result is not ready yet, the code above will
block on waiting for that inference result inside `next(batch1)` preventing any operations with `model2`.

To get around such blocks the special **non-blocking mode** of batch predict operation is implemented. You turn
on this mode by assigning `True` to `degirum.model.Model.non_blocking_batch_predict` property.

When non-blocking mode is enabled, the generator object returned by `predict_batch()` method accepts `None`
from the input iterable object. This allows you to design non-blocking frame data source iterators: when no data
is available, such iterator just yields `None` without waiting for the next frame. If `None` is returned from the
input iterator, the model predict step is simply **skipped** for this iteration.

Also in non-blocking mode when no inference results are available in the result queue at some iteration,
the generator yields `None` result. This allows to continue execution of the code which operates with another model.

In order to operate in non-blocking mode you need to modify your code the following way:
1. Modify frame data source iterator to return `None` if no frame is available yet, instead of waiting for the
next frame.
2. Modify inference loop body to deal with `None` results by simply skipping them.


### Measure Inference Timing

The `degirum.model.Model` class has a facility to measure and collect model inference time information.
To enable inference time collection assign `True` to  `degirum.model.Model.measure_time` property.

When inference timing collection is enabled, the durations of individual steps for each frame prediction are
accumulated in internal statistic accumulators.

To reset time statistic accumulators you use `degirum.model.Model.reset_time_stats` method.

To retrieve time statistic accumulators you use `degirum.model.Model.time_stats` method.
This method returns a dictionary with time statistic objects. Each time statistic object accumulates time statistics
for particular inference step over all frame predictions happened since the timing collection was enabled or reset.
The statistics includes minimum, maximum, average, and count. Inference steps correspond to dictionary keys.
The following dictionary keys are supported:

| Key | Description |
|-----|-------------|
| `FrameTotalDuration_ms` | Frame total inference duration from the moment when you invoke predict method to the moment when inference results are returned |
| `PythonPreprocessDuration_ms` | Duration of client-side pre-processing step including data loading time and data conversion time |
| `CorePreprocessDuration_ms` | Duration of server-side pre-processing step |
| `CoreInferenceDuration_ms` | Duration of server-side AI inference step |
| `CoreLoadResultDuration_ms` | Duration of server-side data movement step |
| `CorePostprocessDuration_ms` | Duration of server-side post-processing step |

For DeGirum Orca AI accelerator hardware additional dictionary keys are supported:

| Key | Description |
|-----|-------------|
| `DeviceInferenceDuration_ms` | Duration of AI inference computations on AI accelerator IC excluding data transfers |
| `DeviceTemperature_C` | Internal temperature of AI accelerator IC in C |
| `DeviceFrequency_MHz` | Working frequency of AI accelerator IC in MHz |


The time statistics object supports pretty-printing so you can directly print it using regular `print()` statement.
For example, the output of the following statement:

```python
print(model.time_stats()["PythonPreprocessDuration_ms"])
```

... will look like this:

```python
PythonPreprocessDuration_ms: [4.62..6.19..13.01]/335
```

It consists of the inference step name (`PythonPreprocessDuration_ms` in this case) followed by four statistic
values presented in a format `[minimum..average..maximum]/count`.


> *Note:* In batch prediction mode many inference phases are pipelined so the pre- and post-processing steps of one 
frame may be executed in parallel with the AI inference step of another frame. Therefore actual frame rate may be 
higher than the frame rate calculated by `FrameTotalDuration_ms` statistic.

> *Note:* `PythonPreprocessDuration_ms` statistic includes data loading time and data conversion time.
This can give very different results for different ways of loading input frame data. For example, if you provide image
URLs for inference, then the `PythonPreprocessDuration_ms` will include image downloading time, which can be much
higher compared with the case when you provide the image as numpy array, which does not require any downloading.

The following example shows how to use time statistics collection interface.
It assumes that the `model` variable is the model created by `load_model()`.

```python
model.measure_time = True # enable accumulation of time statistics

# perform batch prediction
for result in model.predict_batch(source()):
   # process result
   pass

stats = model.time_stats() # query time statistics dictionary

# pretty-print frame total inference duration statistics
print(stats["FrameTotalDuration_ms"])

# print average duration of AI inference step
print(stats["CoreInferenceDuration_ms"].avg)

model.reset_time_stats() # reset time statistics accumulators

# perform one more batch prediction
for result in model.predict_batch(source()):
   # process result
   pass

# print statistics of Python pre-processing step
print(stats["PythonPreprocessDuration_ms"].max)
```

# Configuring and Launching AI Server

PySDK can be used to configure and launch DeGirum AI server on hosts equipped with DeGirum Orca AI accelerator card(s).
This allows you to run AI inferences on this AI server host initiated from remote clients.

You can start AI server process multiple ways:
- running AI server from the shell directly on the host OS;
- running AI server as Linux System Service;
- running AI server inside the Docker container.

## Running AI Server from Shell Directly on Host OS

To run PySDK AI server directly on the host OS, perform the following steps on the host:

- Create or select a user name to be used for all the following configuration steps. This user should have
administrative rights on this host. The user name `ai-user` is used in the instructions below, but it can be changed
to any other user name of your choice.

- For convenience of future maintenance we recommend you to install PySDK into virtual environment, such as
[Miniconda](https://docs.conda.io/en/latest/miniconda.html).

- Make sure you activated your Python virtual environment with the appropriate Python version and that PySDK
installed into this virtual environment.

- Create a directory for the AI server model zoo, and change your current working directory to this directory.
For example:

   ```sh
   mkdir /home/ai-user/zoo
   cd /home/ai-user/zoo
   ```

- If you wish to have your model zoo hosted locally, then you need to download all models from some cloud zoo into
local model zoo directory, created on the previous step. In this case please perform the following steps:

   - If you want to download models from DeGirum Public cloud model zoo into the current working directory, then 
   execute the following command:

      ```python
      degirum download-zoo --path . --token <your cloud API token>
      ```

   - If you want to download models from some other cloud zoo, pass the URL of that cloud zoo as `--url` parameter:

      ```python
      degirum download-zoo --path . --token <your cloud API token> --url "https://cs.degirum.com/<zoo URL>"
      ```

      The `<zoo URL>` suffix is the cloud zoo URL in the form `<organization>/<model zoo name>`. You can confirm 
      zoo URL suffix by visiting your cloud user account and opening the model zoo management page via 
      *Management | Models* main menu item.      

- If you wish your AI server to operate only with cloud zoos, just leave local zoo directory 
(`/home/ai-user/zoo` in our example) empty, but it must be created anyway.

- Start DeGirum AI server process by executing the following command:

   ```python
   degirum server start --zoo /home/ai-user/zoo
   ```

The AI server is now up and running, and will run until you press `ENTER` in the same terminal where you started it.

By default, AI server listens to 8778 TCP port. If you want to change the TCP port, pass `--port` command line
argument when launching the server, for example:

```python
python3 -m degirum.server --zoo /home/ai-user/zoo --port 8780
```

## Running AI Server as Linux System Service

It is convenient to automate the process of AI server launch so that it will be started automatically on each
system startup. On Linux-based hosts, you can achieve this by defining and configuring a system service,
which will handle AI server startup.

Please perform the following steps to create, configure, and start the system service:

- Create the configuration file in `/etc/systemd/system` directory named `degirum.service`. You will need
administrative rights to create this file. You can use the following template as an example:

   ```sh
   [Unit]
   Description=DeGirum AI Service
   [Service]
   # You may want to adjust the working directory:
   WorkingDirectory=/home/ai-user/
   # You may want to adjust the path to your Python executable and --zoo model zoo path.
   # Also you may specify server TCP port other than default 8778 by adding --port <port> argument.
   ExecStart=/home/ai-user/miniconda3/bin/python -m degirum.server --zoo /home/ai-user/zoo
   Restart=always
   # You may want to adjust the restart time interval:
   RestartSec=10
   SyslogIdentifier=degirum-ai-server
   # You may want to change the user name under which this service will run.
   # This user should have rights to access model zoo directory
   User=ai-user
   [Install]
   WantedBy=multi-user.target
   ```

- Please replace `/home/ai-user/zoo` path with the actual path to your local model zoo.
   Please refer to the [Running AI Server from Shell Directly on Host OS](#running-ai-server-from-shell-directly-on-host-os) 
   section for discussions about model zoo hosting options.

- Start the system service by executing the following command:

   ```bash
   sudo systemctl start degirum.service
   ```

- Check the system service status by executing the following command:

   ```bash
   sudo systemctl status degirum.service
   ```

- If the status is "Active", it means that the configuration is good and the service is up and running.
- Then enable the service for automatic startup by executing the following command:

   ```bash
   sudo systemctl enable degirum.service
   ```

## Running AI Server Inside Docker Container

To run PySDK AI server inside the Docker container, perform the following steps on the host:

- Install [Docker Desktop](https://www.docker.com/get-started/) on a host computer where you want to
build or run the docker container.

- Follow the instructions provided on the [DeGirum AI Server Docker Hub page](https://hub.docker.com/r/degirum/aiserver). 
Or, in few words, run the following command:

   ```bash
      docker run --name aiserver -d -p 8778:8778 -v /home/ai-user/zoo:/zoo --privileged degirum/aiserver:latest
   ```

   - Please replace `/home/ai-user/zoo` path with the actual path to your local model zoo.
   Please refer to the [Running AI Server from Shell Directly on Host OS](#running-ai-server-from-shell-directly-on-host-os)
   section for discussions about model zoo hosting options.

   - Use `--privileged` option if you have AI hardware accelerator(s) in stalled on your system. In case of CPU-only
   inferences you may omit it.

   - AI server inside Docker container always listens to 8778 TCP port. `-p 8778:8778` option maps Docker container 
   TCP port to host TCP port. If you want to change the host TCP port, change the first number before the colon, 
   for example: `-p 9999:8778` will map the host port 9999 to the container port 8778.


## Connecting to AI Server from Client Side

Now your AI server is up and running and you may connect to it from Python scripts using PySDK.

If you want to work with models from local AI server model zoo, you pass the AI server network hostname or its IP 
address to the `degirum.connect` PySDK function and do not specify other parameters:

```python
import degirum as dg
model_zoo = dg.connect(host_address)
```

If you run your PySDK script on the **same** host as the AI server, you may use the `"localhost"` string as a network
hostname.

In local Linux networks with standard mDNS configuration the network hostname is a concatenation of the local hostname
as returned by `hostname` command and `.local` suffix, for example, if `hostname` command returns `ai-host`, then the
network hostname will be `ai-host.local`

If your server listens to a TCP port other than default `8778`, you append the TCP port number to the hostname
separated by colon, for example, `"localhost:9999"`.

If you want to work with models from some cloud model zoo of your choice, you pass a cloud zoo URL and cloud API access
token as the second and the third parameter. The cloud model zoo URL is specified in the 
`"https://cs.degirum.com/<zoo URL>"` format (see more on that in 
[Configuration for Cloud Inference](#configuration-for-cloud-inference) section):

```python
import degirum as dg
model_zoo = dg.connect( host_address, "https://cs.degirum.com/<zoo URL>", token = "<your cloud API access token>")
```


## Updating AI Server Local Model Zoo

If you need to update AI Server local model zoo you need to perform the following steps:

- Manage your model zoo directory:
  - Add new models by downloading them from the cloud zoo the way described in the beginning of this chapter.
  - Remove models by deleting model subdirectories.

- If you started your AI server **not** in Docker container, then tell the AI server to rescan the local model zoo
directory by executing the following command on the **same host**, where the AI server runs:

   ```bash
   degirum server rescan-zoo
   ```

- If you started your AI server in the Docker container, then restart the container by executing the following command
(assuming that the container was started with `--name aiserver` option):

   ```bash
   docker restart aiserver
   ```

# PySDK Command-Line Interface

As a part of PySDK installation, the `degirum` executable
[console script](https://setuptools.pypa.io/en/latest/userguide/entry_point.html#console-scripts)
is installed into the system path. It implements command-line interface (CLI) to various PySDK management facilities.
This console script extends PySDK functionality through the mechanism of
[entry points](https://setuptools.pypa.io/en/latest/userguide/entry_point.html#entry-points).

The PySDK CLI supports the following commands:

| Command | Description |
|---------|-------------|
| `download-zoo` | Command to download AI models from the cloud model zoo |
| `server` | Command to control the operation of AI server |
| `sys-info` | Command to obtain system information dump |
| `trace` | Command to manage AI server tracing facility |

You invoke the console script passing the command from the table above as its first argument followed by
command-specific parameters described in the following sections.

```bash
degirum <command> <arguments>
```

## Download Model Zoo Command

Using this command you can download ML models from the cloud model zoo of your choice specified by URL.
The command has the following parameters:

| Parameter        | Description | Possible Values | Default |
|------------------|-------------|-----------------|---------|
| `--path`         | Local filesystem path to store models downloaded from a model zoo repo | Valid local directory path | Current directory |
| `--url`          | Cloud model zoo URL | `"https://cs.degirum.com[/<zoo URL>]"` | `"https://cs.degirum.com"` |
| `--token`        | Cloud API access token | Valid token obtained at cs.degirum.com | Empty |
| `--model_family` | Model family name filter: model name substring or regular expression | Any | Empty |
| `--device`       | Target inference device filter | `ORCA, CPU, EDGETPU, MYRIAD` | Empty |
| `--runtime`      | Runtime agent type filter | `N2X, TFLITE, OPENVINO`| Empty |
| `--precision`    | Model calculation precision filter | `QUANT, FLOAT` |  None |
| `--pruned`       | Model density filter | `PRUNED, DENSE` |  None |

The URL parameter is specified in the `"https://cs.degirum.com/<zoo URL>"` format. Here `<zoo URL>` suffix is the
name of the cloud model zoo in the form of `<organization>/<zoo>`. You can obtain the model zoo URL suffix on 
DeGirum Cloud Portal site https://cs.degirum.com under *Management | Models* main menu item: just select the model 
zoo you want to access to open the model zoo page and click copy button near the model zoo name to copy the model 
zoo URL suffix into the clipboard.

Filter parameters work the same way as in `degirum.zoo_manager.ZooManager.list_models` method: they allow you
downloading only models satisfying filter conditions.

Once models are downloaded into the directory specified by `--path` parameter, you may use this directory as the
model zoo to be served by AI server (see [Server Control Command](#server-control-command) section).

**Example**.

Download models for ORCA device type from DeGirum Public cloud model zoo into `./my-zoo` directory.

```bash
degirum download-zoo --path ./my-zoo --token <your cloud API access token> --device ORCA
```
Here `<your cloud API access token>` is your cloud API access token, which you can generate on DeGirum Cloud Portal 
site https://cs.degirum.com under *Management | My Tokens* main menu item.

## Server Control Command

Using this command you can start AI server, shut it down, or request AI server to rescan its local model zoo.

> You can control only AI server which runs on the same host where you execute this command.
The control of remote AI servers is disabled for security reasons.

This command has the following subcommands, which are passed just after the command:

| Sub-command  | Description |
|--------------|-------------|
| `start`      | Start AI server |
| `rescan-zoo` | Request AI server to rescan its model zoo |
| `shutdown`   | Request AI server to shutdown |

The command has the following parameters:

| Parameter        | Applicable To | Description | Possible Values | Default |
|------------------|---------------|-------------|-----------------|---------|
| `--zoo`          | `start`       | Local model zoo directory to serve models from (applicable only to `start` subcommand) | Any valid path | Current directory |
| `--quiet`        | `start`       | Do not display any output (applicable only to `start` subcommand) | N/A | Disabled |
| `--port`         | `start`       | TCP port to bind AI server to | 1...65535 | 8778 |


**Example**.

Start AI server to serve models from `./my-zoo` directory and bind it to default port:

```bash
degirum server start --zoo ./my-zoo
```

## System Info Command

Using this command you can query the system information either for the local system or for the remote AI server host.
The system info dump is printed to the console.

The command has the following parameters:

| Parameter        | Description | Possible Values | Default |
|------------------|-------------|-----------------|---------|
| `--host` | Remote AI server hostname or IP address; omit to query local system | Valid hostname, IP address, or empty | Empty |


**Example**.

Query system info from remote AI server at IP address `192.168.0.101`:

```bash
degirum sys-info --host 192.168.0.101
```


## Trace Management Command

Using this command you can manage AI server tracing facility.

> AI server tracing facility is used for AI server debugging and time profiling.
It is designed mostly for DeGirum customer support and not intended to be used by the end user directly.

This command has the following subcommands, which are passed just after the command:

| Sub-command  | Description |
|--------------|-------------|
| `list`       | List all available trace groups |
| `configure`  | Configure trace levels for trace groups |
| `read`       | Read trace data to file |

The command has the following parameters:

| Parameter        | Applicable To   | Description | Possible Values | Default |
|------------------|-----------------|-------------|-----------------|---------|
| `--host`         | All subcommands | Remote AI server hostname or IP address | Valid hostname or IP address | `localhost` |
| `--file`         | `read`          | Filename to save trace data into; omit to print to console | Valid local filename | Empty |
| `--filesize`     | `read`          | Maximum trace data size to read | Any integer number | `10000000` |
| `--basic`        | `configure`     | Set `Basic` trace level for a given list of trace groups | One or multiple trace group names as returned by `list` sub-command | Empty |
| `--detailed`     | `configure`     | Set `Detailed` trace level for a given list of trace groups | One or multiple trace group names as returned by `list` sub-command | Empty |
| `--full`         | `configure`     | Set `Full` trace level for a given list of trace groups | One or multiple trace group names as returned by `list` sub-command | Empty |

**Examples**.

Query AI server at `192.168.0.101` address for the list of available trace groups and print it to console:

```bash
degirum trace list --host 192.168.0.101
```

Configure tracing for AI server on `localhost`: by setting various tracing levels for various trace groups:

```bash
degirum trace configure --basic CoreTaskServer --detailed OrcaDMA OrcaRPC --full CoreRuntime
```

Read trace data from AI server on `localhost` and save it to a file `./my-trace-1.txt`

```bash
degirum trace read --file ./my-trace-1.txt
```

# API Documentation
