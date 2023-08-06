# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateCloudAutonomousVmClusterDetails(object):
    """
    Details for the create cloud Autonomous VM cluster operation.
    """

    #: A constant which can be used with the compute_model property of a CreateCloudAutonomousVmClusterDetails.
    #: This constant has a value of "ECPU"
    COMPUTE_MODEL_ECPU = "ECPU"

    #: A constant which can be used with the compute_model property of a CreateCloudAutonomousVmClusterDetails.
    #: This constant has a value of "OCPU"
    COMPUTE_MODEL_OCPU = "OCPU"

    #: A constant which can be used with the license_model property of a CreateCloudAutonomousVmClusterDetails.
    #: This constant has a value of "LICENSE_INCLUDED"
    LICENSE_MODEL_LICENSE_INCLUDED = "LICENSE_INCLUDED"

    #: A constant which can be used with the license_model property of a CreateCloudAutonomousVmClusterDetails.
    #: This constant has a value of "BRING_YOUR_OWN_LICENSE"
    LICENSE_MODEL_BRING_YOUR_OWN_LICENSE = "BRING_YOUR_OWN_LICENSE"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateCloudAutonomousVmClusterDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateCloudAutonomousVmClusterDetails.
        :type compartment_id: str

        :param description:
            The value to assign to the description property of this CreateCloudAutonomousVmClusterDetails.
        :type description: str

        :param subnet_id:
            The value to assign to the subnet_id property of this CreateCloudAutonomousVmClusterDetails.
        :type subnet_id: str

        :param display_name:
            The value to assign to the display_name property of this CreateCloudAutonomousVmClusterDetails.
        :type display_name: str

        :param cloud_exadata_infrastructure_id:
            The value to assign to the cloud_exadata_infrastructure_id property of this CreateCloudAutonomousVmClusterDetails.
        :type cloud_exadata_infrastructure_id: str

        :param total_container_databases:
            The value to assign to the total_container_databases property of this CreateCloudAutonomousVmClusterDetails.
        :type total_container_databases: int

        :param cpu_core_count_per_node:
            The value to assign to the cpu_core_count_per_node property of this CreateCloudAutonomousVmClusterDetails.
        :type cpu_core_count_per_node: int

        :param memory_per_oracle_compute_unit_in_gbs:
            The value to assign to the memory_per_oracle_compute_unit_in_gbs property of this CreateCloudAutonomousVmClusterDetails.
        :type memory_per_oracle_compute_unit_in_gbs: int

        :param autonomous_data_storage_size_in_tbs:
            The value to assign to the autonomous_data_storage_size_in_tbs property of this CreateCloudAutonomousVmClusterDetails.
        :type autonomous_data_storage_size_in_tbs: float

        :param cluster_time_zone:
            The value to assign to the cluster_time_zone property of this CreateCloudAutonomousVmClusterDetails.
        :type cluster_time_zone: str

        :param compute_model:
            The value to assign to the compute_model property of this CreateCloudAutonomousVmClusterDetails.
            Allowed values for this property are: "ECPU", "OCPU"
        :type compute_model: str

        :param is_mtls_enabled_vm_cluster:
            The value to assign to the is_mtls_enabled_vm_cluster property of this CreateCloudAutonomousVmClusterDetails.
        :type is_mtls_enabled_vm_cluster: bool

        :param db_servers:
            The value to assign to the db_servers property of this CreateCloudAutonomousVmClusterDetails.
        :type db_servers: list[str]

        :param maintenance_window_details:
            The value to assign to the maintenance_window_details property of this CreateCloudAutonomousVmClusterDetails.
        :type maintenance_window_details: oci.database.models.MaintenanceWindow

        :param scan_listener_port_tls:
            The value to assign to the scan_listener_port_tls property of this CreateCloudAutonomousVmClusterDetails.
        :type scan_listener_port_tls: int

        :param scan_listener_port_non_tls:
            The value to assign to the scan_listener_port_non_tls property of this CreateCloudAutonomousVmClusterDetails.
        :type scan_listener_port_non_tls: int

        :param license_model:
            The value to assign to the license_model property of this CreateCloudAutonomousVmClusterDetails.
            Allowed values for this property are: "LICENSE_INCLUDED", "BRING_YOUR_OWN_LICENSE"
        :type license_model: str

        :param nsg_ids:
            The value to assign to the nsg_ids property of this CreateCloudAutonomousVmClusterDetails.
        :type nsg_ids: list[str]

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateCloudAutonomousVmClusterDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateCloudAutonomousVmClusterDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'description': 'str',
            'subnet_id': 'str',
            'display_name': 'str',
            'cloud_exadata_infrastructure_id': 'str',
            'total_container_databases': 'int',
            'cpu_core_count_per_node': 'int',
            'memory_per_oracle_compute_unit_in_gbs': 'int',
            'autonomous_data_storage_size_in_tbs': 'float',
            'cluster_time_zone': 'str',
            'compute_model': 'str',
            'is_mtls_enabled_vm_cluster': 'bool',
            'db_servers': 'list[str]',
            'maintenance_window_details': 'MaintenanceWindow',
            'scan_listener_port_tls': 'int',
            'scan_listener_port_non_tls': 'int',
            'license_model': 'str',
            'nsg_ids': 'list[str]',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'description': 'description',
            'subnet_id': 'subnetId',
            'display_name': 'displayName',
            'cloud_exadata_infrastructure_id': 'cloudExadataInfrastructureId',
            'total_container_databases': 'totalContainerDatabases',
            'cpu_core_count_per_node': 'cpuCoreCountPerNode',
            'memory_per_oracle_compute_unit_in_gbs': 'memoryPerOracleComputeUnitInGBs',
            'autonomous_data_storage_size_in_tbs': 'autonomousDataStorageSizeInTBs',
            'cluster_time_zone': 'clusterTimeZone',
            'compute_model': 'computeModel',
            'is_mtls_enabled_vm_cluster': 'isMtlsEnabledVmCluster',
            'db_servers': 'dbServers',
            'maintenance_window_details': 'maintenanceWindowDetails',
            'scan_listener_port_tls': 'scanListenerPortTls',
            'scan_listener_port_non_tls': 'scanListenerPortNonTls',
            'license_model': 'licenseModel',
            'nsg_ids': 'nsgIds',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._compartment_id = None
        self._description = None
        self._subnet_id = None
        self._display_name = None
        self._cloud_exadata_infrastructure_id = None
        self._total_container_databases = None
        self._cpu_core_count_per_node = None
        self._memory_per_oracle_compute_unit_in_gbs = None
        self._autonomous_data_storage_size_in_tbs = None
        self._cluster_time_zone = None
        self._compute_model = None
        self._is_mtls_enabled_vm_cluster = None
        self._db_servers = None
        self._maintenance_window_details = None
        self._scan_listener_port_tls = None
        self._scan_listener_port_non_tls = None
        self._license_model = None
        self._nsg_ids = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateCloudAutonomousVmClusterDetails.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CreateCloudAutonomousVmClusterDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateCloudAutonomousVmClusterDetails.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CreateCloudAutonomousVmClusterDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def description(self):
        """
        Gets the description of this CreateCloudAutonomousVmClusterDetails.
        User defined description of the cloud Autonomous VM cluster.


        :return: The description of this CreateCloudAutonomousVmClusterDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CreateCloudAutonomousVmClusterDetails.
        User defined description of the cloud Autonomous VM cluster.


        :param description: The description of this CreateCloudAutonomousVmClusterDetails.
        :type: str
        """
        self._description = description

    @property
    def subnet_id(self):
        """
        **[Required]** Gets the subnet_id of this CreateCloudAutonomousVmClusterDetails.
        The `OCID`__ of the subnet the cloud Autonomous VM Cluster is associated with.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The subnet_id of this CreateCloudAutonomousVmClusterDetails.
        :rtype: str
        """
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet_id):
        """
        Sets the subnet_id of this CreateCloudAutonomousVmClusterDetails.
        The `OCID`__ of the subnet the cloud Autonomous VM Cluster is associated with.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param subnet_id: The subnet_id of this CreateCloudAutonomousVmClusterDetails.
        :type: str
        """
        self._subnet_id = subnet_id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this CreateCloudAutonomousVmClusterDetails.
        The user-friendly name for the cloud Autonomous VM cluster. The name does not need to be unique.


        :return: The display_name of this CreateCloudAutonomousVmClusterDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateCloudAutonomousVmClusterDetails.
        The user-friendly name for the cloud Autonomous VM cluster. The name does not need to be unique.


        :param display_name: The display_name of this CreateCloudAutonomousVmClusterDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def cloud_exadata_infrastructure_id(self):
        """
        **[Required]** Gets the cloud_exadata_infrastructure_id of this CreateCloudAutonomousVmClusterDetails.
        The `OCID`__ of the cloud Exadata infrastructure.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The cloud_exadata_infrastructure_id of this CreateCloudAutonomousVmClusterDetails.
        :rtype: str
        """
        return self._cloud_exadata_infrastructure_id

    @cloud_exadata_infrastructure_id.setter
    def cloud_exadata_infrastructure_id(self, cloud_exadata_infrastructure_id):
        """
        Sets the cloud_exadata_infrastructure_id of this CreateCloudAutonomousVmClusterDetails.
        The `OCID`__ of the cloud Exadata infrastructure.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param cloud_exadata_infrastructure_id: The cloud_exadata_infrastructure_id of this CreateCloudAutonomousVmClusterDetails.
        :type: str
        """
        self._cloud_exadata_infrastructure_id = cloud_exadata_infrastructure_id

    @property
    def total_container_databases(self):
        """
        Gets the total_container_databases of this CreateCloudAutonomousVmClusterDetails.
        The total number of Autonomous Container Databases that can be created.


        :return: The total_container_databases of this CreateCloudAutonomousVmClusterDetails.
        :rtype: int
        """
        return self._total_container_databases

    @total_container_databases.setter
    def total_container_databases(self, total_container_databases):
        """
        Sets the total_container_databases of this CreateCloudAutonomousVmClusterDetails.
        The total number of Autonomous Container Databases that can be created.


        :param total_container_databases: The total_container_databases of this CreateCloudAutonomousVmClusterDetails.
        :type: int
        """
        self._total_container_databases = total_container_databases

    @property
    def cpu_core_count_per_node(self):
        """
        Gets the cpu_core_count_per_node of this CreateCloudAutonomousVmClusterDetails.
        The number of CPU cores to be enabled per VM cluster node.


        :return: The cpu_core_count_per_node of this CreateCloudAutonomousVmClusterDetails.
        :rtype: int
        """
        return self._cpu_core_count_per_node

    @cpu_core_count_per_node.setter
    def cpu_core_count_per_node(self, cpu_core_count_per_node):
        """
        Sets the cpu_core_count_per_node of this CreateCloudAutonomousVmClusterDetails.
        The number of CPU cores to be enabled per VM cluster node.


        :param cpu_core_count_per_node: The cpu_core_count_per_node of this CreateCloudAutonomousVmClusterDetails.
        :type: int
        """
        self._cpu_core_count_per_node = cpu_core_count_per_node

    @property
    def memory_per_oracle_compute_unit_in_gbs(self):
        """
        Gets the memory_per_oracle_compute_unit_in_gbs of this CreateCloudAutonomousVmClusterDetails.
        The amount of memory (in GBs) to be enabled per each CPU core.


        :return: The memory_per_oracle_compute_unit_in_gbs of this CreateCloudAutonomousVmClusterDetails.
        :rtype: int
        """
        return self._memory_per_oracle_compute_unit_in_gbs

    @memory_per_oracle_compute_unit_in_gbs.setter
    def memory_per_oracle_compute_unit_in_gbs(self, memory_per_oracle_compute_unit_in_gbs):
        """
        Sets the memory_per_oracle_compute_unit_in_gbs of this CreateCloudAutonomousVmClusterDetails.
        The amount of memory (in GBs) to be enabled per each CPU core.


        :param memory_per_oracle_compute_unit_in_gbs: The memory_per_oracle_compute_unit_in_gbs of this CreateCloudAutonomousVmClusterDetails.
        :type: int
        """
        self._memory_per_oracle_compute_unit_in_gbs = memory_per_oracle_compute_unit_in_gbs

    @property
    def autonomous_data_storage_size_in_tbs(self):
        """
        Gets the autonomous_data_storage_size_in_tbs of this CreateCloudAutonomousVmClusterDetails.
        The data disk group size to be allocated for Autonomous Databases, in TBs.


        :return: The autonomous_data_storage_size_in_tbs of this CreateCloudAutonomousVmClusterDetails.
        :rtype: float
        """
        return self._autonomous_data_storage_size_in_tbs

    @autonomous_data_storage_size_in_tbs.setter
    def autonomous_data_storage_size_in_tbs(self, autonomous_data_storage_size_in_tbs):
        """
        Sets the autonomous_data_storage_size_in_tbs of this CreateCloudAutonomousVmClusterDetails.
        The data disk group size to be allocated for Autonomous Databases, in TBs.


        :param autonomous_data_storage_size_in_tbs: The autonomous_data_storage_size_in_tbs of this CreateCloudAutonomousVmClusterDetails.
        :type: float
        """
        self._autonomous_data_storage_size_in_tbs = autonomous_data_storage_size_in_tbs

    @property
    def cluster_time_zone(self):
        """
        Gets the cluster_time_zone of this CreateCloudAutonomousVmClusterDetails.
        The time zone to use for the Cloud Autonomous VM cluster. For details, see `DB System Time Zones`__.

        __ https://docs.cloud.oracle.com/Content/Database/References/timezones.htm


        :return: The cluster_time_zone of this CreateCloudAutonomousVmClusterDetails.
        :rtype: str
        """
        return self._cluster_time_zone

    @cluster_time_zone.setter
    def cluster_time_zone(self, cluster_time_zone):
        """
        Sets the cluster_time_zone of this CreateCloudAutonomousVmClusterDetails.
        The time zone to use for the Cloud Autonomous VM cluster. For details, see `DB System Time Zones`__.

        __ https://docs.cloud.oracle.com/Content/Database/References/timezones.htm


        :param cluster_time_zone: The cluster_time_zone of this CreateCloudAutonomousVmClusterDetails.
        :type: str
        """
        self._cluster_time_zone = cluster_time_zone

    @property
    def compute_model(self):
        """
        Gets the compute_model of this CreateCloudAutonomousVmClusterDetails.
        The compute model of the Cloud Autonomous VM Cluster. See `Compute Models in Autonomous Database on Dedicated Exadata Infrastructure`__ for more details.

        __ https://docs.oracle.com/en/cloud/paas/autonomous-database/dedicated/adbak

        Allowed values for this property are: "ECPU", "OCPU"


        :return: The compute_model of this CreateCloudAutonomousVmClusterDetails.
        :rtype: str
        """
        return self._compute_model

    @compute_model.setter
    def compute_model(self, compute_model):
        """
        Sets the compute_model of this CreateCloudAutonomousVmClusterDetails.
        The compute model of the Cloud Autonomous VM Cluster. See `Compute Models in Autonomous Database on Dedicated Exadata Infrastructure`__ for more details.

        __ https://docs.oracle.com/en/cloud/paas/autonomous-database/dedicated/adbak


        :param compute_model: The compute_model of this CreateCloudAutonomousVmClusterDetails.
        :type: str
        """
        allowed_values = ["ECPU", "OCPU"]
        if not value_allowed_none_or_none_sentinel(compute_model, allowed_values):
            raise ValueError(
                "Invalid value for `compute_model`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._compute_model = compute_model

    @property
    def is_mtls_enabled_vm_cluster(self):
        """
        Gets the is_mtls_enabled_vm_cluster of this CreateCloudAutonomousVmClusterDetails.
        Enable mutual TLS(mTLS) authentication for database at time of provisioning a VMCluster. This is applicable to database TLS Certificates only. Default is TLS


        :return: The is_mtls_enabled_vm_cluster of this CreateCloudAutonomousVmClusterDetails.
        :rtype: bool
        """
        return self._is_mtls_enabled_vm_cluster

    @is_mtls_enabled_vm_cluster.setter
    def is_mtls_enabled_vm_cluster(self, is_mtls_enabled_vm_cluster):
        """
        Sets the is_mtls_enabled_vm_cluster of this CreateCloudAutonomousVmClusterDetails.
        Enable mutual TLS(mTLS) authentication for database at time of provisioning a VMCluster. This is applicable to database TLS Certificates only. Default is TLS


        :param is_mtls_enabled_vm_cluster: The is_mtls_enabled_vm_cluster of this CreateCloudAutonomousVmClusterDetails.
        :type: bool
        """
        self._is_mtls_enabled_vm_cluster = is_mtls_enabled_vm_cluster

    @property
    def db_servers(self):
        """
        Gets the db_servers of this CreateCloudAutonomousVmClusterDetails.
        The list of database servers.


        :return: The db_servers of this CreateCloudAutonomousVmClusterDetails.
        :rtype: list[str]
        """
        return self._db_servers

    @db_servers.setter
    def db_servers(self, db_servers):
        """
        Sets the db_servers of this CreateCloudAutonomousVmClusterDetails.
        The list of database servers.


        :param db_servers: The db_servers of this CreateCloudAutonomousVmClusterDetails.
        :type: list[str]
        """
        self._db_servers = db_servers

    @property
    def maintenance_window_details(self):
        """
        Gets the maintenance_window_details of this CreateCloudAutonomousVmClusterDetails.

        :return: The maintenance_window_details of this CreateCloudAutonomousVmClusterDetails.
        :rtype: oci.database.models.MaintenanceWindow
        """
        return self._maintenance_window_details

    @maintenance_window_details.setter
    def maintenance_window_details(self, maintenance_window_details):
        """
        Sets the maintenance_window_details of this CreateCloudAutonomousVmClusterDetails.

        :param maintenance_window_details: The maintenance_window_details of this CreateCloudAutonomousVmClusterDetails.
        :type: oci.database.models.MaintenanceWindow
        """
        self._maintenance_window_details = maintenance_window_details

    @property
    def scan_listener_port_tls(self):
        """
        Gets the scan_listener_port_tls of this CreateCloudAutonomousVmClusterDetails.
        The SCAN Listener TLS port. Default is 2484.


        :return: The scan_listener_port_tls of this CreateCloudAutonomousVmClusterDetails.
        :rtype: int
        """
        return self._scan_listener_port_tls

    @scan_listener_port_tls.setter
    def scan_listener_port_tls(self, scan_listener_port_tls):
        """
        Sets the scan_listener_port_tls of this CreateCloudAutonomousVmClusterDetails.
        The SCAN Listener TLS port. Default is 2484.


        :param scan_listener_port_tls: The scan_listener_port_tls of this CreateCloudAutonomousVmClusterDetails.
        :type: int
        """
        self._scan_listener_port_tls = scan_listener_port_tls

    @property
    def scan_listener_port_non_tls(self):
        """
        Gets the scan_listener_port_non_tls of this CreateCloudAutonomousVmClusterDetails.
        The SCAN Listener Non TLS port. Default is 1521.


        :return: The scan_listener_port_non_tls of this CreateCloudAutonomousVmClusterDetails.
        :rtype: int
        """
        return self._scan_listener_port_non_tls

    @scan_listener_port_non_tls.setter
    def scan_listener_port_non_tls(self, scan_listener_port_non_tls):
        """
        Sets the scan_listener_port_non_tls of this CreateCloudAutonomousVmClusterDetails.
        The SCAN Listener Non TLS port. Default is 1521.


        :param scan_listener_port_non_tls: The scan_listener_port_non_tls of this CreateCloudAutonomousVmClusterDetails.
        :type: int
        """
        self._scan_listener_port_non_tls = scan_listener_port_non_tls

    @property
    def license_model(self):
        """
        Gets the license_model of this CreateCloudAutonomousVmClusterDetails.
        The Oracle license model that applies to the Oracle Autonomous Database. Bring your own license (BYOL) allows you to apply your current on-premises Oracle software licenses to equivalent, highly automated Oracle PaaS and IaaS services in the cloud.
        License Included allows you to subscribe to new Oracle Database software licenses and the Database service.
        Note that when provisioning an Autonomous Database on `dedicated Exadata infrastructure`__, this attribute must be null because the attribute is already set at the
        Autonomous Exadata Infrastructure level. When using `shared Exadata infrastructure`__, if a value is not specified, the system will supply the value of `BRING_YOUR_OWN_LICENSE`.

        This cannot be updated in parallel with any of the following: cpuCoreCount, computeCount, maxCpuCoreCount, dataStorageSizeInTBs, adminPassword, isMTLSConnectionRequired, dbWorkload, privateEndpointLabel, nsgIds, dbVersion, dbName, scheduledOperations, dbToolsDetails, or isFreeTier.

        __ https://docs.oracle.com/en/cloud/paas/autonomous-database/index.html
        __ https://docs.oracle.com/en/cloud/paas/autonomous-database/index.html

        Allowed values for this property are: "LICENSE_INCLUDED", "BRING_YOUR_OWN_LICENSE"


        :return: The license_model of this CreateCloudAutonomousVmClusterDetails.
        :rtype: str
        """
        return self._license_model

    @license_model.setter
    def license_model(self, license_model):
        """
        Sets the license_model of this CreateCloudAutonomousVmClusterDetails.
        The Oracle license model that applies to the Oracle Autonomous Database. Bring your own license (BYOL) allows you to apply your current on-premises Oracle software licenses to equivalent, highly automated Oracle PaaS and IaaS services in the cloud.
        License Included allows you to subscribe to new Oracle Database software licenses and the Database service.
        Note that when provisioning an Autonomous Database on `dedicated Exadata infrastructure`__, this attribute must be null because the attribute is already set at the
        Autonomous Exadata Infrastructure level. When using `shared Exadata infrastructure`__, if a value is not specified, the system will supply the value of `BRING_YOUR_OWN_LICENSE`.

        This cannot be updated in parallel with any of the following: cpuCoreCount, computeCount, maxCpuCoreCount, dataStorageSizeInTBs, adminPassword, isMTLSConnectionRequired, dbWorkload, privateEndpointLabel, nsgIds, dbVersion, dbName, scheduledOperations, dbToolsDetails, or isFreeTier.

        __ https://docs.oracle.com/en/cloud/paas/autonomous-database/index.html
        __ https://docs.oracle.com/en/cloud/paas/autonomous-database/index.html


        :param license_model: The license_model of this CreateCloudAutonomousVmClusterDetails.
        :type: str
        """
        allowed_values = ["LICENSE_INCLUDED", "BRING_YOUR_OWN_LICENSE"]
        if not value_allowed_none_or_none_sentinel(license_model, allowed_values):
            raise ValueError(
                "Invalid value for `license_model`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._license_model = license_model

    @property
    def nsg_ids(self):
        """
        Gets the nsg_ids of this CreateCloudAutonomousVmClusterDetails.
        The list of `OCIDs`__ for the network security groups (NSGs) to which this resource belongs. Setting this to an empty list removes all resources from all NSGs. For more information about NSGs, see `Security Rules`__.
        **NsgIds restrictions:**
        - A network security group (NSG) is optional for Autonomous Databases with private access. The nsgIds list can be empty.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm
        __ https://docs.cloud.oracle.com/Content/Network/Concepts/securityrules.htm


        :return: The nsg_ids of this CreateCloudAutonomousVmClusterDetails.
        :rtype: list[str]
        """
        return self._nsg_ids

    @nsg_ids.setter
    def nsg_ids(self, nsg_ids):
        """
        Sets the nsg_ids of this CreateCloudAutonomousVmClusterDetails.
        The list of `OCIDs`__ for the network security groups (NSGs) to which this resource belongs. Setting this to an empty list removes all resources from all NSGs. For more information about NSGs, see `Security Rules`__.
        **NsgIds restrictions:**
        - A network security group (NSG) is optional for Autonomous Databases with private access. The nsgIds list can be empty.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm
        __ https://docs.cloud.oracle.com/Content/Network/Concepts/securityrules.htm


        :param nsg_ids: The nsg_ids of this CreateCloudAutonomousVmClusterDetails.
        :type: list[str]
        """
        self._nsg_ids = nsg_ids

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateCloudAutonomousVmClusterDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CreateCloudAutonomousVmClusterDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateCloudAutonomousVmClusterDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CreateCloudAutonomousVmClusterDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateCloudAutonomousVmClusterDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CreateCloudAutonomousVmClusterDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateCloudAutonomousVmClusterDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CreateCloudAutonomousVmClusterDetails.
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
