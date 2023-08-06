# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PlacementConfiguration(object):
    """
    The information of virtual node placement in the virtual node pool.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PlacementConfiguration object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param availability_domain:
            The value to assign to the availability_domain property of this PlacementConfiguration.
        :type availability_domain: str

        :param fault_domain:
            The value to assign to the fault_domain property of this PlacementConfiguration.
        :type fault_domain: list[str]

        :param subnet_id:
            The value to assign to the subnet_id property of this PlacementConfiguration.
        :type subnet_id: str

        """
        self.swagger_types = {
            'availability_domain': 'str',
            'fault_domain': 'list[str]',
            'subnet_id': 'str'
        }

        self.attribute_map = {
            'availability_domain': 'availabilityDomain',
            'fault_domain': 'faultDomain',
            'subnet_id': 'subnetId'
        }

        self._availability_domain = None
        self._fault_domain = None
        self._subnet_id = None

    @property
    def availability_domain(self):
        """
        Gets the availability_domain of this PlacementConfiguration.
        The availability domain in which to place virtual nodes.
        Example: `Uocm:PHX-AD-1`


        :return: The availability_domain of this PlacementConfiguration.
        :rtype: str
        """
        return self._availability_domain

    @availability_domain.setter
    def availability_domain(self, availability_domain):
        """
        Sets the availability_domain of this PlacementConfiguration.
        The availability domain in which to place virtual nodes.
        Example: `Uocm:PHX-AD-1`


        :param availability_domain: The availability_domain of this PlacementConfiguration.
        :type: str
        """
        self._availability_domain = availability_domain

    @property
    def fault_domain(self):
        """
        Gets the fault_domain of this PlacementConfiguration.
        The fault domain of this virtual node.


        :return: The fault_domain of this PlacementConfiguration.
        :rtype: list[str]
        """
        return self._fault_domain

    @fault_domain.setter
    def fault_domain(self, fault_domain):
        """
        Sets the fault_domain of this PlacementConfiguration.
        The fault domain of this virtual node.


        :param fault_domain: The fault_domain of this PlacementConfiguration.
        :type: list[str]
        """
        self._fault_domain = fault_domain

    @property
    def subnet_id(self):
        """
        Gets the subnet_id of this PlacementConfiguration.
        The OCID of the subnet in which to place virtual nodes.


        :return: The subnet_id of this PlacementConfiguration.
        :rtype: str
        """
        return self._subnet_id

    @subnet_id.setter
    def subnet_id(self, subnet_id):
        """
        Sets the subnet_id of this PlacementConfiguration.
        The OCID of the subnet in which to place virtual nodes.


        :param subnet_id: The subnet_id of this PlacementConfiguration.
        :type: str
        """
        self._subnet_id = subnet_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
