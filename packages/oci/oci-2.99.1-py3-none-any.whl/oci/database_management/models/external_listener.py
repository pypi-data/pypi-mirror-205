# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalListener(object):
    """
    The details of an external listener.
    """

    #: A constant which can be used with the listener_type property of a ExternalListener.
    #: This constant has a value of "ASM"
    LISTENER_TYPE_ASM = "ASM"

    #: A constant which can be used with the listener_type property of a ExternalListener.
    #: This constant has a value of "LOCAL"
    LISTENER_TYPE_LOCAL = "LOCAL"

    #: A constant which can be used with the listener_type property of a ExternalListener.
    #: This constant has a value of "SCAN"
    LISTENER_TYPE_SCAN = "SCAN"

    #: A constant which can be used with the lifecycle_state property of a ExternalListener.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a ExternalListener.
    #: This constant has a value of "NOT_CONNECTED"
    LIFECYCLE_STATE_NOT_CONNECTED = "NOT_CONNECTED"

    #: A constant which can be used with the lifecycle_state property of a ExternalListener.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ExternalListener.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ExternalListener.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a ExternalListener.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a ExternalListener.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a ExternalListener.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalListener object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ExternalListener.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this ExternalListener.
        :type display_name: str

        :param component_name:
            The value to assign to the component_name property of this ExternalListener.
        :type component_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ExternalListener.
        :type compartment_id: str

        :param external_db_system_id:
            The value to assign to the external_db_system_id property of this ExternalListener.
        :type external_db_system_id: str

        :param external_connector_id:
            The value to assign to the external_connector_id property of this ExternalListener.
        :type external_connector_id: str

        :param external_db_node_id:
            The value to assign to the external_db_node_id property of this ExternalListener.
        :type external_db_node_id: str

        :param external_db_home_id:
            The value to assign to the external_db_home_id property of this ExternalListener.
        :type external_db_home_id: str

        :param listener_alias:
            The value to assign to the listener_alias property of this ExternalListener.
        :type listener_alias: str

        :param listener_type:
            The value to assign to the listener_type property of this ExternalListener.
            Allowed values for this property are: "ASM", "LOCAL", "SCAN", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type listener_type: str

        :param additional_details:
            The value to assign to the additional_details property of this ExternalListener.
        :type additional_details: dict(str, str)

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ExternalListener.
            Allowed values for this property are: "CREATING", "NOT_CONNECTED", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this ExternalListener.
        :type lifecycle_details: str

        :param listener_ora_location:
            The value to assign to the listener_ora_location property of this ExternalListener.
        :type listener_ora_location: str

        :param oracle_home:
            The value to assign to the oracle_home property of this ExternalListener.
        :type oracle_home: str

        :param host_name:
            The value to assign to the host_name property of this ExternalListener.
        :type host_name: str

        :param adr_home_directory:
            The value to assign to the adr_home_directory property of this ExternalListener.
        :type adr_home_directory: str

        :param log_directory:
            The value to assign to the log_directory property of this ExternalListener.
        :type log_directory: str

        :param trace_directory:
            The value to assign to the trace_directory property of this ExternalListener.
        :type trace_directory: str

        :param version:
            The value to assign to the version property of this ExternalListener.
        :type version: str

        :param endpoints:
            The value to assign to the endpoints property of this ExternalListener.
        :type endpoints: list[oci.database_management.models.ExternalListenerEndpoint]

        :param serviced_databases:
            The value to assign to the serviced_databases property of this ExternalListener.
        :type serviced_databases: list[oci.database_management.models.ExternalListenerServicedDatabase]

        :param serviced_asms:
            The value to assign to the serviced_asms property of this ExternalListener.
        :type serviced_asms: list[oci.database_management.models.ExternalServicedAsm]

        :param time_created:
            The value to assign to the time_created property of this ExternalListener.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ExternalListener.
        :type time_updated: datetime

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'component_name': 'str',
            'compartment_id': 'str',
            'external_db_system_id': 'str',
            'external_connector_id': 'str',
            'external_db_node_id': 'str',
            'external_db_home_id': 'str',
            'listener_alias': 'str',
            'listener_type': 'str',
            'additional_details': 'dict(str, str)',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'listener_ora_location': 'str',
            'oracle_home': 'str',
            'host_name': 'str',
            'adr_home_directory': 'str',
            'log_directory': 'str',
            'trace_directory': 'str',
            'version': 'str',
            'endpoints': 'list[ExternalListenerEndpoint]',
            'serviced_databases': 'list[ExternalListenerServicedDatabase]',
            'serviced_asms': 'list[ExternalServicedAsm]',
            'time_created': 'datetime',
            'time_updated': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'component_name': 'componentName',
            'compartment_id': 'compartmentId',
            'external_db_system_id': 'externalDbSystemId',
            'external_connector_id': 'externalConnectorId',
            'external_db_node_id': 'externalDbNodeId',
            'external_db_home_id': 'externalDbHomeId',
            'listener_alias': 'listenerAlias',
            'listener_type': 'listenerType',
            'additional_details': 'additionalDetails',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'listener_ora_location': 'listenerOraLocation',
            'oracle_home': 'oracleHome',
            'host_name': 'hostName',
            'adr_home_directory': 'adrHomeDirectory',
            'log_directory': 'logDirectory',
            'trace_directory': 'traceDirectory',
            'version': 'version',
            'endpoints': 'endpoints',
            'serviced_databases': 'servicedDatabases',
            'serviced_asms': 'servicedAsms',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated'
        }

        self._id = None
        self._display_name = None
        self._component_name = None
        self._compartment_id = None
        self._external_db_system_id = None
        self._external_connector_id = None
        self._external_db_node_id = None
        self._external_db_home_id = None
        self._listener_alias = None
        self._listener_type = None
        self._additional_details = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._listener_ora_location = None
        self._oracle_home = None
        self._host_name = None
        self._adr_home_directory = None
        self._log_directory = None
        self._trace_directory = None
        self._version = None
        self._endpoints = None
        self._serviced_databases = None
        self._serviced_asms = None
        self._time_created = None
        self._time_updated = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ExternalListener.
        The `OCID`__ of the external listener.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ExternalListener.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ExternalListener.
        The `OCID`__ of the external listener.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ExternalListener.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ExternalListener.
        The user-friendly name for the external listener. The name does not have to be unique.


        :return: The display_name of this ExternalListener.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ExternalListener.
        The user-friendly name for the external listener. The name does not have to be unique.


        :param display_name: The display_name of this ExternalListener.
        :type: str
        """
        self._display_name = display_name

    @property
    def component_name(self):
        """
        **[Required]** Gets the component_name of this ExternalListener.
        The name of the external listener.


        :return: The component_name of this ExternalListener.
        :rtype: str
        """
        return self._component_name

    @component_name.setter
    def component_name(self, component_name):
        """
        Sets the component_name of this ExternalListener.
        The name of the external listener.


        :param component_name: The component_name of this ExternalListener.
        :type: str
        """
        self._component_name = component_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ExternalListener.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ExternalListener.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ExternalListener.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ExternalListener.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def external_db_system_id(self):
        """
        **[Required]** Gets the external_db_system_id of this ExternalListener.
        The `OCID`__ of the external DB system that the listener is a part of.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_db_system_id of this ExternalListener.
        :rtype: str
        """
        return self._external_db_system_id

    @external_db_system_id.setter
    def external_db_system_id(self, external_db_system_id):
        """
        Sets the external_db_system_id of this ExternalListener.
        The `OCID`__ of the external DB system that the listener is a part of.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_db_system_id: The external_db_system_id of this ExternalListener.
        :type: str
        """
        self._external_db_system_id = external_db_system_id

    @property
    def external_connector_id(self):
        """
        Gets the external_connector_id of this ExternalListener.
        The `OCID`__ of the external connector.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_connector_id of this ExternalListener.
        :rtype: str
        """
        return self._external_connector_id

    @external_connector_id.setter
    def external_connector_id(self, external_connector_id):
        """
        Sets the external_connector_id of this ExternalListener.
        The `OCID`__ of the external connector.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_connector_id: The external_connector_id of this ExternalListener.
        :type: str
        """
        self._external_connector_id = external_connector_id

    @property
    def external_db_node_id(self):
        """
        Gets the external_db_node_id of this ExternalListener.
        The `OCID`__ of the external DB node.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_db_node_id of this ExternalListener.
        :rtype: str
        """
        return self._external_db_node_id

    @external_db_node_id.setter
    def external_db_node_id(self, external_db_node_id):
        """
        Sets the external_db_node_id of this ExternalListener.
        The `OCID`__ of the external DB node.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_db_node_id: The external_db_node_id of this ExternalListener.
        :type: str
        """
        self._external_db_node_id = external_db_node_id

    @property
    def external_db_home_id(self):
        """
        Gets the external_db_home_id of this ExternalListener.
        The `OCID`__ of the external DB home.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_db_home_id of this ExternalListener.
        :rtype: str
        """
        return self._external_db_home_id

    @external_db_home_id.setter
    def external_db_home_id(self, external_db_home_id):
        """
        Sets the external_db_home_id of this ExternalListener.
        The `OCID`__ of the external DB home.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_db_home_id: The external_db_home_id of this ExternalListener.
        :type: str
        """
        self._external_db_home_id = external_db_home_id

    @property
    def listener_alias(self):
        """
        Gets the listener_alias of this ExternalListener.
        The listener alias.


        :return: The listener_alias of this ExternalListener.
        :rtype: str
        """
        return self._listener_alias

    @listener_alias.setter
    def listener_alias(self, listener_alias):
        """
        Sets the listener_alias of this ExternalListener.
        The listener alias.


        :param listener_alias: The listener_alias of this ExternalListener.
        :type: str
        """
        self._listener_alias = listener_alias

    @property
    def listener_type(self):
        """
        Gets the listener_type of this ExternalListener.
        The type of listener.

        Allowed values for this property are: "ASM", "LOCAL", "SCAN", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The listener_type of this ExternalListener.
        :rtype: str
        """
        return self._listener_type

    @listener_type.setter
    def listener_type(self, listener_type):
        """
        Sets the listener_type of this ExternalListener.
        The type of listener.


        :param listener_type: The listener_type of this ExternalListener.
        :type: str
        """
        allowed_values = ["ASM", "LOCAL", "SCAN"]
        if not value_allowed_none_or_none_sentinel(listener_type, allowed_values):
            listener_type = 'UNKNOWN_ENUM_VALUE'
        self._listener_type = listener_type

    @property
    def additional_details(self):
        """
        Gets the additional_details of this ExternalListener.
        The additional details of the external listener defined in `{\"key\": \"value\"}` format.
        Example: `{\"bar-key\": \"value\"}`


        :return: The additional_details of this ExternalListener.
        :rtype: dict(str, str)
        """
        return self._additional_details

    @additional_details.setter
    def additional_details(self, additional_details):
        """
        Sets the additional_details of this ExternalListener.
        The additional details of the external listener defined in `{\"key\": \"value\"}` format.
        Example: `{\"bar-key\": \"value\"}`


        :param additional_details: The additional_details of this ExternalListener.
        :type: dict(str, str)
        """
        self._additional_details = additional_details

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ExternalListener.
        The current lifecycle state of the external listener.

        Allowed values for this property are: "CREATING", "NOT_CONNECTED", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ExternalListener.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ExternalListener.
        The current lifecycle state of the external listener.


        :param lifecycle_state: The lifecycle_state of this ExternalListener.
        :type: str
        """
        allowed_values = ["CREATING", "NOT_CONNECTED", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this ExternalListener.
        Additional information about the current lifecycle state.


        :return: The lifecycle_details of this ExternalListener.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this ExternalListener.
        Additional information about the current lifecycle state.


        :param lifecycle_details: The lifecycle_details of this ExternalListener.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def listener_ora_location(self):
        """
        Gets the listener_ora_location of this ExternalListener.
        The location of the listener configuration file listener.ora.


        :return: The listener_ora_location of this ExternalListener.
        :rtype: str
        """
        return self._listener_ora_location

    @listener_ora_location.setter
    def listener_ora_location(self, listener_ora_location):
        """
        Sets the listener_ora_location of this ExternalListener.
        The location of the listener configuration file listener.ora.


        :param listener_ora_location: The listener_ora_location of this ExternalListener.
        :type: str
        """
        self._listener_ora_location = listener_ora_location

    @property
    def oracle_home(self):
        """
        Gets the oracle_home of this ExternalListener.
        The Oracle home location of the listener.


        :return: The oracle_home of this ExternalListener.
        :rtype: str
        """
        return self._oracle_home

    @oracle_home.setter
    def oracle_home(self, oracle_home):
        """
        Sets the oracle_home of this ExternalListener.
        The Oracle home location of the listener.


        :param oracle_home: The oracle_home of this ExternalListener.
        :type: str
        """
        self._oracle_home = oracle_home

    @property
    def host_name(self):
        """
        Gets the host_name of this ExternalListener.
        The name of the host on which the external listener is running.


        :return: The host_name of this ExternalListener.
        :rtype: str
        """
        return self._host_name

    @host_name.setter
    def host_name(self, host_name):
        """
        Sets the host_name of this ExternalListener.
        The name of the host on which the external listener is running.


        :param host_name: The host_name of this ExternalListener.
        :type: str
        """
        self._host_name = host_name

    @property
    def adr_home_directory(self):
        """
        Gets the adr_home_directory of this ExternalListener.
        The directory that stores tracing and logging incidents when Automatic Diagnostic Repository (ADR) is enabled.


        :return: The adr_home_directory of this ExternalListener.
        :rtype: str
        """
        return self._adr_home_directory

    @adr_home_directory.setter
    def adr_home_directory(self, adr_home_directory):
        """
        Sets the adr_home_directory of this ExternalListener.
        The directory that stores tracing and logging incidents when Automatic Diagnostic Repository (ADR) is enabled.


        :param adr_home_directory: The adr_home_directory of this ExternalListener.
        :type: str
        """
        self._adr_home_directory = adr_home_directory

    @property
    def log_directory(self):
        """
        Gets the log_directory of this ExternalListener.
        The destination directory of the listener log file.


        :return: The log_directory of this ExternalListener.
        :rtype: str
        """
        return self._log_directory

    @log_directory.setter
    def log_directory(self, log_directory):
        """
        Sets the log_directory of this ExternalListener.
        The destination directory of the listener log file.


        :param log_directory: The log_directory of this ExternalListener.
        :type: str
        """
        self._log_directory = log_directory

    @property
    def trace_directory(self):
        """
        Gets the trace_directory of this ExternalListener.
        The destination directory of the listener trace file.


        :return: The trace_directory of this ExternalListener.
        :rtype: str
        """
        return self._trace_directory

    @trace_directory.setter
    def trace_directory(self, trace_directory):
        """
        Sets the trace_directory of this ExternalListener.
        The destination directory of the listener trace file.


        :param trace_directory: The trace_directory of this ExternalListener.
        :type: str
        """
        self._trace_directory = trace_directory

    @property
    def version(self):
        """
        Gets the version of this ExternalListener.
        The listener version.


        :return: The version of this ExternalListener.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this ExternalListener.
        The listener version.


        :param version: The version of this ExternalListener.
        :type: str
        """
        self._version = version

    @property
    def endpoints(self):
        """
        Gets the endpoints of this ExternalListener.
        The list of protocol addresses the listener is configured to listen on.


        :return: The endpoints of this ExternalListener.
        :rtype: list[oci.database_management.models.ExternalListenerEndpoint]
        """
        return self._endpoints

    @endpoints.setter
    def endpoints(self, endpoints):
        """
        Sets the endpoints of this ExternalListener.
        The list of protocol addresses the listener is configured to listen on.


        :param endpoints: The endpoints of this ExternalListener.
        :type: list[oci.database_management.models.ExternalListenerEndpoint]
        """
        self._endpoints = endpoints

    @property
    def serviced_databases(self):
        """
        Gets the serviced_databases of this ExternalListener.
        The list of databases that are serviced by the listener.


        :return: The serviced_databases of this ExternalListener.
        :rtype: list[oci.database_management.models.ExternalListenerServicedDatabase]
        """
        return self._serviced_databases

    @serviced_databases.setter
    def serviced_databases(self, serviced_databases):
        """
        Sets the serviced_databases of this ExternalListener.
        The list of databases that are serviced by the listener.


        :param serviced_databases: The serviced_databases of this ExternalListener.
        :type: list[oci.database_management.models.ExternalListenerServicedDatabase]
        """
        self._serviced_databases = serviced_databases

    @property
    def serviced_asms(self):
        """
        Gets the serviced_asms of this ExternalListener.
        The list of ASMs that are serviced by the listener.


        :return: The serviced_asms of this ExternalListener.
        :rtype: list[oci.database_management.models.ExternalServicedAsm]
        """
        return self._serviced_asms

    @serviced_asms.setter
    def serviced_asms(self, serviced_asms):
        """
        Sets the serviced_asms of this ExternalListener.
        The list of ASMs that are serviced by the listener.


        :param serviced_asms: The serviced_asms of this ExternalListener.
        :type: list[oci.database_management.models.ExternalServicedAsm]
        """
        self._serviced_asms = serviced_asms

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this ExternalListener.
        The date and time the external listener was created.


        :return: The time_created of this ExternalListener.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ExternalListener.
        The date and time the external listener was created.


        :param time_created: The time_created of this ExternalListener.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        **[Required]** Gets the time_updated of this ExternalListener.
        The date and time the external listener was last updated.


        :return: The time_updated of this ExternalListener.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this ExternalListener.
        The date and time the external listener was last updated.


        :param time_updated: The time_updated of this ExternalListener.
        :type: datetime
        """
        self._time_updated = time_updated

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
