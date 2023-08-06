# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class RecoveryServiceSubnetInput(object):
    """
    Parameters to retrieve information about a specific recovery service subnet.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new RecoveryServiceSubnetInput object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param recovery_service_subnet_id:
            The value to assign to the recovery_service_subnet_id property of this RecoveryServiceSubnetInput.
        :type recovery_service_subnet_id: str

        """
        self.swagger_types = {
            'recovery_service_subnet_id': 'str'
        }

        self.attribute_map = {
            'recovery_service_subnet_id': 'recoveryServiceSubnetId'
        }

        self._recovery_service_subnet_id = None

    @property
    def recovery_service_subnet_id(self):
        """
        **[Required]** Gets the recovery_service_subnet_id of this RecoveryServiceSubnetInput.
        The recovery service subnet OCID.


        :return: The recovery_service_subnet_id of this RecoveryServiceSubnetInput.
        :rtype: str
        """
        return self._recovery_service_subnet_id

    @recovery_service_subnet_id.setter
    def recovery_service_subnet_id(self, recovery_service_subnet_id):
        """
        Sets the recovery_service_subnet_id of this RecoveryServiceSubnetInput.
        The recovery service subnet OCID.


        :param recovery_service_subnet_id: The recovery_service_subnet_id of this RecoveryServiceSubnetInput.
        :type: str
        """
        self._recovery_service_subnet_id = recovery_service_subnet_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
