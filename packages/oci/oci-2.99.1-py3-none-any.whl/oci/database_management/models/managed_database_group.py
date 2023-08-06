# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ManagedDatabaseGroup(object):
    """
    The details of a Managed Database Group.
    """

    #: A constant which can be used with the lifecycle_state property of a ManagedDatabaseGroup.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a ManagedDatabaseGroup.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a ManagedDatabaseGroup.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a ManagedDatabaseGroup.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a ManagedDatabaseGroup.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a ManagedDatabaseGroup.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Initializes a new ManagedDatabaseGroup object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this ManagedDatabaseGroup.
        :type name: str

        :param id:
            The value to assign to the id property of this ManagedDatabaseGroup.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ManagedDatabaseGroup.
        :type compartment_id: str

        :param description:
            The value to assign to the description property of this ManagedDatabaseGroup.
        :type description: str

        :param managed_databases:
            The value to assign to the managed_databases property of this ManagedDatabaseGroup.
        :type managed_databases: list[oci.database_management.models.ChildDatabase]

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this ManagedDatabaseGroup.
            Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_created:
            The value to assign to the time_created property of this ManagedDatabaseGroup.
        :type time_created: datetime

        :param time_updated:
            The value to assign to the time_updated property of this ManagedDatabaseGroup.
        :type time_updated: datetime

        """
        self.swagger_types = {
            'name': 'str',
            'id': 'str',
            'compartment_id': 'str',
            'description': 'str',
            'managed_databases': 'list[ChildDatabase]',
            'lifecycle_state': 'str',
            'time_created': 'datetime',
            'time_updated': 'datetime'
        }

        self.attribute_map = {
            'name': 'name',
            'id': 'id',
            'compartment_id': 'compartmentId',
            'description': 'description',
            'managed_databases': 'managedDatabases',
            'lifecycle_state': 'lifecycleState',
            'time_created': 'timeCreated',
            'time_updated': 'timeUpdated'
        }

        self._name = None
        self._id = None
        self._compartment_id = None
        self._description = None
        self._managed_databases = None
        self._lifecycle_state = None
        self._time_created = None
        self._time_updated = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this ManagedDatabaseGroup.
        The name of the Managed Database Group.


        :return: The name of this ManagedDatabaseGroup.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ManagedDatabaseGroup.
        The name of the Managed Database Group.


        :param name: The name of this ManagedDatabaseGroup.
        :type: str
        """
        self._name = name

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ManagedDatabaseGroup.
        The `OCID`__ of the Managed Database Group.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ManagedDatabaseGroup.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ManagedDatabaseGroup.
        The `OCID`__ of the Managed Database Group.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ManagedDatabaseGroup.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ManagedDatabaseGroup.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ManagedDatabaseGroup.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ManagedDatabaseGroup.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ManagedDatabaseGroup.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def description(self):
        """
        Gets the description of this ManagedDatabaseGroup.
        The information specified by the user about the Managed Database Group.


        :return: The description of this ManagedDatabaseGroup.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ManagedDatabaseGroup.
        The information specified by the user about the Managed Database Group.


        :param description: The description of this ManagedDatabaseGroup.
        :type: str
        """
        self._description = description

    @property
    def managed_databases(self):
        """
        **[Required]** Gets the managed_databases of this ManagedDatabaseGroup.
        A list of Managed Databases in the Managed Database Group.


        :return: The managed_databases of this ManagedDatabaseGroup.
        :rtype: list[oci.database_management.models.ChildDatabase]
        """
        return self._managed_databases

    @managed_databases.setter
    def managed_databases(self, managed_databases):
        """
        Sets the managed_databases of this ManagedDatabaseGroup.
        A list of Managed Databases in the Managed Database Group.


        :param managed_databases: The managed_databases of this ManagedDatabaseGroup.
        :type: list[oci.database_management.models.ChildDatabase]
        """
        self._managed_databases = managed_databases

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this ManagedDatabaseGroup.
        The current lifecycle state of the Managed Database Group.

        Allowed values for this property are: "CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this ManagedDatabaseGroup.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this ManagedDatabaseGroup.
        The current lifecycle state of the Managed Database Group.


        :param lifecycle_state: The lifecycle_state of this ManagedDatabaseGroup.
        :type: str
        """
        allowed_values = ["CREATING", "UPDATING", "ACTIVE", "DELETING", "DELETED", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this ManagedDatabaseGroup.
        The date and time the Managed Database Group was created.


        :return: The time_created of this ManagedDatabaseGroup.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this ManagedDatabaseGroup.
        The date and time the Managed Database Group was created.


        :param time_created: The time_created of this ManagedDatabaseGroup.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_updated(self):
        """
        Gets the time_updated of this ManagedDatabaseGroup.
        The date and time the Managed Database Group was last updated.


        :return: The time_updated of this ManagedDatabaseGroup.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this ManagedDatabaseGroup.
        The date and time the Managed Database Group was last updated.


        :param time_updated: The time_updated of this ManagedDatabaseGroup.
        :type: datetime
        """
        self._time_updated = time_updated

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
