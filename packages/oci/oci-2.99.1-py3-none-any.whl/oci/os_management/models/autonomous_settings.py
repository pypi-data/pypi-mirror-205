# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AutonomousSettings(object):
    """
    Managed Instance with Autonomous settings
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AutonomousSettings object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param is_auto_update_enabled:
            The value to assign to the is_auto_update_enabled property of this AutonomousSettings.
        :type is_auto_update_enabled: bool

        """
        self.swagger_types = {
            'is_auto_update_enabled': 'bool'
        }

        self.attribute_map = {
            'is_auto_update_enabled': 'isAutoUpdateEnabled'
        }

        self._is_auto_update_enabled = None

    @property
    def is_auto_update_enabled(self):
        """
        Gets the is_auto_update_enabled of this AutonomousSettings.
        True if daily updates are enabled


        :return: The is_auto_update_enabled of this AutonomousSettings.
        :rtype: bool
        """
        return self._is_auto_update_enabled

    @is_auto_update_enabled.setter
    def is_auto_update_enabled(self, is_auto_update_enabled):
        """
        Sets the is_auto_update_enabled of this AutonomousSettings.
        True if daily updates are enabled


        :param is_auto_update_enabled: The is_auto_update_enabled of this AutonomousSettings.
        :type: bool
        """
        self._is_auto_update_enabled = is_auto_update_enabled

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
