# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ReplicationSummary(object):
    """
    Summary information for a replication.
    """

    #: A constant which can be used with the lifecycle_state property of a ReplicationSummary.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a ReplicationSummary.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ReplicationSummary.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a ReplicationSummary.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a ReplicationSummary.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new ReplicationSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param availability_domain:
            The value to assign to the availability_domain property of this ReplicationSummary.
        :type availability_domain: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ReplicationSummary.
        :type compartment_id: str

        :param id:
            The value to assign to the id property of this ReplicationSummary.
        :type id: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ReplicationSummary.
            Allowed values for this property are: "CREATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param display_name:
            The value to assign to the display_name property of this ReplicationSummary.
        :type display_name: str

        :param time_created:
            The value to assign to the time_created property of this ReplicationSummary.
        :type time_created: datetime

        :param replication_interval:
            The value to assign to the replication_interval property of this ReplicationSummary.
        :type replication_interval: int

        :param freeform_tags:
            The value to assign to the freeform_tags property of this ReplicationSummary.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this ReplicationSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this ReplicationSummary.
        :type lifecycle_details: str

        :param recovery_point_time:
            The value to assign to the recovery_point_time property of this ReplicationSummary.
        :type recovery_point_time: datetime

        """
        self.swagger_types = {
            'availability_domain': 'str',
            'compartment_id': 'str',
            'id': 'str',
            'lifecycle_state': 'str',
            'display_name': 'str',
            'time_created': 'datetime',
            'replication_interval': 'int',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'lifecycle_details': 'str',
            'recovery_point_time': 'datetime'
        }

        self.attribute_map = {
            'availability_domain': 'availabilityDomain',
            'compartment_id': 'compartmentId',
            'id': 'id',
            'lifecycle_state': 'lifecycleState',
            'display_name': 'displayName',
            'time_created': 'timeCreated',
            'replication_interval': 'replicationInterval',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'lifecycle_details': 'lifecycleDetails',
            'recovery_point_time': 'recoveryPointTime'
        }

        self._availability_domain = None
        self._compartment_id = None
        self._id = None
        self._lifecycle_state = None
        self._display_name = None
        self._time_created = None
        self._replication_interval = None
        self._freeform_tags = None
        self._defined_tags = None
        self._lifecycle_details = None
        self._recovery_point_time = None

    @property
    def availability_domain(self):
        """
        Gets the availability_domain of this ReplicationSummary.
        The availability domain the replication is in. The replication must be in the same availability domain as the source file system.
        Example: `Uocm:PHX-AD-1`


        :return: The availability_domain of this ReplicationSummary.
        :rtype: str
        """
        return self._availability_domain

    @availability_domain.setter
    def availability_domain(self, availability_domain):
        """
        Sets the availability_domain of this ReplicationSummary.
        The availability domain the replication is in. The replication must be in the same availability domain as the source file system.
        Example: `Uocm:PHX-AD-1`


        :param availability_domain: The availability_domain of this ReplicationSummary.
        :type: str
        """
        self._availability_domain = availability_domain

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this ReplicationSummary.
        The `OCID`__ of the compartment that contains the replication.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ReplicationSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ReplicationSummary.
        The `OCID`__ of the compartment that contains the replication.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ReplicationSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ReplicationSummary.
        The `OCID`__ of the replication.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ReplicationSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ReplicationSummary.
        The `OCID`__ of the replication.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ReplicationSummary.
        :type: str
        """
        self._id = id

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ReplicationSummary.
        The current state of this replication.
        This resource can be in a `FAILED` state if replication target is deleted instead of the replication resource.

        Allowed values for this property are: "CREATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ReplicationSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ReplicationSummary.
        The current state of this replication.
        This resource can be in a `FAILED` state if replication target is deleted instead of the replication resource.


        :param lifecycle_state: The lifecycle_state of this ReplicationSummary.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this ReplicationSummary.
        A user-friendly name. It does not have to be unique, and it is changeable.
        Avoid entering confidential information.
        Example: `My replication`


        :return: The display_name of this ReplicationSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this ReplicationSummary.
        A user-friendly name. It does not have to be unique, and it is changeable.
        Avoid entering confidential information.
        Example: `My replication`


        :param display_name: The display_name of this ReplicationSummary.
        :type: str
        """
        self._display_name = display_name

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this ReplicationSummary.
        The date and time the replication was created
        in `RFC 3339`__ timestamp format.
        Example: `2020-02-04T21:10:29.600Z`

        __ https://tools.ietf.org/rfc/rfc3339


        :return: The time_created of this ReplicationSummary.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ReplicationSummary.
        The date and time the replication was created
        in `RFC 3339`__ timestamp format.
        Example: `2020-02-04T21:10:29.600Z`

        __ https://tools.ietf.org/rfc/rfc3339


        :param time_created: The time_created of this ReplicationSummary.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def replication_interval(self):
        """
        Gets the replication_interval of this ReplicationSummary.
        Duration in minutes between replication snapshots.


        :return: The replication_interval of this ReplicationSummary.
        :rtype: int
        """
        return self._replication_interval

    @replication_interval.setter
    def replication_interval(self, replication_interval):
        """
        Sets the replication_interval of this ReplicationSummary.
        Duration in minutes between replication snapshots.


        :param replication_interval: The replication_interval of this ReplicationSummary.
        :type: int
        """
        self._replication_interval = replication_interval

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this ReplicationSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair
         with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this ReplicationSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this ReplicationSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair
         with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this ReplicationSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this ReplicationSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this ReplicationSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this ReplicationSummary.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this ReplicationSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this ReplicationSummary.
        Additional information about the current `lifecycleState`.


        :return: The lifecycle_details of this ReplicationSummary.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this ReplicationSummary.
        Additional information about the current `lifecycleState`.


        :param lifecycle_details: The lifecycle_details of this ReplicationSummary.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def recovery_point_time(self):
        """
        Gets the recovery_point_time of this ReplicationSummary.
        The `snapshotTime` of the most recent recoverable replication snapshot
        in `RFC 3339`__ timestamp format.
        Example: `2021-04-04T20:01:29.100Z`

        __ https://tools.ietf.org/rfc/rfc3339


        :return: The recovery_point_time of this ReplicationSummary.
        :rtype: datetime
        """
        return self._recovery_point_time

    @recovery_point_time.setter
    def recovery_point_time(self, recovery_point_time):
        """
        Sets the recovery_point_time of this ReplicationSummary.
        The `snapshotTime` of the most recent recoverable replication snapshot
        in `RFC 3339`__ timestamp format.
        Example: `2021-04-04T20:01:29.100Z`

        __ https://tools.ietf.org/rfc/rfc3339


        :param recovery_point_time: The recovery_point_time of this ReplicationSummary.
        :type: datetime
        """
        self._recovery_point_time = recovery_point_time

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
