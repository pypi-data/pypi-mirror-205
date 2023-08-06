# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .update_connection_details import UpdateConnectionDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateMongoDbConnectionDetails(UpdateConnectionDetails):
    """
    The information to update a MongoDB Connection.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateMongoDbConnectionDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.golden_gate.models.UpdateMongoDbConnectionDetails.connection_type` attribute
        of this class is ``MONGODB`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param connection_type:
            The value to assign to the connection_type property of this UpdateMongoDbConnectionDetails.
            Allowed values for this property are: "GOLDENGATE", "KAFKA", "KAFKA_SCHEMA_REGISTRY", "MYSQL", "JAVA_MESSAGE_SERVICE", "MICROSOFT_SQLSERVER", "OCI_OBJECT_STORAGE", "ORACLE", "AZURE_DATA_LAKE_STORAGE", "POSTGRESQL", "AZURE_SYNAPSE_ANALYTICS", "SNOWFLAKE", "AMAZON_S3", "HDFS", "ORACLE_NOSQL", "MONGODB"
        :type connection_type: str

        :param display_name:
            The value to assign to the display_name property of this UpdateMongoDbConnectionDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this UpdateMongoDbConnectionDetails.
        :type description: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateMongoDbConnectionDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateMongoDbConnectionDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param vault_id:
            The value to assign to the vault_id property of this UpdateMongoDbConnectionDetails.
        :type vault_id: str

        :param key_id:
            The value to assign to the key_id property of this UpdateMongoDbConnectionDetails.
        :type key_id: str

        :param nsg_ids:
            The value to assign to the nsg_ids property of this UpdateMongoDbConnectionDetails.
        :type nsg_ids: list[str]

        :param connection_string:
            The value to assign to the connection_string property of this UpdateMongoDbConnectionDetails.
        :type connection_string: str

        :param username:
            The value to assign to the username property of this UpdateMongoDbConnectionDetails.
        :type username: str

        :param password:
            The value to assign to the password property of this UpdateMongoDbConnectionDetails.
        :type password: str

        :param database_id:
            The value to assign to the database_id property of this UpdateMongoDbConnectionDetails.
        :type database_id: str

        """
        self.swagger_types = {
            'connection_type': 'str',
            'display_name': 'str',
            'description': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'vault_id': 'str',
            'key_id': 'str',
            'nsg_ids': 'list[str]',
            'connection_string': 'str',
            'username': 'str',
            'password': 'str',
            'database_id': 'str'
        }

        self.attribute_map = {
            'connection_type': 'connectionType',
            'display_name': 'displayName',
            'description': 'description',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'vault_id': 'vaultId',
            'key_id': 'keyId',
            'nsg_ids': 'nsgIds',
            'connection_string': 'connectionString',
            'username': 'username',
            'password': 'password',
            'database_id': 'databaseId'
        }

        self._connection_type = None
        self._display_name = None
        self._description = None
        self._freeform_tags = None
        self._defined_tags = None
        self._vault_id = None
        self._key_id = None
        self._nsg_ids = None
        self._connection_string = None
        self._username = None
        self._password = None
        self._database_id = None
        self._connection_type = 'MONGODB'

    @property
    def connection_string(self):
        """
        Gets the connection_string of this UpdateMongoDbConnectionDetails.
        MongoDB connection string.
        e.g.: 'mongodb://mongodb0.example.com:27017/recordsrecords'


        :return: The connection_string of this UpdateMongoDbConnectionDetails.
        :rtype: str
        """
        return self._connection_string

    @connection_string.setter
    def connection_string(self, connection_string):
        """
        Sets the connection_string of this UpdateMongoDbConnectionDetails.
        MongoDB connection string.
        e.g.: 'mongodb://mongodb0.example.com:27017/recordsrecords'


        :param connection_string: The connection_string of this UpdateMongoDbConnectionDetails.
        :type: str
        """
        self._connection_string = connection_string

    @property
    def username(self):
        """
        Gets the username of this UpdateMongoDbConnectionDetails.
        The username Oracle GoldenGate uses to connect to the database.
        This username must already exist and be available by the database to be connected to.


        :return: The username of this UpdateMongoDbConnectionDetails.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this UpdateMongoDbConnectionDetails.
        The username Oracle GoldenGate uses to connect to the database.
        This username must already exist and be available by the database to be connected to.


        :param username: The username of this UpdateMongoDbConnectionDetails.
        :type: str
        """
        self._username = username

    @property
    def password(self):
        """
        Gets the password of this UpdateMongoDbConnectionDetails.
        The password Oracle GoldenGate uses to connect the associated database.


        :return: The password of this UpdateMongoDbConnectionDetails.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password):
        """
        Sets the password of this UpdateMongoDbConnectionDetails.
        The password Oracle GoldenGate uses to connect the associated database.


        :param password: The password of this UpdateMongoDbConnectionDetails.
        :type: str
        """
        self._password = password

    @property
    def database_id(self):
        """
        Gets the database_id of this UpdateMongoDbConnectionDetails.
        The `OCID`__ of the Oracle Autonomous Json Database.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The database_id of this UpdateMongoDbConnectionDetails.
        :rtype: str
        """
        return self._database_id

    @database_id.setter
    def database_id(self, database_id):
        """
        Sets the database_id of this UpdateMongoDbConnectionDetails.
        The `OCID`__ of the Oracle Autonomous Json Database.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param database_id: The database_id of this UpdateMongoDbConnectionDetails.
        :type: str
        """
        self._database_id = database_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
