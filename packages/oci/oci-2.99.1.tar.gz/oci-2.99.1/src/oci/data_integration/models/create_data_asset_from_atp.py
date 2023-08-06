# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_data_asset_details import CreateDataAssetDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateDataAssetFromAtp(CreateDataAssetDetails):
    """
    Details for the Autonomous Transaction Processing data asset type.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateDataAssetFromAtp object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.CreateDataAssetFromAtp.model_type` attribute
        of this class is ``ORACLE_ATP_DATA_ASSET`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this CreateDataAssetFromAtp.
            Allowed values for this property are: "ORACLE_DATA_ASSET", "ORACLE_OBJECT_STORAGE_DATA_ASSET", "ORACLE_ATP_DATA_ASSET", "ORACLE_ADWC_DATA_ASSET", "MYSQL_DATA_ASSET", "GENERIC_JDBC_DATA_ASSET", "FUSION_APP_DATA_ASSET", "AMAZON_S3_DATA_ASSET", "LAKE_DATA_ASSET", "REST_DATA_ASSET"
        :type model_type: str

        :param key:
            The value to assign to the key property of this CreateDataAssetFromAtp.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this CreateDataAssetFromAtp.
        :type model_version: str

        :param name:
            The value to assign to the name property of this CreateDataAssetFromAtp.
        :type name: str

        :param description:
            The value to assign to the description property of this CreateDataAssetFromAtp.
        :type description: str

        :param object_status:
            The value to assign to the object_status property of this CreateDataAssetFromAtp.
        :type object_status: int

        :param identifier:
            The value to assign to the identifier property of this CreateDataAssetFromAtp.
        :type identifier: str

        :param external_key:
            The value to assign to the external_key property of this CreateDataAssetFromAtp.
        :type external_key: str

        :param asset_properties:
            The value to assign to the asset_properties property of this CreateDataAssetFromAtp.
        :type asset_properties: dict(str, str)

        :param registry_metadata:
            The value to assign to the registry_metadata property of this CreateDataAssetFromAtp.
        :type registry_metadata: oci.data_integration.models.RegistryMetadata

        :param service_name:
            The value to assign to the service_name property of this CreateDataAssetFromAtp.
        :type service_name: str

        :param driver_class:
            The value to assign to the driver_class property of this CreateDataAssetFromAtp.
        :type driver_class: str

        :param credential_file_content:
            The value to assign to the credential_file_content property of this CreateDataAssetFromAtp.
        :type credential_file_content: str

        :param wallet_secret:
            The value to assign to the wallet_secret property of this CreateDataAssetFromAtp.
        :type wallet_secret: oci.data_integration.models.SensitiveAttribute

        :param wallet_password_secret:
            The value to assign to the wallet_password_secret property of this CreateDataAssetFromAtp.
        :type wallet_password_secret: oci.data_integration.models.SensitiveAttribute

        :param region_id:
            The value to assign to the region_id property of this CreateDataAssetFromAtp.
        :type region_id: str

        :param tenancy_id:
            The value to assign to the tenancy_id property of this CreateDataAssetFromAtp.
        :type tenancy_id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateDataAssetFromAtp.
        :type compartment_id: str

        :param autonomous_db_id:
            The value to assign to the autonomous_db_id property of this CreateDataAssetFromAtp.
        :type autonomous_db_id: str

        :param default_connection:
            The value to assign to the default_connection property of this CreateDataAssetFromAtp.
        :type default_connection: oci.data_integration.models.CreateConnectionFromAtp

        :param staging_data_asset:
            The value to assign to the staging_data_asset property of this CreateDataAssetFromAtp.
        :type staging_data_asset: oci.data_integration.models.DataAsset

        :param staging_connection:
            The value to assign to the staging_connection property of this CreateDataAssetFromAtp.
        :type staging_connection: oci.data_integration.models.Connection

        :param bucket_schema:
            The value to assign to the bucket_schema property of this CreateDataAssetFromAtp.
        :type bucket_schema: oci.data_integration.models.Schema

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'name': 'str',
            'description': 'str',
            'object_status': 'int',
            'identifier': 'str',
            'external_key': 'str',
            'asset_properties': 'dict(str, str)',
            'registry_metadata': 'RegistryMetadata',
            'service_name': 'str',
            'driver_class': 'str',
            'credential_file_content': 'str',
            'wallet_secret': 'SensitiveAttribute',
            'wallet_password_secret': 'SensitiveAttribute',
            'region_id': 'str',
            'tenancy_id': 'str',
            'compartment_id': 'str',
            'autonomous_db_id': 'str',
            'default_connection': 'CreateConnectionFromAtp',
            'staging_data_asset': 'DataAsset',
            'staging_connection': 'Connection',
            'bucket_schema': 'Schema'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'name': 'name',
            'description': 'description',
            'object_status': 'objectStatus',
            'identifier': 'identifier',
            'external_key': 'externalKey',
            'asset_properties': 'assetProperties',
            'registry_metadata': 'registryMetadata',
            'service_name': 'serviceName',
            'driver_class': 'driverClass',
            'credential_file_content': 'credentialFileContent',
            'wallet_secret': 'walletSecret',
            'wallet_password_secret': 'walletPasswordSecret',
            'region_id': 'regionId',
            'tenancy_id': 'tenancyId',
            'compartment_id': 'compartmentId',
            'autonomous_db_id': 'autonomousDbId',
            'default_connection': 'defaultConnection',
            'staging_data_asset': 'stagingDataAsset',
            'staging_connection': 'stagingConnection',
            'bucket_schema': 'bucketSchema'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._name = None
        self._description = None
        self._object_status = None
        self._identifier = None
        self._external_key = None
        self._asset_properties = None
        self._registry_metadata = None
        self._service_name = None
        self._driver_class = None
        self._credential_file_content = None
        self._wallet_secret = None
        self._wallet_password_secret = None
        self._region_id = None
        self._tenancy_id = None
        self._compartment_id = None
        self._autonomous_db_id = None
        self._default_connection = None
        self._staging_data_asset = None
        self._staging_connection = None
        self._bucket_schema = None
        self._model_type = 'ORACLE_ATP_DATA_ASSET'

    @property
    def service_name(self):
        """
        Gets the service_name of this CreateDataAssetFromAtp.
        The Autonomous Transaction Processing instance service name.


        :return: The service_name of this CreateDataAssetFromAtp.
        :rtype: str
        """
        return self._service_name

    @service_name.setter
    def service_name(self, service_name):
        """
        Sets the service_name of this CreateDataAssetFromAtp.
        The Autonomous Transaction Processing instance service name.


        :param service_name: The service_name of this CreateDataAssetFromAtp.
        :type: str
        """
        self._service_name = service_name

    @property
    def driver_class(self):
        """
        Gets the driver_class of this CreateDataAssetFromAtp.
        The Autonomous Transaction Processing driver class.


        :return: The driver_class of this CreateDataAssetFromAtp.
        :rtype: str
        """
        return self._driver_class

    @driver_class.setter
    def driver_class(self, driver_class):
        """
        Sets the driver_class of this CreateDataAssetFromAtp.
        The Autonomous Transaction Processing driver class.


        :param driver_class: The driver_class of this CreateDataAssetFromAtp.
        :type: str
        """
        self._driver_class = driver_class

    @property
    def credential_file_content(self):
        """
        Gets the credential_file_content of this CreateDataAssetFromAtp.
        The credential file content from an Autonomous Transaction Processing wallet.


        :return: The credential_file_content of this CreateDataAssetFromAtp.
        :rtype: str
        """
        return self._credential_file_content

    @credential_file_content.setter
    def credential_file_content(self, credential_file_content):
        """
        Sets the credential_file_content of this CreateDataAssetFromAtp.
        The credential file content from an Autonomous Transaction Processing wallet.


        :param credential_file_content: The credential_file_content of this CreateDataAssetFromAtp.
        :type: str
        """
        self._credential_file_content = credential_file_content

    @property
    def wallet_secret(self):
        """
        Gets the wallet_secret of this CreateDataAssetFromAtp.

        :return: The wallet_secret of this CreateDataAssetFromAtp.
        :rtype: oci.data_integration.models.SensitiveAttribute
        """
        return self._wallet_secret

    @wallet_secret.setter
    def wallet_secret(self, wallet_secret):
        """
        Sets the wallet_secret of this CreateDataAssetFromAtp.

        :param wallet_secret: The wallet_secret of this CreateDataAssetFromAtp.
        :type: oci.data_integration.models.SensitiveAttribute
        """
        self._wallet_secret = wallet_secret

    @property
    def wallet_password_secret(self):
        """
        Gets the wallet_password_secret of this CreateDataAssetFromAtp.

        :return: The wallet_password_secret of this CreateDataAssetFromAtp.
        :rtype: oci.data_integration.models.SensitiveAttribute
        """
        return self._wallet_password_secret

    @wallet_password_secret.setter
    def wallet_password_secret(self, wallet_password_secret):
        """
        Sets the wallet_password_secret of this CreateDataAssetFromAtp.

        :param wallet_password_secret: The wallet_password_secret of this CreateDataAssetFromAtp.
        :type: oci.data_integration.models.SensitiveAttribute
        """
        self._wallet_password_secret = wallet_password_secret

    @property
    def region_id(self):
        """
        Gets the region_id of this CreateDataAssetFromAtp.
        The Autonomous Data Warehouse instance region Id.


        :return: The region_id of this CreateDataAssetFromAtp.
        :rtype: str
        """
        return self._region_id

    @region_id.setter
    def region_id(self, region_id):
        """
        Sets the region_id of this CreateDataAssetFromAtp.
        The Autonomous Data Warehouse instance region Id.


        :param region_id: The region_id of this CreateDataAssetFromAtp.
        :type: str
        """
        self._region_id = region_id

    @property
    def tenancy_id(self):
        """
        Gets the tenancy_id of this CreateDataAssetFromAtp.
        The Autonomous Data Warehouse instance tenancy Id.


        :return: The tenancy_id of this CreateDataAssetFromAtp.
        :rtype: str
        """
        return self._tenancy_id

    @tenancy_id.setter
    def tenancy_id(self, tenancy_id):
        """
        Sets the tenancy_id of this CreateDataAssetFromAtp.
        The Autonomous Data Warehouse instance tenancy Id.


        :param tenancy_id: The tenancy_id of this CreateDataAssetFromAtp.
        :type: str
        """
        self._tenancy_id = tenancy_id

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this CreateDataAssetFromAtp.
        The Autonomous Data Warehouse instance compartment Id.


        :return: The compartment_id of this CreateDataAssetFromAtp.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateDataAssetFromAtp.
        The Autonomous Data Warehouse instance compartment Id.


        :param compartment_id: The compartment_id of this CreateDataAssetFromAtp.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def autonomous_db_id(self):
        """
        Gets the autonomous_db_id of this CreateDataAssetFromAtp.
        Tha Autonomous Database Id


        :return: The autonomous_db_id of this CreateDataAssetFromAtp.
        :rtype: str
        """
        return self._autonomous_db_id

    @autonomous_db_id.setter
    def autonomous_db_id(self, autonomous_db_id):
        """
        Sets the autonomous_db_id of this CreateDataAssetFromAtp.
        Tha Autonomous Database Id


        :param autonomous_db_id: The autonomous_db_id of this CreateDataAssetFromAtp.
        :type: str
        """
        self._autonomous_db_id = autonomous_db_id

    @property
    def default_connection(self):
        """
        Gets the default_connection of this CreateDataAssetFromAtp.

        :return: The default_connection of this CreateDataAssetFromAtp.
        :rtype: oci.data_integration.models.CreateConnectionFromAtp
        """
        return self._default_connection

    @default_connection.setter
    def default_connection(self, default_connection):
        """
        Sets the default_connection of this CreateDataAssetFromAtp.

        :param default_connection: The default_connection of this CreateDataAssetFromAtp.
        :type: oci.data_integration.models.CreateConnectionFromAtp
        """
        self._default_connection = default_connection

    @property
    def staging_data_asset(self):
        """
        Gets the staging_data_asset of this CreateDataAssetFromAtp.

        :return: The staging_data_asset of this CreateDataAssetFromAtp.
        :rtype: oci.data_integration.models.DataAsset
        """
        return self._staging_data_asset

    @staging_data_asset.setter
    def staging_data_asset(self, staging_data_asset):
        """
        Sets the staging_data_asset of this CreateDataAssetFromAtp.

        :param staging_data_asset: The staging_data_asset of this CreateDataAssetFromAtp.
        :type: oci.data_integration.models.DataAsset
        """
        self._staging_data_asset = staging_data_asset

    @property
    def staging_connection(self):
        """
        Gets the staging_connection of this CreateDataAssetFromAtp.

        :return: The staging_connection of this CreateDataAssetFromAtp.
        :rtype: oci.data_integration.models.Connection
        """
        return self._staging_connection

    @staging_connection.setter
    def staging_connection(self, staging_connection):
        """
        Sets the staging_connection of this CreateDataAssetFromAtp.

        :param staging_connection: The staging_connection of this CreateDataAssetFromAtp.
        :type: oci.data_integration.models.Connection
        """
        self._staging_connection = staging_connection

    @property
    def bucket_schema(self):
        """
        Gets the bucket_schema of this CreateDataAssetFromAtp.

        :return: The bucket_schema of this CreateDataAssetFromAtp.
        :rtype: oci.data_integration.models.Schema
        """
        return self._bucket_schema

    @bucket_schema.setter
    def bucket_schema(self, bucket_schema):
        """
        Sets the bucket_schema of this CreateDataAssetFromAtp.

        :param bucket_schema: The bucket_schema of this CreateDataAssetFromAtp.
        :type: oci.data_integration.models.Schema
        """
        self._bucket_schema = bucket_schema

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
