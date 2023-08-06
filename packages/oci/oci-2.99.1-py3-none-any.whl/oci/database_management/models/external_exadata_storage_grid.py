# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .dbm_resource import DbmResource
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExternalExadataStorageGrid(DbmResource):
    """
    The Exadata storage grid details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExternalExadataStorageGrid object with values from keyword arguments. The default value of the :py:attr:`~oci.database_management.models.ExternalExadataStorageGrid.resource_type` attribute
        of this class is ``STORAGE_GRID`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ExternalExadataStorageGrid.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this ExternalExadataStorageGrid.
        :type display_name: str

        :param version:
            The value to assign to the version property of this ExternalExadataStorageGrid.
        :type version: str

        :param internal_id:
            The value to assign to the internal_id property of this ExternalExadataStorageGrid.
        :type internal_id: str

        :param status:
            The value to assign to the status property of this ExternalExadataStorageGrid.
        :type status: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ExternalExadataStorageGrid.
            Allowed values for this property are: "CREATING", "ACTIVE", "INACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_created:
            The value to assign to the time_created property of this ExternalExadataStorageGrid.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ExternalExadataStorageGrid.
        :type time_updated: datetime

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this ExternalExadataStorageGrid.
        :type lifecycle_details: str

        :param additional_details:
            The value to assign to the additional_details property of this ExternalExadataStorageGrid.
        :type additional_details: dict(str, str)

        :param resource_type:
            The value to assign to the resource_type property of this ExternalExadataStorageGrid.
            Allowed values for this property are: "INFRASTRUCTURE_SUMMARY", "INFRASTRUCTURE", "STORAGE_SERVER_SUMMARY", "STORAGE_SERVER", "STORAGE_GRID_SUMMARY", "STORAGE_GRID", "STORAGE_CONNECTOR_SUMMARY", "STORAGE_CONNECTOR", "DATABASE_SYSTEM_SUMMARY", "DATABASE_SUMMARY", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type resource_type: str

        :param exadata_infrastructure_id:
            The value to assign to the exadata_infrastructure_id property of this ExternalExadataStorageGrid.
        :type exadata_infrastructure_id: str

        :param server_count:
            The value to assign to the server_count property of this ExternalExadataStorageGrid.
        :type server_count: float

        :param storage_servers:
            The value to assign to the storage_servers property of this ExternalExadataStorageGrid.
        :type storage_servers: list[oci.database_management.models.ExternalExadataStorageServerSummary]

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'version': 'str',
            'internal_id': 'str',
            'status': 'str',
            'lifecycle_state': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_details': 'str',
            'additional_details': 'dict(str, str)',
            'resource_type': 'str',
            'exadata_infrastructure_id': 'str',
            'server_count': 'float',
            'storage_servers': 'list[ExternalExadataStorageServerSummary]'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'version': 'version',
            'internal_id': 'internalId',
            'status': 'status',
            'lifecycle_state': 'lifecycleState',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_details': 'lifecycleDetails',
            'additional_details': 'additionalDetails',
            'resource_type': 'resourceType',
            'exadata_infrastructure_id': 'exadataInfrastructureId',
            'server_count': 'serverCount',
            'storage_servers': 'storageServers'
        }

        self._id = None
        self._display_name = None
        self._version = None
        self._internal_id = None
        self._status = None
        self._lifecycle_state = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_details = None
        self._additional_details = None
        self._resource_type = None
        self._exadata_infrastructure_id = None
        self._server_count = None
        self._storage_servers = None
        self._resource_type = 'STORAGE_GRID'

    @property
    def exadata_infrastructure_id(self):
        """
        Gets the exadata_infrastructure_id of this ExternalExadataStorageGrid.
        The `OCID`__ of Exadata infrastructure system.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The exadata_infrastructure_id of this ExternalExadataStorageGrid.
        :rtype: str
        """
        return self._exadata_infrastructure_id

    @exadata_infrastructure_id.setter
    def exadata_infrastructure_id(self, exadata_infrastructure_id):
        """
        Sets the exadata_infrastructure_id of this ExternalExadataStorageGrid.
        The `OCID`__ of Exadata infrastructure system.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param exadata_infrastructure_id: The exadata_infrastructure_id of this ExternalExadataStorageGrid.
        :type: str
        """
        self._exadata_infrastructure_id = exadata_infrastructure_id

    @property
    def server_count(self):
        """
        Gets the server_count of this ExternalExadataStorageGrid.
        The number of the storage servers in the Exadata infrastructure.


        :return: The server_count of this ExternalExadataStorageGrid.
        :rtype: float
        """
        return self._server_count

    @server_count.setter
    def server_count(self, server_count):
        """
        Sets the server_count of this ExternalExadataStorageGrid.
        The number of the storage servers in the Exadata infrastructure.


        :param server_count: The server_count of this ExternalExadataStorageGrid.
        :type: float
        """
        self._server_count = server_count

    @property
    def storage_servers(self):
        """
        Gets the storage_servers of this ExternalExadataStorageGrid.
        A list of monitored Exadata storage server.


        :return: The storage_servers of this ExternalExadataStorageGrid.
        :rtype: list[oci.database_management.models.ExternalExadataStorageServerSummary]
        """
        return self._storage_servers

    @storage_servers.setter
    def storage_servers(self, storage_servers):
        """
        Sets the storage_servers of this ExternalExadataStorageGrid.
        A list of monitored Exadata storage server.


        :param storage_servers: The storage_servers of this ExternalExadataStorageGrid.
        :type: list[oci.database_management.models.ExternalExadataStorageServerSummary]
        """
        self._storage_servers = storage_servers

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
