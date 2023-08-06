# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .auth_config import AuthConfig
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ResourcePrincipalAuthConfig(AuthConfig):
    """
    Authentication configuration that uses OCI Resource Principal Auth for Generic REST invocation.
    """

    #: A constant which can be used with the resource_principal_source property of a ResourcePrincipalAuthConfig.
    #: This constant has a value of "WORKSPACE"
    RESOURCE_PRINCIPAL_SOURCE_WORKSPACE = "WORKSPACE"

    #: A constant which can be used with the resource_principal_source property of a ResourcePrincipalAuthConfig.
    #: This constant has a value of "APPLICATION"
    RESOURCE_PRINCIPAL_SOURCE_APPLICATION = "APPLICATION"

    def __init__(self, **kwargs):
        """
        Initializes a new ResourcePrincipalAuthConfig object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.ResourcePrincipalAuthConfig.model_type` attribute
        of this class is ``OCI_RESOURCE_AUTH_CONFIG`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param key:
            The value to assign to the key property of this ResourcePrincipalAuthConfig.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this ResourcePrincipalAuthConfig.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this ResourcePrincipalAuthConfig.
        :type parent_ref: oci.data_integration.models.ParentReference

        :param model_type:
            The value to assign to the model_type property of this ResourcePrincipalAuthConfig.
            Allowed values for this property are: "OCI_RESOURCE_AUTH_CONFIG", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type model_type: str

        :param resource_principal_source:
            The value to assign to the resource_principal_source property of this ResourcePrincipalAuthConfig.
            Allowed values for this property are: "WORKSPACE", "APPLICATION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type resource_principal_source: str

        """
        self.swagger_types = {
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'model_type': 'str',
            'resource_principal_source': 'str'
        }

        self.attribute_map = {
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'model_type': 'modelType',
            'resource_principal_source': 'resourcePrincipalSource'
        }

        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._model_type = None
        self._resource_principal_source = None
        self._model_type = 'OCI_RESOURCE_AUTH_CONFIG'

    @property
    def resource_principal_source(self):
        """
        Gets the resource_principal_source of this ResourcePrincipalAuthConfig.
        The OCI resource type that will supply the authentication token

        Allowed values for this property are: "WORKSPACE", "APPLICATION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The resource_principal_source of this ResourcePrincipalAuthConfig.
        :rtype: str
        """
        return self._resource_principal_source

    @resource_principal_source.setter
    def resource_principal_source(self, resource_principal_source):
        """
        Sets the resource_principal_source of this ResourcePrincipalAuthConfig.
        The OCI resource type that will supply the authentication token


        :param resource_principal_source: The resource_principal_source of this ResourcePrincipalAuthConfig.
        :type: str
        """
        allowed_values = ["WORKSPACE", "APPLICATION"]
        if not value_allowed_none_or_none_sentinel(resource_principal_source, allowed_values):
            resource_principal_source = 'UNKNOWN_ENUM_VALUE'
        self._resource_principal_source = resource_principal_source

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
