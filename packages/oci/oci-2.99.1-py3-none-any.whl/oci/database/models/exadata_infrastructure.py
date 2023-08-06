# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExadataInfrastructure(object):
    """
    ExadataInfrastructure
    """

    #: A constant which can be used with the lifecycle_state property of a ExadataInfrastructure.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a ExadataInfrastructure.
    #: This constant has a value of "REQUIRES_ACTIVATION"
    LIFECYCLE_STATE_REQUIRES_ACTIVATION = "REQUIRES_ACTIVATION"

    #: A constant which can be used with the lifecycle_state property of a ExadataInfrastructure.
    #: This constant has a value of "ACTIVATING"
    LIFECYCLE_STATE_ACTIVATING = "ACTIVATING"

    #: A constant which can be used with the lifecycle_state property of a ExadataInfrastructure.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ExadataInfrastructure.
    #: This constant has a value of "ACTIVATION_FAILED"
    LIFECYCLE_STATE_ACTIVATION_FAILED = "ACTIVATION_FAILED"

    #: A constant which can be used with the lifecycle_state property of a ExadataInfrastructure.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a ExadataInfrastructure.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a ExadataInfrastructure.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a ExadataInfrastructure.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a ExadataInfrastructure.
    #: This constant has a value of "DISCONNECTED"
    LIFECYCLE_STATE_DISCONNECTED = "DISCONNECTED"

    #: A constant which can be used with the lifecycle_state property of a ExadataInfrastructure.
    #: This constant has a value of "MAINTENANCE_IN_PROGRESS"
    LIFECYCLE_STATE_MAINTENANCE_IN_PROGRESS = "MAINTENANCE_IN_PROGRESS"

    #: A constant which can be used with the lifecycle_state property of a ExadataInfrastructure.
    #: This constant has a value of "WAITING_FOR_CONNECTIVITY"
    LIFECYCLE_STATE_WAITING_FOR_CONNECTIVITY = "WAITING_FOR_CONNECTIVITY"

    #: A constant which can be used with the additional_compute_system_model property of a ExadataInfrastructure.
    #: This constant has a value of "X7"
    ADDITIONAL_COMPUTE_SYSTEM_MODEL_X7 = "X7"

    #: A constant which can be used with the additional_compute_system_model property of a ExadataInfrastructure.
    #: This constant has a value of "X8"
    ADDITIONAL_COMPUTE_SYSTEM_MODEL_X8 = "X8"

    #: A constant which can be used with the additional_compute_system_model property of a ExadataInfrastructure.
    #: This constant has a value of "X8M"
    ADDITIONAL_COMPUTE_SYSTEM_MODEL_X8_M = "X8M"

    #: A constant which can be used with the additional_compute_system_model property of a ExadataInfrastructure.
    #: This constant has a value of "X9M"
    ADDITIONAL_COMPUTE_SYSTEM_MODEL_X9_M = "X9M"

    #: A constant which can be used with the maintenance_slo_status property of a ExadataInfrastructure.
    #: This constant has a value of "OK"
    MAINTENANCE_SLO_STATUS_OK = "OK"

    #: A constant which can be used with the maintenance_slo_status property of a ExadataInfrastructure.
    #: This constant has a value of "DEGRADED"
    MAINTENANCE_SLO_STATUS_DEGRADED = "DEGRADED"

    def __init__(self, **kwargs):
        """
        Initializes a new ExadataInfrastructure object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ExadataInfrastructure.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ExadataInfrastructure.
        :type compartment_id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ExadataInfrastructure.
            Allowed values for this property are: "CREATING", "REQUIRES_ACTIVATION", "ACTIVATING", "ACTIVE", "ACTIVATION_FAILED", "FAILED", "UPDATING", "DELETING", "DELETED", "DISCONNECTED", "MAINTENANCE_IN_PROGRESS", "WAITING_FOR_CONNECTIVITY", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param display_name:
            The value to assign to the display_name property of this ExadataInfrastructure.
        :type display_name: str

        :param shape:
            The value to assign to the shape property of this ExadataInfrastructure.
        :type shape: str

        :param time_zone:
            The value to assign to the time_zone property of this ExadataInfrastructure.
        :type time_zone: str

        :param cpus_enabled:
            The value to assign to the cpus_enabled property of this ExadataInfrastructure.
        :type cpus_enabled: int

        :param max_cpu_count:
            The value to assign to the max_cpu_count property of this ExadataInfrastructure.
        :type max_cpu_count: int

        :param memory_size_in_gbs:
            The value to assign to the memory_size_in_gbs property of this ExadataInfrastructure.
        :type memory_size_in_gbs: int

        :param max_memory_in_gbs:
            The value to assign to the max_memory_in_gbs property of this ExadataInfrastructure.
        :type max_memory_in_gbs: int

        :param db_node_storage_size_in_gbs:
            The value to assign to the db_node_storage_size_in_gbs property of this ExadataInfrastructure.
        :type db_node_storage_size_in_gbs: int

        :param max_db_node_storage_in_g_bs:
            The value to assign to the max_db_node_storage_in_g_bs property of this ExadataInfrastructure.
        :type max_db_node_storage_in_g_bs: int

        :param data_storage_size_in_tbs:
            The value to assign to the data_storage_size_in_tbs property of this ExadataInfrastructure.
        :type data_storage_size_in_tbs: float

        :param max_data_storage_in_t_bs:
            The value to assign to the max_data_storage_in_t_bs property of this ExadataInfrastructure.
        :type max_data_storage_in_t_bs: float

        :param rack_serial_number:
            The value to assign to the rack_serial_number property of this ExadataInfrastructure.
        :type rack_serial_number: str

        :param storage_count:
            The value to assign to the storage_count property of this ExadataInfrastructure.
        :type storage_count: int

        :param additional_storage_count:
            The value to assign to the additional_storage_count property of this ExadataInfrastructure.
        :type additional_storage_count: int

        :param activated_storage_count:
            The value to assign to the activated_storage_count property of this ExadataInfrastructure.
        :type activated_storage_count: int

        :param compute_count:
            The value to assign to the compute_count property of this ExadataInfrastructure.
        :type compute_count: int

        :param is_multi_rack_deployment:
            The value to assign to the is_multi_rack_deployment property of this ExadataInfrastructure.
        :type is_multi_rack_deployment: bool

        :param multi_rack_configuration_file:
            The value to assign to the multi_rack_configuration_file property of this ExadataInfrastructure.
        :type multi_rack_configuration_file: str

        :param additional_compute_count:
            The value to assign to the additional_compute_count property of this ExadataInfrastructure.
        :type additional_compute_count: int

        :param additional_compute_system_model:
            The value to assign to the additional_compute_system_model property of this ExadataInfrastructure.
            Allowed values for this property are: "X7", "X8", "X8M", "X9M", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type additional_compute_system_model: str

        :param cloud_control_plane_server1:
            The value to assign to the cloud_control_plane_server1 property of this ExadataInfrastructure.
        :type cloud_control_plane_server1: str

        :param cloud_control_plane_server2:
            The value to assign to the cloud_control_plane_server2 property of this ExadataInfrastructure.
        :type cloud_control_plane_server2: str

        :param netmask:
            The value to assign to the netmask property of this ExadataInfrastructure.
        :type netmask: str

        :param gateway:
            The value to assign to the gateway property of this ExadataInfrastructure.
        :type gateway: str

        :param admin_network_cidr:
            The value to assign to the admin_network_cidr property of this ExadataInfrastructure.
        :type admin_network_cidr: str

        :param infini_band_network_cidr:
            The value to assign to the infini_band_network_cidr property of this ExadataInfrastructure.
        :type infini_band_network_cidr: str

        :param corporate_proxy:
            The value to assign to the corporate_proxy property of this ExadataInfrastructure.
        :type corporate_proxy: str

        :param dns_server:
            The value to assign to the dns_server property of this ExadataInfrastructure.
        :type dns_server: list[str]

        :param ntp_server:
            The value to assign to the ntp_server property of this ExadataInfrastructure.
        :type ntp_server: list[str]

        :param time_created:
            The value to assign to the time_created property of this ExadataInfrastructure.
        :type time_created: datetime

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this ExadataInfrastructure.
        :type lifecycle_details: str

        :param csi_number:
            The value to assign to the csi_number property of this ExadataInfrastructure.
        :type csi_number: str

        :param contacts:
            The value to assign to the contacts property of this ExadataInfrastructure.
        :type contacts: list[oci.database.models.ExadataInfrastructureContact]

        :param maintenance_slo_status:
            The value to assign to the maintenance_slo_status property of this ExadataInfrastructure.
            Allowed values for this property are: "OK", "DEGRADED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type maintenance_slo_status: str

        :param maintenance_window:
            The value to assign to the maintenance_window property of this ExadataInfrastructure.
        :type maintenance_window: oci.database.models.MaintenanceWindow

        :param storage_server_version:
            The value to assign to the storage_server_version property of this ExadataInfrastructure.
        :type storage_server_version: str

        :param db_server_version:
            The value to assign to the db_server_version property of this ExadataInfrastructure.
        :type db_server_version: str

        :param monthly_db_server_version:
            The value to assign to the monthly_db_server_version property of this ExadataInfrastructure.
        :type monthly_db_server_version: str

        :param last_maintenance_run_id:
            The value to assign to the last_maintenance_run_id property of this ExadataInfrastructure.
        :type last_maintenance_run_id: str

        :param next_maintenance_run_id:
            The value to assign to the next_maintenance_run_id property of this ExadataInfrastructure.
        :type next_maintenance_run_id: str

        :param is_cps_offline_report_enabled:
            The value to assign to the is_cps_offline_report_enabled property of this ExadataInfrastructure.
        :type is_cps_offline_report_enabled: bool

        :param network_bonding_mode_details:
            The value to assign to the network_bonding_mode_details property of this ExadataInfrastructure.
        :type network_bonding_mode_details: oci.database.models.NetworkBondingModeDetails

        :param freeform_tags:
            The value to assign to the freeform_tags property of this ExadataInfrastructure.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this ExadataInfrastructure.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'lifecycle_state': 'str',
            'display_name': 'str',
            'shape': 'str',
            'time_zone': 'str',
            'cpus_enabled': 'int',
            'max_cpu_count': 'int',
            'memory_size_in_gbs': 'int',
            'max_memory_in_gbs': 'int',
            'db_node_storage_size_in_gbs': 'int',
            'max_db_node_storage_in_g_bs': 'int',
            'data_storage_size_in_tbs': 'float',
            'max_data_storage_in_t_bs': 'float',
            'rack_serial_number': 'str',
            'storage_count': 'int',
            'additional_storage_count': 'int',
            'activated_storage_count': 'int',
            'compute_count': 'int',
            'is_multi_rack_deployment': 'bool',
            'multi_rack_configuration_file': 'str',
            'additional_compute_count': 'int',
            'additional_compute_system_model': 'str',
            'cloud_control_plane_server1': 'str',
            'cloud_control_plane_server2': 'str',
            'netmask': 'str',
            'gateway': 'str',
            'admin_network_cidr': 'str',
            'infini_band_network_cidr': 'str',
            'corporate_proxy': 'str',
            'dns_server': 'list[str]',
            'ntp_server': 'list[str]',
            'time_created': 'datetime',
            'lifecycle_details': 'str',
            'csi_number': 'str',
            'contacts': 'list[ExadataInfrastructureContact]',
            'maintenance_slo_status': 'str',
            'maintenance_window': 'MaintenanceWindow',
            'storage_server_version': 'str',
            'db_server_version': 'str',
            'monthly_db_server_version': 'str',
            'last_maintenance_run_id': 'str',
            'next_maintenance_run_id': 'str',
            'is_cps_offline_report_enabled': 'bool',
            'network_bonding_mode_details': 'NetworkBondingModeDetails',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'lifecycle_state': 'lifecycleState',
            'display_name': 'displayName',
            'shape': 'shape',
            'time_zone': 'timeZone',
            'cpus_enabled': 'cpusEnabled',
            'max_cpu_count': 'maxCpuCount',
            'memory_size_in_gbs': 'memorySizeInGBs',
            'max_memory_in_gbs': 'maxMemoryInGBs',
            'db_node_storage_size_in_gbs': 'dbNodeStorageSizeInGBs',
            'max_db_node_storage_in_g_bs': 'maxDbNodeStorageInGBs',
            'data_storage_size_in_tbs': 'dataStorageSizeInTBs',
            'max_data_storage_in_t_bs': 'maxDataStorageInTBs',
            'rack_serial_number': 'rackSerialNumber',
            'storage_count': 'storageCount',
            'additional_storage_count': 'additionalStorageCount',
            'activated_storage_count': 'activatedStorageCount',
            'compute_count': 'computeCount',
            'is_multi_rack_deployment': 'isMultiRackDeployment',
            'multi_rack_configuration_file': 'multiRackConfigurationFile',
            'additional_compute_count': 'additionalComputeCount',
            'additional_compute_system_model': 'additionalComputeSystemModel',
            'cloud_control_plane_server1': 'cloudControlPlaneServer1',
            'cloud_control_plane_server2': 'cloudControlPlaneServer2',
            'netmask': 'netmask',
            'gateway': 'gateway',
            'admin_network_cidr': 'adminNetworkCIDR',
            'infini_band_network_cidr': 'infiniBandNetworkCIDR',
            'corporate_proxy': 'corporateProxy',
            'dns_server': 'dnsServer',
            'ntp_server': 'ntpServer',
            'time_created': 'timeCreated',
            'lifecycle_details': 'lifecycleDetails',
            'csi_number': 'csiNumber',
            'contacts': 'contacts',
            'maintenance_slo_status': 'maintenanceSLOStatus',
            'maintenance_window': 'maintenanceWindow',
            'storage_server_version': 'storageServerVersion',
            'db_server_version': 'dbServerVersion',
            'monthly_db_server_version': 'monthlyDbServerVersion',
            'last_maintenance_run_id': 'lastMaintenanceRunId',
            'next_maintenance_run_id': 'nextMaintenanceRunId',
            'is_cps_offline_report_enabled': 'isCpsOfflineReportEnabled',
            'network_bonding_mode_details': 'networkBondingModeDetails',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._id = None
        self._compartment_id = None
        self._lifecycle_state = None
        self._display_name = None
        self._shape = None
        self._time_zone = None
        self._cpus_enabled = None
        self._max_cpu_count = None
        self._memory_size_in_gbs = None
        self._max_memory_in_gbs = None
        self._db_node_storage_size_in_gbs = None
        self._max_db_node_storage_in_g_bs = None
        self._data_storage_size_in_tbs = None
        self._max_data_storage_in_t_bs = None
        self._rack_serial_number = None
        self._storage_count = None
        self._additional_storage_count = None
        self._activated_storage_count = None
        self._compute_count = None
        self._is_multi_rack_deployment = None
        self._multi_rack_configuration_file = None
        self._additional_compute_count = None
        self._additional_compute_system_model = None
        self._cloud_control_plane_server1 = None
        self._cloud_control_plane_server2 = None
        self._netmask = None
        self._gateway = None
        self._admin_network_cidr = None
        self._infini_band_network_cidr = None
        self._corporate_proxy = None
        self._dns_server = None
        self._ntp_server = None
        self._time_created = None
        self._lifecycle_details = None
        self._csi_number = None
        self._contacts = None
        self._maintenance_slo_status = None
        self._maintenance_window = None
        self._storage_server_version = None
        self._db_server_version = None
        self._monthly_db_server_version = None
        self._last_maintenance_run_id = None
        self._next_maintenance_run_id = None
        self._is_cps_offline_report_enabled = None
        self._network_bonding_mode_details = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ExadataInfrastructure.
        The `OCID`__ of the Exadata infrastructure.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ExadataInfrastructure.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ExadataInfrastructure.
        The `OCID`__ of the Exadata infrastructure.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ExadataInfrastructure.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ExadataInfrastructure.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ExadataInfrastructure.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ExadataInfrastructure.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ExadataInfrastructure.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ExadataInfrastructure.
        The current lifecycle state of the Exadata infrastructure.

        Allowed values for this property are: "CREATING", "REQUIRES_ACTIVATION", "ACTIVATING", "ACTIVE", "ACTIVATION_FAILED", "FAILED", "UPDATING", "DELETING", "DELETED", "DISCONNECTED", "MAINTENANCE_IN_PROGRESS", "WAITING_FOR_CONNECTIVITY", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ExadataInfrastructure.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ExadataInfrastructure.
        The current lifecycle state of the Exadata infrastructure.


        :param lifecycle_state: The lifecycle_state of this ExadataInfrastructure.
        :type: str
        """
        allowed_values = ["CREATING", "REQUIRES_ACTIVATION", "ACTIVATING", "ACTIVE", "ACTIVATION_FAILED", "FAILED", "UPDATING", "DELETING", "DELETED", "DISCONNECTED", "MAINTENANCE_IN_PROGRESS", "WAITING_FOR_CONNECTIVITY"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ExadataInfrastructure.
        The user-friendly name for the Exadata Cloud@Customer infrastructure. The name does not need to be unique.


        :return: The display_name of this ExadataInfrastructure.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ExadataInfrastructure.
        The user-friendly name for the Exadata Cloud@Customer infrastructure. The name does not need to be unique.


        :param display_name: The display_name of this ExadataInfrastructure.
        :type: str
        """
        self._display_name = display_name

    @property
    def shape(self):
        """
        **[Required]** Gets the shape of this ExadataInfrastructure.
        The shape of the Exadata infrastructure. The shape determines the amount of CPU, storage, and memory resources allocated to the instance.


        :return: The shape of this ExadataInfrastructure.
        :rtype: str
        """
        return self._shape

    @shape.setter
    def shape(self, shape):
        """
        Sets the shape of this ExadataInfrastructure.
        The shape of the Exadata infrastructure. The shape determines the amount of CPU, storage, and memory resources allocated to the instance.


        :param shape: The shape of this ExadataInfrastructure.
        :type: str
        """
        self._shape = shape

    @property
    def time_zone(self):
        """
        Gets the time_zone of this ExadataInfrastructure.
        The time zone of the Exadata infrastructure. For details, see `Exadata Infrastructure Time Zones`__.

        __ https://docs.cloud.oracle.com/Content/Database/References/timezones.htm


        :return: The time_zone of this ExadataInfrastructure.
        :rtype: str
        """
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        """
        Sets the time_zone of this ExadataInfrastructure.
        The time zone of the Exadata infrastructure. For details, see `Exadata Infrastructure Time Zones`__.

        __ https://docs.cloud.oracle.com/Content/Database/References/timezones.htm


        :param time_zone: The time_zone of this ExadataInfrastructure.
        :type: str
        """
        self._time_zone = time_zone

    @property
    def cpus_enabled(self):
        """
        Gets the cpus_enabled of this ExadataInfrastructure.
        The number of enabled CPU cores.


        :return: The cpus_enabled of this ExadataInfrastructure.
        :rtype: int
        """
        return self._cpus_enabled

    @cpus_enabled.setter
    def cpus_enabled(self, cpus_enabled):
        """
        Sets the cpus_enabled of this ExadataInfrastructure.
        The number of enabled CPU cores.


        :param cpus_enabled: The cpus_enabled of this ExadataInfrastructure.
        :type: int
        """
        self._cpus_enabled = cpus_enabled

    @property
    def max_cpu_count(self):
        """
        Gets the max_cpu_count of this ExadataInfrastructure.
        The total number of CPU cores available.


        :return: The max_cpu_count of this ExadataInfrastructure.
        :rtype: int
        """
        return self._max_cpu_count

    @max_cpu_count.setter
    def max_cpu_count(self, max_cpu_count):
        """
        Sets the max_cpu_count of this ExadataInfrastructure.
        The total number of CPU cores available.


        :param max_cpu_count: The max_cpu_count of this ExadataInfrastructure.
        :type: int
        """
        self._max_cpu_count = max_cpu_count

    @property
    def memory_size_in_gbs(self):
        """
        Gets the memory_size_in_gbs of this ExadataInfrastructure.
        The memory allocated in GBs.


        :return: The memory_size_in_gbs of this ExadataInfrastructure.
        :rtype: int
        """
        return self._memory_size_in_gbs

    @memory_size_in_gbs.setter
    def memory_size_in_gbs(self, memory_size_in_gbs):
        """
        Sets the memory_size_in_gbs of this ExadataInfrastructure.
        The memory allocated in GBs.


        :param memory_size_in_gbs: The memory_size_in_gbs of this ExadataInfrastructure.
        :type: int
        """
        self._memory_size_in_gbs = memory_size_in_gbs

    @property
    def max_memory_in_gbs(self):
        """
        Gets the max_memory_in_gbs of this ExadataInfrastructure.
        The total memory available in GBs.


        :return: The max_memory_in_gbs of this ExadataInfrastructure.
        :rtype: int
        """
        return self._max_memory_in_gbs

    @max_memory_in_gbs.setter
    def max_memory_in_gbs(self, max_memory_in_gbs):
        """
        Sets the max_memory_in_gbs of this ExadataInfrastructure.
        The total memory available in GBs.


        :param max_memory_in_gbs: The max_memory_in_gbs of this ExadataInfrastructure.
        :type: int
        """
        self._max_memory_in_gbs = max_memory_in_gbs

    @property
    def db_node_storage_size_in_gbs(self):
        """
        Gets the db_node_storage_size_in_gbs of this ExadataInfrastructure.
        The local node storage allocated in GBs.


        :return: The db_node_storage_size_in_gbs of this ExadataInfrastructure.
        :rtype: int
        """
        return self._db_node_storage_size_in_gbs

    @db_node_storage_size_in_gbs.setter
    def db_node_storage_size_in_gbs(self, db_node_storage_size_in_gbs):
        """
        Sets the db_node_storage_size_in_gbs of this ExadataInfrastructure.
        The local node storage allocated in GBs.


        :param db_node_storage_size_in_gbs: The db_node_storage_size_in_gbs of this ExadataInfrastructure.
        :type: int
        """
        self._db_node_storage_size_in_gbs = db_node_storage_size_in_gbs

    @property
    def max_db_node_storage_in_g_bs(self):
        """
        Gets the max_db_node_storage_in_g_bs of this ExadataInfrastructure.
        The total local node storage available in GBs.


        :return: The max_db_node_storage_in_g_bs of this ExadataInfrastructure.
        :rtype: int
        """
        return self._max_db_node_storage_in_g_bs

    @max_db_node_storage_in_g_bs.setter
    def max_db_node_storage_in_g_bs(self, max_db_node_storage_in_g_bs):
        """
        Sets the max_db_node_storage_in_g_bs of this ExadataInfrastructure.
        The total local node storage available in GBs.


        :param max_db_node_storage_in_g_bs: The max_db_node_storage_in_g_bs of this ExadataInfrastructure.
        :type: int
        """
        self._max_db_node_storage_in_g_bs = max_db_node_storage_in_g_bs

    @property
    def data_storage_size_in_tbs(self):
        """
        Gets the data_storage_size_in_tbs of this ExadataInfrastructure.
        Size, in terabytes, of the DATA disk group.


        :return: The data_storage_size_in_tbs of this ExadataInfrastructure.
        :rtype: float
        """
        return self._data_storage_size_in_tbs

    @data_storage_size_in_tbs.setter
    def data_storage_size_in_tbs(self, data_storage_size_in_tbs):
        """
        Sets the data_storage_size_in_tbs of this ExadataInfrastructure.
        Size, in terabytes, of the DATA disk group.


        :param data_storage_size_in_tbs: The data_storage_size_in_tbs of this ExadataInfrastructure.
        :type: float
        """
        self._data_storage_size_in_tbs = data_storage_size_in_tbs

    @property
    def max_data_storage_in_t_bs(self):
        """
        Gets the max_data_storage_in_t_bs of this ExadataInfrastructure.
        The total available DATA disk group size.


        :return: The max_data_storage_in_t_bs of this ExadataInfrastructure.
        :rtype: float
        """
        return self._max_data_storage_in_t_bs

    @max_data_storage_in_t_bs.setter
    def max_data_storage_in_t_bs(self, max_data_storage_in_t_bs):
        """
        Sets the max_data_storage_in_t_bs of this ExadataInfrastructure.
        The total available DATA disk group size.


        :param max_data_storage_in_t_bs: The max_data_storage_in_t_bs of this ExadataInfrastructure.
        :type: float
        """
        self._max_data_storage_in_t_bs = max_data_storage_in_t_bs

    @property
    def rack_serial_number(self):
        """
        Gets the rack_serial_number of this ExadataInfrastructure.
        The serial number for the Exadata infrastructure.


        :return: The rack_serial_number of this ExadataInfrastructure.
        :rtype: str
        """
        return self._rack_serial_number

    @rack_serial_number.setter
    def rack_serial_number(self, rack_serial_number):
        """
        Sets the rack_serial_number of this ExadataInfrastructure.
        The serial number for the Exadata infrastructure.


        :param rack_serial_number: The rack_serial_number of this ExadataInfrastructure.
        :type: str
        """
        self._rack_serial_number = rack_serial_number

    @property
    def storage_count(self):
        """
        Gets the storage_count of this ExadataInfrastructure.
        The number of Exadata storage servers for the Exadata infrastructure.


        :return: The storage_count of this ExadataInfrastructure.
        :rtype: int
        """
        return self._storage_count

    @storage_count.setter
    def storage_count(self, storage_count):
        """
        Sets the storage_count of this ExadataInfrastructure.
        The number of Exadata storage servers for the Exadata infrastructure.


        :param storage_count: The storage_count of this ExadataInfrastructure.
        :type: int
        """
        self._storage_count = storage_count

    @property
    def additional_storage_count(self):
        """
        Gets the additional_storage_count of this ExadataInfrastructure.
        The requested number of additional storage servers for the Exadata infrastructure.


        :return: The additional_storage_count of this ExadataInfrastructure.
        :rtype: int
        """
        return self._additional_storage_count

    @additional_storage_count.setter
    def additional_storage_count(self, additional_storage_count):
        """
        Sets the additional_storage_count of this ExadataInfrastructure.
        The requested number of additional storage servers for the Exadata infrastructure.


        :param additional_storage_count: The additional_storage_count of this ExadataInfrastructure.
        :type: int
        """
        self._additional_storage_count = additional_storage_count

    @property
    def activated_storage_count(self):
        """
        Gets the activated_storage_count of this ExadataInfrastructure.
        The requested number of additional storage servers activated for the Exadata infrastructure.


        :return: The activated_storage_count of this ExadataInfrastructure.
        :rtype: int
        """
        return self._activated_storage_count

    @activated_storage_count.setter
    def activated_storage_count(self, activated_storage_count):
        """
        Sets the activated_storage_count of this ExadataInfrastructure.
        The requested number of additional storage servers activated for the Exadata infrastructure.


        :param activated_storage_count: The activated_storage_count of this ExadataInfrastructure.
        :type: int
        """
        self._activated_storage_count = activated_storage_count

    @property
    def compute_count(self):
        """
        Gets the compute_count of this ExadataInfrastructure.
        The number of compute servers for the Exadata infrastructure.


        :return: The compute_count of this ExadataInfrastructure.
        :rtype: int
        """
        return self._compute_count

    @compute_count.setter
    def compute_count(self, compute_count):
        """
        Sets the compute_count of this ExadataInfrastructure.
        The number of compute servers for the Exadata infrastructure.


        :param compute_count: The compute_count of this ExadataInfrastructure.
        :type: int
        """
        self._compute_count = compute_count

    @property
    def is_multi_rack_deployment(self):
        """
        Gets the is_multi_rack_deployment of this ExadataInfrastructure.
        Indicates if deployment is Multi-Rack or not.


        :return: The is_multi_rack_deployment of this ExadataInfrastructure.
        :rtype: bool
        """
        return self._is_multi_rack_deployment

    @is_multi_rack_deployment.setter
    def is_multi_rack_deployment(self, is_multi_rack_deployment):
        """
        Sets the is_multi_rack_deployment of this ExadataInfrastructure.
        Indicates if deployment is Multi-Rack or not.


        :param is_multi_rack_deployment: The is_multi_rack_deployment of this ExadataInfrastructure.
        :type: bool
        """
        self._is_multi_rack_deployment = is_multi_rack_deployment

    @property
    def multi_rack_configuration_file(self):
        """
        Gets the multi_rack_configuration_file of this ExadataInfrastructure.
        The base64 encoded Multi-Rack configuration json file.


        :return: The multi_rack_configuration_file of this ExadataInfrastructure.
        :rtype: str
        """
        return self._multi_rack_configuration_file

    @multi_rack_configuration_file.setter
    def multi_rack_configuration_file(self, multi_rack_configuration_file):
        """
        Sets the multi_rack_configuration_file of this ExadataInfrastructure.
        The base64 encoded Multi-Rack configuration json file.


        :param multi_rack_configuration_file: The multi_rack_configuration_file of this ExadataInfrastructure.
        :type: str
        """
        self._multi_rack_configuration_file = multi_rack_configuration_file

    @property
    def additional_compute_count(self):
        """
        Gets the additional_compute_count of this ExadataInfrastructure.
        The requested number of additional compute servers for the Exadata infrastructure.


        :return: The additional_compute_count of this ExadataInfrastructure.
        :rtype: int
        """
        return self._additional_compute_count

    @additional_compute_count.setter
    def additional_compute_count(self, additional_compute_count):
        """
        Sets the additional_compute_count of this ExadataInfrastructure.
        The requested number of additional compute servers for the Exadata infrastructure.


        :param additional_compute_count: The additional_compute_count of this ExadataInfrastructure.
        :type: int
        """
        self._additional_compute_count = additional_compute_count

    @property
    def additional_compute_system_model(self):
        """
        Gets the additional_compute_system_model of this ExadataInfrastructure.
        Oracle Exadata System Model specification. The system model determines the amount of compute or storage
        server resources available for use. For more information, please see [System and Shape Configuration Options]
        (https://docs.oracle.com/en/engineered-systems/exadata-cloud-at-customer/ecccm/ecc-system-config-options.html#GUID-9E090174-5C57-4EB1-9243-B470F9F10D6B)

        Allowed values for this property are: "X7", "X8", "X8M", "X9M", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The additional_compute_system_model of this ExadataInfrastructure.
        :rtype: str
        """
        return self._additional_compute_system_model

    @additional_compute_system_model.setter
    def additional_compute_system_model(self, additional_compute_system_model):
        """
        Sets the additional_compute_system_model of this ExadataInfrastructure.
        Oracle Exadata System Model specification. The system model determines the amount of compute or storage
        server resources available for use. For more information, please see [System and Shape Configuration Options]
        (https://docs.oracle.com/en/engineered-systems/exadata-cloud-at-customer/ecccm/ecc-system-config-options.html#GUID-9E090174-5C57-4EB1-9243-B470F9F10D6B)


        :param additional_compute_system_model: The additional_compute_system_model of this ExadataInfrastructure.
        :type: str
        """
        allowed_values = ["X7", "X8", "X8M", "X9M"]
        if not value_allowed_none_or_none_sentinel(additional_compute_system_model, allowed_values):
            additional_compute_system_model = 'UNKNOWN_ENUM_VALUE'
        self._additional_compute_system_model = additional_compute_system_model

    @property
    def cloud_control_plane_server1(self):
        """
        Gets the cloud_control_plane_server1 of this ExadataInfrastructure.
        The IP address for the first control plane server.


        :return: The cloud_control_plane_server1 of this ExadataInfrastructure.
        :rtype: str
        """
        return self._cloud_control_plane_server1

    @cloud_control_plane_server1.setter
    def cloud_control_plane_server1(self, cloud_control_plane_server1):
        """
        Sets the cloud_control_plane_server1 of this ExadataInfrastructure.
        The IP address for the first control plane server.


        :param cloud_control_plane_server1: The cloud_control_plane_server1 of this ExadataInfrastructure.
        :type: str
        """
        self._cloud_control_plane_server1 = cloud_control_plane_server1

    @property
    def cloud_control_plane_server2(self):
        """
        Gets the cloud_control_plane_server2 of this ExadataInfrastructure.
        The IP address for the second control plane server.


        :return: The cloud_control_plane_server2 of this ExadataInfrastructure.
        :rtype: str
        """
        return self._cloud_control_plane_server2

    @cloud_control_plane_server2.setter
    def cloud_control_plane_server2(self, cloud_control_plane_server2):
        """
        Sets the cloud_control_plane_server2 of this ExadataInfrastructure.
        The IP address for the second control plane server.


        :param cloud_control_plane_server2: The cloud_control_plane_server2 of this ExadataInfrastructure.
        :type: str
        """
        self._cloud_control_plane_server2 = cloud_control_plane_server2

    @property
    def netmask(self):
        """
        Gets the netmask of this ExadataInfrastructure.
        The netmask for the control plane network.


        :return: The netmask of this ExadataInfrastructure.
        :rtype: str
        """
        return self._netmask

    @netmask.setter
    def netmask(self, netmask):
        """
        Sets the netmask of this ExadataInfrastructure.
        The netmask for the control plane network.


        :param netmask: The netmask of this ExadataInfrastructure.
        :type: str
        """
        self._netmask = netmask

    @property
    def gateway(self):
        """
        Gets the gateway of this ExadataInfrastructure.
        The gateway for the control plane network.


        :return: The gateway of this ExadataInfrastructure.
        :rtype: str
        """
        return self._gateway

    @gateway.setter
    def gateway(self, gateway):
        """
        Sets the gateway of this ExadataInfrastructure.
        The gateway for the control plane network.


        :param gateway: The gateway of this ExadataInfrastructure.
        :type: str
        """
        self._gateway = gateway

    @property
    def admin_network_cidr(self):
        """
        Gets the admin_network_cidr of this ExadataInfrastructure.
        The CIDR block for the Exadata administration network.


        :return: The admin_network_cidr of this ExadataInfrastructure.
        :rtype: str
        """
        return self._admin_network_cidr

    @admin_network_cidr.setter
    def admin_network_cidr(self, admin_network_cidr):
        """
        Sets the admin_network_cidr of this ExadataInfrastructure.
        The CIDR block for the Exadata administration network.


        :param admin_network_cidr: The admin_network_cidr of this ExadataInfrastructure.
        :type: str
        """
        self._admin_network_cidr = admin_network_cidr

    @property
    def infini_band_network_cidr(self):
        """
        Gets the infini_band_network_cidr of this ExadataInfrastructure.
        The CIDR block for the Exadata InfiniBand interconnect.


        :return: The infini_band_network_cidr of this ExadataInfrastructure.
        :rtype: str
        """
        return self._infini_band_network_cidr

    @infini_band_network_cidr.setter
    def infini_band_network_cidr(self, infini_band_network_cidr):
        """
        Sets the infini_band_network_cidr of this ExadataInfrastructure.
        The CIDR block for the Exadata InfiniBand interconnect.


        :param infini_band_network_cidr: The infini_band_network_cidr of this ExadataInfrastructure.
        :type: str
        """
        self._infini_band_network_cidr = infini_band_network_cidr

    @property
    def corporate_proxy(self):
        """
        Gets the corporate_proxy of this ExadataInfrastructure.
        The corporate network proxy for access to the control plane network.


        :return: The corporate_proxy of this ExadataInfrastructure.
        :rtype: str
        """
        return self._corporate_proxy

    @corporate_proxy.setter
    def corporate_proxy(self, corporate_proxy):
        """
        Sets the corporate_proxy of this ExadataInfrastructure.
        The corporate network proxy for access to the control plane network.


        :param corporate_proxy: The corporate_proxy of this ExadataInfrastructure.
        :type: str
        """
        self._corporate_proxy = corporate_proxy

    @property
    def dns_server(self):
        """
        Gets the dns_server of this ExadataInfrastructure.
        The list of DNS server IP addresses. Maximum of 3 allowed.


        :return: The dns_server of this ExadataInfrastructure.
        :rtype: list[str]
        """
        return self._dns_server

    @dns_server.setter
    def dns_server(self, dns_server):
        """
        Sets the dns_server of this ExadataInfrastructure.
        The list of DNS server IP addresses. Maximum of 3 allowed.


        :param dns_server: The dns_server of this ExadataInfrastructure.
        :type: list[str]
        """
        self._dns_server = dns_server

    @property
    def ntp_server(self):
        """
        Gets the ntp_server of this ExadataInfrastructure.
        The list of NTP server IP addresses. Maximum of 3 allowed.


        :return: The ntp_server of this ExadataInfrastructure.
        :rtype: list[str]
        """
        return self._ntp_server

    @ntp_server.setter
    def ntp_server(self, ntp_server):
        """
        Sets the ntp_server of this ExadataInfrastructure.
        The list of NTP server IP addresses. Maximum of 3 allowed.


        :param ntp_server: The ntp_server of this ExadataInfrastructure.
        :type: list[str]
        """
        self._ntp_server = ntp_server

    @property
    def time_created(self):
        """
        Gets the time_created of this ExadataInfrastructure.
        The date and time the Exadata infrastructure was created.


        :return: The time_created of this ExadataInfrastructure.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ExadataInfrastructure.
        The date and time the Exadata infrastructure was created.


        :param time_created: The time_created of this ExadataInfrastructure.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this ExadataInfrastructure.
        Additional information about the current lifecycle state.


        :return: The lifecycle_details of this ExadataInfrastructure.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this ExadataInfrastructure.
        Additional information about the current lifecycle state.


        :param lifecycle_details: The lifecycle_details of this ExadataInfrastructure.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def csi_number(self):
        """
        Gets the csi_number of this ExadataInfrastructure.
        The CSI Number of the Exadata infrastructure.


        :return: The csi_number of this ExadataInfrastructure.
        :rtype: str
        """
        return self._csi_number

    @csi_number.setter
    def csi_number(self, csi_number):
        """
        Sets the csi_number of this ExadataInfrastructure.
        The CSI Number of the Exadata infrastructure.


        :param csi_number: The csi_number of this ExadataInfrastructure.
        :type: str
        """
        self._csi_number = csi_number

    @property
    def contacts(self):
        """
        Gets the contacts of this ExadataInfrastructure.
        The list of contacts for the Exadata infrastructure.


        :return: The contacts of this ExadataInfrastructure.
        :rtype: list[oci.database.models.ExadataInfrastructureContact]
        """
        return self._contacts

    @contacts.setter
    def contacts(self, contacts):
        """
        Sets the contacts of this ExadataInfrastructure.
        The list of contacts for the Exadata infrastructure.


        :param contacts: The contacts of this ExadataInfrastructure.
        :type: list[oci.database.models.ExadataInfrastructureContact]
        """
        self._contacts = contacts

    @property
    def maintenance_slo_status(self):
        """
        Gets the maintenance_slo_status of this ExadataInfrastructure.
        A field to capture \u2018Maintenance SLO Status\u2019 for the Exadata infrastructure with values \u2018OK\u2019, \u2018DEGRADED\u2019. Default is \u2018OK\u2019 when the infrastructure is provisioned.

        Allowed values for this property are: "OK", "DEGRADED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The maintenance_slo_status of this ExadataInfrastructure.
        :rtype: str
        """
        return self._maintenance_slo_status

    @maintenance_slo_status.setter
    def maintenance_slo_status(self, maintenance_slo_status):
        """
        Sets the maintenance_slo_status of this ExadataInfrastructure.
        A field to capture \u2018Maintenance SLO Status\u2019 for the Exadata infrastructure with values \u2018OK\u2019, \u2018DEGRADED\u2019. Default is \u2018OK\u2019 when the infrastructure is provisioned.


        :param maintenance_slo_status: The maintenance_slo_status of this ExadataInfrastructure.
        :type: str
        """
        allowed_values = ["OK", "DEGRADED"]
        if not value_allowed_none_or_none_sentinel(maintenance_slo_status, allowed_values):
            maintenance_slo_status = 'UNKNOWN_ENUM_VALUE'
        self._maintenance_slo_status = maintenance_slo_status

    @property
    def maintenance_window(self):
        """
        Gets the maintenance_window of this ExadataInfrastructure.

        :return: The maintenance_window of this ExadataInfrastructure.
        :rtype: oci.database.models.MaintenanceWindow
        """
        return self._maintenance_window

    @maintenance_window.setter
    def maintenance_window(self, maintenance_window):
        """
        Sets the maintenance_window of this ExadataInfrastructure.

        :param maintenance_window: The maintenance_window of this ExadataInfrastructure.
        :type: oci.database.models.MaintenanceWindow
        """
        self._maintenance_window = maintenance_window

    @property
    def storage_server_version(self):
        """
        Gets the storage_server_version of this ExadataInfrastructure.
        The software version of the storage servers (cells) in the Exadata infrastructure.


        :return: The storage_server_version of this ExadataInfrastructure.
        :rtype: str
        """
        return self._storage_server_version

    @storage_server_version.setter
    def storage_server_version(self, storage_server_version):
        """
        Sets the storage_server_version of this ExadataInfrastructure.
        The software version of the storage servers (cells) in the Exadata infrastructure.


        :param storage_server_version: The storage_server_version of this ExadataInfrastructure.
        :type: str
        """
        self._storage_server_version = storage_server_version

    @property
    def db_server_version(self):
        """
        Gets the db_server_version of this ExadataInfrastructure.
        The software version of the database servers (dom0) in the Exadata infrastructure.


        :return: The db_server_version of this ExadataInfrastructure.
        :rtype: str
        """
        return self._db_server_version

    @db_server_version.setter
    def db_server_version(self, db_server_version):
        """
        Sets the db_server_version of this ExadataInfrastructure.
        The software version of the database servers (dom0) in the Exadata infrastructure.


        :param db_server_version: The db_server_version of this ExadataInfrastructure.
        :type: str
        """
        self._db_server_version = db_server_version

    @property
    def monthly_db_server_version(self):
        """
        Gets the monthly_db_server_version of this ExadataInfrastructure.
        The monthly software version of the database servers (dom0) in the Exadata infrastructure.


        :return: The monthly_db_server_version of this ExadataInfrastructure.
        :rtype: str
        """
        return self._monthly_db_server_version

    @monthly_db_server_version.setter
    def monthly_db_server_version(self, monthly_db_server_version):
        """
        Sets the monthly_db_server_version of this ExadataInfrastructure.
        The monthly software version of the database servers (dom0) in the Exadata infrastructure.


        :param monthly_db_server_version: The monthly_db_server_version of this ExadataInfrastructure.
        :type: str
        """
        self._monthly_db_server_version = monthly_db_server_version

    @property
    def last_maintenance_run_id(self):
        """
        Gets the last_maintenance_run_id of this ExadataInfrastructure.
        The `OCID`__ of the last maintenance run.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The last_maintenance_run_id of this ExadataInfrastructure.
        :rtype: str
        """
        return self._last_maintenance_run_id

    @last_maintenance_run_id.setter
    def last_maintenance_run_id(self, last_maintenance_run_id):
        """
        Sets the last_maintenance_run_id of this ExadataInfrastructure.
        The `OCID`__ of the last maintenance run.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param last_maintenance_run_id: The last_maintenance_run_id of this ExadataInfrastructure.
        :type: str
        """
        self._last_maintenance_run_id = last_maintenance_run_id

    @property
    def next_maintenance_run_id(self):
        """
        Gets the next_maintenance_run_id of this ExadataInfrastructure.
        The `OCID`__ of the next maintenance run.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The next_maintenance_run_id of this ExadataInfrastructure.
        :rtype: str
        """
        return self._next_maintenance_run_id

    @next_maintenance_run_id.setter
    def next_maintenance_run_id(self, next_maintenance_run_id):
        """
        Sets the next_maintenance_run_id of this ExadataInfrastructure.
        The `OCID`__ of the next maintenance run.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param next_maintenance_run_id: The next_maintenance_run_id of this ExadataInfrastructure.
        :type: str
        """
        self._next_maintenance_run_id = next_maintenance_run_id

    @property
    def is_cps_offline_report_enabled(self):
        """
        Gets the is_cps_offline_report_enabled of this ExadataInfrastructure.
        Indicates whether cps offline diagnostic report is enabled for this Exadata infrastructure. This will allow a customer to quickly check status themselves and fix problems on their end, saving time and frustration
        for both Oracle and the customer when they find the CPS in a disconnected state.You can enable offline diagnostic report during Exadata infrastructure provisioning. You can also disable or enable it at any time
        using the UpdateExadatainfrastructure API.


        :return: The is_cps_offline_report_enabled of this ExadataInfrastructure.
        :rtype: bool
        """
        return self._is_cps_offline_report_enabled

    @is_cps_offline_report_enabled.setter
    def is_cps_offline_report_enabled(self, is_cps_offline_report_enabled):
        """
        Sets the is_cps_offline_report_enabled of this ExadataInfrastructure.
        Indicates whether cps offline diagnostic report is enabled for this Exadata infrastructure. This will allow a customer to quickly check status themselves and fix problems on their end, saving time and frustration
        for both Oracle and the customer when they find the CPS in a disconnected state.You can enable offline diagnostic report during Exadata infrastructure provisioning. You can also disable or enable it at any time
        using the UpdateExadatainfrastructure API.


        :param is_cps_offline_report_enabled: The is_cps_offline_report_enabled of this ExadataInfrastructure.
        :type: bool
        """
        self._is_cps_offline_report_enabled = is_cps_offline_report_enabled

    @property
    def network_bonding_mode_details(self):
        """
        Gets the network_bonding_mode_details of this ExadataInfrastructure.

        :return: The network_bonding_mode_details of this ExadataInfrastructure.
        :rtype: oci.database.models.NetworkBondingModeDetails
        """
        return self._network_bonding_mode_details

    @network_bonding_mode_details.setter
    def network_bonding_mode_details(self, network_bonding_mode_details):
        """
        Sets the network_bonding_mode_details of this ExadataInfrastructure.

        :param network_bonding_mode_details: The network_bonding_mode_details of this ExadataInfrastructure.
        :type: oci.database.models.NetworkBondingModeDetails
        """
        self._network_bonding_mode_details = network_bonding_mode_details

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this ExadataInfrastructure.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this ExadataInfrastructure.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this ExadataInfrastructure.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this ExadataInfrastructure.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this ExadataInfrastructure.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this ExadataInfrastructure.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this ExadataInfrastructure.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this ExadataInfrastructure.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
