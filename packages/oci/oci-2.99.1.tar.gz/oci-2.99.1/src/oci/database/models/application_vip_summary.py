# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ApplicationVipSummary(object):
    """
    Details of an application virtual IP (VIP) address.
    """

    #: A constant which can be used with the lifecycle_state property of a ApplicationVipSummary.
    #: This constant has a value of "PROVISIONING"
    LIFECYCLE_STATE_PROVISIONING = "PROVISIONING"

    #: A constant which can be used with the lifecycle_state property of a ApplicationVipSummary.
    #: This constant has a value of "AVAILABLE"
    LIFECYCLE_STATE_AVAILABLE = "AVAILABLE"

    #: A constant which can be used with the lifecycle_state property of a ApplicationVipSummary.
    #: This constant has a value of "TERMINATING"
    LIFECYCLE_STATE_TERMINATING = "TERMINATING"

    #: A constant which can be used with the lifecycle_state property of a ApplicationVipSummary.
    #: This constant has a value of "TERMINATED"
    LIFECYCLE_STATE_TERMINATED = "TERMINATED"

    #: A constant which can be used with the lifecycle_state property of a ApplicationVipSummary.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new ApplicationVipSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ApplicationVipSummary.
        :type id: str

        :param cloud_vm_cluster_id:
            The value to assign to the cloud_vm_cluster_id property of this ApplicationVipSummary.
        :type cloud_vm_cluster_id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ApplicationVipSummary.
        :type compartment_id: str

        :param subnet_id:
            The value to assign to the subnet_id property of this ApplicationVipSummary.
        :type subnet_id: str

        :param ip_address:
            The value to assign to the ip_address property of this ApplicationVipSummary.
        :type ip_address: str

        :param hostname_label:
            The value to assign to the hostname_label property of this ApplicationVipSummary.
        :type hostname_label: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ApplicationVipSummary.
            Allowed values for this property are: "PROVISIONING", "AVAILABLE", "TERMINATING", "TERMINATED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this ApplicationVipSummary.
        :type lifecycle_details: str

        :param time_assigned:
            The value to assign to the time_assigned property of this ApplicationVipSummary.
        :type time_assigned: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this ApplicationVipSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this ApplicationVipSummary.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'cloud_vm_cluster_id': 'str',
            'compartment_id': 'str',
            'subnet_id': 'str',
            'ip_address': 'str',
            'hostname_label': 'str',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'time_assigned': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'cloud_vm_cluster_id': 'cloudVmClusterId',
            'compartment_id': 'compartmentId',
            'subnet_id': 'subnetId',
            'ip_address': 'ipAddress',
            'hostname_label': 'hostnameLabel',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'time_assigned': 'timeAssigned',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._id = None
        self._cloud_vm_cluster_id = None
        self._compartment_id = None
        self._subnet_id = None
        self._ip_address = None
        self._hostname_label = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._time_assigned = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ApplicationVipSummary.
        The `OCID`__ of the application virtual IP (VIP) address.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ApplicationVipSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ApplicationVipSummary.
        The `OCID`__ of the application virtual IP (VIP) address.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ApplicationVipSummary.
        :type: str
        """
        self._id = id

    @property
    def cloud_vm_cluster_id(self):
        """
        **[Required]** Gets the cloud_vm_cluster_id of this ApplicationVipSummary.
        The `OCID`__ of the cloud VM cluster associated with the application virtual IP (VIP) address.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The cloud_vm_cluster_id of this ApplicationVipSummary.
        :rtype: str
        """
        return self._cloud_vm_cluster_id

    @cloud_vm_cluster_id.setter
    def cloud_vm_cluster_id(self, cloud_vm_cluster_id):
        """
        Sets the cloud_vm_cluster_id of this ApplicationVipSummary.
        The `OCID`__ of the cloud VM cluster associated with the application virtual IP (VIP) address.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param cloud_vm_cluster_id: The cloud_vm_cluster_id of this ApplicationVipSummary.
        :type: str
        """
        self._cloud_vm_cluster_id = cloud_vm_cluster_id

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this ApplicationVipSummary.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ApplicationVipSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ApplicationVipSummary.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ApplicationVipSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def subnet_id(self):
        """
        Gets the subnet_id of this ApplicationVipSummary.
        The `OCID`__ of the subnet associated with the application virtual IP (VIP) address.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The subnet_id of this ApplicationVipSummary.
        :rtype: str
        """
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet_id):
        """
        Sets the subnet_id of this ApplicationVipSummary.
        The `OCID`__ of the subnet associated with the application virtual IP (VIP) address.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param subnet_id: The subnet_id of this ApplicationVipSummary.
        :type: str
        """
        self._subnet_id = subnet_id

    @property
    def ip_address(self):
        """
        Gets the ip_address of this ApplicationVipSummary.
        The application virtual IP (VIP) address.


        :return: The ip_address of this ApplicationVipSummary.
        :rtype: str
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        """
        Sets the ip_address of this ApplicationVipSummary.
        The application virtual IP (VIP) address.


        :param ip_address: The ip_address of this ApplicationVipSummary.
        :type: str
        """
        self._ip_address = ip_address

    @property
    def hostname_label(self):
        """
        **[Required]** Gets the hostname_label of this ApplicationVipSummary.
        The hostname of the application virtual IP (VIP) address.


        :return: The hostname_label of this ApplicationVipSummary.
        :rtype: str
        """
        return self._hostname_label

    @hostname_label.setter
    def hostname_label(self, hostname_label):
        """
        Sets the hostname_label of this ApplicationVipSummary.
        The hostname of the application virtual IP (VIP) address.


        :param hostname_label: The hostname_label of this ApplicationVipSummary.
        :type: str
        """
        self._hostname_label = hostname_label

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ApplicationVipSummary.
        The current lifecycle state of the application virtual IP (VIP) address.

        Allowed values for this property are: "PROVISIONING", "AVAILABLE", "TERMINATING", "TERMINATED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ApplicationVipSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ApplicationVipSummary.
        The current lifecycle state of the application virtual IP (VIP) address.


        :param lifecycle_state: The lifecycle_state of this ApplicationVipSummary.
        :type: str
        """
        allowed_values = ["PROVISIONING", "AVAILABLE", "TERMINATING", "TERMINATED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this ApplicationVipSummary.
        Additional information about the current lifecycle state of the application virtual IP (VIP) address.


        :return: The lifecycle_details of this ApplicationVipSummary.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this ApplicationVipSummary.
        Additional information about the current lifecycle state of the application virtual IP (VIP) address.


        :param lifecycle_details: The lifecycle_details of this ApplicationVipSummary.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def time_assigned(self):
        """
        **[Required]** Gets the time_assigned of this ApplicationVipSummary.
        The date and time when the create operation for the application virtual IP (VIP) address completed.


        :return: The time_assigned of this ApplicationVipSummary.
        :rtype: datetime
        """
        return self._time_assigned

    @time_assigned.setter
    def time_assigned(self, time_assigned):
        """
        Sets the time_assigned of this ApplicationVipSummary.
        The date and time when the create operation for the application virtual IP (VIP) address completed.


        :param time_assigned: The time_assigned of this ApplicationVipSummary.
        :type: datetime
        """
        self._time_assigned = time_assigned

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this ApplicationVipSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this ApplicationVipSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this ApplicationVipSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this ApplicationVipSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this ApplicationVipSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this ApplicationVipSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this ApplicationVipSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this ApplicationVipSummary.
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
