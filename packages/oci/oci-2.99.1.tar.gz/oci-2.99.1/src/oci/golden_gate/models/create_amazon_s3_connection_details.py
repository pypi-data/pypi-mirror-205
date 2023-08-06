# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_connection_details import CreateConnectionDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateAmazonS3ConnectionDetails(CreateConnectionDetails):
    """
    The information about a new Amazon S3 Connection.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateAmazonS3ConnectionDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.golden_gate.models.CreateAmazonS3ConnectionDetails.connection_type` attribute
        of this class is ``AMAZON_S3`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param connection_type:
            The value to assign to the connection_type property of this CreateAmazonS3ConnectionDetails.
            Allowed values for this property are: "GOLDENGATE", "KAFKA", "KAFKA_SCHEMA_REGISTRY", "MYSQL", "JAVA_MESSAGE_SERVICE", "MICROSOFT_SQLSERVER", "OCI_OBJECT_STORAGE", "ORACLE", "AZURE_DATA_LAKE_STORAGE", "POSTGRESQL", "AZURE_SYNAPSE_ANALYTICS", "SNOWFLAKE", "AMAZON_S3", "HDFS", "ORACLE_NOSQL", "MONGODB"
        :type connection_type: str

        :param display_name:
            The value to assign to the display_name property of this CreateAmazonS3ConnectionDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this CreateAmazonS3ConnectionDetails.
        :type description: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateAmazonS3ConnectionDetails.
        :type compartment_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateAmazonS3ConnectionDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateAmazonS3ConnectionDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param vault_id:
            The value to assign to the vault_id property of this CreateAmazonS3ConnectionDetails.
        :type vault_id: str

        :param key_id:
            The value to assign to the key_id property of this CreateAmazonS3ConnectionDetails.
        :type key_id: str

        :param subnet_id:
            The value to assign to the subnet_id property of this CreateAmazonS3ConnectionDetails.
        :type subnet_id: str

        :param nsg_ids:
            The value to assign to the nsg_ids property of this CreateAmazonS3ConnectionDetails.
        :type nsg_ids: list[str]

        :param technology_type:
            The value to assign to the technology_type property of this CreateAmazonS3ConnectionDetails.
        :type technology_type: str

        :param access_key_id:
            The value to assign to the access_key_id property of this CreateAmazonS3ConnectionDetails.
        :type access_key_id: str

        :param secret_access_key:
            The value to assign to the secret_access_key property of this CreateAmazonS3ConnectionDetails.
        :type secret_access_key: str

        """
        self.swagger_types = {
            'connection_type': 'str',
            'display_name': 'str',
            'description': 'str',
            'compartment_id': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'vault_id': 'str',
            'key_id': 'str',
            'subnet_id': 'str',
            'nsg_ids': 'list[str]',
            'technology_type': 'str',
            'access_key_id': 'str',
            'secret_access_key': 'str'
        }

        self.attribute_map = {
            'connection_type': 'connectionType',
            'display_name': 'displayName',
            'description': 'description',
            'compartment_id': 'compartmentId',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'vault_id': 'vaultId',
            'key_id': 'keyId',
            'subnet_id': 'subnetId',
            'nsg_ids': 'nsgIds',
            'technology_type': 'technologyType',
            'access_key_id': 'accessKeyId',
            'secret_access_key': 'secretAccessKey'
        }

        self._connection_type = None
        self._display_name = None
        self._description = None
        self._compartment_id = None
        self._freeform_tags = None
        self._defined_tags = None
        self._vault_id = None
        self._key_id = None
        self._subnet_id = None
        self._nsg_ids = None
        self._technology_type = None
        self._access_key_id = None
        self._secret_access_key = None
        self._connection_type = 'AMAZON_S3'

    @property
    def technology_type(self):
        """
        **[Required]** Gets the technology_type of this CreateAmazonS3ConnectionDetails.
        The Amazon S3 technology type.


        :return: The technology_type of this CreateAmazonS3ConnectionDetails.
        :rtype: str
        """
        return self._technology_type

    @technology_type.setter
    def technology_type(self, technology_type):
        """
        Sets the technology_type of this CreateAmazonS3ConnectionDetails.
        The Amazon S3 technology type.


        :param technology_type: The technology_type of this CreateAmazonS3ConnectionDetails.
        :type: str
        """
        self._technology_type = technology_type

    @property
    def access_key_id(self):
        """
        **[Required]** Gets the access_key_id of this CreateAmazonS3ConnectionDetails.
        Access key ID to access the Amazon S3 bucket.
        e.g.: \"this-is-not-the-secret\"


        :return: The access_key_id of this CreateAmazonS3ConnectionDetails.
        :rtype: str
        """
        return self._access_key_id

    @access_key_id.setter
    def access_key_id(self, access_key_id):
        """
        Sets the access_key_id of this CreateAmazonS3ConnectionDetails.
        Access key ID to access the Amazon S3 bucket.
        e.g.: \"this-is-not-the-secret\"


        :param access_key_id: The access_key_id of this CreateAmazonS3ConnectionDetails.
        :type: str
        """
        self._access_key_id = access_key_id

    @property
    def secret_access_key(self):
        """
        **[Required]** Gets the secret_access_key of this CreateAmazonS3ConnectionDetails.
        Secret access key to access the Amazon S3 bucket.
        e.g.: \"this-is-not-the-secret\"


        :return: The secret_access_key of this CreateAmazonS3ConnectionDetails.
        :rtype: str
        """
        return self._secret_access_key

    @secret_access_key.setter
    def secret_access_key(self, secret_access_key):
        """
        Sets the secret_access_key of this CreateAmazonS3ConnectionDetails.
        Secret access key to access the Amazon S3 bucket.
        e.g.: \"this-is-not-the-secret\"


        :param secret_access_key: The secret_access_key of this CreateAmazonS3ConnectionDetails.
        :type: str
        """
        self._secret_access_key = secret_access_key

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
