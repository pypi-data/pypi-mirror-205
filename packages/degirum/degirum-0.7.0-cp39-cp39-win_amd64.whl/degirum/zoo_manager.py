#
# zoo_manager.py - DeGirum Python SDK: zoo manager implementation
# Copyright DeGirum Corp. 2022
#
# Implements DeGirum zoo manager class
#

import pdb
from pathlib import Path
from typing import Tuple, Union
import logging

from .log import log_wrap

from .exceptions import DegirumException
from ._zoo_accessor import (
    _SingleFileZooURLAccessor,
    _LocalHWCloudZooAccessor,
    _AIServerLocalZooAccessor,
    _AIServerCloudZooAccessor,
    _CloudServerZooAccessor,
    _CloudZooAccessorBase,
)

logger = logging.getLogger(__name__)


class ZooManager:
    """Class that manages a model zoo.

    A model zoo in terminology of PySDK is a collection of AI models and simultaneously an ML inference engine
    type and location.

    Depending on the deployment location, there are several types of model zoos supported by PySDK:
    - local model zoo: deployed on the local file system of the PySDK installation host. Inferences are performed on the
    same host using AI accelerators installed on that host.
    - AI server model zoo: deployed on remote host with DeGirum AI server running on that host. Inferences are performed
    by DeGirum AI server on that remote host.
    - Cloud Platform model zoo: deployed on DeGirum Cloud Platform. Inferences are performed by DeGirum Cloud Platform
    servers.

    The type of the model zoo is defined by the URL string which you pass as `zoo_url` parameter into the constructor.

    Zoo manager provides the following functionality:
    - list and search models available in the connected model zoo;
    - create AI model handling objects to perform AI inferences;
    - request various AI model parameters.
    """

    _default_cloud_url = _CloudZooAccessorBase._default_cloud_url
    """ DeGirum public zoo URL. You can freely use all models available in this public model zoo """

    def __dir__(self):
        return [
            "list_models",
            "load_model",
            "model_info",
        ]

    @log_wrap
    def __init__(
        self,
        zoo_url: Union[None, str, Tuple[str, str]] = None,
        token: str = "",
    ):
        """Constructor.

        > *Note:* typically, you never construct `ZooManager` objects yourself: instead you call `degirum.connect`
        function to create `ZooManager` instances for you.

        Parameters:
        - `zoo_url`: URL string or tuple, which defines the model zoo to connect to and inference engine to operate with.
        - `token`: security token string to be passed to the model zoo manager for authentication and authorization.

        ZooManager hierarchy of classes serve dual purpose (thus creating some level of confusion):
        - particular implementation of ZooManager selects what engine will do the inference
          (Cloud Platform, AI Sever, or local hardware);
        - it selects the model zoo to take models from (cloud zoo, AI server local zoo, or single model file).

        > *Note 1*: for DeGirum Cloud Platform connections you need cloud API access token. To obtain this token you 
        need to open a user account on [DeGirum cloud platform](https://cs.degirum.com). Please login to your account
        and go to the token generation page to generate API access token.

        > *Note 2*: when dealing with cloud model zoos you specify the cloud zoo URL in the following format:
        `<cloud server URL>[/<zoo URL>]`. The `<cloud server URL>` part is the cloud platform root URL,
        typically `cs.degirum.com`. The optional `<zoo URL>` part is the cloud zoo URL in the form
        `<organization>/<model zoo name>`. You can confirm zoo URL by visiting your cloud user account and opening
        the model zoo management page. If `<zoo URL>` is not specified, then DeGirum public model zoo
        is used.

        The following use cases are supported:

        1. You want to perform **cloud inferences** and take models from some **cloud model zoo**.
        In this case you specify the `zoo_url` parameter as `"dgcps://<cloud server URL>[/<zoo URL>]"`.
        The `dgcps://` prefix specifies that you want to use cloud inference. It is followed by the cloud zoo URL
        in a format described in the *Note 2* above. Also you specify the `token` parameter equal
        to your API access token.

        2. You want to perform inferences on some **AI server** and take models from its **local model zoo**.
        In this case you specify the `zoo_url` parameter as the hostname or IP address of the AI server machine
        you want to connect to. As a client of the AI server you do not have control on what models are served by
        that AI server: once the AI server model zoo is deployed, it cannot be changed from the client side unless
        the AI server administrator explicitly updates the model zoo on that AI server.
        The `token` parameter is not needed in this use case.

        3. You want to perform inferences on some **AI server** and take models from some **cloud model zoo**.
        In this case you specify the `zoo_url` parameter as a **tuple**. The first element of this tuple should contain
        the hostname or IP address of the AI server machine you want to connect to. The second element of this tuple
        should contain the cloud model zoo URL in the `"https://<cloud server URL>[/<zoo URL>]"` format, described
        in the *Note 2* above. Also you specify the `token` parameter equal to your API access token.

        4. You want to perform inferences on **local AI hardware** and take models from some **cloud model zoo**.
        In this case you specify the `zoo_url` parameter as `"https://<cloud server URL>[/<zoo URL>]"`.
        The `https://` prefix specifies that you want to use local (not cloud) inference. It is followed by the
        cloud zoo URL in a format described in the *Note 2* above. Also you specify the `token` parameter equal
        to your API access token.

        5. You want to perform inferences on **local AI hardware** and use **particular model** from your local drive.
        In this case you specify `zoo_url` parameter equal to the path to the model .json configuration file.
        This option is mostly used for testing/debugging new models during model development which are not
        yet released in any model zoo. The `token` parameter is not needed this use case.

        When connecting to a model zoo the list of AI models is requested and then stored inside the `ZooManager`
        object.
        """
        if not zoo_url:
            zoo_url = ZooManager._default_cloud_url

        if isinstance(zoo_url, str):
            url_lowercase = zoo_url.lower()

            if url_lowercase.startswith("dgcps://") or url_lowercase.startswith(
                "dgcp://"
            ):
                # use case 1: cloud inference + cloud zoo
                logger.info(f"Connecting to cloud inference and zoo at '{zoo_url}'")
                self._zoo = _CloudServerZooAccessor(f"http{zoo_url[4:]}", token=token)
            elif url_lowercase.startswith("https://") or url_lowercase.startswith(
                "http://"
            ):
                # use case 4: local inference + cloud zoo
                logger.info(
                    f"Connecting with local inference to cloud zoo at '{zoo_url}'"
                )
                self._zoo = _LocalHWCloudZooAccessor(zoo_url, token=token)
            elif url_lowercase.endswith(".json"):
                # use case 5: local inference + local model
                logger.info(f"Local inference with local model '{zoo_url}'")
                if Path(zoo_url).exists() and Path(zoo_url).is_file():
                    self._zoo = _SingleFileZooURLAccessor(zoo_url)
                else:
                    raise DegirumException(
                        f"ZooManager: incorrect model file path '{zoo_url}'"
                    )
            else:
                # use case 3: AI server inference + local zoo
                logger.info(f"Connecting to AI server '{zoo_url}' with local zoo")
                self._zoo = _AIServerLocalZooAccessor(zoo_url)

        elif (
            isinstance(zoo_url, tuple)
            and len(zoo_url) == 2
            and isinstance(zoo_url[0], str)
            and isinstance(zoo_url[1], str)
        ):
            # use case 4: AI server inference + cloud zoo
            logger.info(
                f"Connecting to AI server '{zoo_url[0]}' with cloud zoo '{zoo_url[1]}'"
            )
            self._zoo = _AIServerCloudZooAccessor(
                host=zoo_url[0], url=zoo_url[1], token=token
            )

        else:
            raise DegirumException(
                f"ZooManager: unrecognized format of zoo URL parameter: '{zoo_url}'"
            )

    @log_wrap
    def list_models(self, *args, **kwargs):
        """Get a list of names of AI models available in the connected model zoo which match specified
        filtering criteria.

        Parameters:
        - `model_family`: model family name filter. When you pass a string, it will be used as search substring
        in the model name. For example, `"yolo"`, `"mobilenet"`.
        You may also pass `re.Pattern` object: in this case it will do regular expression pattern search.
        - `device`: target inference device - string or list of strings of device names.
        Possible names: `"orca"`, `"cpu"`, `"edgetpu"`, `"myriad"`
        - `precision`: model calculation precision - string or list of strings of model precision labels.
        Possible labels: `"quant"`, `"float"`
        - `pruned`: model density - string or list of strings of model density labels.
        Possible labels: `"dense"`, `"pruned"`
        - `runtime`: runtime agent type - string or list of strings of runtime agent types:
        Possible types: `"n2x"`, `"tflite"`, `"openvino"`

        Returns the list of model name strings matching specified filtering criteria.
        Use a string from that list as a parameter of `load_model()` method.

        **Example**. Find all models of `"yolo"` family capable to run either on CPU or on DeGirum Orca AI accelerator
        from all registered model zoos:
        ```python
            yolo_model_list = zoo_manager.list_models("yolo", device=["cpu", "orca"])
        ```
        """
        return self._zoo.list_models(*args, **kwargs)

    @log_wrap
    def load_model(self, model_name: str):
        """Create and return the model handling object for given model name.

        Parameters:
        - `model_name`: model name string identifying the model to load.
            It should exactly match the model name as it is returned by `list_models()` method.

        Returns model handling object `degirum.model.Model`.
        Using this object you perform AI inferences on this model and also configure various model properties, which
        define how to do input image preprocessing and inference result post-processing:
        - call `degirum.model.Model.predict` method to perform AI inference of a single frame. Inference result object
        is returned;
        - for more efficient pipelined batch predictions call `degirum.model.Model.predict_batch` or
        `degirum.model.Model.predict_dir` methods to perform AI inference of multiple frames;
        - configure the following image pre-processing properties:
            - `degirum.model.Model.input_resize_method` - to set input image resize method;
            - `degirum.model.Model.input_pad_method` - to set input image padding method;
            - `degirum.model.Model.input_letterbox_fill_color` - to set letterbox padding color;
            - `degirum.model.Model.image_backend` - to select image processing library;
        - configure the following model post-processing properties:
            - `output_confidence_threshold` - to set confidence threshold;
            - `output_nms_threshold` - to set non-max suppression threshold;
            - `output_top_k` - to set top-K limit for classification models;
            - `output_pose_threshold` - to set pose detection threshold for pose detection models;
        - configure the following overlay image generation properties:
            - `degirum.model.Model.overlay_color` - to set color for inference results drawing on overlay image;
            - `degirum.model.Model.overlay_line_width` - to set line width for inference results drawing on overlay image;
            - `degirum.model.Model.overlay_show_labels` - to set flag to enable/disable drawing class labels on overlay image;
            - `degirum.model.Model.overlay_show_probabilities` - to set flag to enable/disable drawing class probabilities
            on overlay image;
            - `degirum.model.Model.overlay_alpha` - to set alpha-blend weight for inference results drawing on overlay image;
            - `degirum.model.Model.overlay_font_scale` - to set font scale for inference results drawing on overlay image.

        Inference result object `degirum.postprocessor.InferenceResults` returned by `degirum.model.Model.predict` method
        allows you to access AI inference results:
        - use `degirum.postprocessor.InferenceResults.image` property to access original image;
        - use `degirum.postprocessor.InferenceResults.image_overlay` property to access image with inference results
        drawn on a top of it;
        - use `degirum.postprocessor.InferenceResults.results` property to access the list of numeric inference results.

        """
        return self._zoo.load_model(model_name)

    @log_wrap
    def model_info(self, model_name):
        """Request model parameters for given model name.

        Parameters:
        - `model_name`: model name string. It should exactly match the model name as it is returned by `list_models()`
        method.

        Returns model parameter object which provides read-only access to all model parameters.

        > *Note*: you cannot modify actual model parameters - any changes of model parameter object returned by this
        method are not applied to the real model. Use properties of model handling objects returned by `load_model()`
        method to change parameters of that particular model instance on the fly.
        """
        return self._zoo.model_info(model_name)

    @log_wrap
    def _rescan_zoo(self):
        """Rescan connected model zoo to update the list of available models."""
        self._zoo.rescan_zoo()
