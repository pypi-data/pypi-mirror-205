# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CopyObjectRequestSummary(object):
    """
    Copy metadata object response summary.
    """

    #: A constant which can be used with the copy_metadata_object_request_status property of a CopyObjectRequestSummary.
    #: This constant has a value of "SUCCESSFUL"
    COPY_METADATA_OBJECT_REQUEST_STATUS_SUCCESSFUL = "SUCCESSFUL"

    #: A constant which can be used with the copy_metadata_object_request_status property of a CopyObjectRequestSummary.
    #: This constant has a value of "FAILED"
    COPY_METADATA_OBJECT_REQUEST_STATUS_FAILED = "FAILED"

    #: A constant which can be used with the copy_metadata_object_request_status property of a CopyObjectRequestSummary.
    #: This constant has a value of "IN_PROGRESS"
    COPY_METADATA_OBJECT_REQUEST_STATUS_IN_PROGRESS = "IN_PROGRESS"

    #: A constant which can be used with the copy_metadata_object_request_status property of a CopyObjectRequestSummary.
    #: This constant has a value of "QUEUED"
    COPY_METADATA_OBJECT_REQUEST_STATUS_QUEUED = "QUEUED"

    #: A constant which can be used with the copy_metadata_object_request_status property of a CopyObjectRequestSummary.
    #: This constant has a value of "TERMINATING"
    COPY_METADATA_OBJECT_REQUEST_STATUS_TERMINATING = "TERMINATING"

    #: A constant which can be used with the copy_metadata_object_request_status property of a CopyObjectRequestSummary.
    #: This constant has a value of "TERMINATED"
    COPY_METADATA_OBJECT_REQUEST_STATUS_TERMINATED = "TERMINATED"

    def __init__(self, **kwargs):
        """
        Initializes a new CopyObjectRequestSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param key:
            The value to assign to the key property of this CopyObjectRequestSummary.
        :type key: str

        :param source_workspace_id:
            The value to assign to the source_workspace_id property of this CopyObjectRequestSummary.
        :type source_workspace_id: str

        :param object_keys:
            The value to assign to the object_keys property of this CopyObjectRequestSummary.
        :type object_keys: list[str]

        :param copy_conflict_resolution:
            The value to assign to the copy_conflict_resolution property of this CopyObjectRequestSummary.
        :type copy_conflict_resolution: oci.data_integration.models.CopyConflictResolution

        :param copy_metadata_object_request_status:
            The value to assign to the copy_metadata_object_request_status property of this CopyObjectRequestSummary.
            Allowed values for this property are: "SUCCESSFUL", "FAILED", "IN_PROGRESS", "QUEUED", "TERMINATING", "TERMINATED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type copy_metadata_object_request_status: str

        :param created_by:
            The value to assign to the created_by property of this CopyObjectRequestSummary.
        :type created_by: str

        :param created_by_name:
            The value to assign to the created_by_name property of this CopyObjectRequestSummary.
        :type created_by_name: str

        :param total_source_object_count:
            The value to assign to the total_source_object_count property of this CopyObjectRequestSummary.
        :type total_source_object_count: int

        :param total_objects_copied_into_target:
            The value to assign to the total_objects_copied_into_target property of this CopyObjectRequestSummary.
        :type total_objects_copied_into_target: int

        :param time_started_in_millis:
            The value to assign to the time_started_in_millis property of this CopyObjectRequestSummary.
        :type time_started_in_millis: int

        :param time_ended_in_millis:
            The value to assign to the time_ended_in_millis property of this CopyObjectRequestSummary.
        :type time_ended_in_millis: int

        :param copied_items:
            The value to assign to the copied_items property of this CopyObjectRequestSummary.
        :type copied_items: list[oci.data_integration.models.CopyObjectMetadataSummary]

        :param referenced_items:
            The value to assign to the referenced_items property of this CopyObjectRequestSummary.
        :type referenced_items: list[oci.data_integration.models.CopyObjectMetadataSummary]

        :param name:
            The value to assign to the name property of this CopyObjectRequestSummary.
        :type name: str

        """
        self.swagger_types = {
            'key': 'str',
            'source_workspace_id': 'str',
            'object_keys': 'list[str]',
            'copy_conflict_resolution': 'CopyConflictResolution',
            'copy_metadata_object_request_status': 'str',
            'created_by': 'str',
            'created_by_name': 'str',
            'total_source_object_count': 'int',
            'total_objects_copied_into_target': 'int',
            'time_started_in_millis': 'int',
            'time_ended_in_millis': 'int',
            'copied_items': 'list[CopyObjectMetadataSummary]',
            'referenced_items': 'list[CopyObjectMetadataSummary]',
            'name': 'str'
        }

        self.attribute_map = {
            'key': 'key',
            'source_workspace_id': 'sourceWorkspaceId',
            'object_keys': 'objectKeys',
            'copy_conflict_resolution': 'copyConflictResolution',
            'copy_metadata_object_request_status': 'copyMetadataObjectRequestStatus',
            'created_by': 'createdBy',
            'created_by_name': 'createdByName',
            'total_source_object_count': 'totalSourceObjectCount',
            'total_objects_copied_into_target': 'totalObjectsCopiedIntoTarget',
            'time_started_in_millis': 'timeStartedInMillis',
            'time_ended_in_millis': 'timeEndedInMillis',
            'copied_items': 'copiedItems',
            'referenced_items': 'referencedItems',
            'name': 'name'
        }

        self._key = None
        self._source_workspace_id = None
        self._object_keys = None
        self._copy_conflict_resolution = None
        self._copy_metadata_object_request_status = None
        self._created_by = None
        self._created_by_name = None
        self._total_source_object_count = None
        self._total_objects_copied_into_target = None
        self._time_started_in_millis = None
        self._time_ended_in_millis = None
        self._copied_items = None
        self._referenced_items = None
        self._name = None

    @property
    def key(self):
        """
        Gets the key of this CopyObjectRequestSummary.
        Copy object request key.


        :return: The key of this CopyObjectRequestSummary.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this CopyObjectRequestSummary.
        Copy object request key.


        :param key: The key of this CopyObjectRequestSummary.
        :type: str
        """
        self._key = key

    @property
    def source_workspace_id(self):
        """
        Gets the source_workspace_id of this CopyObjectRequestSummary.
        The workspace id of the source from where we need to copy object.


        :return: The source_workspace_id of this CopyObjectRequestSummary.
        :rtype: str
        """
        return self._source_workspace_id

    @source_workspace_id.setter
    def source_workspace_id(self, source_workspace_id):
        """
        Sets the source_workspace_id of this CopyObjectRequestSummary.
        The workspace id of the source from where we need to copy object.


        :param source_workspace_id: The source_workspace_id of this CopyObjectRequestSummary.
        :type: str
        """
        self._source_workspace_id = source_workspace_id

    @property
    def object_keys(self):
        """
        Gets the object_keys of this CopyObjectRequestSummary.
        The list of the objects to be copied.


        :return: The object_keys of this CopyObjectRequestSummary.
        :rtype: list[str]
        """
        return self._object_keys

    @object_keys.setter
    def object_keys(self, object_keys):
        """
        Sets the object_keys of this CopyObjectRequestSummary.
        The list of the objects to be copied.


        :param object_keys: The object_keys of this CopyObjectRequestSummary.
        :type: list[str]
        """
        self._object_keys = object_keys

    @property
    def copy_conflict_resolution(self):
        """
        Gets the copy_conflict_resolution of this CopyObjectRequestSummary.

        :return: The copy_conflict_resolution of this CopyObjectRequestSummary.
        :rtype: oci.data_integration.models.CopyConflictResolution
        """
        return self._copy_conflict_resolution

    @copy_conflict_resolution.setter
    def copy_conflict_resolution(self, copy_conflict_resolution):
        """
        Sets the copy_conflict_resolution of this CopyObjectRequestSummary.

        :param copy_conflict_resolution: The copy_conflict_resolution of this CopyObjectRequestSummary.
        :type: oci.data_integration.models.CopyConflictResolution
        """
        self._copy_conflict_resolution = copy_conflict_resolution

    @property
    def copy_metadata_object_request_status(self):
        """
        Gets the copy_metadata_object_request_status of this CopyObjectRequestSummary.
        Copy Object request status.

        Allowed values for this property are: "SUCCESSFUL", "FAILED", "IN_PROGRESS", "QUEUED", "TERMINATING", "TERMINATED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The copy_metadata_object_request_status of this CopyObjectRequestSummary.
        :rtype: str
        """
        return self._copy_metadata_object_request_status

    @copy_metadata_object_request_status.setter
    def copy_metadata_object_request_status(self, copy_metadata_object_request_status):
        """
        Sets the copy_metadata_object_request_status of this CopyObjectRequestSummary.
        Copy Object request status.


        :param copy_metadata_object_request_status: The copy_metadata_object_request_status of this CopyObjectRequestSummary.
        :type: str
        """
        allowed_values = ["SUCCESSFUL", "FAILED", "IN_PROGRESS", "QUEUED", "TERMINATING", "TERMINATED"]
        if not value_allowed_none_or_none_sentinel(copy_metadata_object_request_status, allowed_values):
            copy_metadata_object_request_status = 'UNKNOWN_ENUM_VALUE'
        self._copy_metadata_object_request_status = copy_metadata_object_request_status

    @property
    def created_by(self):
        """
        Gets the created_by of this CopyObjectRequestSummary.
        OCID of the user who initiated copy request.


        :return: The created_by of this CopyObjectRequestSummary.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this CopyObjectRequestSummary.
        OCID of the user who initiated copy request.


        :param created_by: The created_by of this CopyObjectRequestSummary.
        :type: str
        """
        self._created_by = created_by

    @property
    def created_by_name(self):
        """
        Gets the created_by_name of this CopyObjectRequestSummary.
        Name of the user who created the copy object request.


        :return: The created_by_name of this CopyObjectRequestSummary.
        :rtype: str
        """
        return self._created_by_name

    @created_by_name.setter
    def created_by_name(self, created_by_name):
        """
        Sets the created_by_name of this CopyObjectRequestSummary.
        Name of the user who created the copy object request.


        :param created_by_name: The created_by_name of this CopyObjectRequestSummary.
        :type: str
        """
        self._created_by_name = created_by_name

    @property
    def total_source_object_count(self):
        """
        Gets the total_source_object_count of this CopyObjectRequestSummary.
        Number of source objects to be copied.


        :return: The total_source_object_count of this CopyObjectRequestSummary.
        :rtype: int
        """
        return self._total_source_object_count

    @total_source_object_count.setter
    def total_source_object_count(self, total_source_object_count):
        """
        Sets the total_source_object_count of this CopyObjectRequestSummary.
        Number of source objects to be copied.


        :param total_source_object_count: The total_source_object_count of this CopyObjectRequestSummary.
        :type: int
        """
        self._total_source_object_count = total_source_object_count

    @property
    def total_objects_copied_into_target(self):
        """
        Gets the total_objects_copied_into_target of this CopyObjectRequestSummary.
        Number of objects copied into the target.


        :return: The total_objects_copied_into_target of this CopyObjectRequestSummary.
        :rtype: int
        """
        return self._total_objects_copied_into_target

    @total_objects_copied_into_target.setter
    def total_objects_copied_into_target(self, total_objects_copied_into_target):
        """
        Sets the total_objects_copied_into_target of this CopyObjectRequestSummary.
        Number of objects copied into the target.


        :param total_objects_copied_into_target: The total_objects_copied_into_target of this CopyObjectRequestSummary.
        :type: int
        """
        self._total_objects_copied_into_target = total_objects_copied_into_target

    @property
    def time_started_in_millis(self):
        """
        Gets the time_started_in_millis of this CopyObjectRequestSummary.
        Time at which the request started getting processed.


        :return: The time_started_in_millis of this CopyObjectRequestSummary.
        :rtype: int
        """
        return self._time_started_in_millis

    @time_started_in_millis.setter
    def time_started_in_millis(self, time_started_in_millis):
        """
        Sets the time_started_in_millis of this CopyObjectRequestSummary.
        Time at which the request started getting processed.


        :param time_started_in_millis: The time_started_in_millis of this CopyObjectRequestSummary.
        :type: int
        """
        self._time_started_in_millis = time_started_in_millis

    @property
    def time_ended_in_millis(self):
        """
        Gets the time_ended_in_millis of this CopyObjectRequestSummary.
        Time at which the request was completely processed.


        :return: The time_ended_in_millis of this CopyObjectRequestSummary.
        :rtype: int
        """
        return self._time_ended_in_millis

    @time_ended_in_millis.setter
    def time_ended_in_millis(self, time_ended_in_millis):
        """
        Sets the time_ended_in_millis of this CopyObjectRequestSummary.
        Time at which the request was completely processed.


        :param time_ended_in_millis: The time_ended_in_millis of this CopyObjectRequestSummary.
        :type: int
        """
        self._time_ended_in_millis = time_ended_in_millis

    @property
    def copied_items(self):
        """
        Gets the copied_items of this CopyObjectRequestSummary.
        The array of copy object details.


        :return: The copied_items of this CopyObjectRequestSummary.
        :rtype: list[oci.data_integration.models.CopyObjectMetadataSummary]
        """
        return self._copied_items

    @copied_items.setter
    def copied_items(self, copied_items):
        """
        Sets the copied_items of this CopyObjectRequestSummary.
        The array of copy object details.


        :param copied_items: The copied_items of this CopyObjectRequestSummary.
        :type: list[oci.data_integration.models.CopyObjectMetadataSummary]
        """
        self._copied_items = copied_items

    @property
    def referenced_items(self):
        """
        Gets the referenced_items of this CopyObjectRequestSummary.
        The array of copied referenced objects.


        :return: The referenced_items of this CopyObjectRequestSummary.
        :rtype: list[oci.data_integration.models.CopyObjectMetadataSummary]
        """
        return self._referenced_items

    @referenced_items.setter
    def referenced_items(self, referenced_items):
        """
        Sets the referenced_items of this CopyObjectRequestSummary.
        The array of copied referenced objects.


        :param referenced_items: The referenced_items of this CopyObjectRequestSummary.
        :type: list[oci.data_integration.models.CopyObjectMetadataSummary]
        """
        self._referenced_items = referenced_items

    @property
    def name(self):
        """
        Gets the name of this CopyObjectRequestSummary.
        Name of the copy object request.


        :return: The name of this CopyObjectRequestSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CopyObjectRequestSummary.
        Name of the copy object request.


        :param name: The name of this CopyObjectRequestSummary.
        :type: str
        """
        self._name = name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
