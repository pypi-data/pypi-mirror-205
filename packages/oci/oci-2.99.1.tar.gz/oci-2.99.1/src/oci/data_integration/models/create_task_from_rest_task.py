# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_task_details import CreateTaskDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateTaskFromRestTask(CreateTaskDetails):
    """
    The information about the Generic REST task. The endpoint and cancelEndpoint  properties are deprecated, use the properties executeRestCallConfig, cancelRestCallConfig and pollRestCallConfig for execute, cancel and polling of the calls.
    """

    #: A constant which can be used with the method_type property of a CreateTaskFromRestTask.
    #: This constant has a value of "GET"
    METHOD_TYPE_GET = "GET"

    #: A constant which can be used with the method_type property of a CreateTaskFromRestTask.
    #: This constant has a value of "POST"
    METHOD_TYPE_POST = "POST"

    #: A constant which can be used with the method_type property of a CreateTaskFromRestTask.
    #: This constant has a value of "PATCH"
    METHOD_TYPE_PATCH = "PATCH"

    #: A constant which can be used with the method_type property of a CreateTaskFromRestTask.
    #: This constant has a value of "DELETE"
    METHOD_TYPE_DELETE = "DELETE"

    #: A constant which can be used with the method_type property of a CreateTaskFromRestTask.
    #: This constant has a value of "PUT"
    METHOD_TYPE_PUT = "PUT"

    #: A constant which can be used with the api_call_mode property of a CreateTaskFromRestTask.
    #: This constant has a value of "SYNCHRONOUS"
    API_CALL_MODE_SYNCHRONOUS = "SYNCHRONOUS"

    #: A constant which can be used with the api_call_mode property of a CreateTaskFromRestTask.
    #: This constant has a value of "ASYNC_OCI_WORKREQUEST"
    API_CALL_MODE_ASYNC_OCI_WORKREQUEST = "ASYNC_OCI_WORKREQUEST"

    #: A constant which can be used with the api_call_mode property of a CreateTaskFromRestTask.
    #: This constant has a value of "ASYNC_GENERIC"
    API_CALL_MODE_ASYNC_GENERIC = "ASYNC_GENERIC"

    #: A constant which can be used with the cancel_method_type property of a CreateTaskFromRestTask.
    #: This constant has a value of "GET"
    CANCEL_METHOD_TYPE_GET = "GET"

    #: A constant which can be used with the cancel_method_type property of a CreateTaskFromRestTask.
    #: This constant has a value of "POST"
    CANCEL_METHOD_TYPE_POST = "POST"

    #: A constant which can be used with the cancel_method_type property of a CreateTaskFromRestTask.
    #: This constant has a value of "PATCH"
    CANCEL_METHOD_TYPE_PATCH = "PATCH"

    #: A constant which can be used with the cancel_method_type property of a CreateTaskFromRestTask.
    #: This constant has a value of "DELETE"
    CANCEL_METHOD_TYPE_DELETE = "DELETE"

    #: A constant which can be used with the cancel_method_type property of a CreateTaskFromRestTask.
    #: This constant has a value of "PUT"
    CANCEL_METHOD_TYPE_PUT = "PUT"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateTaskFromRestTask object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.CreateTaskFromRestTask.model_type` attribute
        of this class is ``REST_TASK`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this CreateTaskFromRestTask.
            Allowed values for this property are: "INTEGRATION_TASK", "DATA_LOADER_TASK", "PIPELINE_TASK", "SQL_TASK", "OCI_DATAFLOW_TASK", "REST_TASK"
        :type model_type: str

        :param key:
            The value to assign to the key property of this CreateTaskFromRestTask.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this CreateTaskFromRestTask.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this CreateTaskFromRestTask.
        :type parent_ref: oci.data_integration.models.ParentReference

        :param name:
            The value to assign to the name property of this CreateTaskFromRestTask.
        :type name: str

        :param description:
            The value to assign to the description property of this CreateTaskFromRestTask.
        :type description: str

        :param object_status:
            The value to assign to the object_status property of this CreateTaskFromRestTask.
        :type object_status: int

        :param identifier:
            The value to assign to the identifier property of this CreateTaskFromRestTask.
        :type identifier: str

        :param input_ports:
            The value to assign to the input_ports property of this CreateTaskFromRestTask.
        :type input_ports: list[oci.data_integration.models.InputPort]

        :param output_ports:
            The value to assign to the output_ports property of this CreateTaskFromRestTask.
        :type output_ports: list[oci.data_integration.models.OutputPort]

        :param parameters:
            The value to assign to the parameters property of this CreateTaskFromRestTask.
        :type parameters: list[oci.data_integration.models.Parameter]

        :param op_config_values:
            The value to assign to the op_config_values property of this CreateTaskFromRestTask.
        :type op_config_values: oci.data_integration.models.ConfigValues

        :param config_provider_delegate:
            The value to assign to the config_provider_delegate property of this CreateTaskFromRestTask.
        :type config_provider_delegate: oci.data_integration.models.CreateConfigProvider

        :param registry_metadata:
            The value to assign to the registry_metadata property of this CreateTaskFromRestTask.
        :type registry_metadata: oci.data_integration.models.RegistryMetadata

        :param auth_details:
            The value to assign to the auth_details property of this CreateTaskFromRestTask.
        :type auth_details: oci.data_integration.models.AuthDetails

        :param auth_config:
            The value to assign to the auth_config property of this CreateTaskFromRestTask.
        :type auth_config: oci.data_integration.models.AuthConfig

        :param endpoint:
            The value to assign to the endpoint property of this CreateTaskFromRestTask.
        :type endpoint: oci.data_integration.models.Expression

        :param method_type:
            The value to assign to the method_type property of this CreateTaskFromRestTask.
            Allowed values for this property are: "GET", "POST", "PATCH", "DELETE", "PUT"
        :type method_type: str

        :param headers:
            The value to assign to the headers property of this CreateTaskFromRestTask.
        :type headers: object

        :param json_data:
            The value to assign to the json_data property of this CreateTaskFromRestTask.
        :type json_data: str

        :param api_call_mode:
            The value to assign to the api_call_mode property of this CreateTaskFromRestTask.
            Allowed values for this property are: "SYNCHRONOUS", "ASYNC_OCI_WORKREQUEST", "ASYNC_GENERIC"
        :type api_call_mode: str

        :param cancel_endpoint:
            The value to assign to the cancel_endpoint property of this CreateTaskFromRestTask.
        :type cancel_endpoint: oci.data_integration.models.Expression

        :param cancel_method_type:
            The value to assign to the cancel_method_type property of this CreateTaskFromRestTask.
            Allowed values for this property are: "GET", "POST", "PATCH", "DELETE", "PUT"
        :type cancel_method_type: str

        :param execute_rest_call_config:
            The value to assign to the execute_rest_call_config property of this CreateTaskFromRestTask.
        :type execute_rest_call_config: oci.data_integration.models.ExecuteRestCallConfig

        :param cancel_rest_call_config:
            The value to assign to the cancel_rest_call_config property of this CreateTaskFromRestTask.
        :type cancel_rest_call_config: oci.data_integration.models.CancelRestCallConfig

        :param poll_rest_call_config:
            The value to assign to the poll_rest_call_config property of this CreateTaskFromRestTask.
        :type poll_rest_call_config: oci.data_integration.models.PollRestCallConfig

        :param typed_expressions:
            The value to assign to the typed_expressions property of this CreateTaskFromRestTask.
        :type typed_expressions: list[oci.data_integration.models.TypedExpression]

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'name': 'str',
            'description': 'str',
            'object_status': 'int',
            'identifier': 'str',
            'input_ports': 'list[InputPort]',
            'output_ports': 'list[OutputPort]',
            'parameters': 'list[Parameter]',
            'op_config_values': 'ConfigValues',
            'config_provider_delegate': 'CreateConfigProvider',
            'registry_metadata': 'RegistryMetadata',
            'auth_details': 'AuthDetails',
            'auth_config': 'AuthConfig',
            'endpoint': 'Expression',
            'method_type': 'str',
            'headers': 'object',
            'json_data': 'str',
            'api_call_mode': 'str',
            'cancel_endpoint': 'Expression',
            'cancel_method_type': 'str',
            'execute_rest_call_config': 'ExecuteRestCallConfig',
            'cancel_rest_call_config': 'CancelRestCallConfig',
            'poll_rest_call_config': 'PollRestCallConfig',
            'typed_expressions': 'list[TypedExpression]'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'name': 'name',
            'description': 'description',
            'object_status': 'objectStatus',
            'identifier': 'identifier',
            'input_ports': 'inputPorts',
            'output_ports': 'outputPorts',
            'parameters': 'parameters',
            'op_config_values': 'opConfigValues',
            'config_provider_delegate': 'configProviderDelegate',
            'registry_metadata': 'registryMetadata',
            'auth_details': 'authDetails',
            'auth_config': 'authConfig',
            'endpoint': 'endpoint',
            'method_type': 'methodType',
            'headers': 'headers',
            'json_data': 'jsonData',
            'api_call_mode': 'apiCallMode',
            'cancel_endpoint': 'cancelEndpoint',
            'cancel_method_type': 'cancelMethodType',
            'execute_rest_call_config': 'executeRestCallConfig',
            'cancel_rest_call_config': 'cancelRestCallConfig',
            'poll_rest_call_config': 'pollRestCallConfig',
            'typed_expressions': 'typedExpressions'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._name = None
        self._description = None
        self._object_status = None
        self._identifier = None
        self._input_ports = None
        self._output_ports = None
        self._parameters = None
        self._op_config_values = None
        self._config_provider_delegate = None
        self._registry_metadata = None
        self._auth_details = None
        self._auth_config = None
        self._endpoint = None
        self._method_type = None
        self._headers = None
        self._json_data = None
        self._api_call_mode = None
        self._cancel_endpoint = None
        self._cancel_method_type = None
        self._execute_rest_call_config = None
        self._cancel_rest_call_config = None
        self._poll_rest_call_config = None
        self._typed_expressions = None
        self._model_type = 'REST_TASK'

    @property
    def auth_details(self):
        """
        Gets the auth_details of this CreateTaskFromRestTask.

        :return: The auth_details of this CreateTaskFromRestTask.
        :rtype: oci.data_integration.models.AuthDetails
        """
        return self._auth_details

    @auth_details.setter
    def auth_details(self, auth_details):
        """
        Sets the auth_details of this CreateTaskFromRestTask.

        :param auth_details: The auth_details of this CreateTaskFromRestTask.
        :type: oci.data_integration.models.AuthDetails
        """
        self._auth_details = auth_details

    @property
    def auth_config(self):
        """
        Gets the auth_config of this CreateTaskFromRestTask.

        :return: The auth_config of this CreateTaskFromRestTask.
        :rtype: oci.data_integration.models.AuthConfig
        """
        return self._auth_config

    @auth_config.setter
    def auth_config(self, auth_config):
        """
        Sets the auth_config of this CreateTaskFromRestTask.

        :param auth_config: The auth_config of this CreateTaskFromRestTask.
        :type: oci.data_integration.models.AuthConfig
        """
        self._auth_config = auth_config

    @property
    def endpoint(self):
        """
        Gets the endpoint of this CreateTaskFromRestTask.

        :return: The endpoint of this CreateTaskFromRestTask.
        :rtype: oci.data_integration.models.Expression
        """
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        """
        Sets the endpoint of this CreateTaskFromRestTask.

        :param endpoint: The endpoint of this CreateTaskFromRestTask.
        :type: oci.data_integration.models.Expression
        """
        self._endpoint = endpoint

    @property
    def method_type(self):
        """
        Gets the method_type of this CreateTaskFromRestTask.
        The REST method to use. This property is deprecated, use ExecuteRestCallConfig's methodType property instead.

        Allowed values for this property are: "GET", "POST", "PATCH", "DELETE", "PUT"


        :return: The method_type of this CreateTaskFromRestTask.
        :rtype: str
        """
        return self._method_type

    @method_type.setter
    def method_type(self, method_type):
        """
        Sets the method_type of this CreateTaskFromRestTask.
        The REST method to use. This property is deprecated, use ExecuteRestCallConfig's methodType property instead.


        :param method_type: The method_type of this CreateTaskFromRestTask.
        :type: str
        """
        allowed_values = ["GET", "POST", "PATCH", "DELETE", "PUT"]
        if not value_allowed_none_or_none_sentinel(method_type, allowed_values):
            raise ValueError(
                "Invalid value for `method_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._method_type = method_type

    @property
    def headers(self):
        """
        Gets the headers of this CreateTaskFromRestTask.
        Headers data for the request.


        :return: The headers of this CreateTaskFromRestTask.
        :rtype: object
        """
        return self._headers

    @headers.setter
    def headers(self, headers):
        """
        Sets the headers of this CreateTaskFromRestTask.
        Headers data for the request.


        :param headers: The headers of this CreateTaskFromRestTask.
        :type: object
        """
        self._headers = headers

    @property
    def json_data(self):
        """
        Gets the json_data of this CreateTaskFromRestTask.
        JSON data for payload body. This property is deprecated, use ExecuteRestCallConfig's payload config param instead.


        :return: The json_data of this CreateTaskFromRestTask.
        :rtype: str
        """
        return self._json_data

    @json_data.setter
    def json_data(self, json_data):
        """
        Sets the json_data of this CreateTaskFromRestTask.
        JSON data for payload body. This property is deprecated, use ExecuteRestCallConfig's payload config param instead.


        :param json_data: The json_data of this CreateTaskFromRestTask.
        :type: str
        """
        self._json_data = json_data

    @property
    def api_call_mode(self):
        """
        Gets the api_call_mode of this CreateTaskFromRestTask.
        The REST invocation pattern to use. ASYNC_OCI_WORKREQUEST is being deprecated as well as cancelEndpoint/MethodType.

        Allowed values for this property are: "SYNCHRONOUS", "ASYNC_OCI_WORKREQUEST", "ASYNC_GENERIC"


        :return: The api_call_mode of this CreateTaskFromRestTask.
        :rtype: str
        """
        return self._api_call_mode

    @api_call_mode.setter
    def api_call_mode(self, api_call_mode):
        """
        Sets the api_call_mode of this CreateTaskFromRestTask.
        The REST invocation pattern to use. ASYNC_OCI_WORKREQUEST is being deprecated as well as cancelEndpoint/MethodType.


        :param api_call_mode: The api_call_mode of this CreateTaskFromRestTask.
        :type: str
        """
        allowed_values = ["SYNCHRONOUS", "ASYNC_OCI_WORKREQUEST", "ASYNC_GENERIC"]
        if not value_allowed_none_or_none_sentinel(api_call_mode, allowed_values):
            raise ValueError(
                "Invalid value for `api_call_mode`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._api_call_mode = api_call_mode

    @property
    def cancel_endpoint(self):
        """
        Gets the cancel_endpoint of this CreateTaskFromRestTask.

        :return: The cancel_endpoint of this CreateTaskFromRestTask.
        :rtype: oci.data_integration.models.Expression
        """
        return self._cancel_endpoint

    @cancel_endpoint.setter
    def cancel_endpoint(self, cancel_endpoint):
        """
        Sets the cancel_endpoint of this CreateTaskFromRestTask.

        :param cancel_endpoint: The cancel_endpoint of this CreateTaskFromRestTask.
        :type: oci.data_integration.models.Expression
        """
        self._cancel_endpoint = cancel_endpoint

    @property
    def cancel_method_type(self):
        """
        Gets the cancel_method_type of this CreateTaskFromRestTask.
        The REST method to use for canceling the original request.

        Allowed values for this property are: "GET", "POST", "PATCH", "DELETE", "PUT"


        :return: The cancel_method_type of this CreateTaskFromRestTask.
        :rtype: str
        """
        return self._cancel_method_type

    @cancel_method_type.setter
    def cancel_method_type(self, cancel_method_type):
        """
        Sets the cancel_method_type of this CreateTaskFromRestTask.
        The REST method to use for canceling the original request.


        :param cancel_method_type: The cancel_method_type of this CreateTaskFromRestTask.
        :type: str
        """
        allowed_values = ["GET", "POST", "PATCH", "DELETE", "PUT"]
        if not value_allowed_none_or_none_sentinel(cancel_method_type, allowed_values):
            raise ValueError(
                "Invalid value for `cancel_method_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._cancel_method_type = cancel_method_type

    @property
    def execute_rest_call_config(self):
        """
        Gets the execute_rest_call_config of this CreateTaskFromRestTask.

        :return: The execute_rest_call_config of this CreateTaskFromRestTask.
        :rtype: oci.data_integration.models.ExecuteRestCallConfig
        """
        return self._execute_rest_call_config

    @execute_rest_call_config.setter
    def execute_rest_call_config(self, execute_rest_call_config):
        """
        Sets the execute_rest_call_config of this CreateTaskFromRestTask.

        :param execute_rest_call_config: The execute_rest_call_config of this CreateTaskFromRestTask.
        :type: oci.data_integration.models.ExecuteRestCallConfig
        """
        self._execute_rest_call_config = execute_rest_call_config

    @property
    def cancel_rest_call_config(self):
        """
        Gets the cancel_rest_call_config of this CreateTaskFromRestTask.

        :return: The cancel_rest_call_config of this CreateTaskFromRestTask.
        :rtype: oci.data_integration.models.CancelRestCallConfig
        """
        return self._cancel_rest_call_config

    @cancel_rest_call_config.setter
    def cancel_rest_call_config(self, cancel_rest_call_config):
        """
        Sets the cancel_rest_call_config of this CreateTaskFromRestTask.

        :param cancel_rest_call_config: The cancel_rest_call_config of this CreateTaskFromRestTask.
        :type: oci.data_integration.models.CancelRestCallConfig
        """
        self._cancel_rest_call_config = cancel_rest_call_config

    @property
    def poll_rest_call_config(self):
        """
        Gets the poll_rest_call_config of this CreateTaskFromRestTask.

        :return: The poll_rest_call_config of this CreateTaskFromRestTask.
        :rtype: oci.data_integration.models.PollRestCallConfig
        """
        return self._poll_rest_call_config

    @poll_rest_call_config.setter
    def poll_rest_call_config(self, poll_rest_call_config):
        """
        Sets the poll_rest_call_config of this CreateTaskFromRestTask.

        :param poll_rest_call_config: The poll_rest_call_config of this CreateTaskFromRestTask.
        :type: oci.data_integration.models.PollRestCallConfig
        """
        self._poll_rest_call_config = poll_rest_call_config

    @property
    def typed_expressions(self):
        """
        Gets the typed_expressions of this CreateTaskFromRestTask.
        List of typed expressions.


        :return: The typed_expressions of this CreateTaskFromRestTask.
        :rtype: list[oci.data_integration.models.TypedExpression]
        """
        return self._typed_expressions

    @typed_expressions.setter
    def typed_expressions(self, typed_expressions):
        """
        Sets the typed_expressions of this CreateTaskFromRestTask.
        List of typed expressions.


        :param typed_expressions: The typed_expressions of this CreateTaskFromRestTask.
        :type: list[oci.data_integration.models.TypedExpression]
        """
        self._typed_expressions = typed_expressions

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
