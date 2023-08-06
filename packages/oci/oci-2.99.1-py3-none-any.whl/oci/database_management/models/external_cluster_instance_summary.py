# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalClusterInstanceSummary(object):
    """
    The summary of an external cluster instance.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalClusterInstanceSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ExternalClusterInstanceSummary.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this ExternalClusterInstanceSummary.
        :type display_name: str

        :param component_name:
            The value to assign to the component_name property of this ExternalClusterInstanceSummary.
        :type component_name: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ExternalClusterInstanceSummary.
        :type compartment_id: str

        :param external_cluster_id:
            The value to assign to the external_cluster_id property of this ExternalClusterInstanceSummary.
        :type external_cluster_id: str

        :param external_db_system_id:
            The value to assign to the external_db_system_id property of this ExternalClusterInstanceSummary.
        :type external_db_system_id: str

        :param external_db_node_id:
            The value to assign to the external_db_node_id property of this ExternalClusterInstanceSummary.
        :type external_db_node_id: str

        :param external_connector_id:
            The value to assign to the external_connector_id property of this ExternalClusterInstanceSummary.
        :type external_connector_id: str

        :param host_name:
            The value to assign to the host_name property of this ExternalClusterInstanceSummary.
        :type host_name: str

        :param node_role:
            The value to assign to the node_role property of this ExternalClusterInstanceSummary.
        :type node_role: str

        :param crs_base_directory:
            The value to assign to the crs_base_directory property of this ExternalClusterInstanceSummary.
        :type crs_base_directory: str

        :param adr_home_directory:
            The value to assign to the adr_home_directory property of this ExternalClusterInstanceSummary.
        :type adr_home_directory: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ExternalClusterInstanceSummary.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this ExternalClusterInstanceSummary.
        :type lifecycle_details: str

        :param time_created:
            The value to assign to the time_created property of this ExternalClusterInstanceSummary.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ExternalClusterInstanceSummary.
        :type time_updated: datetime

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'component_name': 'str',
            'compartment_id': 'str',
            'external_cluster_id': 'str',
            'external_db_system_id': 'str',
            'external_db_node_id': 'str',
            'external_connector_id': 'str',
            'host_name': 'str',
            'node_role': 'str',
            'crs_base_directory': 'str',
            'adr_home_directory': 'str',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'component_name': 'componentName',
            'compartment_id': 'compartmentId',
            'external_cluster_id': 'externalClusterId',
            'external_db_system_id': 'externalDbSystemId',
            'external_db_node_id': 'externalDbNodeId',
            'external_connector_id': 'externalConnectorId',
            'host_name': 'hostName',
            'node_role': 'nodeRole',
            'crs_base_directory': 'crsBaseDirectory',
            'adr_home_directory': 'adrHomeDirectory',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated'
        }

        self._id = None
        self._display_name = None
        self._component_name = None
        self._compartment_id = None
        self._external_cluster_id = None
        self._external_db_system_id = None
        self._external_db_node_id = None
        self._external_connector_id = None
        self._host_name = None
        self._node_role = None
        self._crs_base_directory = None
        self._adr_home_directory = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._time_created = None
        self._time_updated = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ExternalClusterInstanceSummary.
        The `OCID`__ of the external cluster instance.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ExternalClusterInstanceSummary.
        The `OCID`__ of the external cluster instance.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ExternalClusterInstanceSummary.
        The user-friendly name for the cluster instance. The name does not have to be unique.


        :return: The display_name of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ExternalClusterInstanceSummary.
        The user-friendly name for the cluster instance. The name does not have to be unique.


        :param display_name: The display_name of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def component_name(self):
        """
        **[Required]** Gets the component_name of this ExternalClusterInstanceSummary.
        The name of the external cluster instance.


        :return: The component_name of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._component_name

    @component_name.setter
    def component_name(self, component_name):
        """
        Sets the component_name of this ExternalClusterInstanceSummary.
        The name of the external cluster instance.


        :param component_name: The component_name of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._component_name = component_name

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ExternalClusterInstanceSummary.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ExternalClusterInstanceSummary.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def external_cluster_id(self):
        """
        **[Required]** Gets the external_cluster_id of this ExternalClusterInstanceSummary.
        The `OCID`__ of the external cluster that the cluster instance belongs to.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_cluster_id of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._external_cluster_id

    @external_cluster_id.setter
    def external_cluster_id(self, external_cluster_id):
        """
        Sets the external_cluster_id of this ExternalClusterInstanceSummary.
        The `OCID`__ of the external cluster that the cluster instance belongs to.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_cluster_id: The external_cluster_id of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._external_cluster_id = external_cluster_id

    @property
    def external_db_system_id(self):
        """
        **[Required]** Gets the external_db_system_id of this ExternalClusterInstanceSummary.
        The `OCID`__ of the external DB system that the cluster instance is a part of.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_db_system_id of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._external_db_system_id

    @external_db_system_id.setter
    def external_db_system_id(self, external_db_system_id):
        """
        Sets the external_db_system_id of this ExternalClusterInstanceSummary.
        The `OCID`__ of the external DB system that the cluster instance is a part of.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_db_system_id: The external_db_system_id of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._external_db_system_id = external_db_system_id

    @property
    def external_db_node_id(self):
        """
        Gets the external_db_node_id of this ExternalClusterInstanceSummary.
        The `OCID`__ of the external DB node.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_db_node_id of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._external_db_node_id

    @external_db_node_id.setter
    def external_db_node_id(self, external_db_node_id):
        """
        Sets the external_db_node_id of this ExternalClusterInstanceSummary.
        The `OCID`__ of the external DB node.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_db_node_id: The external_db_node_id of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._external_db_node_id = external_db_node_id

    @property
    def external_connector_id(self):
        """
        Gets the external_connector_id of this ExternalClusterInstanceSummary.
        The `OCID`__ of the external connector.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_connector_id of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._external_connector_id

    @external_connector_id.setter
    def external_connector_id(self, external_connector_id):
        """
        Sets the external_connector_id of this ExternalClusterInstanceSummary.
        The `OCID`__ of the external connector.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_connector_id: The external_connector_id of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._external_connector_id = external_connector_id

    @property
    def host_name(self):
        """
        Gets the host_name of this ExternalClusterInstanceSummary.
        The name of the host on which the cluster instance is running.


        :return: The host_name of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._host_name

    @host_name.setter
    def host_name(self, host_name):
        """
        Sets the host_name of this ExternalClusterInstanceSummary.
        The name of the host on which the cluster instance is running.


        :param host_name: The host_name of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._host_name = host_name

    @property
    def node_role(self):
        """
        Gets the node_role of this ExternalClusterInstanceSummary.
        The role of the cluster node.


        :return: The node_role of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._node_role

    @node_role.setter
    def node_role(self, node_role):
        """
        Sets the node_role of this ExternalClusterInstanceSummary.
        The role of the cluster node.


        :param node_role: The node_role of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._node_role = node_role

    @property
    def crs_base_directory(self):
        """
        Gets the crs_base_directory of this ExternalClusterInstanceSummary.
        The Oracle base location of Cluster Ready Services (CRS).


        :return: The crs_base_directory of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._crs_base_directory

    @crs_base_directory.setter
    def crs_base_directory(self, crs_base_directory):
        """
        Sets the crs_base_directory of this ExternalClusterInstanceSummary.
        The Oracle base location of Cluster Ready Services (CRS).


        :param crs_base_directory: The crs_base_directory of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._crs_base_directory = crs_base_directory

    @property
    def adr_home_directory(self):
        """
        Gets the adr_home_directory of this ExternalClusterInstanceSummary.
        The Automatic Diagnostic Repository (ADR) home directory for the cluster instance.


        :return: The adr_home_directory of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._adr_home_directory

    @adr_home_directory.setter
    def adr_home_directory(self, adr_home_directory):
        """
        Sets the adr_home_directory of this ExternalClusterInstanceSummary.
        The Automatic Diagnostic Repository (ADR) home directory for the cluster instance.


        :param adr_home_directory: The adr_home_directory of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._adr_home_directory = adr_home_directory

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ExternalClusterInstanceSummary.
        The current lifecycle state of the external cluster instance.


        :return: The lifecycle_state of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ExternalClusterInstanceSummary.
        The current lifecycle state of the external cluster instance.


        :param lifecycle_state: The lifecycle_state of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this ExternalClusterInstanceSummary.
        Additional information about the current lifecycle state.


        :return: The lifecycle_details of this ExternalClusterInstanceSummary.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this ExternalClusterInstanceSummary.
        Additional information about the current lifecycle state.


        :param lifecycle_details: The lifecycle_details of this ExternalClusterInstanceSummary.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def time_created(self):
        """
        Gets the time_created of this ExternalClusterInstanceSummary.
        The date and time the external cluster instance was created.


        :return: The time_created of this ExternalClusterInstanceSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ExternalClusterInstanceSummary.
        The date and time the external cluster instance was created.


        :param time_created: The time_created of this ExternalClusterInstanceSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this ExternalClusterInstanceSummary.
        The date and time the external cluster instance was last updated.


        :return: The time_updated of this ExternalClusterInstanceSummary.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this ExternalClusterInstanceSummary.
        The date and time the external cluster instance was last updated.


        :param time_updated: The time_updated of this ExternalClusterInstanceSummary.
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
