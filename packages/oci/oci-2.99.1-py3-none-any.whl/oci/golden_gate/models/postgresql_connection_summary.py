# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .connection_summary import ConnectionSummary
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PostgresqlConnectionSummary(ConnectionSummary):
    """
    Summary of the PostgreSQL Database Connection.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PostgresqlConnectionSummary object with values from keyword arguments. The default value of the :py:attr:`~oci.golden_gate.models.PostgresqlConnectionSummary.connection_type` attribute
        of this class is ``POSTGRESQL`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param connection_type:
            The value to assign to the connection_type property of this PostgresqlConnectionSummary.
            Allowed values for this property are: "GOLDENGATE", "KAFKA", "KAFKA_SCHEMA_REGISTRY", "MYSQL", "JAVA_MESSAGE_SERVICE", "MICROSOFT_SQLSERVER", "OCI_OBJECT_STORAGE", "ORACLE", "AZURE_DATA_LAKE_STORAGE", "POSTGRESQL", "AZURE_SYNAPSE_ANALYTICS", "SNOWFLAKE", "AMAZON_S3", "HDFS", "ORACLE_NOSQL", "MONGODB"
        :type connection_type: str

        :param id:
            The value to assign to the id property of this PostgresqlConnectionSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this PostgresqlConnectionSummary.
        :type display_name: str

        :param description:
            The value to assign to the description property of this PostgresqlConnectionSummary.
        :type description: str

        :param compartment_id:
            The value to assign to the compartment_id property of this PostgresqlConnectionSummary.
        :type compartment_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this PostgresqlConnectionSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this PostgresqlConnectionSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this PostgresqlConnectionSummary.
        :type system_tags: dict(str, dict(str, object))

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this PostgresqlConnectionSummary.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this PostgresqlConnectionSummary.
        :type lifecycle_details: str

        :param time_created:
            The value to assign to the time_created property of this PostgresqlConnectionSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this PostgresqlConnectionSummary.
        :type time_updated: datetime

        :param vault_id:
            The value to assign to the vault_id property of this PostgresqlConnectionSummary.
        :type vault_id: str

        :param key_id:
            The value to assign to the key_id property of this PostgresqlConnectionSummary.
        :type key_id: str

        :param subnet_id:
            The value to assign to the subnet_id property of this PostgresqlConnectionSummary.
        :type subnet_id: str

        :param ingress_ips:
            The value to assign to the ingress_ips property of this PostgresqlConnectionSummary.
        :type ingress_ips: list[oci.golden_gate.models.IngressIpDetails]

        :param nsg_ids:
            The value to assign to the nsg_ids property of this PostgresqlConnectionSummary.
        :type nsg_ids: list[str]

        :param technology_type:
            The value to assign to the technology_type property of this PostgresqlConnectionSummary.
        :type technology_type: str

        :param database_name:
            The value to assign to the database_name property of this PostgresqlConnectionSummary.
        :type database_name: str

        :param host:
            The value to assign to the host property of this PostgresqlConnectionSummary.
        :type host: str

        :param port:
            The value to assign to the port property of this PostgresqlConnectionSummary.
        :type port: int

        :param username:
            The value to assign to the username property of this PostgresqlConnectionSummary.
        :type username: str

        :param additional_attributes:
            The value to assign to the additional_attributes property of this PostgresqlConnectionSummary.
        :type additional_attributes: list[oci.golden_gate.models.NameValuePair]

        :param security_protocol:
            The value to assign to the security_protocol property of this PostgresqlConnectionSummary.
        :type security_protocol: str

        :param ssl_mode:
            The value to assign to the ssl_mode property of this PostgresqlConnectionSummary.
        :type ssl_mode: str

        :param private_ip:
            The value to assign to the private_ip property of this PostgresqlConnectionSummary.
        :type private_ip: str

        """
        self.swagger_types = {
            'connection_type': 'str',
            'id': 'str',
            'display_name': 'str',
            'description': 'str',
            'compartment_id': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'vault_id': 'str',
            'key_id': 'str',
            'subnet_id': 'str',
            'ingress_ips': 'list[IngressIpDetails]',
            'nsg_ids': 'list[str]',
            'technology_type': 'str',
            'database_name': 'str',
            'host': 'str',
            'port': 'int',
            'username': 'str',
            'additional_attributes': 'list[NameValuePair]',
            'security_protocol': 'str',
            'ssl_mode': 'str',
            'private_ip': 'str'
        }

        self.attribute_map = {
            'connection_type': 'connectionType',
            'id': 'id',
            'display_name': 'displayName',
            'description': 'description',
            'compartment_id': 'compartmentId',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'vault_id': 'vaultId',
            'key_id': 'keyId',
            'subnet_id': 'subnetId',
            'ingress_ips': 'ingressIps',
            'nsg_ids': 'nsgIds',
            'technology_type': 'technologyType',
            'database_name': 'databaseName',
            'host': 'host',
            'port': 'port',
            'username': 'username',
            'additional_attributes': 'additionalAttributes',
            'security_protocol': 'securityProtocol',
            'ssl_mode': 'sslMode',
            'private_ip': 'privateIp'
        }

        self._connection_type = None
        self._id = None
        self._display_name = None
        self._description = None
        self._compartment_id = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._time_created = None
        self._time_updated = None
        self._vault_id = None
        self._key_id = None
        self._subnet_id = None
        self._ingress_ips = None
        self._nsg_ids = None
        self._technology_type = None
        self._database_name = None
        self._host = None
        self._port = None
        self._username = None
        self._additional_attributes = None
        self._security_protocol = None
        self._ssl_mode = None
        self._private_ip = None
        self._connection_type = 'POSTGRESQL'

    @property
    def technology_type(self):
        """
        **[Required]** Gets the technology_type of this PostgresqlConnectionSummary.
        The PostgreSQL technology type.


        :return: The technology_type of this PostgresqlConnectionSummary.
        :rtype: str
        """
        return self._technology_type

    @technology_type.setter
    def technology_type(self, technology_type):
        """
        Sets the technology_type of this PostgresqlConnectionSummary.
        The PostgreSQL technology type.


        :param technology_type: The technology_type of this PostgresqlConnectionSummary.
        :type: str
        """
        self._technology_type = technology_type

    @property
    def database_name(self):
        """
        **[Required]** Gets the database_name of this PostgresqlConnectionSummary.
        The name of the database.


        :return: The database_name of this PostgresqlConnectionSummary.
        :rtype: str
        """
        return self._database_name

    @database_name.setter
    def database_name(self, database_name):
        """
        Sets the database_name of this PostgresqlConnectionSummary.
        The name of the database.


        :param database_name: The database_name of this PostgresqlConnectionSummary.
        :type: str
        """
        self._database_name = database_name

    @property
    def host(self):
        """
        **[Required]** Gets the host of this PostgresqlConnectionSummary.
        The name or address of a host.


        :return: The host of this PostgresqlConnectionSummary.
        :rtype: str
        """
        return self._host

    @host.setter
    def host(self, host):
        """
        Sets the host of this PostgresqlConnectionSummary.
        The name or address of a host.


        :param host: The host of this PostgresqlConnectionSummary.
        :type: str
        """
        self._host = host

    @property
    def port(self):
        """
        **[Required]** Gets the port of this PostgresqlConnectionSummary.
        The port of an endpoint usually specified for a connection.


        :return: The port of this PostgresqlConnectionSummary.
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """
        Sets the port of this PostgresqlConnectionSummary.
        The port of an endpoint usually specified for a connection.


        :param port: The port of this PostgresqlConnectionSummary.
        :type: int
        """
        self._port = port

    @property
    def username(self):
        """
        **[Required]** Gets the username of this PostgresqlConnectionSummary.
        The username Oracle GoldenGate uses to connect the associated system of the given technology.
        This username must already exist and be available by the system/application to be connected to
        and must conform to the case sensitivty requirments defined in it.


        :return: The username of this PostgresqlConnectionSummary.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """
        Sets the username of this PostgresqlConnectionSummary.
        The username Oracle GoldenGate uses to connect the associated system of the given technology.
        This username must already exist and be available by the system/application to be connected to
        and must conform to the case sensitivty requirments defined in it.


        :param username: The username of this PostgresqlConnectionSummary.
        :type: str
        """
        self._username = username

    @property
    def additional_attributes(self):
        """
        Gets the additional_attributes of this PostgresqlConnectionSummary.
        An array of name-value pair attribute entries.
        Used as additional parameters in connection string.


        :return: The additional_attributes of this PostgresqlConnectionSummary.
        :rtype: list[oci.golden_gate.models.NameValuePair]
        """
        return self._additional_attributes

    @additional_attributes.setter
    def additional_attributes(self, additional_attributes):
        """
        Sets the additional_attributes of this PostgresqlConnectionSummary.
        An array of name-value pair attribute entries.
        Used as additional parameters in connection string.


        :param additional_attributes: The additional_attributes of this PostgresqlConnectionSummary.
        :type: list[oci.golden_gate.models.NameValuePair]
        """
        self._additional_attributes = additional_attributes

    @property
    def security_protocol(self):
        """
        **[Required]** Gets the security_protocol of this PostgresqlConnectionSummary.
        Security protocol for PostgreSQL.


        :return: The security_protocol of this PostgresqlConnectionSummary.
        :rtype: str
        """
        return self._security_protocol

    @security_protocol.setter
    def security_protocol(self, security_protocol):
        """
        Sets the security_protocol of this PostgresqlConnectionSummary.
        Security protocol for PostgreSQL.


        :param security_protocol: The security_protocol of this PostgresqlConnectionSummary.
        :type: str
        """
        self._security_protocol = security_protocol

    @property
    def ssl_mode(self):
        """
        Gets the ssl_mode of this PostgresqlConnectionSummary.
        SSL modes for PostgreSQL.


        :return: The ssl_mode of this PostgresqlConnectionSummary.
        :rtype: str
        """
        return self._ssl_mode

    @ssl_mode.setter
    def ssl_mode(self, ssl_mode):
        """
        Sets the ssl_mode of this PostgresqlConnectionSummary.
        SSL modes for PostgreSQL.


        :param ssl_mode: The ssl_mode of this PostgresqlConnectionSummary.
        :type: str
        """
        self._ssl_mode = ssl_mode

    @property
    def private_ip(self):
        """
        Gets the private_ip of this PostgresqlConnectionSummary.
        The private IP address of the connection's endpoint in the customer's VCN, typically a
        database endpoint or a big data endpoint (e.g. Kafka bootstrap server).
        In case the privateIp is provided, the subnetId must also be provided.
        In case the privateIp (and the subnetId) is not provided it is assumed the datasource is publicly accessible.
        In case the connection is accessible only privately, the lack of privateIp will result in not being able to access the connection.


        :return: The private_ip of this PostgresqlConnectionSummary.
        :rtype: str
        """
        return self._private_ip

    @private_ip.setter
    def private_ip(self, private_ip):
        """
        Sets the private_ip of this PostgresqlConnectionSummary.
        The private IP address of the connection's endpoint in the customer's VCN, typically a
        database endpoint or a big data endpoint (e.g. Kafka bootstrap server).
        In case the privateIp is provided, the subnetId must also be provided.
        In case the privateIp (and the subnetId) is not provided it is assumed the datasource is publicly accessible.
        In case the connection is accessible only privately, the lack of privateIp will result in not being able to access the connection.


        :param private_ip: The private_ip of this PostgresqlConnectionSummary.
        :type: str
        """
        self._private_ip = private_ip

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
