# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class BlocklistTarget(object):
    """
    A resource to blocklist for certain operation.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new BlocklistTarget object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param fleet_id:
            The value to assign to the fleet_id property of this BlocklistTarget.
        :type fleet_id: str

        :param managed_instance_id:
            The value to assign to the managed_instance_id property of this BlocklistTarget.
        :type managed_instance_id: str

        :param installation_key:
            The value to assign to the installation_key property of this BlocklistTarget.
        :type installation_key: str

        """
        self.swagger_types = {
            'fleet_id': 'str',
            'managed_instance_id': 'str',
            'installation_key': 'str'
        }

        self.attribute_map = {
            'fleet_id': 'fleetId',
            'managed_instance_id': 'managedInstanceId',
            'installation_key': 'installationKey'
        }

        self._fleet_id = None
        self._managed_instance_id = None
        self._installation_key = None

    @property
    def fleet_id(self):
        """
        **[Required]** Gets the fleet_id of this BlocklistTarget.
        The `OCID`__ of the fleet.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The fleet_id of this BlocklistTarget.
        :rtype: str
        """
        return self._fleet_id

    @fleet_id.setter
    def fleet_id(self, fleet_id):
        """
        Sets the fleet_id of this BlocklistTarget.
        The `OCID`__ of the fleet.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param fleet_id: The fleet_id of this BlocklistTarget.
        :type: str
        """
        self._fleet_id = fleet_id

    @property
    def managed_instance_id(self):
        """
        Gets the managed_instance_id of this BlocklistTarget.
        The `OCID`__ of the related managed instance.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The managed_instance_id of this BlocklistTarget.
        :rtype: str
        """
        return self._managed_instance_id

    @managed_instance_id.setter
    def managed_instance_id(self, managed_instance_id):
        """
        Sets the managed_instance_id of this BlocklistTarget.
        The `OCID`__ of the related managed instance.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param managed_instance_id: The managed_instance_id of this BlocklistTarget.
        :type: str
        """
        self._managed_instance_id = managed_instance_id

    @property
    def installation_key(self):
        """
        Gets the installation_key of this BlocklistTarget.
        The unique identifier for the installation of Java Runtime at a specific path on a specific operating system.


        :return: The installation_key of this BlocklistTarget.
        :rtype: str
        """
        return self._installation_key

    @installation_key.setter
    def installation_key(self, installation_key):
        """
        Sets the installation_key of this BlocklistTarget.
        The unique identifier for the installation of Java Runtime at a specific path on a specific operating system.


        :param installation_key: The installation_key of this BlocklistTarget.
        :type: str
        """
        self._installation_key = installation_key

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
