# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Node(object):
    """
    The properties that define a node.
    """

    #: A constant which can be used with the lifecycle_state property of a Node.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a Node.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a Node.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a Node.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a Node.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a Node.
    #: This constant has a value of "FAILING"
    LIFECYCLE_STATE_FAILING = "FAILING"

    #: A constant which can be used with the lifecycle_state property of a Node.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    def __init__(self, **kwargs):
        """
        Initializes a new Node object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this Node.
        :type id: str

        :param name:
            The value to assign to the name property of this Node.
        :type name: str

        :param kubernetes_version:
            The value to assign to the kubernetes_version property of this Node.
        :type kubernetes_version: str

        :param availability_domain:
            The value to assign to the availability_domain property of this Node.
        :type availability_domain: str

        :param subnet_id:
            The value to assign to the subnet_id property of this Node.
        :type subnet_id: str

        :param node_pool_id:
            The value to assign to the node_pool_id property of this Node.
        :type node_pool_id: str

        :param fault_domain:
            The value to assign to the fault_domain property of this Node.
        :type fault_domain: str

        :param private_ip:
            The value to assign to the private_ip property of this Node.
        :type private_ip: str

        :param public_ip:
            The value to assign to the public_ip property of this Node.
        :type public_ip: str

        :param node_error:
            The value to assign to the node_error property of this Node.
        :type node_error: oci.container_engine.models.NodeError

        :param freeform_tags:
            The value to assign to the freeform_tags property of this Node.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this Node.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this Node.
        :type system_tags: dict(str, dict(str, object))

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this Node.
            Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILING", "INACTIVE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this Node.
        :type lifecycle_details: str

        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'kubernetes_version': 'str',
            'availability_domain': 'str',
            'subnet_id': 'str',
            'node_pool_id': 'str',
            'fault_domain': 'str',
            'private_ip': 'str',
            'public_ip': 'str',
            'node_error': 'NodeError',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'kubernetes_version': 'kubernetesVersion',
            'availability_domain': 'availabilityDomain',
            'subnet_id': 'subnetId',
            'node_pool_id': 'nodePoolId',
            'fault_domain': 'faultDomain',
            'private_ip': 'privateIp',
            'public_ip': 'publicIp',
            'node_error': 'nodeError',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails'
        }

        self._id = None
        self._name = None
        self._kubernetes_version = None
        self._availability_domain = None
        self._subnet_id = None
        self._node_pool_id = None
        self._fault_domain = None
        self._private_ip = None
        self._public_ip = None
        self._node_error = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._lifecycle_state = None
        self._lifecycle_details = None

    @property
    def id(self):
        """
        Gets the id of this Node.
        The OCID of the compute instance backing this node.


        :return: The id of this Node.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Node.
        The OCID of the compute instance backing this node.


        :param id: The id of this Node.
        :type: str
        """
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Node.
        The name of the node.


        :return: The name of this Node.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Node.
        The name of the node.


        :param name: The name of this Node.
        :type: str
        """
        self._name = name

    @property
    def kubernetes_version(self):
        """
        Gets the kubernetes_version of this Node.
        The version of Kubernetes this node is running.


        :return: The kubernetes_version of this Node.
        :rtype: str
        """
        return self._kubernetes_version

    @kubernetes_version.setter
    def kubernetes_version(self, kubernetes_version):
        """
        Sets the kubernetes_version of this Node.
        The version of Kubernetes this node is running.


        :param kubernetes_version: The kubernetes_version of this Node.
        :type: str
        """
        self._kubernetes_version = kubernetes_version

    @property
    def availability_domain(self):
        """
        Gets the availability_domain of this Node.
        The name of the availability domain in which this node is placed.


        :return: The availability_domain of this Node.
        :rtype: str
        """
        return self._availability_domain

    @availability_domain.setter
    def availability_domain(self, availability_domain):
        """
        Sets the availability_domain of this Node.
        The name of the availability domain in which this node is placed.


        :param availability_domain: The availability_domain of this Node.
        :type: str
        """
        self._availability_domain = availability_domain

    @property
    def subnet_id(self):
        """
        Gets the subnet_id of this Node.
        The OCID of the subnet in which this node is placed.


        :return: The subnet_id of this Node.
        :rtype: str
        """
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet_id):
        """
        Sets the subnet_id of this Node.
        The OCID of the subnet in which this node is placed.


        :param subnet_id: The subnet_id of this Node.
        :type: str
        """
        self._subnet_id = subnet_id

    @property
    def node_pool_id(self):
        """
        Gets the node_pool_id of this Node.
        The OCID of the node pool to which this node belongs.


        :return: The node_pool_id of this Node.
        :rtype: str
        """
        return self._node_pool_id

    @node_pool_id.setter
    def node_pool_id(self, node_pool_id):
        """
        Sets the node_pool_id of this Node.
        The OCID of the node pool to which this node belongs.


        :param node_pool_id: The node_pool_id of this Node.
        :type: str
        """
        self._node_pool_id = node_pool_id

    @property
    def fault_domain(self):
        """
        Gets the fault_domain of this Node.
        The fault domain of this node.


        :return: The fault_domain of this Node.
        :rtype: str
        """
        return self._fault_domain

    @fault_domain.setter
    def fault_domain(self, fault_domain):
        """
        Sets the fault_domain of this Node.
        The fault domain of this node.


        :param fault_domain: The fault_domain of this Node.
        :type: str
        """
        self._fault_domain = fault_domain

    @property
    def private_ip(self):
        """
        Gets the private_ip of this Node.
        The private IP address of this node.


        :return: The private_ip of this Node.
        :rtype: str
        """
        return self._private_ip

    @private_ip.setter
    def private_ip(self, private_ip):
        """
        Sets the private_ip of this Node.
        The private IP address of this node.


        :param private_ip: The private_ip of this Node.
        :type: str
        """
        self._private_ip = private_ip

    @property
    def public_ip(self):
        """
        Gets the public_ip of this Node.
        The public IP address of this node.


        :return: The public_ip of this Node.
        :rtype: str
        """
        return self._public_ip

    @public_ip.setter
    def public_ip(self, public_ip):
        """
        Sets the public_ip of this Node.
        The public IP address of this node.


        :param public_ip: The public_ip of this Node.
        :type: str
        """
        self._public_ip = public_ip

    @property
    def node_error(self):
        """
        Gets the node_error of this Node.
        An error that may be associated with the node.


        :return: The node_error of this Node.
        :rtype: oci.container_engine.models.NodeError
        """
        return self._node_error

    @node_error.setter
    def node_error(self, node_error):
        """
        Sets the node_error of this Node.
        An error that may be associated with the node.


        :param node_error: The node_error of this Node.
        :type: oci.container_engine.models.NodeError
        """
        self._node_error = node_error

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this Node.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this Node.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this Node.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this Node.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this Node.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this Node.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this Node.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this Node.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def system_tags(self):
        """
        Gets the system_tags of this Node.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :return: The system_tags of this Node.
        :rtype: dict(str, dict(str, object))
        """
        return self._system_tags

    @system_tags.setter
    def system_tags(self, system_tags):
        """
        Sets the system_tags of this Node.
        Usage of system tag keys. These predefined keys are scoped to namespaces.
        Example: `{\"orcl-cloud\": {\"free-tier-retained\": \"true\"}}`


        :param system_tags: The system_tags of this Node.
        :type: dict(str, dict(str, object))
        """
        self._system_tags = system_tags

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this Node.
        The state of the node.

        Allowed values for this property are: "CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILING", "INACTIVE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this Node.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this Node.
        The state of the node.


        :param lifecycle_state: The lifecycle_state of this Node.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "UPDATING", "DELETING", "DELETED", "FAILING", "INACTIVE"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this Node.
        Details about the state of the node.


        :return: The lifecycle_details of this Node.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this Node.
        Details about the state of the node.


        :param lifecycle_details: The lifecycle_details of this Node.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
