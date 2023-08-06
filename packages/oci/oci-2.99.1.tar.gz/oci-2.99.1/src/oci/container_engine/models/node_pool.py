# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class NodePool(object):
    """
    A pool of compute nodes attached to a cluster. Avoid entering confidential information.
    """

    #: A constant which can be used with the lifecycle_state property of a NodePool.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a NodePool.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a NodePool.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a NodePool.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a NodePool.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a NodePool.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a NodePool.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a NodePool.
    #: This constant has a value of "NEEDS_ATTENTION"
    LIFECYCLE_STATE_NEEDS_ATTENTION = "NEEDS_ATTENTION"

    def __init__(self, **kwargs):
        """
        Initializes a new NodePool object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this NodePool.
        :type id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this NodePool.
            Allowed values for this property are: "DELETED", "CREATING", "ACTIVE", "UPDATING", "DELETING", "FAILED", "INACTIVE", "NEEDS_ATTENTION", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this NodePool.
        :type lifecycle_details: str

        :param compartment_id:
            The value to assign to the compartment_id property of this NodePool.
        :type compartment_id: str

        :param cluster_id:
            The value to assign to the cluster_id property of this NodePool.
        :type cluster_id: str

        :param name:
            The value to assign to the name property of this NodePool.
        :type name: str

        :param kubernetes_version:
            The value to assign to the kubernetes_version property of this NodePool.
        :type kubernetes_version: str

        :param node_metadata:
            The value to assign to the node_metadata property of this NodePool.
        :type node_metadata: dict(str, str)

        :param node_image_id:
            The value to assign to the node_image_id property of this NodePool.
        :type node_image_id: str

        :param node_image_name:
            The value to assign to the node_image_name property of this NodePool.
        :type node_image_name: str

        :param node_shape_config:
            The value to assign to the node_shape_config property of this NodePool.
        :type node_shape_config: oci.container_engine.models.NodeShapeConfig

        :param node_source:
            The value to assign to the node_source property of this NodePool.
        :type node_source: oci.container_engine.models.NodeSourceOption

        :param node_source_details:
            The value to assign to the node_source_details property of this NodePool.
        :type node_source_details: oci.container_engine.models.NodeSourceDetails

        :param node_shape:
            The value to assign to the node_shape property of this NodePool.
        :type node_shape: str

        :param initial_node_labels:
            The value to assign to the initial_node_labels property of this NodePool.
        :type initial_node_labels: list[oci.container_engine.models.KeyValue]

        :param ssh_public_key:
            The value to assign to the ssh_public_key property of this NodePool.
        :type ssh_public_key: str

        :param quantity_per_subnet:
            The value to assign to the quantity_per_subnet property of this NodePool.
        :type quantity_per_subnet: int

        :param subnet_ids:
            The value to assign to the subnet_ids property of this NodePool.
        :type subnet_ids: list[str]

        :param nodes:
            The value to assign to the nodes property of this NodePool.
        :type nodes: list[oci.container_engine.models.Node]

        :param node_config_details:
            The value to assign to the node_config_details property of this NodePool.
        :type node_config_details: oci.container_engine.models.NodePoolNodeConfigDetails

        :param freeform_tags:
            The value to assign to the freeform_tags property of this NodePool.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this NodePool.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this NodePool.
        :type system_tags: dict(str, dict(str, object))

        :param node_eviction_node_pool_settings:
            The value to assign to the node_eviction_node_pool_settings property of this NodePool.
        :type node_eviction_node_pool_settings: oci.container_engine.models.NodeEvictionNodePoolSettings

        """
        self.swagger_types = {
            'id': 'str',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'compartment_id': 'str',
            'cluster_id': 'str',
            'name': 'str',
            'kubernetes_version': 'str',
            'node_metadata': 'dict(str, str)',
            'node_image_id': 'str',
            'node_image_name': 'str',
            'node_shape_config': 'NodeShapeConfig',
            'node_source': 'NodeSourceOption',
            'node_source_details': 'NodeSourceDetails',
            'node_shape': 'str',
            'initial_node_labels': 'list[KeyValue]',
            'ssh_public_key': 'str',
            'quantity_per_subnet': 'int',
            'subnet_ids': 'list[str]',
            'nodes': 'list[Node]',
            'node_config_details': 'NodePoolNodeConfigDetails',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'node_eviction_node_pool_settings': 'NodeEvictionNodePoolSettings'
        }

        self.attribute_map = {
            'id': 'id',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'compartment_id': 'compartmentId',
            'cluster_id': 'clusterId',
            'name': 'name',
            'kubernetes_version': 'kubernetesVersion',
            'node_metadata': 'nodeMetadata',
            'node_image_id': 'nodeImageId',
            'node_image_name': 'nodeImageName',
            'node_shape_config': 'nodeShapeConfig',
            'node_source': 'nodeSource',
            'node_source_details': 'nodeSourceDetails',
            'node_shape': 'nodeShape',
            'initial_node_labels': 'initialNodeLabels',
            'ssh_public_key': 'sshPublicKey',
            'quantity_per_subnet': 'quantityPerSubnet',
            'subnet_ids': 'subnetIds',
            'nodes': 'nodes',
            'node_config_details': 'nodeConfigDetails',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'node_eviction_node_pool_settings': 'nodeEvictionNodePoolSettings'
        }

        self._id = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._compartment_id = None
        self._cluster_id = None
        self._name = None
        self._kubernetes_version = None
        self._node_metadata = None
        self._node_image_id = None
        self._node_image_name = None
        self._node_shape_config = None
        self._node_source = None
        self._node_source_details = None
        self._node_shape = None
        self._initial_node_labels = None
        self._ssh_public_key = None
        self._quantity_per_subnet = None
        self._subnet_ids = None
        self._nodes = None
        self._node_config_details = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._node_eviction_node_pool_settings = None

    @property
    def id(self):
        """
        Gets the id of this NodePool.
        The OCID of the node pool.


        :return: The id of this NodePool.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this NodePool.
        The OCID of the node pool.


        :param id: The id of this NodePool.
        :type: str
        """
        self._id = id

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this NodePool.
        The state of the nodepool.

        Allowed values for this property are: "DELETED", "CREATING", "ACTIVE", "UPDATING", "DELETING", "FAILED", "INACTIVE", "NEEDS_ATTENTION", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this NodePool.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this NodePool.
        The state of the nodepool.


        :param lifecycle_state: The lifecycle_state of this NodePool.
        :type: str
        """
        allowed_values = ["DELETED", "CREATING", "ACTIVE", "UPDATING", "DELETING", "FAILED", "INACTIVE", "NEEDS_ATTENTION"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this NodePool.
        Details about the state of the nodepool.


        :return: The lifecycle_details of this NodePool.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this NodePool.
        Details about the state of the nodepool.


        :param lifecycle_details: The lifecycle_details of this NodePool.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this NodePool.
        The OCID of the compartment in which the node pool exists.


        :return: The compartment_id of this NodePool.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this NodePool.
        The OCID of the compartment in which the node pool exists.


        :param compartment_id: The compartment_id of this NodePool.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def cluster_id(self):
        """
        Gets the cluster_id of this NodePool.
        The OCID of the cluster to which this node pool is attached.


        :return: The cluster_id of this NodePool.
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """
        Sets the cluster_id of this NodePool.
        The OCID of the cluster to which this node pool is attached.


        :param cluster_id: The cluster_id of this NodePool.
        :type: str
        """
        self._cluster_id = cluster_id

    @property
    def name(self):
        """
        Gets the name of this NodePool.
        The name of the node pool.


        :return: The name of this NodePool.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this NodePool.
        The name of the node pool.


        :param name: The name of this NodePool.
        :type: str
        """
        self._name = name

    @property
    def kubernetes_version(self):
        """
        Gets the kubernetes_version of this NodePool.
        The version of Kubernetes running on the nodes in the node pool.


        :return: The kubernetes_version of this NodePool.
        :rtype: str
        """
        return self._kubernetes_version

    @kubernetes_version.setter
    def kubernetes_version(self, kubernetes_version):
        """
        Sets the kubernetes_version of this NodePool.
        The version of Kubernetes running on the nodes in the node pool.


        :param kubernetes_version: The kubernetes_version of this NodePool.
        :type: str
        """
        self._kubernetes_version = kubernetes_version

    @property
    def node_metadata(self):
        """
        Gets the node_metadata of this NodePool.
        A list of key/value pairs to add to each underlying OCI instance in the node pool on launch.


        :return: The node_metadata of this NodePool.
        :rtype: dict(str, str)
        """
        return self._node_metadata

    @node_metadata.setter
    def node_metadata(self, node_metadata):
        """
        Sets the node_metadata of this NodePool.
        A list of key/value pairs to add to each underlying OCI instance in the node pool on launch.


        :param node_metadata: The node_metadata of this NodePool.
        :type: dict(str, str)
        """
        self._node_metadata = node_metadata

    @property
    def node_image_id(self):
        """
        Gets the node_image_id of this NodePool.
        Deprecated. see `nodeSource`. The OCID of the image running on the nodes in the node pool.


        :return: The node_image_id of this NodePool.
        :rtype: str
        """
        return self._node_image_id

    @node_image_id.setter
    def node_image_id(self, node_image_id):
        """
        Sets the node_image_id of this NodePool.
        Deprecated. see `nodeSource`. The OCID of the image running on the nodes in the node pool.


        :param node_image_id: The node_image_id of this NodePool.
        :type: str
        """
        self._node_image_id = node_image_id

    @property
    def node_image_name(self):
        """
        Gets the node_image_name of this NodePool.
        Deprecated. see `nodeSource`. The name of the image running on the nodes in the node pool.


        :return: The node_image_name of this NodePool.
        :rtype: str
        """
        return self._node_image_name

    @node_image_name.setter
    def node_image_name(self, node_image_name):
        """
        Sets the node_image_name of this NodePool.
        Deprecated. see `nodeSource`. The name of the image running on the nodes in the node pool.


        :param node_image_name: The node_image_name of this NodePool.
        :type: str
        """
        self._node_image_name = node_image_name

    @property
    def node_shape_config(self):
        """
        Gets the node_shape_config of this NodePool.
        The shape configuration of the nodes.


        :return: The node_shape_config of this NodePool.
        :rtype: oci.container_engine.models.NodeShapeConfig
        """
        return self._node_shape_config

    @node_shape_config.setter
    def node_shape_config(self, node_shape_config):
        """
        Sets the node_shape_config of this NodePool.
        The shape configuration of the nodes.


        :param node_shape_config: The node_shape_config of this NodePool.
        :type: oci.container_engine.models.NodeShapeConfig
        """
        self._node_shape_config = node_shape_config

    @property
    def node_source(self):
        """
        Gets the node_source of this NodePool.
        Deprecated. see `nodeSourceDetails`. Source running on the nodes in the node pool.


        :return: The node_source of this NodePool.
        :rtype: oci.container_engine.models.NodeSourceOption
        """
        return self._node_source

    @node_source.setter
    def node_source(self, node_source):
        """
        Sets the node_source of this NodePool.
        Deprecated. see `nodeSourceDetails`. Source running on the nodes in the node pool.


        :param node_source: The node_source of this NodePool.
        :type: oci.container_engine.models.NodeSourceOption
        """
        self._node_source = node_source

    @property
    def node_source_details(self):
        """
        Gets the node_source_details of this NodePool.
        Source running on the nodes in the node pool.


        :return: The node_source_details of this NodePool.
        :rtype: oci.container_engine.models.NodeSourceDetails
        """
        return self._node_source_details

    @node_source_details.setter
    def node_source_details(self, node_source_details):
        """
        Sets the node_source_details of this NodePool.
        Source running on the nodes in the node pool.


        :param node_source_details: The node_source_details of this NodePool.
        :type: oci.container_engine.models.NodeSourceDetails
        """
        self._node_source_details = node_source_details

    @property
    def node_shape(self):
        """
        Gets the node_shape of this NodePool.
        The name of the node shape of the nodes in the node pool.


        :return: The node_shape of this NodePool.
        :rtype: str
        """
        return self._node_shape

    @node_shape.setter
    def node_shape(self, node_shape):
        """
        Sets the node_shape of this NodePool.
        The name of the node shape of the nodes in the node pool.


        :param node_shape: The node_shape of this NodePool.
        :type: str
        """
        self._node_shape = node_shape

    @property
    def initial_node_labels(self):
        """
        Gets the initial_node_labels of this NodePool.
        A list of key/value pairs to add to nodes after they join the Kubernetes cluster.


        :return: The initial_node_labels of this NodePool.
        :rtype: list[oci.container_engine.models.KeyValue]
        """
        return self._initial_node_labels

    @initial_node_labels.setter
    def initial_node_labels(self, initial_node_labels):
        """
        Sets the initial_node_labels of this NodePool.
        A list of key/value pairs to add to nodes after they join the Kubernetes cluster.


        :param initial_node_labels: The initial_node_labels of this NodePool.
        :type: list[oci.container_engine.models.KeyValue]
        """
        self._initial_node_labels = initial_node_labels

    @property
    def ssh_public_key(self):
        """
        Gets the ssh_public_key of this NodePool.
        The SSH public key on each node in the node pool on launch.


        :return: The ssh_public_key of this NodePool.
        :rtype: str
        """
        return self._ssh_public_key

    @ssh_public_key.setter
    def ssh_public_key(self, ssh_public_key):
        """
        Sets the ssh_public_key of this NodePool.
        The SSH public key on each node in the node pool on launch.


        :param ssh_public_key: The ssh_public_key of this NodePool.
        :type: str
        """
        self._ssh_public_key = ssh_public_key

    @property
    def quantity_per_subnet(self):
        """
        Gets the quantity_per_subnet of this NodePool.
        The number of nodes in each subnet.


        :return: The quantity_per_subnet of this NodePool.
        :rtype: int
        """
        return self._quantity_per_subnet

    @quantity_per_subnet.setter
    def quantity_per_subnet(self, quantity_per_subnet):
        """
        Sets the quantity_per_subnet of this NodePool.
        The number of nodes in each subnet.


        :param quantity_per_subnet: The quantity_per_subnet of this NodePool.
        :type: int
        """
        self._quantity_per_subnet = quantity_per_subnet

    @property
    def subnet_ids(self):
        """
        Gets the subnet_ids of this NodePool.
        The OCIDs of the subnets in which to place nodes for this node pool.


        :return: The subnet_ids of this NodePool.
        :rtype: list[str]
        """
        return self._subnet_ids

    @subnet_ids.setter
    def subnet_ids(self, subnet_ids):
        """
        Sets the subnet_ids of this NodePool.
        The OCIDs of the subnets in which to place nodes for this node pool.


        :param subnet_ids: The subnet_ids of this NodePool.
        :type: list[str]
        """
        self._subnet_ids = subnet_ids

    @property
    def nodes(self):
        """
        Gets the nodes of this NodePool.
        The nodes in the node pool.


        :return: The nodes of this NodePool.
        :rtype: list[oci.container_engine.models.Node]
        """
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        """
        Sets the nodes of this NodePool.
        The nodes in the node pool.


        :param nodes: The nodes of this NodePool.
        :type: list[oci.container_engine.models.Node]
        """
        self._nodes = nodes

    @property
    def node_config_details(self):
        """
        Gets the node_config_details of this NodePool.
        The configuration of nodes in the node pool.


        :return: The node_config_details of this NodePool.
        :rtype: oci.container_engine.models.NodePoolNodeConfigDetails
        """
        return self._node_config_details

    @node_config_details.setter
    def node_config_details(self, node_config_details):
        """
        Sets the node_config_details of this NodePool.
        The configuration of nodes in the node pool.


        :param node_config_details: The node_config_details of this NodePool.
        :type: oci.container_engine.models.NodePoolNodeConfigDetails
        """
        self._node_config_details = node_config_details

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this NodePool.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this NodePool.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this NodePool.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this NodePool.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this NodePool.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this NodePool.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this NodePool.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this NodePool.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this NodePool.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this NodePool.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this NodePool.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this NodePool.
        :type: dict(str, dict(str, object))
        """
        self._system_tags = system_tags

    @property
    def node_eviction_node_pool_settings(self):
        """
        Gets the node_eviction_node_pool_settings of this NodePool.

        :return: The node_eviction_node_pool_settings of this NodePool.
        :rtype: oci.container_engine.models.NodeEvictionNodePoolSettings
        """
        return self._node_eviction_node_pool_settings

    @node_eviction_node_pool_settings.setter
    def node_eviction_node_pool_settings(self, node_eviction_node_pool_settings):
        """
        Sets the node_eviction_node_pool_settings of this NodePool.

        :param node_eviction_node_pool_settings: The node_eviction_node_pool_settings of this NodePool.
        :type: oci.container_engine.models.NodeEvictionNodePoolSettings
        """
        self._node_eviction_node_pool_settings = node_eviction_node_pool_settings

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
