# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateAutonomousContainerDatabaseDataGuardAssociationDetails(object):
    """
    The configuration details for updating a Autonomous Container DatabaseData Guard association for a Autonomous Container Database.
    """

    #: A constant which can be used with the protection_mode property of a UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
    #: This constant has a value of "MAXIMUM_AVAILABILITY"
    PROTECTION_MODE_MAXIMUM_AVAILABILITY = "MAXIMUM_AVAILABILITY"

    #: A constant which can be used with the protection_mode property of a UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
    #: This constant has a value of "MAXIMUM_PERFORMANCE"
    PROTECTION_MODE_MAXIMUM_PERFORMANCE = "MAXIMUM_PERFORMANCE"

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateAutonomousContainerDatabaseDataGuardAssociationDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param is_automatic_failover_enabled:
            The value to assign to the is_automatic_failover_enabled property of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        :type is_automatic_failover_enabled: bool

        :param protection_mode:
            The value to assign to the protection_mode property of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
            Allowed values for this property are: "MAXIMUM_AVAILABILITY", "MAXIMUM_PERFORMANCE"
        :type protection_mode: str

        :param fast_start_fail_over_lag_limit_in_seconds:
            The value to assign to the fast_start_fail_over_lag_limit_in_seconds property of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        :type fast_start_fail_over_lag_limit_in_seconds: int

        """
        self.swagger_types = {
            'is_automatic_failover_enabled': 'bool',
            'protection_mode': 'str',
            'fast_start_fail_over_lag_limit_in_seconds': 'int'
        }

        self.attribute_map = {
            'is_automatic_failover_enabled': 'isAutomaticFailoverEnabled',
            'protection_mode': 'protectionMode',
            'fast_start_fail_over_lag_limit_in_seconds': 'fastStartFailOverLagLimitInSeconds'
        }

        self._is_automatic_failover_enabled = None
        self._protection_mode = None
        self._fast_start_fail_over_lag_limit_in_seconds = None

    @property
    def is_automatic_failover_enabled(self):
        """
        Gets the is_automatic_failover_enabled of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        Indicates whether Automatic Failover is enabled for Autonomous Container Database Dataguard Association


        :return: The is_automatic_failover_enabled of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        :rtype: bool
        """
        return self._is_automatic_failover_enabled

    @is_automatic_failover_enabled.setter
    def is_automatic_failover_enabled(self, is_automatic_failover_enabled):
        """
        Sets the is_automatic_failover_enabled of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        Indicates whether Automatic Failover is enabled for Autonomous Container Database Dataguard Association


        :param is_automatic_failover_enabled: The is_automatic_failover_enabled of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        :type: bool
        """
        self._is_automatic_failover_enabled = is_automatic_failover_enabled

    @property
    def protection_mode(self):
        """
        Gets the protection_mode of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        The protection mode of this Autonomous Data Guard association. For more information, see
        `Oracle Data Guard Protection Modes`__
        in the Oracle Data Guard documentation.

        __ http://docs.oracle.com/database/122/SBYDB/oracle-data-guard-protection-modes.htm#SBYDB02000

        Allowed values for this property are: "MAXIMUM_AVAILABILITY", "MAXIMUM_PERFORMANCE"


        :return: The protection_mode of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        :rtype: str
        """
        return self._protection_mode

    @protection_mode.setter
    def protection_mode(self, protection_mode):
        """
        Sets the protection_mode of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        The protection mode of this Autonomous Data Guard association. For more information, see
        `Oracle Data Guard Protection Modes`__
        in the Oracle Data Guard documentation.

        __ http://docs.oracle.com/database/122/SBYDB/oracle-data-guard-protection-modes.htm#SBYDB02000


        :param protection_mode: The protection_mode of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        :type: str
        """
        allowed_values = ["MAXIMUM_AVAILABILITY", "MAXIMUM_PERFORMANCE"]
        if not value_allowed_none_or_none_sentinel(protection_mode, allowed_values):
            raise ValueError(
                "Invalid value for `protection_mode`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._protection_mode = protection_mode

    @property
    def fast_start_fail_over_lag_limit_in_seconds(self):
        """
        Gets the fast_start_fail_over_lag_limit_in_seconds of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        The lag time for my preference based on data loss tolerance in seconds.


        :return: The fast_start_fail_over_lag_limit_in_seconds of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        :rtype: int
        """
        return self._fast_start_fail_over_lag_limit_in_seconds

    @fast_start_fail_over_lag_limit_in_seconds.setter
    def fast_start_fail_over_lag_limit_in_seconds(self, fast_start_fail_over_lag_limit_in_seconds):
        """
        Sets the fast_start_fail_over_lag_limit_in_seconds of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        The lag time for my preference based on data loss tolerance in seconds.


        :param fast_start_fail_over_lag_limit_in_seconds: The fast_start_fail_over_lag_limit_in_seconds of this UpdateAutonomousContainerDatabaseDataGuardAssociationDetails.
        :type: int
        """
        self._fast_start_fail_over_lag_limit_in_seconds = fast_start_fail_over_lag_limit_in_seconds

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
