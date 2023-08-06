# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .discovered_external_db_system_component import DiscoveredExternalDbSystemComponent
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DiscoveredExternalAsmInstance(DiscoveredExternalDbSystemComponent):
    """
    The details of an ASM instance discovered in an external DB system discovery run.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DiscoveredExternalAsmInstance object with values from keyword arguments. The default value of the :py:attr:`~oci.database_management.models.DiscoveredExternalAsmInstance.component_type` attribute
        of this class is ``ASM_INSTANCE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param component_id:
            The value to assign to the component_id property of this DiscoveredExternalAsmInstance.
        :type component_id: str

        :param display_name:
            The value to assign to the display_name property of this DiscoveredExternalAsmInstance.
        :type display_name: str

        :param component_name:
            The value to assign to the component_name property of this DiscoveredExternalAsmInstance.
        :type component_name: str

        :param component_type:
            The value to assign to the component_type property of this DiscoveredExternalAsmInstance.
            Allowed values for this property are: "ASM", "ASM_INSTANCE", "CLUSTER", "CLUSTER_INSTANCE", "DATABASE", "DATABASE_INSTANCE", "DATABASE_HOME", "DATABASE_NODE", "DBSYSTEM", "LISTENER", "PLUGGABLE_DATABASE"
        :type component_type: str

        :param resource_id:
            The value to assign to the resource_id property of this DiscoveredExternalAsmInstance.
        :type resource_id: str

        :param is_selected_for_monitoring:
            The value to assign to the is_selected_for_monitoring property of this DiscoveredExternalAsmInstance.
        :type is_selected_for_monitoring: bool

        :param status:
            The value to assign to the status property of this DiscoveredExternalAsmInstance.
            Allowed values for this property are: "NEW", "EXISTING", "MARKED_FOR_DELETION", "UNKNOWN"
        :type status: str

        :param associated_components:
            The value to assign to the associated_components property of this DiscoveredExternalAsmInstance.
        :type associated_components: list[oci.database_management.models.AssociatedComponent]

        :param host_name:
            The value to assign to the host_name property of this DiscoveredExternalAsmInstance.
        :type host_name: str

        :param instance_name:
            The value to assign to the instance_name property of this DiscoveredExternalAsmInstance.
        :type instance_name: str

        :param adr_home_directory:
            The value to assign to the adr_home_directory property of this DiscoveredExternalAsmInstance.
        :type adr_home_directory: str

        """
        self.swagger_types = {
            'component_id': 'str',
            'display_name': 'str',
            'component_name': 'str',
            'component_type': 'str',
            'resource_id': 'str',
            'is_selected_for_monitoring': 'bool',
            'status': 'str',
            'associated_components': 'list[AssociatedComponent]',
            'host_name': 'str',
            'instance_name': 'str',
            'adr_home_directory': 'str'
        }

        self.attribute_map = {
            'component_id': 'componentId',
            'display_name': 'displayName',
            'component_name': 'componentName',
            'component_type': 'componentType',
            'resource_id': 'resourceId',
            'is_selected_for_monitoring': 'isSelectedForMonitoring',
            'status': 'status',
            'associated_components': 'associatedComponents',
            'host_name': 'hostName',
            'instance_name': 'instanceName',
            'adr_home_directory': 'adrHomeDirectory'
        }

        self._component_id = None
        self._display_name = None
        self._component_name = None
        self._component_type = None
        self._resource_id = None
        self._is_selected_for_monitoring = None
        self._status = None
        self._associated_components = None
        self._host_name = None
        self._instance_name = None
        self._adr_home_directory = None
        self._component_type = 'ASM_INSTANCE'

    @property
    def host_name(self):
        """
        **[Required]** Gets the host_name of this DiscoveredExternalAsmInstance.
        The name of the host on which the ASM instance is running.


        :return: The host_name of this DiscoveredExternalAsmInstance.
        :rtype: str
        """
        return self._host_name

    @host_name.setter
    def host_name(self, host_name):
        """
        Sets the host_name of this DiscoveredExternalAsmInstance.
        The name of the host on which the ASM instance is running.


        :param host_name: The host_name of this DiscoveredExternalAsmInstance.
        :type: str
        """
        self._host_name = host_name

    @property
    def instance_name(self):
        """
        Gets the instance_name of this DiscoveredExternalAsmInstance.
        The name of the ASM instance.


        :return: The instance_name of this DiscoveredExternalAsmInstance.
        :rtype: str
        """
        return self._instance_name

    @instance_name.setter
    def instance_name(self, instance_name):
        """
        Sets the instance_name of this DiscoveredExternalAsmInstance.
        The name of the ASM instance.


        :param instance_name: The instance_name of this DiscoveredExternalAsmInstance.
        :type: str
        """
        self._instance_name = instance_name

    @property
    def adr_home_directory(self):
        """
        Gets the adr_home_directory of this DiscoveredExternalAsmInstance.
        The Automatic Diagnostic Repository (ADR) home directory for the ASM instance.


        :return: The adr_home_directory of this DiscoveredExternalAsmInstance.
        :rtype: str
        """
        return self._adr_home_directory

    @adr_home_directory.setter
    def adr_home_directory(self, adr_home_directory):
        """
        Sets the adr_home_directory of this DiscoveredExternalAsmInstance.
        The Automatic Diagnostic Repository (ADR) home directory for the ASM instance.


        :param adr_home_directory: The adr_home_directory of this DiscoveredExternalAsmInstance.
        :type: str
        """
        self._adr_home_directory = adr_home_directory

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
