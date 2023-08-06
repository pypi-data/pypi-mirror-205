# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .host_configuration_summary import HostConfigurationSummary
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PeComanagedHostConfigurationSummary(HostConfigurationSummary):
    """
    Configuration Summary of a PeComanaged host.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PeComanagedHostConfigurationSummary object with values from keyword arguments. The default value of the :py:attr:`~oci.opsi.models.PeComanagedHostConfigurationSummary.entity_source` attribute
        of this class is ``PE_COMANAGED_HOST`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param host_insight_id:
            The value to assign to the host_insight_id property of this PeComanagedHostConfigurationSummary.
        :type host_insight_id: str

        :param entity_source:
            The value to assign to the entity_source property of this PeComanagedHostConfigurationSummary.
            Allowed values for this property are: "MACS_MANAGED_EXTERNAL_HOST", "EM_MANAGED_EXTERNAL_HOST", "MACS_MANAGED_CLOUD_HOST", "PE_COMANAGED_HOST"
        :type entity_source: str

        :param compartment_id:
            The value to assign to the compartment_id property of this PeComanagedHostConfigurationSummary.
        :type compartment_id: str

        :param host_name:
            The value to assign to the host_name property of this PeComanagedHostConfigurationSummary.
        :type host_name: str

        :param platform_type:
            The value to assign to the platform_type property of this PeComanagedHostConfigurationSummary.
            Allowed values for this property are: "LINUX", "SOLARIS", "SUNOS", "ZLINUX"
        :type platform_type: str

        :param platform_version:
            The value to assign to the platform_version property of this PeComanagedHostConfigurationSummary.
        :type platform_version: str

        :param platform_vendor:
            The value to assign to the platform_vendor property of this PeComanagedHostConfigurationSummary.
        :type platform_vendor: str

        :param total_cpus:
            The value to assign to the total_cpus property of this PeComanagedHostConfigurationSummary.
        :type total_cpus: int

        :param total_memory_in_gbs:
            The value to assign to the total_memory_in_gbs property of this PeComanagedHostConfigurationSummary.
        :type total_memory_in_gbs: float

        :param cpu_architecture:
            The value to assign to the cpu_architecture property of this PeComanagedHostConfigurationSummary.
        :type cpu_architecture: str

        :param cpu_cache_in_mbs:
            The value to assign to the cpu_cache_in_mbs property of this PeComanagedHostConfigurationSummary.
        :type cpu_cache_in_mbs: float

        :param cpu_vendor:
            The value to assign to the cpu_vendor property of this PeComanagedHostConfigurationSummary.
        :type cpu_vendor: str

        :param cpu_frequency_in_mhz:
            The value to assign to the cpu_frequency_in_mhz property of this PeComanagedHostConfigurationSummary.
        :type cpu_frequency_in_mhz: float

        :param cpu_implementation:
            The value to assign to the cpu_implementation property of this PeComanagedHostConfigurationSummary.
        :type cpu_implementation: str

        :param cores_per_socket:
            The value to assign to the cores_per_socket property of this PeComanagedHostConfigurationSummary.
        :type cores_per_socket: int

        :param total_sockets:
            The value to assign to the total_sockets property of this PeComanagedHostConfigurationSummary.
        :type total_sockets: int

        :param threads_per_socket:
            The value to assign to the threads_per_socket property of this PeComanagedHostConfigurationSummary.
        :type threads_per_socket: int

        :param is_hyper_threading_enabled:
            The value to assign to the is_hyper_threading_enabled property of this PeComanagedHostConfigurationSummary.
        :type is_hyper_threading_enabled: bool

        :param defined_tags:
            The value to assign to the defined_tags property of this PeComanagedHostConfigurationSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param freeform_tags:
            The value to assign to the freeform_tags property of this PeComanagedHostConfigurationSummary.
        :type freeform_tags: dict(str, str)

        :param opsi_private_endpoint_id:
            The value to assign to the opsi_private_endpoint_id property of this PeComanagedHostConfigurationSummary.
        :type opsi_private_endpoint_id: str

        :param parent_id:
            The value to assign to the parent_id property of this PeComanagedHostConfigurationSummary.
        :type parent_id: str

        :param exadata_details:
            The value to assign to the exadata_details property of this PeComanagedHostConfigurationSummary.
        :type exadata_details: oci.opsi.models.ExadataDetails

        """
        self.swagger_types = {
            'host_insight_id': 'str',
            'entity_source': 'str',
            'compartment_id': 'str',
            'host_name': 'str',
            'platform_type': 'str',
            'platform_version': 'str',
            'platform_vendor': 'str',
            'total_cpus': 'int',
            'total_memory_in_gbs': 'float',
            'cpu_architecture': 'str',
            'cpu_cache_in_mbs': 'float',
            'cpu_vendor': 'str',
            'cpu_frequency_in_mhz': 'float',
            'cpu_implementation': 'str',
            'cores_per_socket': 'int',
            'total_sockets': 'int',
            'threads_per_socket': 'int',
            'is_hyper_threading_enabled': 'bool',
            'defined_tags': 'dict(str, dict(str, object))',
            'freeform_tags': 'dict(str, str)',
            'opsi_private_endpoint_id': 'str',
            'parent_id': 'str',
            'exadata_details': 'ExadataDetails'
        }

        self.attribute_map = {
            'host_insight_id': 'hostInsightId',
            'entity_source': 'entitySource',
            'compartment_id': 'compartmentId',
            'host_name': 'hostName',
            'platform_type': 'platformType',
            'platform_version': 'platformVersion',
            'platform_vendor': 'platformVendor',
            'total_cpus': 'totalCpus',
            'total_memory_in_gbs': 'totalMemoryInGBs',
            'cpu_architecture': 'cpuArchitecture',
            'cpu_cache_in_mbs': 'cpuCacheInMBs',
            'cpu_vendor': 'cpuVendor',
            'cpu_frequency_in_mhz': 'cpuFrequencyInMhz',
            'cpu_implementation': 'cpuImplementation',
            'cores_per_socket': 'coresPerSocket',
            'total_sockets': 'totalSockets',
            'threads_per_socket': 'threadsPerSocket',
            'is_hyper_threading_enabled': 'isHyperThreadingEnabled',
            'defined_tags': 'definedTags',
            'freeform_tags': 'freeformTags',
            'opsi_private_endpoint_id': 'opsiPrivateEndpointId',
            'parent_id': 'parentId',
            'exadata_details': 'exadataDetails'
        }

        self._host_insight_id = None
        self._entity_source = None
        self._compartment_id = None
        self._host_name = None
        self._platform_type = None
        self._platform_version = None
        self._platform_vendor = None
        self._total_cpus = None
        self._total_memory_in_gbs = None
        self._cpu_architecture = None
        self._cpu_cache_in_mbs = None
        self._cpu_vendor = None
        self._cpu_frequency_in_mhz = None
        self._cpu_implementation = None
        self._cores_per_socket = None
        self._total_sockets = None
        self._threads_per_socket = None
        self._is_hyper_threading_enabled = None
        self._defined_tags = None
        self._freeform_tags = None
        self._opsi_private_endpoint_id = None
        self._parent_id = None
        self._exadata_details = None
        self._entity_source = 'PE_COMANAGED_HOST'

    @property
    def opsi_private_endpoint_id(self):
        """
        **[Required]** Gets the opsi_private_endpoint_id of this PeComanagedHostConfigurationSummary.
        The `OCID`__ of the OPSI private endpoint

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The opsi_private_endpoint_id of this PeComanagedHostConfigurationSummary.
        :rtype: str
        """
        return self._opsi_private_endpoint_id

    @opsi_private_endpoint_id.setter
    def opsi_private_endpoint_id(self, opsi_private_endpoint_id):
        """
        Sets the opsi_private_endpoint_id of this PeComanagedHostConfigurationSummary.
        The `OCID`__ of the OPSI private endpoint

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param opsi_private_endpoint_id: The opsi_private_endpoint_id of this PeComanagedHostConfigurationSummary.
        :type: str
        """
        self._opsi_private_endpoint_id = opsi_private_endpoint_id

    @property
    def parent_id(self):
        """
        **[Required]** Gets the parent_id of this PeComanagedHostConfigurationSummary.
        The `OCID`__ of the database.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The parent_id of this PeComanagedHostConfigurationSummary.
        :rtype: str
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """
        Sets the parent_id of this PeComanagedHostConfigurationSummary.
        The `OCID`__ of the database.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param parent_id: The parent_id of this PeComanagedHostConfigurationSummary.
        :type: str
        """
        self._parent_id = parent_id

    @property
    def exadata_details(self):
        """
        **[Required]** Gets the exadata_details of this PeComanagedHostConfigurationSummary.

        :return: The exadata_details of this PeComanagedHostConfigurationSummary.
        :rtype: oci.opsi.models.ExadataDetails
        """
        return self._exadata_details

    @exadata_details.setter
    def exadata_details(self, exadata_details):
        """
        Sets the exadata_details of this PeComanagedHostConfigurationSummary.

        :param exadata_details: The exadata_details of this PeComanagedHostConfigurationSummary.
        :type: oci.opsi.models.ExadataDetails
        """
        self._exadata_details = exadata_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
