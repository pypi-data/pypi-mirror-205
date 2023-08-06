# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class VirtualNodePool(object):
    """
    A pool of virtual nodes attached to a cluster.
    """

    #: A constant which can be used with the lifecycle_state property of a VirtualNodePool.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a VirtualNodePool.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a VirtualNodePool.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a VirtualNodePool.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a VirtualNodePool.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a VirtualNodePool.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a VirtualNodePool.
    #: This constant has a value of "NEEDS_ATTENTION"
    LIFECYCLE_STATE_NEEDS_ATTENTION = "NEEDS_ATTENTION"

    def __init__(self, **kwargs):
        """
        Initializes a new VirtualNodePool object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this VirtualNodePool.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this VirtualNodePool.
        :type compartment_id: str

        :param cluster_id:
            The value to assign to the cluster_id property of this VirtualNodePool.
        :type cluster_id: str

        :param display_name:
            The value to assign to the display_name property of this VirtualNodePool.
        :type display_name: str

        :param kubernetes_version:
            The value to assign to the kubernetes_version property of this VirtualNodePool.
        :type kubernetes_version: str

        :param initial_virtual_node_labels:
            The value to assign to the initial_virtual_node_labels property of this VirtualNodePool.
        :type initial_virtual_node_labels: list[oci.container_engine.models.InitialVirtualNodeLabel]

        :param taints:
            The value to assign to the taints property of this VirtualNodePool.
        :type taints: list[oci.container_engine.models.Taint]

        :param size:
            The value to assign to the size property of this VirtualNodePool.
        :type size: int

        :param placement_configurations:
            The value to assign to the placement_configurations property of this VirtualNodePool.
        :type placement_configurations: list[oci.container_engine.models.PlacementConfiguration]

        :param nsg_ids:
            The value to assign to the nsg_ids property of this VirtualNodePool.
        :type nsg_ids: list[str]

        :param pod_configuration:
            The value to assign to the pod_configuration property of this VirtualNodePool.
        :type pod_configuration: oci.container_engine.models.PodConfiguration

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this VirtualNodePool.
            Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this VirtualNodePool.
        :type lifecycle_details: str

        :param time_created:
            The value to assign to the time_created property of this VirtualNodePool.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this VirtualNodePool.
        :type time_updated: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this VirtualNodePool.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this VirtualNodePool.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this VirtualNodePool.
        :type system_tags: dict(str, dict(str, object))

        :param virtual_node_tags:
            The value to assign to the virtual_node_tags property of this VirtualNodePool.
        :type virtual_node_tags: oci.container_engine.models.VirtualNodeTags

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'cluster_id': 'str',
            'display_name': 'str',
            'kubernetes_version': 'str',
            'initial_virtual_node_labels': 'list[InitialVirtualNodeLabel]',
            'taints': 'list[Taint]',
            'size': 'int',
            'placement_configurations': 'list[PlacementConfiguration]',
            'nsg_ids': 'list[str]',
            'pod_configuration': 'PodConfiguration',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'virtual_node_tags': 'VirtualNodeTags'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'cluster_id': 'clusterId',
            'display_name': 'displayName',
            'kubernetes_version': 'kubernetesVersion',
            'initial_virtual_node_labels': 'initialVirtualNodeLabels',
            'taints': 'taints',
            'size': 'size',
            'placement_configurations': 'placementConfigurations',
            'nsg_ids': 'nsgIds',
            'pod_configuration': 'podConfiguration',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'virtual_node_tags': 'virtualNodeTags'
        }

        self._id = None
        self._compartment_id = None
        self._cluster_id = None
        self._display_name = None
        self._kubernetes_version = None
        self._initial_virtual_node_labels = None
        self._taints = None
        self._size = None
        self._placement_configurations = None
        self._nsg_ids = None
        self._pod_configuration = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._time_created = None
        self._time_updated = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._virtual_node_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this VirtualNodePool.
        The OCID of the virtual node pool.


        :return: The id of this VirtualNodePool.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this VirtualNodePool.
        The OCID of the virtual node pool.


        :param id: The id of this VirtualNodePool.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this VirtualNodePool.
        Compartment of the virtual node pool.


        :return: The compartment_id of this VirtualNodePool.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this VirtualNodePool.
        Compartment of the virtual node pool.


        :param compartment_id: The compartment_id of this VirtualNodePool.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def cluster_id(self):
        """
        **[Required]** Gets the cluster_id of this VirtualNodePool.
        The cluster the virtual node pool is associated with. A virtual node pool can only be associated with one cluster.


        :return: The cluster_id of this VirtualNodePool.
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """
        Sets the cluster_id of this VirtualNodePool.
        The cluster the virtual node pool is associated with. A virtual node pool can only be associated with one cluster.


        :param cluster_id: The cluster_id of this VirtualNodePool.
        :type: str
        """
        self._cluster_id = cluster_id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this VirtualNodePool.
        Display name of the virtual node pool. This is a non-unique value.


        :return: The display_name of this VirtualNodePool.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this VirtualNodePool.
        Display name of the virtual node pool. This is a non-unique value.


        :param display_name: The display_name of this VirtualNodePool.
        :type: str
        """
        self._display_name = display_name

    @property
    def kubernetes_version(self):
        """
        **[Required]** Gets the kubernetes_version of this VirtualNodePool.
        The version of Kubernetes running on the nodes in the node pool.


        :return: The kubernetes_version of this VirtualNodePool.
        :rtype: str
        """
        return self._kubernetes_version

    @kubernetes_version.setter
    def kubernetes_version(self, kubernetes_version):
        """
        Sets the kubernetes_version of this VirtualNodePool.
        The version of Kubernetes running on the nodes in the node pool.


        :param kubernetes_version: The kubernetes_version of this VirtualNodePool.
        :type: str
        """
        self._kubernetes_version = kubernetes_version

    @property
    def initial_virtual_node_labels(self):
        """
        Gets the initial_virtual_node_labels of this VirtualNodePool.
        Initial labels that will be added to the Kubernetes Virtual Node object when it registers. This is the same as virtualNodePool resources.


        :return: The initial_virtual_node_labels of this VirtualNodePool.
        :rtype: list[oci.container_engine.models.InitialVirtualNodeLabel]
        """
        return self._initial_virtual_node_labels

    @initial_virtual_node_labels.setter
    def initial_virtual_node_labels(self, initial_virtual_node_labels):
        """
        Sets the initial_virtual_node_labels of this VirtualNodePool.
        Initial labels that will be added to the Kubernetes Virtual Node object when it registers. This is the same as virtualNodePool resources.


        :param initial_virtual_node_labels: The initial_virtual_node_labels of this VirtualNodePool.
        :type: list[oci.container_engine.models.InitialVirtualNodeLabel]
        """
        self._initial_virtual_node_labels = initial_virtual_node_labels

    @property
    def taints(self):
        """
        Gets the taints of this VirtualNodePool.
        A taint is a collection of <key, value, effect>. These taints will be applied to the Virtual Nodes of this Virtual Node Pool for Kubernetes scheduling.


        :return: The taints of this VirtualNodePool.
        :rtype: list[oci.container_engine.models.Taint]
        """
        return self._taints

    @taints.setter
    def taints(self, taints):
        """
        Sets the taints of this VirtualNodePool.
        A taint is a collection of <key, value, effect>. These taints will be applied to the Virtual Nodes of this Virtual Node Pool for Kubernetes scheduling.


        :param taints: The taints of this VirtualNodePool.
        :type: list[oci.container_engine.models.Taint]
        """
        self._taints = taints

    @property
    def size(self):
        """
        Gets the size of this VirtualNodePool.
        The number of Virtual Nodes that should be in the Virtual Node Pool. The placement configurations determine where these virtual nodes are placed.


        :return: The size of this VirtualNodePool.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Sets the size of this VirtualNodePool.
        The number of Virtual Nodes that should be in the Virtual Node Pool. The placement configurations determine where these virtual nodes are placed.


        :param size: The size of this VirtualNodePool.
        :type: int
        """
        self._size = size

    @property
    def placement_configurations(self):
        """
        **[Required]** Gets the placement_configurations of this VirtualNodePool.
        The list of placement configurations which determines where Virtual Nodes will be provisioned across as it relates to the subnet and availability domains. The size attribute determines how many we evenly spread across these placement configurations


        :return: The placement_configurations of this VirtualNodePool.
        :rtype: list[oci.container_engine.models.PlacementConfiguration]
        """
        return self._placement_configurations

    @placement_configurations.setter
    def placement_configurations(self, placement_configurations):
        """
        Sets the placement_configurations of this VirtualNodePool.
        The list of placement configurations which determines where Virtual Nodes will be provisioned across as it relates to the subnet and availability domains. The size attribute determines how many we evenly spread across these placement configurations


        :param placement_configurations: The placement_configurations of this VirtualNodePool.
        :type: list[oci.container_engine.models.PlacementConfiguration]
        """
        self._placement_configurations = placement_configurations

    @property
    def nsg_ids(self):
        """
        Gets the nsg_ids of this VirtualNodePool.
        List of network security group id's applied to the Virtual Node VNIC.


        :return: The nsg_ids of this VirtualNodePool.
        :rtype: list[str]
        """
        return self._nsg_ids

    @nsg_ids.setter
    def nsg_ids(self, nsg_ids):
        """
        Sets the nsg_ids of this VirtualNodePool.
        List of network security group id's applied to the Virtual Node VNIC.


        :param nsg_ids: The nsg_ids of this VirtualNodePool.
        :type: list[str]
        """
        self._nsg_ids = nsg_ids

    @property
    def pod_configuration(self):
        """
        Gets the pod_configuration of this VirtualNodePool.
        The pod configuration for pods run on virtual nodes of this virtual node pool.


        :return: The pod_configuration of this VirtualNodePool.
        :rtype: oci.container_engine.models.PodConfiguration
        """
        return self._pod_configuration

    @pod_configuration.setter
    def pod_configuration(self, pod_configuration):
        """
        Sets the pod_configuration of this VirtualNodePool.
        The pod configuration for pods run on virtual nodes of this virtual node pool.


        :param pod_configuration: The pod_configuration of this VirtualNodePool.
        :type: oci.container_engine.models.PodConfiguration
        """
        self._pod_configuration = pod_configuration

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this VirtualNodePool.
        The state of the Virtual Node Pool.

        Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this VirtualNodePool.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this VirtualNodePool.
        The state of the Virtual Node Pool.


        :param lifecycle_state: The lifecycle_state of this VirtualNodePool.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILED", "NEEDS_ATTENTION"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this VirtualNodePool.
        Details about the state of the Virtual Node Pool.


        :return: The lifecycle_details of this VirtualNodePool.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this VirtualNodePool.
        Details about the state of the Virtual Node Pool.


        :param lifecycle_details: The lifecycle_details of this VirtualNodePool.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def time_created(self):
        """
        Gets the time_created of this VirtualNodePool.
        The time the virtual node pool was created.


        :return: The time_created of this VirtualNodePool.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this VirtualNodePool.
        The time the virtual node pool was created.


        :param time_created: The time_created of this VirtualNodePool.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this VirtualNodePool.
        The time the virtual node pool was updated.


        :return: The time_updated of this VirtualNodePool.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this VirtualNodePool.
        The time the virtual node pool was updated.


        :param time_updated: The time_updated of this VirtualNodePool.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this VirtualNodePool.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this VirtualNodePool.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this VirtualNodePool.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this VirtualNodePool.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this VirtualNodePool.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this VirtualNodePool.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this VirtualNodePool.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this VirtualNodePool.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this VirtualNodePool.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this VirtualNodePool.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this VirtualNodePool.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this VirtualNodePool.
        :type: dict(str, dict(str, object))
        """
        self._system_tags = system_tags

    @property
    def virtual_node_tags(self):
        """
        Gets the virtual_node_tags of this VirtualNodePool.

        :return: The virtual_node_tags of this VirtualNodePool.
        :rtype: oci.container_engine.models.VirtualNodeTags
        """
        return self._virtual_node_tags

    @virtual_node_tags.setter
    def virtual_node_tags(self, virtual_node_tags):
        """
        Sets the virtual_node_tags of this VirtualNodePool.

        :param virtual_node_tags: The virtual_node_tags of this VirtualNodePool.
        :type: oci.container_engine.models.VirtualNodeTags
        """
        self._virtual_node_tags = virtual_node_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
