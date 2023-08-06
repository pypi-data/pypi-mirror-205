# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class NetworkSecurityGroup(object):
    """
    A *network security group* (NSG) provides virtual firewall rules for a specific set of
    :class:`Vnic` in a VCN. Compare NSGs with :class:`SecurityList`,
    which provide virtual firewall rules to all the VNICs in a *subnet*.

    A network security group consists of two items:

    * The set of :class:`Vnic` that all have the same security rule needs (for
    example, a group of Compute instances all running the same application)
    * A set of NSG :class:`SecurityRule` that apply to the VNICs in the group

    After creating an NSG, you can add VNICs and security rules to it. For example, when you create
    an instance, you can specify one or more NSGs to add the instance to (see
    :func:`create_vnic_details`). Or you can add an existing
    instance to an NSG with :func:`update_vnic`.

    To add security rules to an NSG, see
    :func:`add_network_security_group_security_rules`.

    To list the VNICs in an NSG, see
    :func:`list_network_security_group_vnics`.

    To list the security rules in an NSG, see
    :func:`list_network_security_group_security_rules`.

    For more information about network security groups, see
    `Network Security Groups`__.

    **Important:** Oracle Cloud Infrastructure Compute service images automatically include firewall rules (for example,
    Linux iptables, Windows firewall). If there are issues with some type of access to an instance,
    make sure all of the following are set correctly:

    * Any security rules in any NSGs the instance's VNIC belongs to
    * Any :class:`SecurityList` associated with the instance's subnet
    * The instance's OS firewall rules

    To use any of the API operations, you must be authorized in an IAM policy. If you're not authorized,
    talk to an administrator. If you're an administrator who needs to write policies to give users access, see
    `Getting Started with Policies`__.

    __ https://docs.cloud.oracle.com/iaas/Content/Network/Concepts/networksecuritygroups.htm
    __ https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policygetstarted.htm
    """

    #: A constant which can be used with the lifecycle_state property of a NetworkSecurityGroup.
    #: This constant has a value of "PROVISIONING"
    LIFECYCLE_STATE_PROVISIONING = "PROVISIONING"

    #: A constant which can be used with the lifecycle_state property of a NetworkSecurityGroup.
    #: This constant has a value of "AVAILABLE"
    LIFECYCLE_STATE_AVAILABLE = "AVAILABLE"

    #: A constant which can be used with the lifecycle_state property of a NetworkSecurityGroup.
    #: This constant has a value of "TERMINATING"
    LIFECYCLE_STATE_TERMINATING = "TERMINATING"

    #: A constant which can be used with the lifecycle_state property of a NetworkSecurityGroup.
    #: This constant has a value of "TERMINATED"
    LIFECYCLE_STATE_TERMINATED = "TERMINATED"

    def __init__(self, **kwargs):
        """
        Initializes a new NetworkSecurityGroup object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this NetworkSecurityGroup.
        :type compartment_id: str

        :param defined_tags:
            The value to assign to the defined_tags property of this NetworkSecurityGroup.
        :type defined_tags: dict(str, dict(str, object))

        :param display_name:
            The value to assign to the display_name property of this NetworkSecurityGroup.
        :type display_name: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this NetworkSecurityGroup.
        :type freeform_tags: dict(str, str)

        :param id:
            The value to assign to the id property of this NetworkSecurityGroup.
        :type id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this NetworkSecurityGroup.
            Allowed values for this property are: "PROVISIONING", "AVAILABLE", "TERMINATING", "TERMINATED"
        :type lifecycle_state: str

        :param time_created:
            The value to assign to the time_created property of this NetworkSecurityGroup.
        :type time_created: datetime

        :param vcn_id:
            The value to assign to the vcn_id property of this NetworkSecurityGroup.
        :type vcn_id: str

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'defined_tags': 'dict(str, dict(str, object))',
            'display_name': 'str',
            'freeform_tags': 'dict(str, str)',
            'id': 'str',
            'lifecycle_state': 'str',
            'time_created': 'datetime',
            'vcn_id': 'str'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'defined_tags': 'definedTags',
            'display_name': 'displayName',
            'freeform_tags': 'freeformTags',
            'id': 'id',
            'lifecycle_state': 'lifecycleState',
            'time_created': 'timeCreated',
            'vcn_id': 'vcnId'
        }

        self._compartment_id = None
        self._defined_tags = None
        self._display_name = None
        self._freeform_tags = None
        self._id = None
        self._lifecycle_state = None
        self._time_created = None
        self._vcn_id = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this NetworkSecurityGroup.
        The `OCID`__ of the compartment the network security group is in.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this NetworkSecurityGroup.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this NetworkSecurityGroup.
        The `OCID`__ of the compartment the network security group is in.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this NetworkSecurityGroup.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this NetworkSecurityGroup.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this NetworkSecurityGroup.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this NetworkSecurityGroup.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this NetworkSecurityGroup.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def display_name(self):
        """
        Gets the display_name of this NetworkSecurityGroup.
        A user-friendly name. Does not have to be unique, and it's changeable.
        Avoid entering confidential information.


        :return: The display_name of this NetworkSecurityGroup.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this NetworkSecurityGroup.
        A user-friendly name. Does not have to be unique, and it's changeable.
        Avoid entering confidential information.


        :param display_name: The display_name of this NetworkSecurityGroup.
        :type: str
        """
        self._display_name = display_name

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this NetworkSecurityGroup.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this NetworkSecurityGroup.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this NetworkSecurityGroup.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this NetworkSecurityGroup.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def id(self):
        """
        **[Required]** Gets the id of this NetworkSecurityGroup.
        The `OCID`__ of the network security group.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The id of this NetworkSecurityGroup.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this NetworkSecurityGroup.
        The `OCID`__ of the network security group.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param id: The id of this NetworkSecurityGroup.
        :type: str
        """
        self._id = id

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this NetworkSecurityGroup.
        The network security group's current state.

        Allowed values for this property are: "PROVISIONING", "AVAILABLE", "TERMINATING", "TERMINATED"


        :return: The lifecycle_state of this NetworkSecurityGroup.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this NetworkSecurityGroup.
        The network security group's current state.


        :param lifecycle_state: The lifecycle_state of this NetworkSecurityGroup.
        :type: str
        """
        allowed_values = ["PROVISIONING", "AVAILABLE", "TERMINATING", "TERMINATED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            raise ValueError(
                "Invalid value for `lifecycle_state`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._lifecycle_state = lifecycle_state

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this NetworkSecurityGroup.
        The date and time the network security group was created, in the format defined by `RFC3339`__.

        Example: `2016-08-25T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :return: The time_created of this NetworkSecurityGroup.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this NetworkSecurityGroup.
        The date and time the network security group was created, in the format defined by `RFC3339`__.

        Example: `2016-08-25T21:10:29.600Z`

        __ https://tools.ietf.org/html/rfc3339


        :param time_created: The time_created of this NetworkSecurityGroup.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def vcn_id(self):
        """
        **[Required]** Gets the vcn_id of this NetworkSecurityGroup.
        The `OCID`__ of the network security group's VCN.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The vcn_id of this NetworkSecurityGroup.
        :rtype: str
        """
        return self._vcn_id

    @vcn_id.setter
    def vcn_id(self, vcn_id):
        """
        Sets the vcn_id of this NetworkSecurityGroup.
        The `OCID`__ of the network security group's VCN.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param vcn_id: The vcn_id of this NetworkSecurityGroup.
        :type: str
        """
        self._vcn_id = vcn_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
