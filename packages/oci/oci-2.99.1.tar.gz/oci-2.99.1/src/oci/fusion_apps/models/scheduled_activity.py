# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ScheduledActivity(object):
    """
    Details of scheduled activity.
    """

    #: A constant which can be used with the run_cycle property of a ScheduledActivity.
    #: This constant has a value of "QUARTERLY"
    RUN_CYCLE_QUARTERLY = "QUARTERLY"

    #: A constant which can be used with the run_cycle property of a ScheduledActivity.
    #: This constant has a value of "MONTHLY"
    RUN_CYCLE_MONTHLY = "MONTHLY"

    #: A constant which can be used with the run_cycle property of a ScheduledActivity.
    #: This constant has a value of "ONEOFF"
    RUN_CYCLE_ONEOFF = "ONEOFF"

    #: A constant which can be used with the run_cycle property of a ScheduledActivity.
    #: This constant has a value of "VERTEX"
    RUN_CYCLE_VERTEX = "VERTEX"

    #: A constant which can be used with the lifecycle_state property of a ScheduledActivity.
    #: This constant has a value of "ACCEPTED"
    LIFECYCLE_STATE_ACCEPTED = "ACCEPTED"

    #: A constant which can be used with the lifecycle_state property of a ScheduledActivity.
    #: This constant has a value of "IN_PROGRESS"
    LIFECYCLE_STATE_IN_PROGRESS = "IN_PROGRESS"

    #: A constant which can be used with the lifecycle_state property of a ScheduledActivity.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a ScheduledActivity.
    #: This constant has a value of "SUCCEEDED"
    LIFECYCLE_STATE_SUCCEEDED = "SUCCEEDED"

    #: A constant which can be used with the lifecycle_state property of a ScheduledActivity.
    #: This constant has a value of "CANCELED"
    LIFECYCLE_STATE_CANCELED = "CANCELED"

    #: A constant which can be used with the service_availability property of a ScheduledActivity.
    #: This constant has a value of "AVAILABLE"
    SERVICE_AVAILABILITY_AVAILABLE = "AVAILABLE"

    #: A constant which can be used with the service_availability property of a ScheduledActivity.
    #: This constant has a value of "UNAVAILABLE"
    SERVICE_AVAILABILITY_UNAVAILABLE = "UNAVAILABLE"

    #: A constant which can be used with the lifecycle_details property of a ScheduledActivity.
    #: This constant has a value of "NONE"
    LIFECYCLE_DETAILS_NONE = "NONE"

    #: A constant which can be used with the lifecycle_details property of a ScheduledActivity.
    #: This constant has a value of "ROLLBACKACCEPTED"
    LIFECYCLE_DETAILS_ROLLBACKACCEPTED = "ROLLBACKACCEPTED"

    #: A constant which can be used with the lifecycle_details property of a ScheduledActivity.
    #: This constant has a value of "ROLLBACKINPROGRESS"
    LIFECYCLE_DETAILS_ROLLBACKINPROGRESS = "ROLLBACKINPROGRESS"

    #: A constant which can be used with the lifecycle_details property of a ScheduledActivity.
    #: This constant has a value of "ROLLBACKSUCCEEDED"
    LIFECYCLE_DETAILS_ROLLBACKSUCCEEDED = "ROLLBACKSUCCEEDED"

    #: A constant which can be used with the lifecycle_details property of a ScheduledActivity.
    #: This constant has a value of "ROLLBACKFAILED"
    LIFECYCLE_DETAILS_ROLLBACKFAILED = "ROLLBACKFAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new ScheduledActivity object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ScheduledActivity.
        :type id: str

        :param display_name:
            The value to assign to the display_name property of this ScheduledActivity.
        :type display_name: str

        :param run_cycle:
            The value to assign to the run_cycle property of this ScheduledActivity.
            Allowed values for this property are: "QUARTERLY", "MONTHLY", "ONEOFF", "VERTEX", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type run_cycle: str

        :param fusion_environment_id:
            The value to assign to the fusion_environment_id property of this ScheduledActivity.
        :type fusion_environment_id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ScheduledActivity.
            Allowed values for this property are: "ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param actions:
            The value to assign to the actions property of this ScheduledActivity.
        :type actions: list[oci.fusion_apps.models.Action]

        :param service_availability:
            The value to assign to the service_availability property of this ScheduledActivity.
            Allowed values for this property are: "AVAILABLE", "UNAVAILABLE", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type service_availability: str

        :param time_scheduled_start:
            The value to assign to the time_scheduled_start property of this ScheduledActivity.
        :type time_scheduled_start: datetime

        :param time_expected_finish:
            The value to assign to the time_expected_finish property of this ScheduledActivity.
        :type time_expected_finish: datetime

        :param time_finished:
            The value to assign to the time_finished property of this ScheduledActivity.
        :type time_finished: datetime

        :param delay_in_hours:
            The value to assign to the delay_in_hours property of this ScheduledActivity.
        :type delay_in_hours: int

        :param time_created:
            The value to assign to the time_created property of this ScheduledActivity.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ScheduledActivity.
        :type time_updated: datetime

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this ScheduledActivity.
            Allowed values for this property are: "NONE", "ROLLBACKACCEPTED", "ROLLBACKINPROGRESS", "ROLLBACKSUCCEEDED", "ROLLBACKFAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_details: str

        """
        self.swagger_types = {
            'id': 'str',
            'display_name': 'str',
            'run_cycle': 'str',
            'fusion_environment_id': 'str',
            'lifecycle_state': 'str',
            'actions': 'list[Action]',
            'service_availability': 'str',
            'time_scheduled_start': 'datetime',
            'time_expected_finish': 'datetime',
            'time_finished': 'datetime',
            'delay_in_hours': 'int',
            'time_created': 'datetime',
            'time_updated': 'datetime',
            'lifecycle_details': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'display_name': 'displayName',
            'run_cycle': 'runCycle',
            'fusion_environment_id': 'fusionEnvironmentId',
            'lifecycle_state': 'lifecycleState',
            'actions': 'actions',
            'service_availability': 'serviceAvailability',
            'time_scheduled_start': 'timeScheduledStart',
            'time_expected_finish': 'timeExpectedFinish',
            'time_finished': 'timeFinished',
            'delay_in_hours': 'delayInHours',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated',
            'lifecycle_details': 'lifecycleDetails'
        }

        self._id = None
        self._display_name = None
        self._run_cycle = None
        self._fusion_environment_id = None
        self._lifecycle_state = None
        self._actions = None
        self._service_availability = None
        self._time_scheduled_start = None
        self._time_expected_finish = None
        self._time_finished = None
        self._delay_in_hours = None
        self._time_created = None
        self._time_updated = None
        self._lifecycle_details = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ScheduledActivity.
        Unique identifier that is immutable on creation.


        :return: The id of this ScheduledActivity.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ScheduledActivity.
        Unique identifier that is immutable on creation.


        :param id: The id of this ScheduledActivity.
        :type: str
        """
        self._id = id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ScheduledActivity.
        scheduled activity display name, can be renamed.


        :return: The display_name of this ScheduledActivity.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ScheduledActivity.
        scheduled activity display name, can be renamed.


        :param display_name: The display_name of this ScheduledActivity.
        :type: str
        """
        self._display_name = display_name

    @property
    def run_cycle(self):
        """
        **[Required]** Gets the run_cycle of this ScheduledActivity.
        run cadence.

        Allowed values for this property are: "QUARTERLY", "MONTHLY", "ONEOFF", "VERTEX", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The run_cycle of this ScheduledActivity.
        :rtype: str
        """
        return self._run_cycle

    @run_cycle.setter
    def run_cycle(self, run_cycle):
        """
        Sets the run_cycle of this ScheduledActivity.
        run cadence.


        :param run_cycle: The run_cycle of this ScheduledActivity.
        :type: str
        """
        allowed_values = ["QUARTERLY", "MONTHLY", "ONEOFF", "VERTEX"]
        if not value_allowed_none_or_none_sentinel(run_cycle, allowed_values):
            run_cycle = 'UNKNOWN_ENUM_VALUE'
        self._run_cycle = run_cycle

    @property
    def fusion_environment_id(self):
        """
        **[Required]** Gets the fusion_environment_id of this ScheduledActivity.
        FAaaS Environment Identifier.


        :return: The fusion_environment_id of this ScheduledActivity.
        :rtype: str
        """
        return self._fusion_environment_id

    @fusion_environment_id.setter
    def fusion_environment_id(self, fusion_environment_id):
        """
        Sets the fusion_environment_id of this ScheduledActivity.
        FAaaS Environment Identifier.


        :param fusion_environment_id: The fusion_environment_id of this ScheduledActivity.
        :type: str
        """
        self._fusion_environment_id = fusion_environment_id

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ScheduledActivity.
        The current state of the scheduledActivity.

        Allowed values for this property are: "ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ScheduledActivity.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ScheduledActivity.
        The current state of the scheduledActivity.


        :param lifecycle_state: The lifecycle_state of this ScheduledActivity.
        :type: str
        """
        allowed_values = ["ACCEPTED", "IN_PROGRESS", "FAILED", "SUCCEEDED", "CANCELED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def actions(self):
        """
        Gets the actions of this ScheduledActivity.
        List of actions


        :return: The actions of this ScheduledActivity.
        :rtype: list[oci.fusion_apps.models.Action]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """
        Sets the actions of this ScheduledActivity.
        List of actions


        :param actions: The actions of this ScheduledActivity.
        :type: list[oci.fusion_apps.models.Action]
        """
        self._actions = actions

    @property
    def service_availability(self):
        """
        **[Required]** Gets the service_availability of this ScheduledActivity.
        Service availability / impact during scheduled activity execution up down

        Allowed values for this property are: "AVAILABLE", "UNAVAILABLE", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The service_availability of this ScheduledActivity.
        :rtype: str
        """
        return self._service_availability

    @service_availability.setter
    def service_availability(self, service_availability):
        """
        Sets the service_availability of this ScheduledActivity.
        Service availability / impact during scheduled activity execution up down


        :param service_availability: The service_availability of this ScheduledActivity.
        :type: str
        """
        allowed_values = ["AVAILABLE", "UNAVAILABLE"]
        if not value_allowed_none_or_none_sentinel(service_availability, allowed_values):
            service_availability = 'UNKNOWN_ENUM_VALUE'
        self._service_availability = service_availability

    @property
    def time_scheduled_start(self):
        """
        **[Required]** Gets the time_scheduled_start of this ScheduledActivity.
        Current time the scheduled activity is scheduled to start. An RFC3339 formatted datetime string.


        :return: The time_scheduled_start of this ScheduledActivity.
        :rtype: datetime
        """
        return self._time_scheduled_start

    @time_scheduled_start.setter
    def time_scheduled_start(self, time_scheduled_start):
        """
        Sets the time_scheduled_start of this ScheduledActivity.
        Current time the scheduled activity is scheduled to start. An RFC3339 formatted datetime string.


        :param time_scheduled_start: The time_scheduled_start of this ScheduledActivity.
        :type: datetime
        """
        self._time_scheduled_start = time_scheduled_start

    @property
    def time_expected_finish(self):
        """
        **[Required]** Gets the time_expected_finish of this ScheduledActivity.
        Current time the scheduled activity is scheduled to end. An RFC3339 formatted datetime string.


        :return: The time_expected_finish of this ScheduledActivity.
        :rtype: datetime
        """
        return self._time_expected_finish

    @time_expected_finish.setter
    def time_expected_finish(self, time_expected_finish):
        """
        Sets the time_expected_finish of this ScheduledActivity.
        Current time the scheduled activity is scheduled to end. An RFC3339 formatted datetime string.


        :param time_expected_finish: The time_expected_finish of this ScheduledActivity.
        :type: datetime
        """
        self._time_expected_finish = time_expected_finish

    @property
    def time_finished(self):
        """
        Gets the time_finished of this ScheduledActivity.
        The time the scheduled activity actually completed / cancelled / failed. An RFC3339 formatted datetime string.


        :return: The time_finished of this ScheduledActivity.
        :rtype: datetime
        """
        return self._time_finished

    @time_finished.setter
    def time_finished(self, time_finished):
        """
        Sets the time_finished of this ScheduledActivity.
        The time the scheduled activity actually completed / cancelled / failed. An RFC3339 formatted datetime string.


        :param time_finished: The time_finished of this ScheduledActivity.
        :type: datetime
        """
        self._time_finished = time_finished

    @property
    def delay_in_hours(self):
        """
        Gets the delay_in_hours of this ScheduledActivity.
        Cumulative delay hours


        :return: The delay_in_hours of this ScheduledActivity.
        :rtype: int
        """
        return self._delay_in_hours

    @delay_in_hours.setter
    def delay_in_hours(self, delay_in_hours):
        """
        Sets the delay_in_hours of this ScheduledActivity.
        Cumulative delay hours


        :param delay_in_hours: The delay_in_hours of this ScheduledActivity.
        :type: int
        """
        self._delay_in_hours = delay_in_hours

    @property
    def time_created(self):
        """
        Gets the time_created of this ScheduledActivity.
        The time the scheduled activity record was created. An RFC3339 formatted datetime string.


        :return: The time_created of this ScheduledActivity.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ScheduledActivity.
        The time the scheduled activity record was created. An RFC3339 formatted datetime string.


        :param time_created: The time_created of this ScheduledActivity.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this ScheduledActivity.
        The time the scheduled activity record was updated. An RFC3339 formatted datetime string.


        :return: The time_updated of this ScheduledActivity.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this ScheduledActivity.
        The time the scheduled activity record was updated. An RFC3339 formatted datetime string.


        :param time_updated: The time_updated of this ScheduledActivity.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this ScheduledActivity.
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.

        Allowed values for this property are: "NONE", "ROLLBACKACCEPTED", "ROLLBACKINPROGRESS", "ROLLBACKSUCCEEDED", "ROLLBACKFAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_details of this ScheduledActivity.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this ScheduledActivity.
        A message describing the current state in more detail. For example, can be used to provide actionable information for a resource in Failed state.


        :param lifecycle_details: The lifecycle_details of this ScheduledActivity.
        :type: str
        """
        allowed_values = ["NONE", "ROLLBACKACCEPTED", "ROLLBACKINPROGRESS", "ROLLBACKSUCCEEDED", "ROLLBACKFAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_details, allowed_values):
            lifecycle_details = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_details = lifecycle_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
