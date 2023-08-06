# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_configuration_source_provider_details import CreateConfigurationSourceProviderDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails(CreateConfigurationSourceProviderDetails):
    """
    The details for creating a configuration source provider of the type `BITBUCKET_SERVER_ACCESS_TOKEN`.
    This type corresponds to a configuration source provider in Bitbucket server that is authenticated with a personal access token.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.resource_manager.models.CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.config_source_provider_type` attribute
        of this class is ``BITBUCKET_SERVER_ACCESS_TOKEN`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :type description: str

        :param config_source_provider_type:
            The value to assign to the config_source_provider_type property of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :type config_source_provider_type: str

        :param private_server_config_details:
            The value to assign to the private_server_config_details property of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :type private_server_config_details: oci.resource_manager.models.PrivateServerConfigDetails

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param secret_id:
            The value to assign to the secret_id property of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :type secret_id: str

        :param api_endpoint:
            The value to assign to the api_endpoint property of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :type api_endpoint: str

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'config_source_provider_type': 'str',
            'private_server_config_details': 'PrivateServerConfigDetails',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'secret_id': 'str',
            'api_endpoint': 'str'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'description': 'description',
            'config_source_provider_type': 'configSourceProviderType',
            'private_server_config_details': 'privateServerConfigDetails',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'secret_id': 'secretId',
            'api_endpoint': 'apiEndpoint'
        }

        self._compartment_id = None
        self._display_name = None
        self._description = None
        self._config_source_provider_type = None
        self._private_server_config_details = None
        self._freeform_tags = None
        self._defined_tags = None
        self._secret_id = None
        self._api_endpoint = None
        self._config_source_provider_type = 'BITBUCKET_SERVER_ACCESS_TOKEN'

    @property
    def secret_id(self):
        """
        **[Required]** Gets the secret_id of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        The secret ocid which is used to authorize the user.


        :return: The secret_id of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :rtype: str
        """
        return self._secret_id

    @secret_id.setter
    def secret_id(self, secret_id):
        """
        Sets the secret_id of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        The secret ocid which is used to authorize the user.


        :param secret_id: The secret_id of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :type: str
        """
        self._secret_id = secret_id

    @property
    def api_endpoint(self):
        """
        **[Required]** Gets the api_endpoint of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        The Bitbucket Server service endpoint
        Example: `https://bitbucket.org/`


        :return: The api_endpoint of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :rtype: str
        """
        return self._api_endpoint

    @api_endpoint.setter
    def api_endpoint(self, api_endpoint):
        """
        Sets the api_endpoint of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        The Bitbucket Server service endpoint
        Example: `https://bitbucket.org/`


        :param api_endpoint: The api_endpoint of this CreateBitbucketServerAccessTokenConfigurationSourceProviderDetails.
        :type: str
        """
        self._api_endpoint = api_endpoint

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
