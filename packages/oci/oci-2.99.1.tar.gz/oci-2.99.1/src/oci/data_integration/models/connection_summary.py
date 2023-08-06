# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ConnectionSummary(object):
    """
    The connection summary object.
    """

    #: A constant which can be used with the model_type property of a ConnectionSummary.
    #: This constant has a value of "ORACLE_ADWC_CONNECTION"
    MODEL_TYPE_ORACLE_ADWC_CONNECTION = "ORACLE_ADWC_CONNECTION"

    #: A constant which can be used with the model_type property of a ConnectionSummary.
    #: This constant has a value of "ORACLE_ATP_CONNECTION"
    MODEL_TYPE_ORACLE_ATP_CONNECTION = "ORACLE_ATP_CONNECTION"

    #: A constant which can be used with the model_type property of a ConnectionSummary.
    #: This constant has a value of "ORACLE_OBJECT_STORAGE_CONNECTION"
    MODEL_TYPE_ORACLE_OBJECT_STORAGE_CONNECTION = "ORACLE_OBJECT_STORAGE_CONNECTION"

    #: A constant which can be used with the model_type property of a ConnectionSummary.
    #: This constant has a value of "ORACLEDB_CONNECTION"
    MODEL_TYPE_ORACLEDB_CONNECTION = "ORACLEDB_CONNECTION"

    #: A constant which can be used with the model_type property of a ConnectionSummary.
    #: This constant has a value of "MYSQL_CONNECTION"
    MODEL_TYPE_MYSQL_CONNECTION = "MYSQL_CONNECTION"

    #: A constant which can be used with the model_type property of a ConnectionSummary.
    #: This constant has a value of "GENERIC_JDBC_CONNECTION"
    MODEL_TYPE_GENERIC_JDBC_CONNECTION = "GENERIC_JDBC_CONNECTION"

    #: A constant which can be used with the model_type property of a ConnectionSummary.
    #: This constant has a value of "BICC_CONNECTION"
    MODEL_TYPE_BICC_CONNECTION = "BICC_CONNECTION"

    #: A constant which can be used with the model_type property of a ConnectionSummary.
    #: This constant has a value of "AMAZON_S3_CONNECTION"
    MODEL_TYPE_AMAZON_S3_CONNECTION = "AMAZON_S3_CONNECTION"

    #: A constant which can be used with the model_type property of a ConnectionSummary.
    #: This constant has a value of "BIP_CONNECTION"
    MODEL_TYPE_BIP_CONNECTION = "BIP_CONNECTION"

    #: A constant which can be used with the model_type property of a ConnectionSummary.
    #: This constant has a value of "LAKE_CONNECTION"
    MODEL_TYPE_LAKE_CONNECTION = "LAKE_CONNECTION"

    #: A constant which can be used with the model_type property of a ConnectionSummary.
    #: This constant has a value of "REST_NO_AUTH_CONNECTION"
    MODEL_TYPE_REST_NO_AUTH_CONNECTION = "REST_NO_AUTH_CONNECTION"

    #: A constant which can be used with the model_type property of a ConnectionSummary.
    #: This constant has a value of "REST_BASIC_AUTH_CONNECTION"
    MODEL_TYPE_REST_BASIC_AUTH_CONNECTION = "REST_BASIC_AUTH_CONNECTION"

    def __init__(self, **kwargs):
        """
        Initializes a new ConnectionSummary object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.data_integration.models.ConnectionSummaryFromJdbc`
        * :class:`~oci.data_integration.models.ConnectionSummaryFromBICC`
        * :class:`~oci.data_integration.models.ConnectionSummaryFromRestNoAuth`
        * :class:`~oci.data_integration.models.ConnectionSummaryFromAtp`
        * :class:`~oci.data_integration.models.ConnectionSummaryFromOracle`
        * :class:`~oci.data_integration.models.ConnectionSummaryFromAmazonS3`
        * :class:`~oci.data_integration.models.ConnectionSummaryFromRestBasicAuth`
        * :class:`~oci.data_integration.models.ConnectionSummaryFromAdwc`
        * :class:`~oci.data_integration.models.ConnectionSummaryFromMySQL`
        * :class:`~oci.data_integration.models.ConnectionSummaryFromLake`
        * :class:`~oci.data_integration.models.ConnectionSummaryFromBIP`
        * :class:`~oci.data_integration.models.ConnectionSummaryFromObjectStorage`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this ConnectionSummary.
            Allowed values for this property are: "ORACLE_ADWC_CONNECTION", "ORACLE_ATP_CONNECTION", "ORACLE_OBJECT_STORAGE_CONNECTION", "ORACLEDB_CONNECTION", "MYSQL_CONNECTION", "GENERIC_JDBC_CONNECTION", "BICC_CONNECTION", "AMAZON_S3_CONNECTION", "BIP_CONNECTION", "LAKE_CONNECTION", "REST_NO_AUTH_CONNECTION", "REST_BASIC_AUTH_CONNECTION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type model_type: str

        :param key:
            The value to assign to the key property of this ConnectionSummary.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this ConnectionSummary.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this ConnectionSummary.
        :type parent_ref: oci.data_integration.models.ParentReference

        :param name:
            The value to assign to the name property of this ConnectionSummary.
        :type name: str

        :param description:
            The value to assign to the description property of this ConnectionSummary.
        :type description: str

        :param object_version:
            The value to assign to the object_version property of this ConnectionSummary.
        :type object_version: int

        :param object_status:
            The value to assign to the object_status property of this ConnectionSummary.
        :type object_status: int

        :param identifier:
            The value to assign to the identifier property of this ConnectionSummary.
        :type identifier: str

        :param primary_schema:
            The value to assign to the primary_schema property of this ConnectionSummary.
        :type primary_schema: oci.data_integration.models.Schema

        :param connection_properties:
            The value to assign to the connection_properties property of this ConnectionSummary.
        :type connection_properties: list[oci.data_integration.models.ConnectionProperty]

        :param is_default:
            The value to assign to the is_default property of this ConnectionSummary.
        :type is_default: bool

        :param metadata:
            The value to assign to the metadata property of this ConnectionSummary.
        :type metadata: oci.data_integration.models.ObjectMetadata

        :param key_map:
            The value to assign to the key_map property of this ConnectionSummary.
        :type key_map: dict(str, str)

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'name': 'str',
            'description': 'str',
            'object_version': 'int',
            'object_status': 'int',
            'identifier': 'str',
            'primary_schema': 'Schema',
            'connection_properties': 'list[ConnectionProperty]',
            'is_default': 'bool',
            'metadata': 'ObjectMetadata',
            'key_map': 'dict(str, str)'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'name': 'name',
            'description': 'description',
            'object_version': 'objectVersion',
            'object_status': 'objectStatus',
            'identifier': 'identifier',
            'primary_schema': 'primarySchema',
            'connection_properties': 'connectionProperties',
            'is_default': 'isDefault',
            'metadata': 'metadata',
            'key_map': 'keyMap'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._name = None
        self._description = None
        self._object_version = None
        self._object_status = None
        self._identifier = None
        self._primary_schema = None
        self._connection_properties = None
        self._is_default = None
        self._metadata = None
        self._key_map = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['modelType']

        if type == 'GENERIC_JDBC_CONNECTION':
            return 'ConnectionSummaryFromJdbc'

        if type == 'BICC_CONNECTION':
            return 'ConnectionSummaryFromBICC'

        if type == 'REST_NO_AUTH_CONNECTION':
            return 'ConnectionSummaryFromRestNoAuth'

        if type == 'ORACLE_ATP_CONNECTION':
            return 'ConnectionSummaryFromAtp'

        if type == 'ORACLEDB_CONNECTION':
            return 'ConnectionSummaryFromOracle'

        if type == 'AMAZON_S3_CONNECTION':
            return 'ConnectionSummaryFromAmazonS3'

        if type == 'REST_BASIC_AUTH_CONNECTION':
            return 'ConnectionSummaryFromRestBasicAuth'

        if type == 'ORACLE_ADWC_CONNECTION':
            return 'ConnectionSummaryFromAdwc'

        if type == 'MYSQL_CONNECTION':
            return 'ConnectionSummaryFromMySQL'

        if type == 'LAKE_CONNECTION':
            return 'ConnectionSummaryFromLake'

        if type == 'BIP_CONNECTION':
            return 'ConnectionSummaryFromBIP'

        if type == 'ORACLE_OBJECT_STORAGE_CONNECTION':
            return 'ConnectionSummaryFromObjectStorage'
        else:
            return 'ConnectionSummary'

    @property
    def model_type(self):
        """
        **[Required]** Gets the model_type of this ConnectionSummary.
        The type of the connection.

        Allowed values for this property are: "ORACLE_ADWC_CONNECTION", "ORACLE_ATP_CONNECTION", "ORACLE_OBJECT_STORAGE_CONNECTION", "ORACLEDB_CONNECTION", "MYSQL_CONNECTION", "GENERIC_JDBC_CONNECTION", "BICC_CONNECTION", "AMAZON_S3_CONNECTION", "BIP_CONNECTION", "LAKE_CONNECTION", "REST_NO_AUTH_CONNECTION", "REST_BASIC_AUTH_CONNECTION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The model_type of this ConnectionSummary.
        :rtype: str
        """
        return self._model_type

    @model_type.setter
    def model_type(self, model_type):
        """
        Sets the model_type of this ConnectionSummary.
        The type of the connection.


        :param model_type: The model_type of this ConnectionSummary.
        :type: str
        """
        allowed_values = ["ORACLE_ADWC_CONNECTION", "ORACLE_ATP_CONNECTION", "ORACLE_OBJECT_STORAGE_CONNECTION", "ORACLEDB_CONNECTION", "MYSQL_CONNECTION", "GENERIC_JDBC_CONNECTION", "BICC_CONNECTION", "AMAZON_S3_CONNECTION", "BIP_CONNECTION", "LAKE_CONNECTION", "REST_NO_AUTH_CONNECTION", "REST_BASIC_AUTH_CONNECTION"]
        if not value_allowed_none_or_none_sentinel(model_type, allowed_values):
            model_type = 'UNKNOWN_ENUM_VALUE'
        self._model_type = model_type

    @property
    def key(self):
        """
        Gets the key of this ConnectionSummary.
        Generated key that can be used in API calls to identify connection. On scenarios where reference to the connection is needed, a value can be passed in create.


        :return: The key of this ConnectionSummary.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this ConnectionSummary.
        Generated key that can be used in API calls to identify connection. On scenarios where reference to the connection is needed, a value can be passed in create.


        :param key: The key of this ConnectionSummary.
        :type: str
        """
        self._key = key

    @property
    def model_version(self):
        """
        Gets the model_version of this ConnectionSummary.
        The model version of an object.


        :return: The model_version of this ConnectionSummary.
        :rtype: str
        """
        return self._model_version

    @model_version.setter
    def model_version(self, model_version):
        """
        Sets the model_version of this ConnectionSummary.
        The model version of an object.


        :param model_version: The model_version of this ConnectionSummary.
        :type: str
        """
        self._model_version = model_version

    @property
    def parent_ref(self):
        """
        Gets the parent_ref of this ConnectionSummary.

        :return: The parent_ref of this ConnectionSummary.
        :rtype: oci.data_integration.models.ParentReference
        """
        return self._parent_ref

    @parent_ref.setter
    def parent_ref(self, parent_ref):
        """
        Sets the parent_ref of this ConnectionSummary.

        :param parent_ref: The parent_ref of this ConnectionSummary.
        :type: oci.data_integration.models.ParentReference
        """
        self._parent_ref = parent_ref

    @property
    def name(self):
        """
        Gets the name of this ConnectionSummary.
        Free form text without any restriction on permitted characters. Name can have letters, numbers, and special characters. The value is editable and is restricted to 1000 characters.


        :return: The name of this ConnectionSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ConnectionSummary.
        Free form text without any restriction on permitted characters. Name can have letters, numbers, and special characters. The value is editable and is restricted to 1000 characters.


        :param name: The name of this ConnectionSummary.
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this ConnectionSummary.
        User-defined description for the connection.


        :return: The description of this ConnectionSummary.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ConnectionSummary.
        User-defined description for the connection.


        :param description: The description of this ConnectionSummary.
        :type: str
        """
        self._description = description

    @property
    def object_version(self):
        """
        Gets the object_version of this ConnectionSummary.
        The version of the object that is used to track changes in the object instance.


        :return: The object_version of this ConnectionSummary.
        :rtype: int
        """
        return self._object_version

    @object_version.setter
    def object_version(self, object_version):
        """
        Sets the object_version of this ConnectionSummary.
        The version of the object that is used to track changes in the object instance.


        :param object_version: The object_version of this ConnectionSummary.
        :type: int
        """
        self._object_version = object_version

    @property
    def object_status(self):
        """
        Gets the object_status of this ConnectionSummary.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :return: The object_status of this ConnectionSummary.
        :rtype: int
        """
        return self._object_status

    @object_status.setter
    def object_status(self, object_status):
        """
        Sets the object_status of this ConnectionSummary.
        The status of an object that can be set to value 1 for shallow references across objects, other values reserved.


        :param object_status: The object_status of this ConnectionSummary.
        :type: int
        """
        self._object_status = object_status

    @property
    def identifier(self):
        """
        Gets the identifier of this ConnectionSummary.
        Value can only contain upper case letters, underscore and numbers. It should begin with upper case letter or underscore. The value can be modified.


        :return: The identifier of this ConnectionSummary.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this ConnectionSummary.
        Value can only contain upper case letters, underscore and numbers. It should begin with upper case letter or underscore. The value can be modified.


        :param identifier: The identifier of this ConnectionSummary.
        :type: str
        """
        self._identifier = identifier

    @property
    def primary_schema(self):
        """
        Gets the primary_schema of this ConnectionSummary.

        :return: The primary_schema of this ConnectionSummary.
        :rtype: oci.data_integration.models.Schema
        """
        return self._primary_schema

    @primary_schema.setter
    def primary_schema(self, primary_schema):
        """
        Sets the primary_schema of this ConnectionSummary.

        :param primary_schema: The primary_schema of this ConnectionSummary.
        :type: oci.data_integration.models.Schema
        """
        self._primary_schema = primary_schema

    @property
    def connection_properties(self):
        """
        Gets the connection_properties of this ConnectionSummary.
        The properties for the connection.


        :return: The connection_properties of this ConnectionSummary.
        :rtype: list[oci.data_integration.models.ConnectionProperty]
        """
        return self._connection_properties

    @connection_properties.setter
    def connection_properties(self, connection_properties):
        """
        Sets the connection_properties of this ConnectionSummary.
        The properties for the connection.


        :param connection_properties: The connection_properties of this ConnectionSummary.
        :type: list[oci.data_integration.models.ConnectionProperty]
        """
        self._connection_properties = connection_properties

    @property
    def is_default(self):
        """
        Gets the is_default of this ConnectionSummary.
        The default property for the connection.


        :return: The is_default of this ConnectionSummary.
        :rtype: bool
        """
        return self._is_default

    @is_default.setter
    def is_default(self, is_default):
        """
        Sets the is_default of this ConnectionSummary.
        The default property for the connection.


        :param is_default: The is_default of this ConnectionSummary.
        :type: bool
        """
        self._is_default = is_default

    @property
    def metadata(self):
        """
        Gets the metadata of this ConnectionSummary.

        :return: The metadata of this ConnectionSummary.
        :rtype: oci.data_integration.models.ObjectMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this ConnectionSummary.

        :param metadata: The metadata of this ConnectionSummary.
        :type: oci.data_integration.models.ObjectMetadata
        """
        self._metadata = metadata

    @property
    def key_map(self):
        """
        Gets the key_map of this ConnectionSummary.
        A key map. If provided, key is replaced with generated key. This structure provides mapping between user provided key and generated key.


        :return: The key_map of this ConnectionSummary.
        :rtype: dict(str, str)
        """
        return self._key_map

    @key_map.setter
    def key_map(self, key_map):
        """
        Sets the key_map of this ConnectionSummary.
        A key map. If provided, key is replaced with generated key. This structure provides mapping between user provided key and generated key.


        :param key_map: The key_map of this ConnectionSummary.
        :type: dict(str, str)
        """
        self._key_map = key_map

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
