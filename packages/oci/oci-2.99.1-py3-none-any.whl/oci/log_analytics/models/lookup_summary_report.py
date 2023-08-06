# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class LookupSummaryReport(object):
    """
    Summary report of lookups in the tenancy.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new LookupSummaryReport object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param user_created_count:
            The value to assign to the user_created_count property of this LookupSummaryReport.
        :type user_created_count: int

        :param oracle_defined_count:
            The value to assign to the oracle_defined_count property of this LookupSummaryReport.
        :type oracle_defined_count: int

        :param total_count:
            The value to assign to the total_count property of this LookupSummaryReport.
        :type total_count: int

        """
        self.swagger_types = {
            'user_created_count': 'int',
            'oracle_defined_count': 'int',
            'total_count': 'int'
        }

        self.attribute_map = {
            'user_created_count': 'userCreatedCount',
            'oracle_defined_count': 'oracleDefinedCount',
            'total_count': 'totalCount'
        }

        self._user_created_count = None
        self._oracle_defined_count = None
        self._total_count = None

    @property
    def user_created_count(self):
        """
        Gets the user_created_count of this LookupSummaryReport.
        The number of user created lookups.


        :return: The user_created_count of this LookupSummaryReport.
        :rtype: int
        """
        return self._user_created_count

    @user_created_count.setter
    def user_created_count(self, user_created_count):
        """
        Sets the user_created_count of this LookupSummaryReport.
        The number of user created lookups.


        :param user_created_count: The user_created_count of this LookupSummaryReport.
        :type: int
        """
        self._user_created_count = user_created_count

    @property
    def oracle_defined_count(self):
        """
        Gets the oracle_defined_count of this LookupSummaryReport.
        The number of oracle defined lookups.


        :return: The oracle_defined_count of this LookupSummaryReport.
        :rtype: int
        """
        return self._oracle_defined_count

    @oracle_defined_count.setter
    def oracle_defined_count(self, oracle_defined_count):
        """
        Sets the oracle_defined_count of this LookupSummaryReport.
        The number of oracle defined lookups.


        :param oracle_defined_count: The oracle_defined_count of this LookupSummaryReport.
        :type: int
        """
        self._oracle_defined_count = oracle_defined_count

    @property
    def total_count(self):
        """
        Gets the total_count of this LookupSummaryReport.
        The total number of lookups.


        :return: The total_count of this LookupSummaryReport.
        :rtype: int
        """
        return self._total_count

    @total_count.setter
    def total_count(self, total_count):
        """
        Sets the total_count of this LookupSummaryReport.
        The total number of lookups.


        :param total_count: The total_count of this LookupSummaryReport.
        :type: int
        """
        self._total_count = total_count

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
