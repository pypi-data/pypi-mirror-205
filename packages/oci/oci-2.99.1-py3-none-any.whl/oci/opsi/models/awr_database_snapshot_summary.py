# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AwrDatabaseSnapshotSummary(object):
    """
    The AWR snapshot summary of one snapshot.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AwrDatabaseSnapshotSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param awr_source_database_identifier:
            The value to assign to the awr_source_database_identifier property of this AwrDatabaseSnapshotSummary.
        :type awr_source_database_identifier: str

        :param instance_number:
            The value to assign to the instance_number property of this AwrDatabaseSnapshotSummary.
        :type instance_number: int

        :param time_db_startup:
            The value to assign to the time_db_startup property of this AwrDatabaseSnapshotSummary.
        :type time_db_startup: datetime

        :param time_begin:
            The value to assign to the time_begin property of this AwrDatabaseSnapshotSummary.
        :type time_begin: datetime

        :param time_end:
            The value to assign to the time_end property of this AwrDatabaseSnapshotSummary.
        :type time_end: datetime

        :param snapshot_identifier:
            The value to assign to the snapshot_identifier property of this AwrDatabaseSnapshotSummary.
        :type snapshot_identifier: int

        :param error_count:
            The value to assign to the error_count property of this AwrDatabaseSnapshotSummary.
        :type error_count: int

        """
        self.swagger_types = {
            'awr_source_database_identifier': 'str',
            'instance_number': 'int',
            'time_db_startup': 'datetime',
            'time_begin': 'datetime',
            'time_end': 'datetime',
            'snapshot_identifier': 'int',
            'error_count': 'int'
        }

        self.attribute_map = {
            'awr_source_database_identifier': 'awrSourceDatabaseIdentifier',
            'instance_number': 'instanceNumber',
            'time_db_startup': 'timeDbStartup',
            'time_begin': 'timeBegin',
            'time_end': 'timeEnd',
            'snapshot_identifier': 'snapshotIdentifier',
            'error_count': 'errorCount'
        }

        self._awr_source_database_identifier = None
        self._instance_number = None
        self._time_db_startup = None
        self._time_begin = None
        self._time_end = None
        self._snapshot_identifier = None
        self._error_count = None

    @property
    def awr_source_database_identifier(self):
        """
        **[Required]** Gets the awr_source_database_identifier of this AwrDatabaseSnapshotSummary.
        Internal ID of the database. The internal ID of the database is not the `OCID`__.
        It can be retrieved from the following endpoint:
        /awrHubs/{awrHubId}/awrDatabases

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The awr_source_database_identifier of this AwrDatabaseSnapshotSummary.
        :rtype: str
        """
        return self._awr_source_database_identifier

    @awr_source_database_identifier.setter
    def awr_source_database_identifier(self, awr_source_database_identifier):
        """
        Sets the awr_source_database_identifier of this AwrDatabaseSnapshotSummary.
        Internal ID of the database. The internal ID of the database is not the `OCID`__.
        It can be retrieved from the following endpoint:
        /awrHubs/{awrHubId}/awrDatabases

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param awr_source_database_identifier: The awr_source_database_identifier of this AwrDatabaseSnapshotSummary.
        :type: str
        """
        self._awr_source_database_identifier = awr_source_database_identifier

    @property
    def instance_number(self):
        """
        Gets the instance_number of this AwrDatabaseSnapshotSummary.
        The database instance number.


        :return: The instance_number of this AwrDatabaseSnapshotSummary.
        :rtype: int
        """
        return self._instance_number

    @instance_number.setter
    def instance_number(self, instance_number):
        """
        Sets the instance_number of this AwrDatabaseSnapshotSummary.
        The database instance number.


        :param instance_number: The instance_number of this AwrDatabaseSnapshotSummary.
        :type: int
        """
        self._instance_number = instance_number

    @property
    def time_db_startup(self):
        """
        Gets the time_db_startup of this AwrDatabaseSnapshotSummary.
        The timestamp of the database startup.


        :return: The time_db_startup of this AwrDatabaseSnapshotSummary.
        :rtype: datetime
        """
        return self._time_db_startup

    @time_db_startup.setter
    def time_db_startup(self, time_db_startup):
        """
        Sets the time_db_startup of this AwrDatabaseSnapshotSummary.
        The timestamp of the database startup.


        :param time_db_startup: The time_db_startup of this AwrDatabaseSnapshotSummary.
        :type: datetime
        """
        self._time_db_startup = time_db_startup

    @property
    def time_begin(self):
        """
        Gets the time_begin of this AwrDatabaseSnapshotSummary.
        The start time of the snapshot.


        :return: The time_begin of this AwrDatabaseSnapshotSummary.
        :rtype: datetime
        """
        return self._time_begin

    @time_begin.setter
    def time_begin(self, time_begin):
        """
        Sets the time_begin of this AwrDatabaseSnapshotSummary.
        The start time of the snapshot.


        :param time_begin: The time_begin of this AwrDatabaseSnapshotSummary.
        :type: datetime
        """
        self._time_begin = time_begin

    @property
    def time_end(self):
        """
        Gets the time_end of this AwrDatabaseSnapshotSummary.
        The end time of the snapshot.


        :return: The time_end of this AwrDatabaseSnapshotSummary.
        :rtype: datetime
        """
        return self._time_end

    @time_end.setter
    def time_end(self, time_end):
        """
        Sets the time_end of this AwrDatabaseSnapshotSummary.
        The end time of the snapshot.


        :param time_end: The time_end of this AwrDatabaseSnapshotSummary.
        :type: datetime
        """
        self._time_end = time_end

    @property
    def snapshot_identifier(self):
        """
        **[Required]** Gets the snapshot_identifier of this AwrDatabaseSnapshotSummary.
        The ID of the snapshot. The snapshot identifier is not the `OCID`__.
        It can be retrieved from the following endpoint:
        /awrHubs/{awrHubId}/awrDbSnapshots

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The snapshot_identifier of this AwrDatabaseSnapshotSummary.
        :rtype: int
        """
        return self._snapshot_identifier

    @snapshot_identifier.setter
    def snapshot_identifier(self, snapshot_identifier):
        """
        Sets the snapshot_identifier of this AwrDatabaseSnapshotSummary.
        The ID of the snapshot. The snapshot identifier is not the `OCID`__.
        It can be retrieved from the following endpoint:
        /awrHubs/{awrHubId}/awrDbSnapshots

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param snapshot_identifier: The snapshot_identifier of this AwrDatabaseSnapshotSummary.
        :type: int
        """
        self._snapshot_identifier = snapshot_identifier

    @property
    def error_count(self):
        """
        Gets the error_count of this AwrDatabaseSnapshotSummary.
        The total number of errors.


        :return: The error_count of this AwrDatabaseSnapshotSummary.
        :rtype: int
        """
        return self._error_count

    @error_count.setter
    def error_count(self, error_count):
        """
        Sets the error_count of this AwrDatabaseSnapshotSummary.
        The total number of errors.


        :param error_count: The error_count of this AwrDatabaseSnapshotSummary.
        :type: int
        """
        self._error_count = error_count

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
