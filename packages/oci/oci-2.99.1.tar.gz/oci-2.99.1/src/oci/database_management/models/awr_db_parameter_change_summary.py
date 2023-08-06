# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AwrDbParameterChangeSummary(object):
    """
    A summary of the changes made to a single AWR database parameter.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AwrDbParameterChangeSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param time_begin:
            The value to assign to the time_begin property of this AwrDbParameterChangeSummary.
        :type time_begin: datetime

        :param time_end:
            The value to assign to the time_end property of this AwrDbParameterChangeSummary.
        :type time_end: datetime

        :param instance_number:
            The value to assign to the instance_number property of this AwrDbParameterChangeSummary.
        :type instance_number: int

        :param previous_value:
            The value to assign to the previous_value property of this AwrDbParameterChangeSummary.
        :type previous_value: str

        :param value:
            The value to assign to the value property of this AwrDbParameterChangeSummary.
        :type value: str

        :param snapshot_id:
            The value to assign to the snapshot_id property of this AwrDbParameterChangeSummary.
        :type snapshot_id: int

        :param value_modified:
            The value to assign to the value_modified property of this AwrDbParameterChangeSummary.
        :type value_modified: str

        :param is_default:
            The value to assign to the is_default property of this AwrDbParameterChangeSummary.
        :type is_default: bool

        """
        self.swagger_types = {
            'time_begin': 'datetime',
            'time_end': 'datetime',
            'instance_number': 'int',
            'previous_value': 'str',
            'value': 'str',
            'snapshot_id': 'int',
            'value_modified': 'str',
            'is_default': 'bool'
        }

        self.attribute_map = {
            'time_begin': 'timeBegin',
            'time_end': 'timeEnd',
            'instance_number': 'instanceNumber',
            'previous_value': 'previousValue',
            'value': 'value',
            'snapshot_id': 'snapshotId',
            'value_modified': 'valueModified',
            'is_default': 'isDefault'
        }

        self._time_begin = None
        self._time_end = None
        self._instance_number = None
        self._previous_value = None
        self._value = None
        self._snapshot_id = None
        self._value_modified = None
        self._is_default = None

    @property
    def time_begin(self):
        """
        Gets the time_begin of this AwrDbParameterChangeSummary.
        The start time of the interval.


        :return: The time_begin of this AwrDbParameterChangeSummary.
        :rtype: datetime
        """
        return self._time_begin

    @time_begin.setter
    def time_begin(self, time_begin):
        """
        Sets the time_begin of this AwrDbParameterChangeSummary.
        The start time of the interval.


        :param time_begin: The time_begin of this AwrDbParameterChangeSummary.
        :type: datetime
        """
        self._time_begin = time_begin

    @property
    def time_end(self):
        """
        Gets the time_end of this AwrDbParameterChangeSummary.
        The end time of the interval.


        :return: The time_end of this AwrDbParameterChangeSummary.
        :rtype: datetime
        """
        return self._time_end

    @time_end.setter
    def time_end(self, time_end):
        """
        Sets the time_end of this AwrDbParameterChangeSummary.
        The end time of the interval.


        :param time_end: The time_end of this AwrDbParameterChangeSummary.
        :type: datetime
        """
        self._time_end = time_end

    @property
    def instance_number(self):
        """
        Gets the instance_number of this AwrDbParameterChangeSummary.
        The database instance number.


        :return: The instance_number of this AwrDbParameterChangeSummary.
        :rtype: int
        """
        return self._instance_number

    @instance_number.setter
    def instance_number(self, instance_number):
        """
        Sets the instance_number of this AwrDbParameterChangeSummary.
        The database instance number.


        :param instance_number: The instance_number of this AwrDbParameterChangeSummary.
        :type: int
        """
        self._instance_number = instance_number

    @property
    def previous_value(self):
        """
        Gets the previous_value of this AwrDbParameterChangeSummary.
        The previous value of the database parameter.


        :return: The previous_value of this AwrDbParameterChangeSummary.
        :rtype: str
        """
        return self._previous_value

    @previous_value.setter
    def previous_value(self, previous_value):
        """
        Sets the previous_value of this AwrDbParameterChangeSummary.
        The previous value of the database parameter.


        :param previous_value: The previous_value of this AwrDbParameterChangeSummary.
        :type: str
        """
        self._previous_value = previous_value

    @property
    def value(self):
        """
        Gets the value of this AwrDbParameterChangeSummary.
        The current value of the database parameter.


        :return: The value of this AwrDbParameterChangeSummary.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this AwrDbParameterChangeSummary.
        The current value of the database parameter.


        :param value: The value of this AwrDbParameterChangeSummary.
        :type: str
        """
        self._value = value

    @property
    def snapshot_id(self):
        """
        **[Required]** Gets the snapshot_id of this AwrDbParameterChangeSummary.
        The ID of the snapshot with the parameter value changed. The snapshot ID is not the `OCID`__.
        It can be retrieved from the following endpoint:
        /managedDatabases/{managedDatabaseId}/awrDbs/{awrDbId}/awrDbSnapshots

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The snapshot_id of this AwrDbParameterChangeSummary.
        :rtype: int
        """
        return self._snapshot_id

    @snapshot_id.setter
    def snapshot_id(self, snapshot_id):
        """
        Sets the snapshot_id of this AwrDbParameterChangeSummary.
        The ID of the snapshot with the parameter value changed. The snapshot ID is not the `OCID`__.
        It can be retrieved from the following endpoint:
        /managedDatabases/{managedDatabaseId}/awrDbs/{awrDbId}/awrDbSnapshots

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param snapshot_id: The snapshot_id of this AwrDbParameterChangeSummary.
        :type: int
        """
        self._snapshot_id = snapshot_id

    @property
    def value_modified(self):
        """
        Gets the value_modified of this AwrDbParameterChangeSummary.
        Indicates whether the parameter has been modified after instance startup:
         - MODIFIED - Parameter has been modified with ALTER SESSION
         - SYSTEM_MOD - Parameter has been modified with ALTER SYSTEM (which causes all the currently logged in sessions\u2019 values to be modified)
         - FALSE - Parameter has not been modified after instance startup


        :return: The value_modified of this AwrDbParameterChangeSummary.
        :rtype: str
        """
        return self._value_modified

    @value_modified.setter
    def value_modified(self, value_modified):
        """
        Sets the value_modified of this AwrDbParameterChangeSummary.
        Indicates whether the parameter has been modified after instance startup:
         - MODIFIED - Parameter has been modified with ALTER SESSION
         - SYSTEM_MOD - Parameter has been modified with ALTER SYSTEM (which causes all the currently logged in sessions\u2019 values to be modified)
         - FALSE - Parameter has not been modified after instance startup


        :param value_modified: The value_modified of this AwrDbParameterChangeSummary.
        :type: str
        """
        self._value_modified = value_modified

    @property
    def is_default(self):
        """
        Gets the is_default of this AwrDbParameterChangeSummary.
        Indicates whether the parameter value in the end snapshot is the default.


        :return: The is_default of this AwrDbParameterChangeSummary.
        :rtype: bool
        """
        return self._is_default

    @is_default.setter
    def is_default(self, is_default):
        """
        Sets the is_default of this AwrDbParameterChangeSummary.
        Indicates whether the parameter value in the end snapshot is the default.


        :param is_default: The is_default of this AwrDbParameterChangeSummary.
        :type: bool
        """
        self._is_default = is_default

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
