# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExecuteRestCallConfig(object):
    """
    The REST API configuration for execution.
    """

    #: A constant which can be used with the method_type property of a ExecuteRestCallConfig.
    #: This constant has a value of "GET"
    METHOD_TYPE_GET = "GET"

    #: A constant which can be used with the method_type property of a ExecuteRestCallConfig.
    #: This constant has a value of "POST"
    METHOD_TYPE_POST = "POST"

    #: A constant which can be used with the method_type property of a ExecuteRestCallConfig.
    #: This constant has a value of "PATCH"
    METHOD_TYPE_PATCH = "PATCH"

    #: A constant which can be used with the method_type property of a ExecuteRestCallConfig.
    #: This constant has a value of "DELETE"
    METHOD_TYPE_DELETE = "DELETE"

    #: A constant which can be used with the method_type property of a ExecuteRestCallConfig.
    #: This constant has a value of "PUT"
    METHOD_TYPE_PUT = "PUT"

    def __init__(self, **kwargs):
        """
        Initializes a new ExecuteRestCallConfig object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param method_type:
            The value to assign to the method_type property of this ExecuteRestCallConfig.
            Allowed values for this property are: "GET", "POST", "PATCH", "DELETE", "PUT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type method_type: str

        :param request_headers:
            The value to assign to the request_headers property of this ExecuteRestCallConfig.
        :type request_headers: dict(str, str)

        :param config_values:
            The value to assign to the config_values property of this ExecuteRestCallConfig.
        :type config_values: oci.data_integration.models.ConfigValues

        """
        self.swagger_types = {
            'method_type': 'str',
            'request_headers': 'dict(str, str)',
            'config_values': 'ConfigValues'
        }

        self.attribute_map = {
            'method_type': 'methodType',
            'request_headers': 'requestHeaders',
            'config_values': 'configValues'
        }

        self._method_type = None
        self._request_headers = None
        self._config_values = None

    @property
    def method_type(self):
        """
        Gets the method_type of this ExecuteRestCallConfig.
        The REST method to use.

        Allowed values for this property are: "GET", "POST", "PATCH", "DELETE", "PUT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The method_type of this ExecuteRestCallConfig.
        :rtype: str
        """
        return self._method_type

    @method_type.setter
    def method_type(self, method_type):
        """
        Sets the method_type of this ExecuteRestCallConfig.
        The REST method to use.


        :param method_type: The method_type of this ExecuteRestCallConfig.
        :type: str
        """
        allowed_values = ["GET", "POST", "PATCH", "DELETE", "PUT"]
        if not value_allowed_none_or_none_sentinel(method_type, allowed_values):
            method_type = 'UNKNOWN_ENUM_VALUE'
        self._method_type = method_type

    @property
    def request_headers(self):
        """
        Gets the request_headers of this ExecuteRestCallConfig.
        The headers for the REST call.


        :return: The request_headers of this ExecuteRestCallConfig.
        :rtype: dict(str, str)
        """
        return self._request_headers

    @request_headers.setter
    def request_headers(self, request_headers):
        """
        Sets the request_headers of this ExecuteRestCallConfig.
        The headers for the REST call.


        :param request_headers: The request_headers of this ExecuteRestCallConfig.
        :type: dict(str, str)
        """
        self._request_headers = request_headers

    @property
    def config_values(self):
        """
        Gets the config_values of this ExecuteRestCallConfig.

        :return: The config_values of this ExecuteRestCallConfig.
        :rtype: oci.data_integration.models.ConfigValues
        """
        return self._config_values

    @config_values.setter
    def config_values(self, config_values):
        """
        Sets the config_values of this ExecuteRestCallConfig.

        :param config_values: The config_values of this ExecuteRestCallConfig.
        :type: oci.data_integration.models.ConfigValues
        """
        self._config_values = config_values

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
