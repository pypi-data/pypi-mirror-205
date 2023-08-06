# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class LaunchInstanceDetails(object):
    """
    Instance launch details.
    Use the `sourceDetails` parameter to specify whether a boot volume or an image should be used to launch a new instance.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new LaunchInstanceDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param availability_domain:
            The value to assign to the availability_domain property of this LaunchInstanceDetails.
        :type availability_domain: str

        :param capacity_reservation_id:
            The value to assign to the capacity_reservation_id property of this LaunchInstanceDetails.
        :type capacity_reservation_id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this LaunchInstanceDetails.
        :type compartment_id: str

        :param create_vnic_details:
            The value to assign to the create_vnic_details property of this LaunchInstanceDetails.
        :type create_vnic_details: oci.cloud_migrations.models.CreateVnicDetails

        :param dedicated_vm_host_id:
            The value to assign to the dedicated_vm_host_id property of this LaunchInstanceDetails.
        :type dedicated_vm_host_id: str

        :param defined_tags:
            The value to assign to the defined_tags property of this LaunchInstanceDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param display_name:
            The value to assign to the display_name property of this LaunchInstanceDetails.
        :type display_name: str

        :param fault_domain:
            The value to assign to the fault_domain property of this LaunchInstanceDetails.
        :type fault_domain: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this LaunchInstanceDetails.
        :type freeform_tags: dict(str, str)

        :param hostname_label:
            The value to assign to the hostname_label property of this LaunchInstanceDetails.
        :type hostname_label: str

        :param ipxe_script:
            The value to assign to the ipxe_script property of this LaunchInstanceDetails.
        :type ipxe_script: str

        :param instance_options:
            The value to assign to the instance_options property of this LaunchInstanceDetails.
        :type instance_options: oci.cloud_migrations.models.InstanceOptions

        :param preemptible_instance_config:
            The value to assign to the preemptible_instance_config property of this LaunchInstanceDetails.
        :type preemptible_instance_config: oci.cloud_migrations.models.PreemptibleInstanceConfigDetails

        :param agent_config:
            The value to assign to the agent_config property of this LaunchInstanceDetails.
        :type agent_config: oci.cloud_migrations.models.LaunchInstanceAgentConfigDetails

        :param shape:
            The value to assign to the shape property of this LaunchInstanceDetails.
        :type shape: str

        :param shape_config:
            The value to assign to the shape_config property of this LaunchInstanceDetails.
        :type shape_config: oci.cloud_migrations.models.LaunchInstanceShapeConfigDetails

        :param source_details:
            The value to assign to the source_details property of this LaunchInstanceDetails.
        :type source_details: oci.cloud_migrations.models.InstanceSourceDetails

        :param is_pv_encryption_in_transit_enabled:
            The value to assign to the is_pv_encryption_in_transit_enabled property of this LaunchInstanceDetails.
        :type is_pv_encryption_in_transit_enabled: bool

        """
        self.swagger_types = {
            'availability_domain': 'str',
            'capacity_reservation_id': 'str',
            'compartment_id': 'str',
            'create_vnic_details': 'CreateVnicDetails',
            'dedicated_vm_host_id': 'str',
            'defined_tags': 'dict(str, dict(str, object))',
            'display_name': 'str',
            'fault_domain': 'str',
            'freeform_tags': 'dict(str, str)',
            'hostname_label': 'str',
            'ipxe_script': 'str',
            'instance_options': 'InstanceOptions',
            'preemptible_instance_config': 'PreemptibleInstanceConfigDetails',
            'agent_config': 'LaunchInstanceAgentConfigDetails',
            'shape': 'str',
            'shape_config': 'LaunchInstanceShapeConfigDetails',
            'source_details': 'InstanceSourceDetails',
            'is_pv_encryption_in_transit_enabled': 'bool'
        }

        self.attribute_map = {
            'availability_domain': 'availabilityDomain',
            'capacity_reservation_id': 'capacityReservationId',
            'compartment_id': 'compartmentId',
            'create_vnic_details': 'createVnicDetails',
            'dedicated_vm_host_id': 'dedicatedVmHostId',
            'defined_tags': 'definedTags',
            'display_name': 'displayName',
            'fault_domain': 'faultDomain',
            'freeform_tags': 'freeformTags',
            'hostname_label': 'hostnameLabel',
            'ipxe_script': 'ipxeScript',
            'instance_options': 'instanceOptions',
            'preemptible_instance_config': 'preemptibleInstanceConfig',
            'agent_config': 'agentConfig',
            'shape': 'shape',
            'shape_config': 'shapeConfig',
            'source_details': 'sourceDetails',
            'is_pv_encryption_in_transit_enabled': 'isPvEncryptionInTransitEnabled'
        }

        self._availability_domain = None
        self._capacity_reservation_id = None
        self._compartment_id = None
        self._create_vnic_details = None
        self._dedicated_vm_host_id = None
        self._defined_tags = None
        self._display_name = None
        self._fault_domain = None
        self._freeform_tags = None
        self._hostname_label = None
        self._ipxe_script = None
        self._instance_options = None
        self._preemptible_instance_config = None
        self._agent_config = None
        self._shape = None
        self._shape_config = None
        self._source_details = None
        self._is_pv_encryption_in_transit_enabled = None

    @property
    def availability_domain(self):
        """
        Gets the availability_domain of this LaunchInstanceDetails.
        The availability domain of the instance.

        Example: `Uocm:PHX-AD-1`


        :return: The availability_domain of this LaunchInstanceDetails.
        :rtype: str
        """
        return self._availability_domain

    @availability_domain.setter
    def availability_domain(self, availability_domain):
        """
        Sets the availability_domain of this LaunchInstanceDetails.
        The availability domain of the instance.

        Example: `Uocm:PHX-AD-1`


        :param availability_domain: The availability_domain of this LaunchInstanceDetails.
        :type: str
        """
        self._availability_domain = availability_domain

    @property
    def capacity_reservation_id(self):
        """
        Gets the capacity_reservation_id of this LaunchInstanceDetails.
        The OCID of the compute capacity reservation under which this instance is launched.
        You can opt out of all default reservations by specifying an empty string as input for this field.
        For more information, see `Capacity Reservations`__.

        __ https://docs.cloud.oracle.com/iaas/Content/Compute/Tasks/reserve-capacity.htm#default


        :return: The capacity_reservation_id of this LaunchInstanceDetails.
        :rtype: str
        """
        return self._capacity_reservation_id

    @capacity_reservation_id.setter
    def capacity_reservation_id(self, capacity_reservation_id):
        """
        Sets the capacity_reservation_id of this LaunchInstanceDetails.
        The OCID of the compute capacity reservation under which this instance is launched.
        You can opt out of all default reservations by specifying an empty string as input for this field.
        For more information, see `Capacity Reservations`__.

        __ https://docs.cloud.oracle.com/iaas/Content/Compute/Tasks/reserve-capacity.htm#default


        :param capacity_reservation_id: The capacity_reservation_id of this LaunchInstanceDetails.
        :type: str
        """
        self._capacity_reservation_id = capacity_reservation_id

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this LaunchInstanceDetails.
        The OCID of the compartment.


        :return: The compartment_id of this LaunchInstanceDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this LaunchInstanceDetails.
        The OCID of the compartment.


        :param compartment_id: The compartment_id of this LaunchInstanceDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def create_vnic_details(self):
        """
        Gets the create_vnic_details of this LaunchInstanceDetails.

        :return: The create_vnic_details of this LaunchInstanceDetails.
        :rtype: oci.cloud_migrations.models.CreateVnicDetails
        """
        return self._create_vnic_details

    @create_vnic_details.setter
    def create_vnic_details(self, create_vnic_details):
        """
        Sets the create_vnic_details of this LaunchInstanceDetails.

        :param create_vnic_details: The create_vnic_details of this LaunchInstanceDetails.
        :type: oci.cloud_migrations.models.CreateVnicDetails
        """
        self._create_vnic_details = create_vnic_details

    @property
    def dedicated_vm_host_id(self):
        """
        Gets the dedicated_vm_host_id of this LaunchInstanceDetails.
        The OCID of the dedicated VM host.


        :return: The dedicated_vm_host_id of this LaunchInstanceDetails.
        :rtype: str
        """
        return self._dedicated_vm_host_id

    @dedicated_vm_host_id.setter
    def dedicated_vm_host_id(self, dedicated_vm_host_id):
        """
        Sets the dedicated_vm_host_id of this LaunchInstanceDetails.
        The OCID of the dedicated VM host.


        :param dedicated_vm_host_id: The dedicated_vm_host_id of this LaunchInstanceDetails.
        :type: str
        """
        self._dedicated_vm_host_id = dedicated_vm_host_id

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this LaunchInstanceDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this LaunchInstanceDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this LaunchInstanceDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this LaunchInstanceDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def display_name(self):
        """
        Gets the display_name of this LaunchInstanceDetails.
        A user-friendly name. Does not have to be unique, and it's changeable.
        Avoid entering confidential information.


        :return: The display_name of this LaunchInstanceDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this LaunchInstanceDetails.
        A user-friendly name. Does not have to be unique, and it's changeable.
        Avoid entering confidential information.


        :param display_name: The display_name of this LaunchInstanceDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def fault_domain(self):
        """
        Gets the fault_domain of this LaunchInstanceDetails.
        A fault domain is a grouping of hardware and infrastructure within an availability domain.
        Each availability domain contains three fault domains. Fault domains lets you distribute your
        instances so that they are not on the same physical hardware within a single availability domain.
        A hardware failure or Compute hardware maintenance that affects one fault domain does not affect
        instances in other fault domains.

        If you do not specify the fault domain, the system selects one for you.


        To get a list of fault domains, use the
        :func:`list_fault_domains` operation in the
        Identity and Access Management Service API.

        Example: `FAULT-DOMAIN-1`


        :return: The fault_domain of this LaunchInstanceDetails.
        :rtype: str
        """
        return self._fault_domain

    @fault_domain.setter
    def fault_domain(self, fault_domain):
        """
        Sets the fault_domain of this LaunchInstanceDetails.
        A fault domain is a grouping of hardware and infrastructure within an availability domain.
        Each availability domain contains three fault domains. Fault domains lets you distribute your
        instances so that they are not on the same physical hardware within a single availability domain.
        A hardware failure or Compute hardware maintenance that affects one fault domain does not affect
        instances in other fault domains.

        If you do not specify the fault domain, the system selects one for you.


        To get a list of fault domains, use the
        :func:`list_fault_domains` operation in the
        Identity and Access Management Service API.

        Example: `FAULT-DOMAIN-1`


        :param fault_domain: The fault_domain of this LaunchInstanceDetails.
        :type: str
        """
        self._fault_domain = fault_domain

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this LaunchInstanceDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. It exists only for cross-compatibility.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this LaunchInstanceDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this LaunchInstanceDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. It exists only for cross-compatibility.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this LaunchInstanceDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def hostname_label(self):
        """
        Gets the hostname_label of this LaunchInstanceDetails.
        Deprecated. Instead use `hostnameLabel` in
        :class:`CreateVnicDetails`.
        If you provide both, the values must match.


        :return: The hostname_label of this LaunchInstanceDetails.
        :rtype: str
        """
        return self._hostname_label

    @hostname_label.setter
    def hostname_label(self, hostname_label):
        """
        Sets the hostname_label of this LaunchInstanceDetails.
        Deprecated. Instead use `hostnameLabel` in
        :class:`CreateVnicDetails`.
        If you provide both, the values must match.


        :param hostname_label: The hostname_label of this LaunchInstanceDetails.
        :type: str
        """
        self._hostname_label = hostname_label

    @property
    def ipxe_script(self):
        """
        Gets the ipxe_script of this LaunchInstanceDetails.
        This is an advanced option.

        When a bare metal or virtual machine
        instance boots, the iPXE firmware that runs on the instance is
        configured to run an iPXE script to continue the boot process.

        If you want more control over the boot process, you can provide
        your own custom iPXE script that will run when the instance boots.
        Be aware that the same iPXE script will run
        every time an instance boots, not only after the initial
        LaunchInstance call.

        By default, the iPXE script connects to the instance's local boot
        volume over iSCSI and performs a network boot. If you use a custom iPXE
        script and want to network-boot from the instance's local boot volume
        over iSCSI in the same way as the default iPXE script, use the
        following iSCSI IP address: 169.254.0.2, and boot volume IQN:
        iqn.2015-02.oracle.boot.

        If your instance boot volume type is paravirtualized,
        the boot volume is attached to the instance through virtio-scsi and no iPXE script is used.
        If your instance boot volume type is paravirtualized
        and you use custom iPXE to perform network-boot into your instance,
        the primary boot volume is attached as a data volume through the virtio-scsi drive.

        For more information about the Bring Your Own Image feature of
        Oracle Cloud Infrastructure, see
        `Bring Your Own Image`__.

        For more information about iPXE, see http://ipxe.org.

        __ https://docs.cloud.oracle.com/iaas/Content/Compute/References/bringyourownimage.htm


        :return: The ipxe_script of this LaunchInstanceDetails.
        :rtype: str
        """
        return self._ipxe_script

    @ipxe_script.setter
    def ipxe_script(self, ipxe_script):
        """
        Sets the ipxe_script of this LaunchInstanceDetails.
        This is an advanced option.

        When a bare metal or virtual machine
        instance boots, the iPXE firmware that runs on the instance is
        configured to run an iPXE script to continue the boot process.

        If you want more control over the boot process, you can provide
        your own custom iPXE script that will run when the instance boots.
        Be aware that the same iPXE script will run
        every time an instance boots, not only after the initial
        LaunchInstance call.

        By default, the iPXE script connects to the instance's local boot
        volume over iSCSI and performs a network boot. If you use a custom iPXE
        script and want to network-boot from the instance's local boot volume
        over iSCSI in the same way as the default iPXE script, use the
        following iSCSI IP address: 169.254.0.2, and boot volume IQN:
        iqn.2015-02.oracle.boot.

        If your instance boot volume type is paravirtualized,
        the boot volume is attached to the instance through virtio-scsi and no iPXE script is used.
        If your instance boot volume type is paravirtualized
        and you use custom iPXE to perform network-boot into your instance,
        the primary boot volume is attached as a data volume through the virtio-scsi drive.

        For more information about the Bring Your Own Image feature of
        Oracle Cloud Infrastructure, see
        `Bring Your Own Image`__.

        For more information about iPXE, see http://ipxe.org.

        __ https://docs.cloud.oracle.com/iaas/Content/Compute/References/bringyourownimage.htm


        :param ipxe_script: The ipxe_script of this LaunchInstanceDetails.
        :type: str
        """
        self._ipxe_script = ipxe_script

    @property
    def instance_options(self):
        """
        Gets the instance_options of this LaunchInstanceDetails.

        :return: The instance_options of this LaunchInstanceDetails.
        :rtype: oci.cloud_migrations.models.InstanceOptions
        """
        return self._instance_options

    @instance_options.setter
    def instance_options(self, instance_options):
        """
        Sets the instance_options of this LaunchInstanceDetails.

        :param instance_options: The instance_options of this LaunchInstanceDetails.
        :type: oci.cloud_migrations.models.InstanceOptions
        """
        self._instance_options = instance_options

    @property
    def preemptible_instance_config(self):
        """
        Gets the preemptible_instance_config of this LaunchInstanceDetails.

        :return: The preemptible_instance_config of this LaunchInstanceDetails.
        :rtype: oci.cloud_migrations.models.PreemptibleInstanceConfigDetails
        """
        return self._preemptible_instance_config

    @preemptible_instance_config.setter
    def preemptible_instance_config(self, preemptible_instance_config):
        """
        Sets the preemptible_instance_config of this LaunchInstanceDetails.

        :param preemptible_instance_config: The preemptible_instance_config of this LaunchInstanceDetails.
        :type: oci.cloud_migrations.models.PreemptibleInstanceConfigDetails
        """
        self._preemptible_instance_config = preemptible_instance_config

    @property
    def agent_config(self):
        """
        Gets the agent_config of this LaunchInstanceDetails.

        :return: The agent_config of this LaunchInstanceDetails.
        :rtype: oci.cloud_migrations.models.LaunchInstanceAgentConfigDetails
        """
        return self._agent_config

    @agent_config.setter
    def agent_config(self, agent_config):
        """
        Sets the agent_config of this LaunchInstanceDetails.

        :param agent_config: The agent_config of this LaunchInstanceDetails.
        :type: oci.cloud_migrations.models.LaunchInstanceAgentConfigDetails
        """
        self._agent_config = agent_config

    @property
    def shape(self):
        """
        Gets the shape of this LaunchInstanceDetails.
        The shape of an instance. The shape determines the number of CPUs, amount of memory,
        and other resources allocated to the instance.

        You can enumerate all available shapes by calling :func:`list_shapes`.


        :return: The shape of this LaunchInstanceDetails.
        :rtype: str
        """
        return self._shape

    @shape.setter
    def shape(self, shape):
        """
        Sets the shape of this LaunchInstanceDetails.
        The shape of an instance. The shape determines the number of CPUs, amount of memory,
        and other resources allocated to the instance.

        You can enumerate all available shapes by calling :func:`list_shapes`.


        :param shape: The shape of this LaunchInstanceDetails.
        :type: str
        """
        self._shape = shape

    @property
    def shape_config(self):
        """
        Gets the shape_config of this LaunchInstanceDetails.

        :return: The shape_config of this LaunchInstanceDetails.
        :rtype: oci.cloud_migrations.models.LaunchInstanceShapeConfigDetails
        """
        return self._shape_config

    @shape_config.setter
    def shape_config(self, shape_config):
        """
        Sets the shape_config of this LaunchInstanceDetails.

        :param shape_config: The shape_config of this LaunchInstanceDetails.
        :type: oci.cloud_migrations.models.LaunchInstanceShapeConfigDetails
        """
        self._shape_config = shape_config

    @property
    def source_details(self):
        """
        Gets the source_details of this LaunchInstanceDetails.

        :return: The source_details of this LaunchInstanceDetails.
        :rtype: oci.cloud_migrations.models.InstanceSourceDetails
        """
        return self._source_details

    @source_details.setter
    def source_details(self, source_details):
        """
        Sets the source_details of this LaunchInstanceDetails.

        :param source_details: The source_details of this LaunchInstanceDetails.
        :type: oci.cloud_migrations.models.InstanceSourceDetails
        """
        self._source_details = source_details

    @property
    def is_pv_encryption_in_transit_enabled(self):
        """
        Gets the is_pv_encryption_in_transit_enabled of this LaunchInstanceDetails.
        Whether to enable in-transit encryption for the data volume's paravirtualized attachment. This field applies to both block volumes and boot volumes. By default, the value is false.


        :return: The is_pv_encryption_in_transit_enabled of this LaunchInstanceDetails.
        :rtype: bool
        """
        return self._is_pv_encryption_in_transit_enabled

    @is_pv_encryption_in_transit_enabled.setter
    def is_pv_encryption_in_transit_enabled(self, is_pv_encryption_in_transit_enabled):
        """
        Sets the is_pv_encryption_in_transit_enabled of this LaunchInstanceDetails.
        Whether to enable in-transit encryption for the data volume's paravirtualized attachment. This field applies to both block volumes and boot volumes. By default, the value is false.


        :param is_pv_encryption_in_transit_enabled: The is_pv_encryption_in_transit_enabled of this LaunchInstanceDetails.
        :type: bool
        """
        self._is_pv_encryption_in_transit_enabled = is_pv_encryption_in_transit_enabled

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
