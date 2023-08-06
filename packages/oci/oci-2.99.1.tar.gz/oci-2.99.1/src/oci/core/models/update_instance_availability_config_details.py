# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateInstanceAvailabilityConfigDetails(object):
    """
    Options for defining the availability of a VM instance after a maintenance event that impacts the underlying
    hardware, including whether to live migrate supported VM instances when possible without sending a prior customer notification.
    """

    #: A constant which can be used with the recovery_action property of a UpdateInstanceAvailabilityConfigDetails.
    #: This constant has a value of "RESTORE_INSTANCE"
    RECOVERY_ACTION_RESTORE_INSTANCE = "RESTORE_INSTANCE"

    #: A constant which can be used with the recovery_action property of a UpdateInstanceAvailabilityConfigDetails.
    #: This constant has a value of "STOP_INSTANCE"
    RECOVERY_ACTION_STOP_INSTANCE = "STOP_INSTANCE"

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateInstanceAvailabilityConfigDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param is_live_migration_preferred:
            The value to assign to the is_live_migration_preferred property of this UpdateInstanceAvailabilityConfigDetails.
        :type is_live_migration_preferred: bool

        :param recovery_action:
            The value to assign to the recovery_action property of this UpdateInstanceAvailabilityConfigDetails.
            Allowed values for this property are: "RESTORE_INSTANCE", "STOP_INSTANCE"
        :type recovery_action: str

        """
        self.swagger_types = {
            'is_live_migration_preferred': 'bool',
            'recovery_action': 'str'
        }

        self.attribute_map = {
            'is_live_migration_preferred': 'isLiveMigrationPreferred',
            'recovery_action': 'recoveryAction'
        }

        self._is_live_migration_preferred = None
        self._recovery_action = None

    @property
    def is_live_migration_preferred(self):
        """
        Gets the is_live_migration_preferred of this UpdateInstanceAvailabilityConfigDetails.
        Whether to live migrate supported VM instances to a healthy physical VM host without
        disrupting running instances during infrastructure maintenance events. If null, Oracle
        chooses the best option for migrating the VM during infrastructure maintenance events.


        :return: The is_live_migration_preferred of this UpdateInstanceAvailabilityConfigDetails.
        :rtype: bool
        """
        return self._is_live_migration_preferred

    @is_live_migration_preferred.setter
    def is_live_migration_preferred(self, is_live_migration_preferred):
        """
        Sets the is_live_migration_preferred of this UpdateInstanceAvailabilityConfigDetails.
        Whether to live migrate supported VM instances to a healthy physical VM host without
        disrupting running instances during infrastructure maintenance events. If null, Oracle
        chooses the best option for migrating the VM during infrastructure maintenance events.


        :param is_live_migration_preferred: The is_live_migration_preferred of this UpdateInstanceAvailabilityConfigDetails.
        :type: bool
        """
        self._is_live_migration_preferred = is_live_migration_preferred

    @property
    def recovery_action(self):
        """
        Gets the recovery_action of this UpdateInstanceAvailabilityConfigDetails.
        The lifecycle state for an instance when it is recovered after infrastructure maintenance.
        * `RESTORE_INSTANCE` - The instance is restored to the lifecycle state it was in before the maintenance event.
        If the instance was running, it is automatically rebooted. This is the default action when a value is not set.
        * `STOP_INSTANCE` - The instance is recovered in the stopped state.

        Allowed values for this property are: "RESTORE_INSTANCE", "STOP_INSTANCE"


        :return: The recovery_action of this UpdateInstanceAvailabilityConfigDetails.
        :rtype: str
        """
        return self._recovery_action

    @recovery_action.setter
    def recovery_action(self, recovery_action):
        """
        Sets the recovery_action of this UpdateInstanceAvailabilityConfigDetails.
        The lifecycle state for an instance when it is recovered after infrastructure maintenance.
        * `RESTORE_INSTANCE` - The instance is restored to the lifecycle state it was in before the maintenance event.
        If the instance was running, it is automatically rebooted. This is the default action when a value is not set.
        * `STOP_INSTANCE` - The instance is recovered in the stopped state.


        :param recovery_action: The recovery_action of this UpdateInstanceAvailabilityConfigDetails.
        :type: str
        """
        allowed_values = ["RESTORE_INSTANCE", "STOP_INSTANCE"]
        if not value_allowed_none_or_none_sentinel(recovery_action, allowed_values):
            raise ValueError(
                "Invalid value for `recovery_action`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._recovery_action = recovery_action

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
