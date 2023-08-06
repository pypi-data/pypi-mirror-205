# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateContainerVnicDetails(object):
    """
    Create a Virtual Network Interface Card (VNIC) which gives
    Containers on this Container Instance access to a Virtual Client Network (VCN).

    This VNIC will be created in the same compartment as the specified subnet on
    behalf of the customer.

    The VNIC created by this call will contain both the tags specified
    in this object as well as any tags specified in the parent ContainerInstance object.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateContainerVnicDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this CreateContainerVnicDetails.
        :type display_name: str

        :param hostname_label:
            The value to assign to the hostname_label property of this CreateContainerVnicDetails.
        :type hostname_label: str

        :param is_public_ip_assigned:
            The value to assign to the is_public_ip_assigned property of this CreateContainerVnicDetails.
        :type is_public_ip_assigned: bool

        :param skip_source_dest_check:
            The value to assign to the skip_source_dest_check property of this CreateContainerVnicDetails.
        :type skip_source_dest_check: bool

        :param nsg_ids:
            The value to assign to the nsg_ids property of this CreateContainerVnicDetails.
        :type nsg_ids: list[str]

        :param private_ip:
            The value to assign to the private_ip property of this CreateContainerVnicDetails.
        :type private_ip: str

        :param subnet_id:
            The value to assign to the subnet_id property of this CreateContainerVnicDetails.
        :type subnet_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateContainerVnicDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateContainerVnicDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'display_name': 'str',
            'hostname_label': 'str',
            'is_public_ip_assigned': 'bool',
            'skip_source_dest_check': 'bool',
            'nsg_ids': 'list[str]',
            'private_ip': 'str',
            'subnet_id': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'hostname_label': 'hostnameLabel',
            'is_public_ip_assigned': 'isPublicIpAssigned',
            'skip_source_dest_check': 'skipSourceDestCheck',
            'nsg_ids': 'nsgIds',
            'private_ip': 'privateIp',
            'subnet_id': 'subnetId',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._display_name = None
        self._hostname_label = None
        self._is_public_ip_assigned = None
        self._skip_source_dest_check = None
        self._nsg_ids = None
        self._private_ip = None
        self._subnet_id = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def display_name(self):
        """
        Gets the display_name of this CreateContainerVnicDetails.
        A user-friendly name for the VNIC. Does not have to be unique.
        Avoid entering confidential information.


        :return: The display_name of this CreateContainerVnicDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateContainerVnicDetails.
        A user-friendly name for the VNIC. Does not have to be unique.
        Avoid entering confidential information.


        :param display_name: The display_name of this CreateContainerVnicDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def hostname_label(self):
        """
        Gets the hostname_label of this CreateContainerVnicDetails.
        The hostname for the VNIC's primary private IP.


        :return: The hostname_label of this CreateContainerVnicDetails.
        :rtype: str
        """
        return self._hostname_label

    @hostname_label.setter
    def hostname_label(self, hostname_label):
        """
        Sets the hostname_label of this CreateContainerVnicDetails.
        The hostname for the VNIC's primary private IP.


        :param hostname_label: The hostname_label of this CreateContainerVnicDetails.
        :type: str
        """
        self._hostname_label = hostname_label

    @property
    def is_public_ip_assigned(self):
        """
        Gets the is_public_ip_assigned of this CreateContainerVnicDetails.
        Whether the VNIC should be assigned a public IP address.


        :return: The is_public_ip_assigned of this CreateContainerVnicDetails.
        :rtype: bool
        """
        return self._is_public_ip_assigned

    @is_public_ip_assigned.setter
    def is_public_ip_assigned(self, is_public_ip_assigned):
        """
        Sets the is_public_ip_assigned of this CreateContainerVnicDetails.
        Whether the VNIC should be assigned a public IP address.


        :param is_public_ip_assigned: The is_public_ip_assigned of this CreateContainerVnicDetails.
        :type: bool
        """
        self._is_public_ip_assigned = is_public_ip_assigned

    @property
    def skip_source_dest_check(self):
        """
        Gets the skip_source_dest_check of this CreateContainerVnicDetails.
        Whether the source/destination check is disabled on the VNIC.


        :return: The skip_source_dest_check of this CreateContainerVnicDetails.
        :rtype: bool
        """
        return self._skip_source_dest_check

    @skip_source_dest_check.setter
    def skip_source_dest_check(self, skip_source_dest_check):
        """
        Sets the skip_source_dest_check of this CreateContainerVnicDetails.
        Whether the source/destination check is disabled on the VNIC.


        :param skip_source_dest_check: The skip_source_dest_check of this CreateContainerVnicDetails.
        :type: bool
        """
        self._skip_source_dest_check = skip_source_dest_check

    @property
    def nsg_ids(self):
        """
        Gets the nsg_ids of this CreateContainerVnicDetails.
        A list of the OCIDs of the network security groups (NSGs) to add the VNIC to.


        :return: The nsg_ids of this CreateContainerVnicDetails.
        :rtype: list[str]
        """
        return self._nsg_ids

    @nsg_ids.setter
    def nsg_ids(self, nsg_ids):
        """
        Sets the nsg_ids of this CreateContainerVnicDetails.
        A list of the OCIDs of the network security groups (NSGs) to add the VNIC to.


        :param nsg_ids: The nsg_ids of this CreateContainerVnicDetails.
        :type: list[str]
        """
        self._nsg_ids = nsg_ids

    @property
    def private_ip(self):
        """
        Gets the private_ip of this CreateContainerVnicDetails.
        A private IP address of your choice to assign to the VNIC. Must be an
        available IP address within the subnet's CIDR.


        :return: The private_ip of this CreateContainerVnicDetails.
        :rtype: str
        """
        return self._private_ip

    @private_ip.setter
    def private_ip(self, private_ip):
        """
        Sets the private_ip of this CreateContainerVnicDetails.
        A private IP address of your choice to assign to the VNIC. Must be an
        available IP address within the subnet's CIDR.


        :param private_ip: The private_ip of this CreateContainerVnicDetails.
        :type: str
        """
        self._private_ip = private_ip

    @property
    def subnet_id(self):
        """
        **[Required]** Gets the subnet_id of this CreateContainerVnicDetails.
        The OCID of the subnet to create the VNIC in.


        :return: The subnet_id of this CreateContainerVnicDetails.
        :rtype: str
        """
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet_id):
        """
        Sets the subnet_id of this CreateContainerVnicDetails.
        The OCID of the subnet to create the VNIC in.


        :param subnet_id: The subnet_id of this CreateContainerVnicDetails.
        :type: str
        """
        self._subnet_id = subnet_id

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateContainerVnicDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this CreateContainerVnicDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateContainerVnicDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this CreateContainerVnicDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateContainerVnicDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this CreateContainerVnicDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateContainerVnicDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this CreateContainerVnicDetails.
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
